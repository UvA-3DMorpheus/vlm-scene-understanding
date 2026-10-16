"""Metrics for verification questions (Experiment 1.1): yes/no and two-option choices.

All functions consume plain records produced from typed answers; an answer of ``None``
means it did not parse and counts as wrong, never dropped.

Yes/no. Each object is asked about its true material (a positive question) and about
each other material of the label set (negative questions), so most questions are
negatives. Raw accuracy rewards a model that always says "no"; the main number is
balanced accuracy, the mean of the true positive rate and the true negative rate. The yes
rate shows a bias towards agreeing.

Two options. Each pair of materials is asked in both orders ("metal or wood", "wood or
metal"). The first-option rate shows a preference for whichever material is named first
(0.5 is unbiased), and order consistency is the fraction of swapped pairs where the model
picks the same material both times.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Hashable, Iterable, Sequence
from dataclasses import dataclass
from typing import Any


def _rate(num: int, den: int) -> float | None:
    return (num / den) if den else None


# ---------------------------------------------------------------- yes / no


@dataclass(frozen=True)
class YesNoRecord:
    """One verification question: the material asked about, the true one, the reply."""

    asked: str
    truth: str
    reply: str | None  # "yes", "no", or None when unparsed

    @property
    def positive(self) -> bool:
        return self.asked == self.truth

    @property
    def correct(self) -> bool:
        expected = "yes" if self.positive else "no"
        return self.reply == expected


def yesno_summary(records: Sequence[YesNoRecord]) -> dict[str, Any]:
    """Accuracy, balanced accuracy, yes rate, and where false acceptances come from.

    ``false_yes_by_asked``: for negative questions, how often each asked material was
    wrongly accepted (which materials the model is too ready to see).
    ``true_yes_by_truth``: for positive questions, how often each true material was
    recognised.
    """
    pos = [r for r in records if r.positive]
    neg = [r for r in records if not r.positive]
    parsed = [r for r in records if r.reply is not None]
    tpr = _rate(sum(r.correct for r in pos), len(pos))
    tnr = _rate(sum(r.correct for r in neg), len(neg))
    balanced = None if tpr is None or tnr is None else (tpr + tnr) / 2
    false_yes: dict[str, list[bool]] = defaultdict(list)
    for r in neg:
        false_yes[r.asked].append(r.reply == "yes")
    true_yes: dict[str, list[bool]] = defaultdict(list)
    for r in pos:
        true_yes[r.truth].append(r.reply == "yes")
    return {
        "n": len(records),
        "n_positive": len(pos),
        "n_negative": len(neg),
        "n_parsed": len(parsed),
        "accuracy": _rate(sum(r.correct for r in records), len(records)),
        "balanced_accuracy": balanced,
        "true_positive_rate": tpr,
        "true_negative_rate": tnr,
        "yes_rate": _rate(sum(r.reply == "yes" for r in parsed), len(parsed)),
        "false_yes_by_asked": {k: sum(v) / len(v) for k, v in sorted(false_yes.items())},
        "true_yes_by_truth": {k: sum(v) / len(v) for k, v in sorted(true_yes.items())},
    }


# ---------------------------------------------------------------- two options


@dataclass(frozen=True)
class ChoiceRecord:
    """One two-option question: the two materials in prompt order, the truth, the pick.

    ``chosen`` is one of ``first``/``second``, None when unparsed, or any other string when
    the reply named neither option.
    """

    first: str
    second: str
    truth: str
    chosen: str | None
    group: Hashable  # the same object and view: identifies the swapped partner

    @property
    def distractor(self) -> str:
        return self.second if self.first == self.truth else self.first

    @property
    def valid(self) -> bool:
        return self.chosen in (self.first, self.second)

    @property
    def correct(self) -> bool:
        return self.chosen == self.truth


def choice_summary(records: Sequence[ChoiceRecord]) -> dict[str, Any]:
    """Accuracy, first-option rate, order consistency and accuracy per distractor.

    Order consistency is computed over swapped pairs: two questions with the same group and
    the same two materials in opposite orders, both answered with a valid option.
    """
    valid = [r for r in records if r.valid]
    pairs: dict[tuple[Hashable, frozenset[str]], list[ChoiceRecord]] = defaultdict(list)
    for r in records:
        pairs[(r.group, frozenset((r.first, r.second)))].append(r)
    swapped = [
        (a, b)
        for group in pairs.values()
        if len(group) == 2
        for a, b in [group]
        if a.first == b.second and a.second == b.first and a.valid and b.valid
    ]
    by_distractor: dict[str, list[bool]] = defaultdict(list)
    for r in records:
        by_distractor[r.distractor].append(r.correct)
    return {
        "n": len(records),
        "n_valid": len(valid),
        "accuracy": _rate(sum(r.correct for r in records), len(records)),
        "invalid_rate": _rate(len(records) - len(valid), len(records)),
        "first_option_rate": _rate(sum(r.chosen == r.first for r in valid), len(valid)),
        "n_swapped_pairs": len(swapped),
        "order_consistency": _rate(sum(a.chosen == b.chosen for a, b in swapped), len(swapped)),
        "accuracy_by_distractor": {k: sum(v) / len(v) for k, v in sorted(by_distractor.items())},
    }


def group_by(records: Iterable[Any], key: Any) -> dict[Any, list[Any]]:
    """Records grouped by ``key(record)``, keys sorted."""
    out: dict[Any, list[Any]] = defaultdict(list)
    for r in records:
        out[key(r)].append(r)
    return dict(sorted(out.items()))
