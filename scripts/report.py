"""Aggregate finished runs under VSU_RESULTS_ROOT into csv and markdown tables.

    python scripts/report.py                 # every experiment with finished runs
    python scripts/report.py --experiment exp1 --out results/tables

Consumes: the latest finished run per (experiment, model, variant). Produces, under
``--out`` (default ``results/tables`` in the repository, committed so the meeting numbers
are in git): per dataset ``<exp>_<dataset>_accuracy.csv``, ``_agreement.csv`` and
``_per_material.csv``, plus ``<exp>_runs.csv`` and one ``<exp>_report.md`` that joins
them. The benchmark dataset (simulated scenes) comes first; sanity datasets (smoke
photos) are reported in their own section and never mixed in.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from vsu.experiments import EXPERIMENTS
from vsu.experiments.reporting import (
    exp1_accuracy_rows,
    exp1_agreement_rows,
    exp1_camera_rows,
    exp1_confusion_tables,
    exp1_dataset_roles,
    exp1_per_material_rows,
    finished_runs,
    markdown_table,
    run_provenance_rows,
    write_csv,
)
from vsu.settings import REPO_ROOT, get_settings


def report_exp1(out: Path, settings) -> list[Path]:  # type: ignore[no-untyped-def]
    runs = finished_runs("exp1", settings=settings)
    if not runs:
        return []
    primary, sanity = exp1_dataset_roles(runs)
    written: list[Path] = []
    parts = [
        "# Experiment 1: material recognition\n",
        f"Latest finished run per model and variant under `{settings.results_root}`.\n",
        f"The **{primary}** dataset is the benchmark and the only one to quote. "
        f"The {', '.join(sanity)} dataset is a sanity check that the pipeline works on real "
        "photos; its numbers are reported apart and never mixed with the benchmark.\n",
    ]
    for dataset, title in [
        (primary, f"{primary} (benchmark)"),
        *[(d, f"{d} (sanity check)") for d in sanity],
    ]:
        acc = exp1_accuracy_rows(runs, dataset)
        if not acc:
            continue
        agree = exp1_agreement_rows(runs, dataset)
        per_material = exp1_per_material_rows(runs, dataset)
        confusion = exp1_confusion_tables(runs, dataset)
        for name, rows in (("accuracy", acc), ("agreement", agree), ("per_material", per_material)):
            path = out / f"exp1_{dataset}_{name}.csv"
            write_csv(path, rows)
            written.append(path)
        cameras = exp1_camera_rows(runs, dataset)
        parts += [
            f"## {title}\n",
            "### Accuracy and macro F1 per condition\n",
            markdown_table(acc),
        ]
        if cameras:
            write_csv(out / f"exp1_{dataset}_cameras.csv", cameras)
            written.append(out / f"exp1_{dataset}_cameras.csv")
            parts += ["### Accuracy per camera (viewpoint robustness)\n", markdown_table(cameras)]
        parts += [
            "### Agreement across prompt variants\n",
            markdown_table(agree),
            "### Per material recall (which materials are recognisable at all)\n",
            markdown_table(per_material),
            "### Confusion matrices\n",
        ]
        for key, rows in confusion.items():
            parts += [f"#### {key}\n", markdown_table(rows)]
    prov = run_provenance_rows(runs)
    write_csv(out / "exp1_runs.csv", prov)
    written.append(out / "exp1_runs.csv")
    parts += ["## Runs\n", markdown_table(prov)]
    report = out / "exp1_report.md"
    report.write_text("\n".join(parts))
    written.append(report)
    return written


REPORTERS = {"exp1": report_exp1}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--experiment", choices=sorted(EXPERIMENTS), default=None)
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "results" / "tables")
    args = parser.parse_args(argv)
    settings = get_settings()
    names = [args.experiment] if args.experiment else sorted(REPORTERS)
    args.out.mkdir(parents=True, exist_ok=True)
    total = 0
    for name in names:
        written = REPORTERS[name](args.out, settings)
        for path in written:
            print(path)
        total += len(written)
    if not total:
        print("no finished runs found under", settings.results_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
