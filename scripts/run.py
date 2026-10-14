"""Run an experiment for one or more models and prompt variants.

    python scripts/run.py exp1 --models dummy qwen3vl-8b --variants v1 v2 v3
    python scripts/run.py exp1 --models dummy --stage score        # re-score the latest runs
    python scripts/run.py exp1 --models dummy --no-cache --limit 5  # fresh calls, first 5 questions

Consumes: an experiment name (configs/experiments/<exp>.yaml), model config names
(configs/models/<name>.yaml) and variant names (templates). Produces: run directories
under VSU_RESULTS_ROOT/<exp>/<model>/<variant>/<timestamp>/ with config.yaml,
questions.jsonl, raw.jsonl, scored.jsonl and summary.json.

Stages: ``all`` builds questions, answers, scores and reports; ``questions`` only creates
the run directory with its questions; ``run`` answers (resumable); ``score`` and
``report`` rerun those stages on the latest run of each model and variant without
loading any model. Models are loaded once and variants loop inside, so one SLURM job
per model covers all variants.
"""

from __future__ import annotations

import argparse
import logging
import sys

from vsu.experiments import get_experiment, load_experiment_config
from vsu.experiments.base import Experiment, RunDir
from vsu.experiments.reporting import (
    exp1_accuracy_rows,
    exp1_dataset_roles,
    finished_runs,
    markdown_table,
)
from vsu.models.registry import build_model, load_model_config
from vsu.settings import get_settings
from vsu.utils.logging import setup_logging

STAGES = ("all", "questions", "run", "score", "report")
log = logging.getLogger("vsu.run")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("experiment", help="Experiment name, for example exp1.")
    parser.add_argument(
        "--models",
        nargs="+",
        default=None,
        help="Model config names; default from the experiment config.",
    )
    parser.add_argument(
        "--variants", nargs="*", default=None, help="Prompt variants; default all from the config."
    )
    parser.add_argument("--stage", choices=STAGES, default="all")
    parser.add_argument("--no-cache", action="store_true", help="Bypass the response cache.")
    parser.add_argument(
        "--no-resume", action="store_true", help="Always start a new run directory."
    )
    parser.add_argument("--limit", type=int, default=None, help="Only the first N questions.")
    parser.add_argument("--log-level", default="INFO")
    return parser


def latest_or_fail(exp: Experiment, model_id: str, variant: str) -> RunDir:
    run = exp.latest_run(model_id, variant)
    if run is None:
        raise SystemExit(f"no run of {exp.name}/{model_id}/{variant} to re-score; run first")
    return run


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    setup_logging(getattr(logging, args.log_level.upper(), logging.INFO))
    settings = get_settings()
    experiment_cls = get_experiment(args.experiment)
    config = load_experiment_config(args.experiment, settings)
    exp = experiment_cls(config, settings=settings)
    models = args.models or config.models
    variants = args.variants or exp.variants()
    unknown = [v for v in variants if v not in exp.variants()]
    if unknown:
        raise SystemExit(f"unknown variants {unknown}; configured: {exp.variants()}")
    log.info("%s: models %s, variants %s, stage %s", exp.name, models, variants, args.stage)

    questions = exp.build_questions() if args.stage in ("all", "questions", "run") else None
    for model_id in models:
        model_config = load_model_config(model_id, settings)
        model = None
        if args.stage in ("all", "run"):
            model = build_model(model_config, settings=settings, use_cache=not args.no_cache)
        try:
            for variant in variants:
                if args.stage in ("all", "questions", "run"):
                    assert questions is not None
                    run = exp.start_run(
                        model_config,
                        variant,
                        questions,
                        use_cache=not args.no_cache,
                        resume=not args.no_resume,
                    )
                else:
                    run = latest_or_fail(exp, model_id, variant)
                if args.stage in ("all", "run"):
                    assert model is not None
                    exp.run(run, model, variant, use_cache=not args.no_cache, limit=args.limit)
                if args.stage in ("all", "run", "score"):
                    exp.score(run, variant)
                if args.stage in ("all", "run", "score", "report"):
                    summary = exp.report(run, variant)
                    log.info("%s/%s/%s -> %s", exp.name, model_id, variant, run.path)
                    for name, d in summary.get("datasets", {}).items():
                        log.info(
                            "  %s (%s): accuracy=%s n=%s", name, d["role"], d["accuracy"], d["n"]
                        )
        finally:
            if model is not None:
                model.close()

    if args.stage != "questions" and exp.name == "exp1":
        runs = finished_runs(exp.name, settings=settings)
        primary, sanity = exp1_dataset_roles(runs)
        for dataset, title in [(primary, "benchmark"), *[(d, "sanity check") for d in sanity]]:
            rows = [r for r in exp1_accuracy_rows(runs, dataset) if r["model"] in models]
            if rows:
                sys.stdout.write(f"\n{dataset} ({title}):\n" + markdown_table(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
