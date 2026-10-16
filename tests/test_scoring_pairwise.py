"""Pair metrics against hand computed values."""

from __future__ import annotations

import pytest

from vsu.scoring.pairwise import PairRecord, pair_summary

P = ("tray", "book", "front/crop")


def four(chosen: tuple[str | None, str | None, str | None, str | None]) -> list[PairRecord]:
    """The four forms of one pair (tray is ceramic, book is paper), with the given letters."""
    return [
        PairRecord(P, "tray", "book", "ceramic", "tray", chosen[0]),  # truth A
        PairRecord(P, "tray", "book", "paper", "book", chosen[1]),  # truth B
        PairRecord(P, "book", "tray", "ceramic", "tray", chosen[2]),  # truth B
        PairRecord(P, "book", "tray", "paper", "book", chosen[3]),  # truth A
    ]


def test_perfect_pair() -> None:
    s = pair_summary(four(("A", "B", "B", "A")))
    assert s["accuracy"] == 1.0 and s["a_rate"] == 0.5 and s["solved_rate"] == 1.0
    assert s["image_order_consistency"] == 1.0 and s["label_consistency"] == 1.0
    assert s["n_pairs"] == 1 and s["n_valid"] == 4


def test_always_a_is_inconsistent_and_half_right() -> None:
    s = pair_summary(four(("A", "A", "A", "A")))
    assert s["accuracy"] == 0.5 and s["a_rate"] == 1.0 and s["solved_rate"] == 0.0
    # swapping the images while answering A picks a different object each time
    assert s["image_order_consistency"] == 0.0
    # asking about either material while answering A picks the same object
    assert s["label_consistency"] == 0.0


def test_consistent_but_wrong_and_unparsed() -> None:
    s = pair_summary(four(("B", "A", "A", "B")))  # always the other object
    assert (
        s["accuracy"] == 0.0
        and s["image_order_consistency"] == 1.0
        and s["label_consistency"] == 1.0
    )
    s = pair_summary(four(("A", None, "B", "A")))
    assert s["accuracy"] == pytest.approx(3 / 4) and s["n_valid"] == 3 and s["solved_rate"] == 0.0
    assert s["a_rate"] == pytest.approx(2 / 3)
    assert s["image_order_consistency"] == 1.0  # only the ceramic question pair is complete
    assert s["label_consistency"] == 1.0  # only the book-first pair is complete


def test_empty() -> None:
    s = pair_summary([])
    assert s["accuracy"] is None and s["solved_rate"] is None
