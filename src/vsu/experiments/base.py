"""Experiment skeleton: ``build_questions`` / ``run`` (resumable) / ``score`` / ``report``.

An experiment is a pipeline of files under one run directory::

    VSU_RESULTS_ROOT/<exp>/<model>/<variant>/<timestamp>/
      config.yaml       fully resolved: settings roots, git commit, package versions,
                        hostname, SLURM job id, model config, decoding, template hash
      questions.jsonl   one line per question (inputs, target, prompt context)
      raw.jsonl         one line per answered question: prompt text, model response
      scored.jsonl      one line per question: parse outcome and derived fields
      summary.json      aggregate metrics of this run

Each stage reads the previous file and writes the next, so stages can be rerun on their
own. ``run`` appends to ``raw.jsonl`` and skips question ids already present, so a timed
out job is resubmitted with the same command and resumes. A run is identified by a key
over everything that determines its answers (model config, variant, template, decoding,
question ids); a resubmission finds the latest run directory with the same key and
continues it, a changed input starts a new directory.

Subclasses implement ``build_questions``, ``score_record`` and ``summarize``, and set
``name`` and ``answer_schema``.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import platform
import subprocess
from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from tqdm import tqdm

from vsu.models.base import VLM, CacheMiss, Response
from vsu.models.registry import ModelConfig
from vsu.prompts import loader as prompts
from vsu.settings import Settings, get_settings
from vsu.utils.io import (
    append_jsonl,
    read_json,
    read_jsonl,
    utc_timestamp,
    write_json,
    write_jsonl,
    write_yaml,
)
from vsu.utils.parsing import parse_answer

log = logging.getLogger(__name__)

CONFIG_FILE = "config.yaml"
QUESTIONS_FILE = "questions.jsonl"
RAW_FILE = "raw.jsonl"
SCORED_FILE = "scored.jsonl"
SUMMARY_FILE = "summary.json"


class Question(BaseModel):
    """One model query: images, prompt context and the ground truth needed to score it."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="Unique within the experiment; stable across runs.")
    dataset: str = Field(description="smoke, sim, physion_pp, ...")
    item_id: str = Field(description="Scene id or image id the question is about.")
    condition: str = Field(default="default", description="Input condition (frame, crop, ...).")
    images: list[str] = Field(description="Absolute image paths, in prompt order.")
    context: dict[str, Any] = Field(default_factory=dict, description="Template variables.")
    target: dict[str, Any] = Field(default_factory=dict, description="Ground truth for scoring.")
    meta: dict[str, Any] = Field(default_factory=dict, description="Anything useful for reports.")


class RawRecord(BaseModel):
    """What ``run`` writes per question."""

    model_config = ConfigDict(extra="forbid")

    question_id: str
    prompt: str
    images: list[str]
    response: Response


class ScoredRecord(BaseModel):
    """What ``score`` writes per question: the parse outcome plus experiment specific fields."""

    model_config = ConfigDict(extra="forbid")

    question_id: str
    dataset: str
    item_id: str
    condition: str
    parse_ok: bool
    parse_error: str | None = None
    answer: dict[str, Any] | None = Field(default=None, description="Validated answer as dict.")
    target: dict[str, Any]
    derived: dict[str, Any] = Field(default_factory=dict, description="Scores and labels.")
    meta: dict[str, Any] = Field(default_factory=dict)
    cached: bool = False
    latency_s: float = 0.0


class ExperimentConfig(BaseModel):
    """``configs/experiments/<name>.yaml``, validated. ``options`` is experiment specific."""

    model_config = ConfigDict(extra="forbid")

    name: str
    variants: list[str] = Field(min_length=1)
    models: list[str] = Field(default_factory=lambda: ["dummy"], description="Default models.")
    seed: int = 0
    options: dict[str, Any] = Field(default_factory=dict)
    notes: str | None = None


