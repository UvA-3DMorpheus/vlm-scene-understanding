"""Run an experiment for one or more models and prompt variants.

Usage::

    python scripts/run.py exp1 --models dummy qwen3vl-8b --variants v1 v2 v3
    python scripts/run.py exp1 --models dummy --stage score   # rerun one stage on existing files
    python scripts/run.py exp1 --models dummy --no-cache      # force fresh model calls

Consumes: experiment name, model names (configs/models/<name>.yaml), variant names,
optional stage and cache flags. Produces: files under
``VSU_RESULTS_ROOT/<exp>/<model>/<variant>/<timestamp>/`` (see PLAN.md Section 6).
The experiment implementations arrive in Step 4.
"""

from __future__ import annotations

import argparse

STAGES = ("all", "questions", "run", "score", "report")


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser shared with run_exp.slurm."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("experiment", help="Experiment name, for example exp1.")
    parser.add_argument("--models", nargs="+", required=True, help="Model config names.")
    parser.add_argument("--variants", nargs="*", default=None, help="Prompt variants; default all.")
    parser.add_argument("--stage", choices=STAGES, default="all", help="Pipeline stage to execute.")
    parser.add_argument("--no-cache", action="store_true", help="Bypass the response cache.")
    parser.add_argument(
        "--limit", type=int, default=None, help="Only the first N questions (debugging)."
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and dispatch to the experiment. Returns a process exit code."""
    args = build_parser().parse_args(argv)
    raise SystemExit(
        f"Experiment '{args.experiment}' is not implemented yet (Step 4). Parsed: {vars(args)}"
    )


if __name__ == "__main__":
    raise SystemExit(main())
