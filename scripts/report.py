"""Aggregate finished runs under VSU_RESULTS_ROOT into csv and markdown tables.

    python scripts/report.py                 # every experiment with finished runs
    python scripts/report.py --experiment exp1 --out results/tables

Consumes: the latest finished run per (experiment, model, variant). Produces, under
``--out`` (default ``results/tables`` in the repository, committed so the meeting numbers
are in git): per dataset ``<exp>_<dataset>_accuracy.csv``, ``_agreement.csv`` and
``_per_material.csv``, plus ``<exp>_runs.csv`` and one ``<exp>_report.md`` that joins
them. The benchmark dataset (realistic simulated scenes) comes first, then comparison
datasets (preview renders), then sanity checks (smoke photos); no number mixes datasets.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from vsu.experiments.material.tables import (
    report_exp1,
    report_exp1_1,
    report_exp1_2,
    report_material,
)
from vsu.settings import REPO_ROOT, get_settings

REPORTERS = {
    "exp1": report_exp1,
    "exp1_1": report_exp1_1,
    "exp1_2": report_exp1_2,
    "material": report_material,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--experiment",
        choices=sorted(REPORTERS),
        default=None,
        help="One report (default all); 'material' combines exp1, exp1_1 and exp1_2.",
    )
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