def load_experiment_config(name: str, settings: Settings | None = None) -> ExperimentConfig:
    settings = settings or get_settings()
    path = settings.experiment_configs_dir / f"{name}.yaml"
    if not path.is_file():
        raise FileNotFoundError(f"no experiment config {path}")
    import yaml

    raw = yaml.safe_load(path.read_text()) or {}
    raw.setdefault("name", name)
    return ExperimentConfig(**raw)


@dataclass(frozen=True)
class RunDir:
    """Paths of one run directory."""

    path: Path

    @property
    def config(self) -> Path:
        return self.path / CONFIG_FILE

    @property
    def questions(self) -> Path:
        return self.path / QUESTIONS_FILE

    @property
    def raw(self) -> Path:
        return self.path / RAW_FILE

    @property
    def scored(self) -> Path:
        return self.path / SCORED_FILE

    @property
    def summary(self) -> Path:
        return self.path / SUMMARY_FILE

    def read_config(self) -> dict[str, Any]:
        import yaml

        return yaml.safe_load(self.config.read_text())

    def read_questions(self) -> list[Question]:
        return [Question.model_validate(r) for r in read_jsonl(self.questions)]

    def read_raw(self) -> list[RawRecord]:
        return [RawRecord.model_validate(r) for r in read_jsonl(self.raw)]

    def read_scored(self) -> list[ScoredRecord]:
        return [ScoredRecord.model_validate(r) for r in read_jsonl(self.scored)]

    def read_summary(self) -> dict[str, Any]:
        return read_json(self.summary)

    def answered_ids(self) -> set[str]:
        return {r["question_id"] for r in read_jsonl(self.raw)}


# ---------------------------------------------------------------- provenance


def git_state(repo: Path) -> dict[str, Any]:
    """Commit and dirty flag of the repository, or Nones outside a checkout."""
    try:
        commit = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "-C", str(repo), "status", "--porcelain", "--untracked-files=no"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
        )
        return {"commit": commit, "dirty": dirty}
    except Exception:
        return {"commit": None, "dirty": None}


def package_versions(
    names: Iterable[str] = ("vsu", "pydantic", "transformers", "torch"),
) -> dict[str, str | None]:
    out: dict[str, str | None] = {}
    for name in names:
        try:
            out[name] = version(name)
        except PackageNotFoundError:
            out[name] = None
    return out


def environment_record() -> dict[str, Any]:
    return {
        "hostname": platform.node(),
        "python": platform.python_version(),
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
        "packages": package_versions(),
    }


def error_response(model: VLM, error: str) -> Response:
    """A placeholder response for a question the backend could not answer.

    Stored in ``raw.jsonl`` like any answer so the question is not silently missing; it
    parses as a failure and ``summary.json`` counts it under ``num_errors``.
    """
    return Response(
        text="",
        model_id=model.model_id,
        backend_model=model.backend_model,
        decoding=model.default_decoding,
        latency_s=0.0,
        cached=False,
        request_hash="error",
        extra={"error": error[:1000]},
    )


# ---------------------------------------------------------------- experiment


