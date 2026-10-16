"""Cross-task consistency of the material experiments, and the combined overview.

Experiments 1.0, 1.1 and 1.2 ask about the same objects in the same views, so a model's
answers can be checked against each other. The reference is the model's own Experiment
1.0 label for that object and view, not the ground truth: a model that calls the tray
"metal" in 1.0 is consistent in 1.1 if it then says yes to "is it made of metal?", even
though both answers are wrong. Consistency and accuracy are reported side by side.

Tasks are paired by answer style (``MODES``): the direct mode pairs the answer-only
variants, the reasoning mode the variants with a reasoning step.

- yes/no: consistent when the reply is yes exactly for the 1.0 label.
- two options: consistent when the pick is the 1.0 label; only questions whose two options
  include the 1.0 label are scored.
- matching: consistent when the picked object is the one whose 1.0 label is the asked
  material; only questions where exactly one of the two objects carries that label are
  scored.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from vsu.experiments.base import ScoredRecord
from vsu.experiments.reporting import FinishedRun, finished_runs
from vsu.settings import Settings

#: mode -> experiment -> variant(s). Experiment 1.1 has one variant per task.
MODES: dict[str, dict[str, tuple[str, ...]]] = {
    "direct": {"exp1": ("v1",), "exp1_1": ("yesno_v1", "choice_v1"), "exp1_2": ("v1",)},
    "reasoning": {"exp1": ("v3",), "exp1_1": ("yesno_v2", "choice_v2"), "exp1_2": ("v2",)},
}

Labels = Mapping[str, str | None]  # 1.0 view id -> predicted label (None if unparsed)


def _rate(num: int, den: int) -> float | None:
    return (num / den) if den else None


def identification_labels(scored: Iterable[ScoredRecord]) -> dict[str, str | None]:
    """1.0 view id -> the label the model gave (None when the answer did not parse)."""
    return {s.question_id: (s.derived.get("predicted") if s.parse_ok else None) for s in scored}


def yesno_consistency(labels: Labels, scored: Iterable[ScoredRecord]) -> dict[str, Any]:
    """Fraction of yes/no answers that agree with the 1.0 label of the same view."""
    n = agree = 0
    for s in scored:
        label = labels.get(s.meta["view"])
        reply = s.derived.get("reply") if s.parse_ok else None
        if label is None or reply is None:
            continue
        n += 1
        agree += (reply == "yes") == (s.meta["asked"] == label)
    return {"n": n, "consistency": _rate(agree, n)}


def choice_consistency(labels: Labels, scored: Iterable[ScoredRecord]) -> dict[str, Any]:
    """Fraction of two-option picks equal to the 1.0 label, where that label is an option."""
    n = agree = 0
    for s in scored:
        label = labels.get(s.meta["view"])
        chosen = s.derived.get("chosen") if s.parse_ok else None
        if label is None or chosen is None or label not in (s.meta["first"], s.meta["second"]):
            continue
        n += 1
        agree += chosen == label
    return {"n": n, "consistency": _rate(agree, n)}


def matching_consistency(labels: Labels, scored: Iterable[ScoredRecord]) -> dict[str, Any]:
    """Fraction of matching picks that point at the object 1.0 gave the asked material."""
    n = agree = 0
    for s in scored:
        la, lb = labels.get(s.meta["view_a"]), labels.get(s.meta["view_b"])
        chosen = s.derived.get("chosen") if s.parse_ok else None
        asked = s.meta["asked"]
        if chosen is None or (la == asked) == (lb == asked):
            continue  # unparsed, or 1.0 gave the asked label to both objects or to neither
        n += 1
        agree += chosen == ("A" if la == asked else "B")
    return {"n": n, "consistency": _rate(agree, n)}


def _latest(runs: Sequence[FinishedRun], model: str, variant: str) -> FinishedRun | None:
    return next((r for r in runs if r.model == model and r.variant == variant), None)


def _dataset(scored: list[ScoredRecord], dataset: str) -> list[ScoredRecord]:
    return [s for s in scored if s.dataset == dataset]


def overview_rows(settings: Settings, dataset: str) -> list[dict[str, Any]]:
    """One row per model and mode: the headline of every task and the three consistencies.

    Columns: 1.0 accuracy, 1.1 yes/no balanced accuracy, 1.1 two-option accuracy, 1.2
    matching accuracy and solved rate, then consistency of each 1.1/1.2 task with 1.0.
    A missing run leaves its columns empty.
    """
    runs = {name: finished_runs(name, settings=settings) for name in ("exp1", "exp1_1", "exp1_2")}
    models = sorted({r.model for rs in runs.values() for r in rs})
    rows = []
    for model in models:
        for mode, variants in MODES.items():
            ident = _latest(runs["exp1"], model, variants["exp1"][0])
            yesno = _latest(runs["exp1_1"], model, variants["exp1_1"][0])
            choice = _latest(runs["exp1_1"], model, variants["exp1_1"][1])
            match = _latest(runs["exp1_2"], model, variants["exp1_2"][0])
            if not any((ident, yesno, choice, match)):
                continue
            row: dict[str, Any] = {"model": model, "mode": mode}
            row["identify acc"] = _metric(ident, dataset, "accuracy")
            row["yes/no bal. acc"] = _metric(yesno, dataset, "balanced_accuracy")
            row["yes rate"] = _metric(yesno, dataset, "yes_rate")
            row["two options acc"] = _metric(choice, dataset, "accuracy")
            row["matching acc"] = _metric(match, dataset, "accuracy")
            row["matching solved"] = _metric(match, dataset, "solved_rate")
            labels = identification_labels(_dataset(ident.scored, dataset)) if ident else {}
            for name, run, fn in (
                ("yes/no", yesno, yesno_consistency),
                ("two options", choice, choice_consistency),
                ("matching", match, matching_consistency),
            ):
                result = fn(labels, _dataset(run.scored, dataset)) if run and labels else None
                row[f"{name} vs 1.0"] = None if result is None else _round(result["consistency"])
            rows.append(row)
    return rows


def _metric(run: FinishedRun | None, dataset: str, key: str) -> float | None:
    if run is None:
        return None
    d = run.summary.get("datasets", {}).get(dataset) or {}
    return _round(d.get(key))


def _round(value: float | None) -> float | None:
    return None if value is None else round(float(value), 3)
