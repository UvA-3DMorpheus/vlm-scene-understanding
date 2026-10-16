"""Check the material experiments' scoring with simulated models on the real questions.

    python scripts/verify_scoring.py --out /scratch/somewhere
    python scripts/verify_scoring.py --out /scratch/somewhere --datasets sim_preview smoke

Writes the answers of two simulated models straight into run directories under ``--out``
(no real model is called), then scores and reports them with the pipeline's own code:

- ``perfect`` always answers correctly;
- ``biased`` always says "metal" (1.0), "yes" (1.1 yes/no), the first option (1.1 two
  options) and "A" (1.2).

Every metric then has a value it must take (perfect: 1.0 everywhere, a yes rate of 1/5, a
first-option and A rate of 0.5; biased: the bias at its extreme, accuracy at chance, the
consistency rates at 0). A wrong value means the counting, the answer mapping, the grouping
or the consistency logic is broken. Exit code 1 on any mismatch, with the failures listed.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any

from vsu.experiments import get_experiment, load_experiment_config
from vsu.experiments.base import Question, RawRecord
from vsu.experiments.material.consistency import overview_rows
from vsu.experiments.material.items import label_text
from vsu.models.base import Decoding, Response
from vsu.models.registry import ModelConfig
from vsu.settings import get_settings
from vsu.utils.io import append_jsonl

VARIANTS = {"exp1": ["v1"], "exp1_1": ["yesno_v1", "choice_v1"], "exp1_2": ["v1"]}
DATASETS = ["sim_realistic", "smoke"]


def simulated_answer(policy: str, experiment: str, q: Question) -> str:
    """The reply text a simulated model gives."""
    truth = q.target["material"]
    if experiment == "exp1":
        return truth if policy == "perfect" else "metal"
    if experiment == "exp1_1" and q.meta["task"] == "yesno":
        return "yes" if policy == "biased" or q.meta["asked"] == truth else "no"
    if experiment == "exp1_1":
        return q.context["first"] if policy == "biased" else label_text(truth)
    if policy == "biased":
        return "A"
    return "A" if q.target["object"] == q.meta["image_a"] else "B"


def expected(policy: str, experiment: str, variant: str, metal_share: float) -> dict[str, float]:
    """The values each metric must take for a simulated policy."""
    if experiment == "exp1":
        return {"accuracy": 1.0 if policy == "perfect" else metal_share}
    if variant == "yesno_v1":
        if policy == "perfect":
            return {"accuracy": 1.0, "balanced_accuracy": 1.0, "yes_rate": 1 / 5}
        return {"balanced_accuracy": 0.5, "yes_rate": 1.0, "true_positive_rate": 1.0}
    if variant == "choice_v1":
        if policy == "perfect":
            return {
                "accuracy": 1.0,
                "first_option_rate": 0.5,
                "order_consistency": 1.0,
                "invalid_rate": 0.0,
            }
        return {
            "accuracy": 0.5,
            "first_option_rate": 1.0,
            "order_consistency": 0.0,
            "invalid_rate": 0.0,
        }
    if policy == "perfect":
        return {
            "accuracy": 1.0,
            "solved_rate": 1.0,
            "a_rate": 0.5,
            "image_order_consistency": 1.0,
            "label_consistency": 1.0,
        }
    return {
        "accuracy": 0.5,
        "solved_rate": 0.0,
        "a_rate": 1.0,
        "image_order_consistency": 0.0,
        "label_consistency": 0.0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--out", type=Path, required=True, help="scratch results root")
    parser.add_argument("--datasets", nargs="+", default=DATASETS, help="datasets to check")
    args = parser.parse_args(argv)
    settings = get_settings(results_root=args.out / "runs")
    failures: list[str] = []
    checked = 0

    def check(label: str, got: Any, want: float) -> None:
        nonlocal checked
        checked += 1
        ok = got is not None and math.isclose(float(got), want, abs_tol=1e-9)
        print(f"{'ok  ' if ok else 'FAIL'} {label}: {got} (expected {want:.4g})")
        if not ok:
            failures.append(label)

    for policy in ("perfect", "biased"):
        config = ModelConfig(name=policy, backend="dummy")
        for name, variants in VARIANTS.items():
            config_ = load_experiment_config(name, settings)
            config_.options["datasets"] = list(args.datasets)
            exp = get_experiment(name)(config_, settings=settings)
            questions = exp.build_questions()
            for variant in variants:
                qs = exp.questions_for(variant, questions)
                run = exp.start_run(config, variant, qs, resume=False)
                for q in qs:
                    response = Response(
                        text=simulated_answer(policy, name, q),
                        model_id=policy,
                        backend_model="simulated",
                        decoding=Decoding(),
                        latency_s=0.0,
                        request_hash="simulated",
                    )
                    record = RawRecord(
                        question_id=q.id, prompt="", images=q.images, response=response
                    )
                    append_jsonl(run.raw, record.model_dump(mode="json"))
                scored = exp.score(run, variant)
                summary = exp.report(run, variant)
                check(f"{policy} {name} {variant} parse failures", summary["num_parse_failures"], 0)
                for dataset in args.datasets:
                    d = summary["datasets"].get(dataset)
                    if d is None:
                        failures.append(f"{policy} {name} {variant} {dataset}: no questions")
                        print(f"FAIL {policy} {name} {variant} {dataset}: no questions")
                        continue
                    in_ds = [s for s in scored if s.dataset == dataset]
                    metal_share = sum(s.target["material"] == "metal" for s in in_ds) / len(in_ds)
                    for metric, want in expected(policy, name, variant, metal_share).items():
                        check(f"{policy} {name} {variant} {dataset} {metric}", d.get(metric), want)

    for dataset in args.datasets:
        rows = {(r["model"], r["mode"]): r for r in overview_rows(settings, dataset)}
        perfect = rows.get(("perfect", "direct"))
        if perfect is None:
            failures.append(f"overview {dataset}: no perfect row")
            continue
        for column in ("yes/no vs 1.0", "two options vs 1.0", "matching vs 1.0"):
            check(f"overview {dataset} perfect {column}", perfect[column], 1.0)

    print(f"\n{checked} checks, {len(failures)} failed")
    for f in failures:
        print("  failed:", f)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
