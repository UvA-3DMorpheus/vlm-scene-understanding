"""Metrics for questions about two objects shown together (Experiment 1.2, later Experiment 3).

A pair question shows object A and object B and asks which one has a property ("which is
made of metal?"). Each pair is asked in four forms: both image orders times both asked
values. The metrics separate getting it right from answering consistently:

- ``accuracy``: the right object picked, over all questions (unparsed counts as wrong).
- ``a_rate``: how often the answer is A, over valid answers; 0.5 is unbiased, so a value
  away from it is a position bias.
- ``image_order_consistency``: over question pairs that differ only in image order, the
  fraction where the same object is picked both times (the letter flips with the images).
- ``label_consistency``: over question pairs that differ only in the asked value, the
  fraction where different objects are picked (one object cannot be both materials).
- ``solved_rate``: the fraction of pairs where all four forms are answered correctly.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Hashable, Sequence
from dataclasses import dataclass
from typing import Any

LETTERS = ("A", "B")


def _rate(num: int, den: int) -> float | None:
    return (num / den) if den else None


@dataclass(frozen=True)
class PairRecord:
    """One pair question.

    ``pair`` identifies the two objects in one view regardless of order; ``image_a`` and
    ``image_b`` name the objects in the order shown; ``asked`` is the asked value and
    ``answer_object`` the object that has it; ``chosen`` is ``A``, ``B`` or None.
    """

    pair: Hashable
    image_a: str
    image_b: str
    asked: str
    answer_object: str
    chosen: str | None

    @property
    def truth(self) -> str:
        return "A" if self.answer_object == self.image_a else "B"

    @property
    def valid(self) -> bool:
        return self.chosen in LETTERS

    @property
    def correct(self) -> bool:
        return self.chosen == self.truth

    @property
    def chosen_object(self) -> str | None:
        if self.chosen == "A":
            return self.image_a
        if self.chosen == "B":
            return self.image_b
        return None


def pair_summary(records: Sequence[PairRecord]) -> dict[str, Any]:
    """Accuracy, letter bias and the three consistency rates. See the module docstring."""
    valid = [r for r in records if r.valid]
    by_asked: dict[tuple[Hashable, str], list[PairRecord]] = defaultdict(list)
    by_order: dict[tuple[Hashable, str, str], list[PairRecord]] = defaultdict(list)
    by_pair: dict[Hashable, list[PairRecord]] = defaultdict(list)
    for r in records:
        by_asked[(r.pair, r.asked)].append(r)
        by_order[(r.pair, r.image_a, r.image_b)].append(r)
        by_pair[r.pair].append(r)
    order_pairs = [
        (a, b)
        for group in by_asked.values()
        for i, a in enumerate(group)
        for b in group[i + 1 :]
        if a.image_a == b.image_b and a.image_b == b.image_a and a.valid and b.valid
    ]
    label_pairs = [
        (a, b)
        for group in by_order.values()
        for i, a in enumerate(group)
        for b in group[i + 1 :]
        if a.asked != b.asked and a.valid and b.valid
    ]
    complete = [g for g in by_pair.values() if len(g) == 4]
    return {
        "n": len(records),
        "n_valid": len(valid),
        "n_pairs": len(by_pair),
        "accuracy": _rate(sum(r.correct for r in records), len(records)),
        "a_rate": _rate(sum(r.chosen == "A" for r in valid), len(valid)),
        "image_order_consistency": _rate(
            sum(a.chosen_object == b.chosen_object for a, b in order_pairs), len(order_pairs)
        ),
        "label_consistency": _rate(
            sum(a.chosen_object != b.chosen_object for a, b in label_pairs), len(label_pairs)
        ),
        "solved_rate": _rate(sum(all(r.correct for r in g) for g in complete), len(complete)),
    }