class Experiment(ABC):
    """Base class. See the module docstring for the file pipeline."""

    name: str = "abstract"
    answer_schema: type[BaseModel]
    #: For prompt variants that ask for a bare word: the answer field a bare line maps onto.
    bare_label_field: str | None = None

    def __init__(
        self,
        config: ExperimentConfig,
        settings: Settings | None = None,
        templates_dir: Path | None = None,
    ) -> None:
        self.config = config
        self.settings = settings or get_settings()
        self.templates_dir = templates_dir or prompts.TEMPLATES_DIR

    # ---- to implement

    @abstractmethod
    def build_questions(self) -> list[Question]:
        """Produce every question of the experiment from the data on disk."""

    @abstractmethod
    def score_record(
        self, question: Question, answer: BaseModel | None, variant: str
    ) -> dict[str, Any]:
        """Derived fields for one question (labels, errors); ``answer`` is None if unparsed."""

    @abstractmethod
    def summarize(self, scored: list[ScoredRecord], variant: str) -> dict[str, Any]:
        """Aggregate metrics of one run."""

    # ---- prompts

    def render_prompt(self, question: Question, variant: str) -> str:
        return prompts.render(self.name, variant, self.templates_dir, **question.context)

    def variants(self) -> list[str]:
        return list(self.config.variants)

    # ---- run directories

    def run_key(self, model_config: ModelConfig, variant: str, questions: list[Question]) -> str:
        """Hash of everything that determines the answers of a run."""
        payload = {
            "experiment": self.name,
            "model": model_config.model_dump(mode="json"),
            "variant": variant,
            "template": prompts.template_hash(self.name, variant, self.templates_dir),
            "questions": [q.id for q in questions],
            "options": self.config.options,
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    def runs_root(self, model_id: str, variant: str) -> Path:
        return self.settings.results_root / self.name / model_id / variant

    def list_runs(self, model_id: str, variant: str) -> list[RunDir]:
        root = self.runs_root(model_id, variant)
        if not root.is_dir():
            return []
        return [RunDir(p) for p in sorted(root.iterdir()) if (p / CONFIG_FILE).is_file()]

    def latest_run(self, model_id: str, variant: str) -> RunDir | None:
        runs = self.list_runs(model_id, variant)
        return runs[-1] if runs else None

    def start_run(
        self,
        model_config: ModelConfig,
        variant: str,
        questions: list[Question],
        *,
        use_cache: bool = True,
        resume: bool = True,
    ) -> RunDir:
        """Create a run directory, or continue the latest one with the same run key.

        Writes ``config.yaml`` and ``questions.jsonl``. Existing directories are scanned
        newest first; one is reused only when its key matches and it has no
        ``summary.json`` yet (an unfinished run).
        """
        key = self.run_key(model_config, variant, questions)
        if resume:
            for candidate in reversed(self.list_runs(model_config.name, variant)):
                if candidate.summary.is_file():
                    continue
                if candidate.read_config().get("run_key") == key:
                    n = len(candidate.answered_ids())
                    log.info("resuming %s (%d answered)", candidate.path, n)
                    return candidate
        run = RunDir(self._new_run_path(model_config.name, variant))
        run.path.mkdir(parents=True, exist_ok=False)
        write_yaml(
            run.config,
            {
                "experiment": self.config.model_dump(mode="json"),
                "model": model_config.model_dump(mode="json"),
                "variant": variant,
                "template": {
                    "name": prompts.template_name(self.name, variant),
                    "sha256": prompts.template_hash(self.name, variant, self.templates_dir),
                },
                "decoding": model_config.decoding.model_dump(mode="json"),
                "use_cache": use_cache,
                "num_questions": len(questions),
                "run_key": key,
                "started": utc_timestamp(),
                "settings": self.settings.resolved_roots(),
                "git": git_state(self.settings.configs_root.parent),
                "environment": environment_record(),
            },
        )
        write_jsonl(run.questions, (q.model_dump(mode="json") for q in questions))
        log.info("new run %s", run.path)
        return run

    def _new_run_path(self, model_id: str, variant: str) -> Path:
        """A fresh timestamped directory; a suffix separates runs started in the same second."""
        root = self.runs_root(model_id, variant)
        stamp = utc_timestamp()
        path = root / stamp
        n = 1
        while path.exists():
            path = root / f"{stamp}-{n}"
            n += 1
        return path

    # ---- stages

    def run(
        self,
        run: RunDir,
        model: VLM,
        variant: str,
        *,
        use_cache: bool = True,
        limit: int | None = None,
    ) -> int:
        """Answer every question not yet in ``raw.jsonl``. Returns the number answered now."""
        questions = run.read_questions()
        if limit is not None:
            questions = questions[:limit]
        done = run.answered_ids()
        todo = [q for q in questions if q.id not in done]
        log.info(
            "%s/%s/%s: %d questions, %d done, %d to do",
            self.name,
            model.model_id,
            variant,
            len(questions),
            len(done),
            len(todo),
        )
        if not todo:
            return 0
        # No model.prepare() here: generate() loads the model on the first cache miss, so a run
        # whose answers are all cached never loads weights (and can run without a GPU).
        for question in tqdm(todo, desc=f"{self.name} {model.model_id} {variant}", unit="q"):
            prompt = self.render_prompt(question, variant)
            try:
                response = model.generate(
                    question.images, prompt, schema=self.schema_for(variant), use_cache=use_cache
                )
            except CacheMiss:
                raise  # cache-only runs stop at the first miss instead of recording errors
            except Exception as exc:  # noqa: BLE001 - one bad question must not abort the run
                log.error("%s: model error on %s: %r", self.name, question.id, exc)
                response = error_response(model, repr(exc))
            record = RawRecord(
                question_id=question.id, prompt=prompt, images=question.images, response=response
            )
            append_jsonl(run.raw, record.model_dump(mode="json"))
        return len(todo)

    def score(self, run: RunDir, variant: str) -> list[ScoredRecord]:
        """Parse every raw answer once and attach derived fields; writes ``scored.jsonl``."""
        questions = {q.id: q for q in run.read_questions()}
        scored: list[ScoredRecord] = []
        for raw in run.read_raw():
            question = questions[raw.question_id]
            parsed = parse_answer(
                raw.response.text,
                self.schema_for(variant),
                raw.question_id,
                bare_label_field=self.bare_label_field_for(variant),
            )
            derived = self.score_record(question, parsed.answer, variant)
            scored.append(
                ScoredRecord(
                    question_id=question.id,
                    dataset=question.dataset,
                    item_id=question.item_id,
                    condition=question.condition,
                    parse_ok=parsed.ok,
                    parse_error=parsed.error,
                    answer=None if parsed.answer is None else parsed.answer.model_dump(mode="json"),
                    target=question.target,
                    derived=derived,
                    meta={**question.meta, "_error": raw.response.extra.get("error")}
                    if raw.response.extra.get("error")
                    else question.meta,
                    cached=raw.response.cached,
                    latency_s=raw.response.latency_s,
                )
            )
        write_jsonl(run.scored, (s.model_dump(mode="json") for s in scored))
        return scored

    def report(self, run: RunDir, variant: str) -> dict[str, Any]:
        """Aggregate ``scored.jsonl`` into ``summary.json``."""
        scored = run.read_scored()
        summary = {
            "experiment": self.name,
            "variant": variant,
            "num_questions": len(run.read_questions()),
            "num_answered": len(scored),
            "num_parse_failures": sum(not s.parse_ok for s in scored),
            "num_errors": sum(bool(s.meta.get("_error")) for s in scored),
            "parse_failure_rate": (sum(not s.parse_ok for s in scored) / len(scored))
            if scored
            else None,
            "num_cached": sum(s.cached for s in scored),
            "mean_latency_s": (
                sum(s.latency_s for s in scored if not s.cached)
                / max(1, sum(not s.cached for s in scored))
            )
            if scored
            else None,
            **self.summarize(scored, variant),
        }
        write_json(run.summary, summary)
        return summary

    def questions_for(self, variant: str, questions: list[Question]) -> list[Question]:
        """The questions a variant asks. Default: all of them; experiments whose variants ask
        different kinds of question (yes/no versus two options) select their own subset."""
        return questions

    def schema_for(self, variant: str) -> type[BaseModel]:
        """The answer schema of a variant. Default: ``answer_schema`` for every variant;
        experiments whose variants ask different kinds of question override this."""
        return self.answer_schema

    def bare_label_field_for(self, variant: str) -> str | None:
        """The answer field a bare one-word reply maps onto, or None to require JSON."""
        return self.bare_label_field if self.uses_bare_label(variant) else None

    def uses_bare_label(self, variant: str) -> bool:
        """Whether a bare one word answer is acceptable for this variant. Default: never."""
        return False

    def complete(self, run: RunDir) -> bool:
        return run.summary.is_file()
