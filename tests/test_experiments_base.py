"""The experiment pipeline: run directories, resumable runs, scoring and summaries on the dummy."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from PIL import Image
from pydantic import BaseModel

from vsu.experiments.base import (
    CONFIG_FILE,
    Experiment,
    ExperimentConfig,
    Question,
    RunDir,
    ScoredRecord,
)
from vsu.models.dummy_backend import DummyModel
from vsu.models.registry import ModelConfig
from vsu.schemas import MaterialAnswer
from vsu.settings import Settings
from vsu.utils.io import read_jsonl

N = 6


class LabelExperiment(Experiment):
    """Minimal concrete experiment: ask the material of N images, compare with a target."""

    name = "expt"
    answer_schema = MaterialAnswer
    bare_label_field = "material"

    def __init__(self, *args: Any, images: list[Path], **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._images = images

    def build_questions(self) -> list[Question]:
        return [
            Question(
                id=f"q{i:02d}",
                dataset="tmp",
                item_id=p.stem,
                condition="frame",
                images=[str(p)],
                context={"labels": ["metal", "wood"]},
                target={"material": "metal"},
            )
            for i, p in enumerate(self._images)
        ]

    def score_record(
        self, question: Question, answer: BaseModel | None, variant: str
    ) -> dict[str, Any]:
        if answer is None:
            return {"correct": None}
        assert isinstance(answer, MaterialAnswer)
        return {"correct": answer.material == question.target["material"]}

    def summarize(self, scored: list[ScoredRecord], variant: str) -> dict[str, Any]:
        ok = [s for s in scored if s.parse_ok]
        return {"accuracy": (sum(s.derived["correct"] for s in ok) / len(ok)) if ok else None}

    def uses_bare_label(self, variant: str) -> bool:
        return variant == "v1"


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(
        results_root=tmp_path / "runs",
        cache_root=tmp_path / "cache",
        data_root=tmp_path / "data",
        _env_file=None,
    )


@pytest.fixture
def templates(tmp_path: Path) -> Path:
    d = tmp_path / "templates"
    d.mkdir()
    (d / "expt_v1.jinja").write_text("Material? One of {{ labels | join(', ') }}.")
    (d / "expt_v2.jinja").write_text("Think, then answer JSON. Labels: {{ labels | join(', ') }}.")
    return d


@pytest.fixture
def images(tmp_path: Path) -> list[Path]:
    out = []
    for i in range(N):
        p = tmp_path / f"img{i}.png"
        Image.new("RGB", (8, 8), (i * 20, 0, 0)).save(p)
        out.append(p)
    return out


@pytest.fixture
def exp(settings: Settings, templates: Path, images: list[Path]) -> LabelExperiment:
    cfg = ExperimentConfig(name="expt", variants=["v1", "v2"])
    return LabelExperiment(cfg, settings=settings, templates_dir=templates, images=images)


def dummy(**options: Any) -> tuple[ModelConfig, DummyModel]:
    cfg = ModelConfig(name="dummy", backend="dummy", options=options)
    return cfg, DummyModel(cfg)


# ---------------------------------------------------------------- run directories


def test_start_run_writes_config_and_questions(exp: LabelExperiment, settings: Settings) -> None:
    cfg, _ = dummy()
    questions = exp.build_questions()
    run = exp.start_run(cfg, "v1", questions)
    assert run.path.parent == settings.results_root / "expt" / "dummy" / "v1"
    config = run.read_config()
    assert config["variant"] == "v1" and config["num_questions"] == N
    assert config["model"]["backend"] == "dummy" and config["decoding"]["temperature"] == 0.0
    assert config["template"]["name"] == "expt_v1.jinja" and len(config["template"]["sha256"]) == 64
    assert config["settings"]["VSU_RESULTS_ROOT"] == str(settings.results_root)
    assert "commit" in config["git"] and "hostname" in config["environment"]
    assert config["environment"]["packages"]["pydantic"]
    assert [q.id for q in run.read_questions()] == [f"q{i:02d}" for i in range(N)]


def test_full_pipeline_on_dummy(exp: LabelExperiment) -> None:
    cfg, model = dummy()
    run = exp.start_run(cfg, "v1", exp.build_questions())
    assert exp.run(run, model, "v1") == N
    raw = run.read_raw()
    assert len(raw) == N and raw[0].prompt == "Material? One of metal, wood."
    assert all(not r.response.cached for r in raw)
    scored = exp.score(run, "v1")
    assert len(scored) == N and all(s.parse_ok for s in scored)
    assert all(s.derived["correct"] in (True, False) for s in scored)
    summary = exp.report(run, "v1")
    assert summary["num_answered"] == N and summary["num_parse_failures"] == 0
    assert summary["parse_failure_rate"] == 0.0 and 0.0 <= summary["accuracy"] <= 1.0
    assert run.summary.is_file() and exp.complete(run)
    assert json.loads(run.summary.read_text())["variant"] == "v1"


def test_resume_skips_answered_questions(exp: LabelExperiment) -> None:
    cfg, model = dummy()
    questions = exp.build_questions()
    run = exp.start_run(cfg, "v1", questions)
    exp.run(run, model, "v1", limit=4)  # a job that timed out after 4 answers
    assert len(run.answered_ids()) == 4
    again = exp.start_run(cfg, "v1", questions)  # resubmission with the same command
    assert again.path == run.path
    assert exp.run(again, model, "v1") == 2
    assert len(again.read_raw()) == N
    assert exp.run(again, model, "v1") == 0


def test_finished_run_is_not_resumed_but_cache_makes_rerun_free(exp: LabelExperiment) -> None:
    cfg, _ = dummy()
    model = DummyModel(
        cfg,
        cache=__import__("vsu.models.cache", fromlist=["ResponseCache"]).ResponseCache(
            exp.settings.cache_root
        ),
    )
    questions = exp.build_questions()
    run = exp.start_run(cfg, "v1", questions)
    exp.run(run, model, "v1")
    exp.score(run, "v1")
    exp.report(run, "v1")
    second = exp.start_run(cfg, "v1", questions)
    assert second.path != run.path
    exp.run(second, model, "v1")
    assert all(r.response.cached for r in second.read_raw())
    assert [r.response.text for r in second.read_raw()] == [r.response.text for r in run.read_raw()]
    assert exp.list_runs("dummy", "v1") == [run, second] and exp.latest_run("dummy", "v1") == second


def test_changed_template_or_questions_starts_a_new_run(
    exp: LabelExperiment, templates: Path
) -> None:
    cfg, model = dummy()
    questions = exp.build_questions()
    run = exp.start_run(cfg, "v1", questions)
    exp.run(run, model, "v1", limit=1)
    (templates / "expt_v1.jinja").write_text("Different wording: {{ labels }}")
    assert exp.start_run(cfg, "v1", questions).path != run.path
    (templates / "expt_v1.jinja").write_text("Material? One of {{ labels | join(', ') }}.")
    assert exp.start_run(cfg, "v1", questions).path == run.path
    assert exp.start_run(cfg, "v1", questions[:3]).path != run.path
    other_cfg = ModelConfig(name="dummy", backend="dummy", decoding={"temperature": 0.5})
    assert exp.start_run(other_cfg, "v1", questions).path != run.path


def test_variants_have_separate_directories(exp: LabelExperiment) -> None:
    cfg, model = dummy()
    questions = exp.build_questions()
    r1 = exp.start_run(cfg, "v1", questions)
    r2 = exp.start_run(cfg, "v2", questions)
    assert r1.path.parent != r2.path.parent
    exp.run(r2, model, "v2")
    assert r2.read_raw()[0].prompt.startswith("Think, then answer JSON.")


def test_parse_failures_are_counted_not_dropped(exp: LabelExperiment) -> None:
    cfg, model = dummy(failure_rate=0.8)
    run = exp.start_run(cfg, "v2", exp.build_questions())
    exp.run(run, model, "v2")
    scored = exp.score(run, "v2")
    failures = [s for s in scored if not s.parse_ok]
    assert 0 < len(failures) < N
    assert all(
        s.answer is None and s.derived == {"correct": None} and s.parse_error for s in failures
    )
    summary = exp.report(run, "v2")
    assert summary["num_parse_failures"] == len(failures)
    assert summary["num_answered"] == N


def test_bare_label_only_for_opted_in_variants(exp: LabelExperiment) -> None:
    cfg, _ = dummy()
    questions = exp.build_questions()
    for variant in ("v1", "v2"):
        run = exp.start_run(cfg, variant, questions)
        for q in questions:
            __import__("vsu.utils.io", fromlist=["append_jsonl"]).append_jsonl(
                run.raw,
                {
                    "question_id": q.id,
                    "prompt": "p",
                    "images": q.images,
                    "response": {
                        "text": "metal",
                        "model_id": "dummy",
                        "backend_model": "dummy:dummy",
                        "decoding": {"temperature": 0.0, "max_tokens": 1, "top_p": 1.0, "seed": 0},
                        "latency_s": 0.0,
                        "request_hash": "x",
                    },
                },
            )
        scored = exp.score(run, variant)
        assert all(s.parse_ok for s in scored) == (variant == "v1")


def test_runs_started_in_the_same_second_get_distinct_directories(exp: LabelExperiment) -> None:
    cfg, _ = dummy()
    questions = exp.build_questions()
    paths = set()
    for _ in range(3):
        run = exp.start_run(cfg, "v1", questions, resume=False)
        paths.add(run.path)
    assert len(paths) == 3 and len(exp.list_runs("dummy", "v1")) == 3


def test_run_dir_without_config_is_ignored(exp: LabelExperiment, settings: Settings) -> None:
    stray = settings.results_root / "expt" / "dummy" / "v1" / "20000101T000000Z"
    stray.mkdir(parents=True)
    assert exp.list_runs("dummy", "v1") == []
    (stray / CONFIG_FILE).write_text("run_key: nope\n")
    assert exp.list_runs("dummy", "v1") == [RunDir(stray)]
    assert exp.start_run(dummy()[0], "v1", exp.build_questions()).path != stray


def test_read_jsonl_tolerates_blank_lines(tmp_path: Path) -> None:
    p = tmp_path / "x.jsonl"
    p.write_text('{"a": 1}\n\n{"a": 2}\n')
    assert [r["a"] for r in read_jsonl(p)] == [1, 2]
    assert list(read_jsonl(tmp_path / "missing.jsonl")) == []


def test_backend_error_is_recorded_and_the_run_continues(exp: LabelExperiment) -> None:
    cfg, model = dummy()

    class Flaky(DummyModel):
        def _generate(self, images, prompt, schema, decoding):  # type: ignore[no-untyped-def]
            if "One of" in prompt and images and images[0].pil.getpixel((0, 0))[0] == 40:
                raise RuntimeError("context length exceeded")
            return super()._generate(images, prompt, schema, decoding)

    run = exp.start_run(cfg, "v1", exp.build_questions())
    assert exp.run(run, Flaky(cfg), "v1") == N
    raw = run.read_raw()
    errors = [r for r in raw if r.response.extra.get("error")]
    assert len(errors) == 1 and "context length" in errors[0].response.extra["error"]
    assert errors[0].response.text == "" and errors[0].response.request_hash == "error"
    scored = exp.score(run, "v1")
    bad = [s for s in scored if s.meta.get("_error")]
    assert len(bad) == 1 and not bad[0].parse_ok
    summary = exp.report(run, "v1")
    assert summary["num_errors"] == 1 and summary["num_parse_failures"] >= 1
