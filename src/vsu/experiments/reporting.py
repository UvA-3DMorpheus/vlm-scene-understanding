"""Aggregate finished runs into tables: one row per model and variant, agreement per model.

Consumes the ``summary.json`` and ``scored.jsonl`` of the latest finished run of every
(experiment, model, variant) under ``VSU_RESULTS_ROOT``. Produces plain rows (lists of
dictionaries) that ``scripts/report.py`` writes as csv and markdown under
``results/tables/``. Nothing here reads raw model text.
"""

from __future__ import annotations

import csv
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from vsu.experiments.base import CONFIG_FILE, RunDir, ScoredRecord
from vsu.scoring.classification import agreement
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


# ---------------------------------------------------------------- experiment 1 tables


def exp1_accuracy_rows(runs: Iterable[FinishedRun], dataset: str) -> list[Row]:
    """One row per model and variant for one dataset: accuracy per condition, macro F1, failures."""
    rows = []
    for fr in runs:
        s = fr.summary
        d = s.get("datasets", {}).get(dataset)
        if d is None:
            continue
        row: Row = {
            "model": fr.model,
            "variant": fr.variant,
            "n": d["n"],
            "accuracy": _r(d["accuracy"]),
            "exact_label_rate": _r(d.get("exact_label_rate")),
            "parse_failures": d["n_parse_failures"],
        }
        for group, g in sorted(s["groups"].items()):
            if group.startswith(f"{dataset}/"):
                condition = group.split("/", 1)[1]
                row[f"{condition} acc"] = _r(g["accuracy"])
                row[f"{condition} macro_f1"] = _r(g["macro_f1"])
        row["mean_latency_s"] = _r(s.get("mean_latency_s"), 2)
        row["run"] = fr.run.path.name
        rows.append(row)
    return rows


def exp1_camera_rows(runs: Iterable[FinishedRun], dataset: str) -> list[Row]:
    """One row per model and variant: accuracy per camera (viewpoint robustness)."""
    rows = []
    for fr in runs:
        d = fr.summary.get("datasets", {}).get(dataset) or {}
        by_camera = d.get("by_camera") or {}
        if not by_camera:
            continue
        row: Row = {"model": fr.model, "variant": fr.variant}
        for camera, c in by_camera.items():
            row[f"{camera} (n={c['n']})"] = _r(c["accuracy"])
        rows.append(row)
    return rows


def exp1_dataset_roles(runs: Sequence[FinishedRun]) -> tuple[str, list[str]]:
    """(primary dataset, sanity datasets) as recorded in the summaries."""
    for fr in runs:
        s = fr.summary
        if "primary_dataset" in s:
            return s["primary_dataset"], list(s.get("sanity_datasets", []))
    return "sim", ["smoke"]


def exp1_per_material_rows(runs: Iterable[FinishedRun], dataset: str) -> list[Row]:
    """One row per model, variant, condition and material of a dataset."""
    rows = []
    for fr in runs:
        for group, g in sorted(fr.summary["groups"].items()):
            if not group.startswith(f"{dataset}/"):
                continue
            for material, pc in g["per_class"].items():
                if not pc["support"]:
                    continue
                rows.append(
                    {
                        "model": fr.model,
                        "variant": fr.variant,
                        "condition": group.split("/", 1)[1],
                        "material": material,
                        "support": pc["support"],
                        "recall": _r(pc["recall"]),
                        "precision": _r(pc["precision"]),
                        "f1": _r(pc["f1"]),
                    }
                )
    return rows


def exp1_confusion_tables(runs: Iterable[FinishedRun], dataset: str) -> dict[str, list[Row]]:
    """``"<model>/<variant>/<condition>" -> rows`` of the confusion matrix (true label per row)."""
    tables: dict[str, list[Row]] = {}
    for fr in runs:
        for group, g in sorted(fr.summary["groups"].items()):
            if not group.startswith(f"{dataset}/"):
                continue
            cm = g["confusion"]
            rows = [
                {"true \\ predicted": t, **{c: cm["matrix"][t][c] for c in cm["columns"]}}
                for t in cm["labels"]
            ]
            tables[f"{fr.model}/{fr.variant}/{group.split('/', 1)[1]}"] = rows
    return tables


def exp1_agreement_rows(runs: Sequence[FinishedRun], dataset: str) -> list[Row]:
    """One row per model: agreement of its variants on the dataset's questions they all answered."""
    by_model: dict[str, dict[str, dict[str, str | None]]] = {}
    for fr in runs:
        preds = {
            s.question_id: (s.derived.get("predicted") if s.parse_ok else None)
            for s in fr.scored
            if s.dataset == dataset
        }
        by_model.setdefault(fr.model, {})[fr.variant] = preds
    rows = []
    for model, variants in sorted(by_model.items()):
        a = agreement(variants)
        row: Row = {
            "model": model,
            "variants": ",".join(a["variants"]),
            "n_common": a["n_common"],
            "all_agree": _r(a["all_agree"]),
            "fleiss_kappa": _r(a["fleiss_kappa"]),
        }
        for pair, value in sorted(a["pairwise"].items()):
            row[f"agree {pair}"] = _r(value)
        rows.append(row)
    return rows


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


def _r(value: float | None, digits: int = 3) -> float | None:
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
