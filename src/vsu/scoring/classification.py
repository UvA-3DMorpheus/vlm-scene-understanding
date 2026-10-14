"""Classification metrics for material recognition: accuracy, macro F1, confusion matrix,
per class rows, and agreement across prompt variants.

All functions consume plain label lists or dictionaries produced from typed answers. A
prediction of ``None`` means the answer did not parse; it is never dropped. Accuracy is
reported twice: over all questions (a failure counts as wrong) and over parsed ones only.
Predictions outside the label set are kept under ``OTHER`` so open set answers that map
to nothing still show up in the confusion matrix.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from itertools import combinations
from typing import Any

UNPARSED = "<unparsed>"
OTHER = "<other>"

Label = str | None


def _norm(pred: Label, labels: Sequence[str]) -> str:
    if pred is None:
        return UNPARSED
    return pred if pred in labels else OTHER


def accuracy(y_true: Sequence[str], y_pred: Sequence[Label]) -> dict[str, float | int | None]:
    """Accuracy over all questions (failures wrong) and over parsed questions only."""
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred differ in length")
    n = len(y_true)
    parsed = [(t, p) for t, p in zip(y_true, y_pred, strict=True) if p is not None]
    correct = sum(t == p for t, p in parsed)
    return {
        "n": n,
        "n_parsed": len(parsed),
        "accuracy": (correct / n) if n else None,
        "accuracy_parsed": (correct / len(parsed)) if parsed else None,
    }


def confusion_matrix(
    y_true: Sequence[str], y_pred: Sequence[Label], labels: Sequence[str]
) -> dict[str, Any]:
    """Counts ``matrix[true][pred]`` with extra prediction columns OTHER and UNPARSED."""
    columns = [*labels, OTHER, UNPARSED]
    matrix = {t: dict.fromkeys(columns, 0) for t in labels}
    for t, p in zip(y_true, y_pred, strict=True):
        if t not in matrix:
            raise ValueError(f"true label {t!r} not in labels {list(labels)}")
        matrix[t][_norm(p, labels)] += 1
    return {"labels": list(labels), "columns": columns, "matrix": matrix}


def per_class(
    y_true: Sequence[str], y_pred: Sequence[Label], labels: Sequence[str]
) -> dict[str, dict[str, float | int | None]]:
    """Precision, recall, F1 and support per label; failures count as wrong predictions."""
    rows: dict[str, dict[str, float | int | None]] = {}
    for label in labels:
        tp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == label and p == label)
        fp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t != label and p == label)
        fn = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == label and p != label)
        support = tp + fn
        precision = tp / (tp + fp) if tp + fp else None
        recall = tp / support if support else None
        f1 = (
            2 * precision * recall / (precision + recall)
            if precision is not None and recall is not None and precision + recall
            else (0.0 if support else None)
        )
        rows[label] = {"support": support, "precision": precision, "recall": recall, "f1": f1}
    return rows


def macro_f1(rows: Mapping[str, Mapping[str, float | int | None]]) -> float | None:
    """Mean F1 over labels that occur in the ground truth (support > 0)."""
    values = [r["f1"] for r in rows.values() if r["support"] and r["f1"] is not None]
    return (sum(values) / len(values)) if values else None  # type: ignore[arg-type]


def classification_summary(
    y_true: Sequence[str], y_pred: Sequence[Label], labels: Sequence[str]
) -> dict[str, Any]:
    """Everything a report needs for one run, JSON serializable."""
    rows = per_class(y_true, y_pred, labels)
    return {
        **accuracy(y_true, y_pred),
        "macro_f1": macro_f1(rows),
        "per_class": rows,
        "confusion": confusion_matrix(y_true, y_pred, labels),
    }


# ---------------------------------------------------------------- agreement across variants


def fleiss_kappa(ratings: Sequence[Sequence[str]]) -> float | None:
    """Fleiss' kappa for a fixed number of raters per subject.

    ``ratings[i]`` holds the category chosen by each rater for subject ``i``; every subject
    needs the same number of raters, at least two. Returns None when undefined (fewer than
    two raters or no subjects); 1.0 when all raters agree everywhere.
    """
    if not ratings:
        return None
    n = len(ratings[0])
    if n < 2 or any(len(r) != n for r in ratings):
        return None
    categories = sorted({c for r in ratings for c in r})
    counts = [Counter(r) for r in ratings]
    p_i = [(sum(c[k] ** 2 for k in categories) - n) / (n * (n - 1)) for c in counts]
    p_bar = sum(p_i) / len(ratings)
    totals = Counter()
    for c in counts:
        totals.update(c)
    p_j = [totals[k] / (len(ratings) * n) for k in categories]
    p_e = sum(p**2 for p in p_j)
    if p_e >= 1.0:
        return 1.0
    return (p_bar - p_e) / (1 - p_e)


def agreement(predictions: Mapping[str, Mapping[str, Label]]) -> dict[str, Any]:
    """How much prompt variants agree with each other, on the questions they all answered.

    ``predictions[variant][question_id]`` is the predicted label (None if unparsed).
    Returns the fraction of questions where every variant gave the same label, the pairwise
    agreement rate per variant pair, and Fleiss' kappa over variants as raters. An
    unparsed answer is its own category, so failing to answer counts as disagreeing.
    """
    variants = sorted(predictions)
    if not variants:
        return {
            "variants": [],
            "n_common": 0,
            "all_agree": None,
            "pairwise": {},
            "fleiss_kappa": None,
        }
    common = sorted(set.intersection(*(set(predictions[v]) for v in variants)))
    rows = [[_label(predictions[v][q]) for v in variants] for q in common]
    pairwise: dict[str, float | None] = {}
    for a, b in combinations(variants, 2):
        same = sum(predictions[a][q] == predictions[b][q] for q in common)
        pairwise[f"{a}-{b}"] = (same / len(common)) if common else None
    return {
        "variants": variants,
        "n_common": len(common),
        "all_agree": (sum(len(set(r)) == 1 for r in rows) / len(rows)) if rows else None,
        "pairwise": pairwise,
        "fleiss_kappa": fleiss_kappa(rows) if len(variants) >= 2 else None,
    }


def _label(value: Label) -> str:
    return UNPARSED if value is None else value


def label_counts(values: Iterable[Label]) -> dict[str, int]:
    """Histogram of predicted labels, with UNPARSED for None."""
    return dict(Counter(_label(v) for v in values))
