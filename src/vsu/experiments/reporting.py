"""Generic reporting: finished runs, dataset sections, provenance rows, csv and markdown.

Consumes the ``summary.json`` and ``scored.jsonl`` of the latest finished run of every
(experiment, model, variant) under ``VSU_RESULTS_ROOT``. Experiment specific tables are
built in their own packages (``vsu.experiments.material.tables``) from these pieces.
Nothing here reads raw model text.
"""

from __future__ import annotations

import csv
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from vsu.experiments.base import CONFIG_FILE, RunDir, ScoredRecord
from vsu.settings import Settings, get_settings

Row = dict[str, Any]


@dataclass(frozen=True)
class FinishedRun:
    experiment: str
    model: str
    variant: str
    run: RunDir

    @property
    def summary(self) -> dict[str, Any]:
        return self.run.read_summary()

    @property
    def scored(self) -> list[ScoredRecord]:
        return self.run.read_scored()


def finished_runs(
    experiment: str, results_root: Path | None = None, *, settings: Settings | None = None
) -> list[FinishedRun]:
    """The latest finished run per (model, variant) of an experiment, sorted."""
    root = (
        Path(results_root)
        if results_root is not None
        else (settings or get_settings()).results_root
    )
    out: list[FinishedRun] = []
    exp_dir = root / experiment
    if not exp_dir.is_dir():
        return out
    for model_dir in sorted(p for p in exp_dir.iterdir() if p.is_dir()):
        for variant_dir in sorted(p for p in model_dir.iterdir() if p.is_dir()):
            runs = [
                RunDir(p)
                for p in sorted(variant_dir.iterdir())
                if (p / CONFIG_FILE).is_file() and (p / "summary.json").is_file()
            ]
            if runs:
                out.append(FinishedRun(experiment, model_dir.name, variant_dir.name, runs[-1]))
    return out


ROLE_ORDER = ("primary", "secondary", "sanity", "other")
ROLE_TITLES = {
    "primary": "benchmark",
    "secondary": "comparison",
    "sanity": "sanity check",
    "other": "other",
}


def dataset_sections(runs: Sequence[FinishedRun]) -> list[tuple[str, str]]:
    """``(dataset, role)`` pairs in report order: the benchmark first, sanity checks last.

    Roles come from the summaries' ``datasets`` blocks, so a report never needs the config.
    """
    roles: dict[str, str] = {}
    for fr in runs:
        for dataset, d in (fr.summary.get("datasets") or {}).items():
            roles.setdefault(dataset, d.get("role", "other"))
    return sorted(
        roles.items(), key=lambda kv: (ROLE_ORDER.index(kv[1]) if kv[1] in ROLE_ORDER else 9, kv[0])
    )


def run_provenance_rows(runs: Iterable[FinishedRun]) -> list[Row]:
    """Where each number came from: run directory, commit, template hash, host, job."""
    rows = []
    for fr in runs:
        cfg = fr.run.read_config()
        rows.append(
            {
                "experiment": fr.experiment,
                "model": fr.model,
                "variant": fr.variant,
                "run": fr.run.path.name,
                "commit": (cfg.get("git") or {}).get("commit"),
                "dirty": (cfg.get("git") or {}).get("dirty"),
                "template_sha256": (cfg.get("template") or {}).get("sha256", "")[:12],
                "hostname": (cfg.get("environment") or {}).get("hostname"),
                "slurm_job_id": (cfg.get("environment") or {}).get("slurm_job_id"),
                "backend_model": (cfg.get("model") or {}).get("hf_id")
                or (cfg.get("model") or {}).get("backend"),
            }
        )
    return rows


# ---------------------------------------------------------------- writers


def rounded(value: float | None, digits: int = 3) -> float | None:
    """``value`` rounded for a table, None kept as None."""
    return None if value is None else round(float(value), digits)


def write_csv(path: Path, rows: list[Row]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    columns = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns)
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in columns})


def markdown_table(rows: list[Row]) -> str:
    if not rows:
        return "_no data_\n"
    columns = list(dict.fromkeys(k for r in rows for k in r))
    lines = ["| " + " | ".join(columns) + " |", "|" + "---|" * len(columns)]
    for r in rows:
        lines.append(
            "| " + " | ".join("" if r.get(c) is None else str(r.get(c)) for c in columns) + " |"
        )
    return "\n".join(lines) + "\n"
