"""Cross-task consistency rules, on hand-made scored records."""

from __future__ import annotations

from typing import Any

from vsu.experiments.base import ScoredRecord
from vsu.experiments.material.consistency import (
    choice_consistency,
    identification_labels,
    matching_consistency,
    yesno_consistency,
)


def rec(qid: str, derived: dict[str, Any], meta: dict[str, Any], ok: bool = True) -> ScoredRecord:
    return ScoredRecord(
        question_id=qid,
        dataset="sim_realistic",
        item_id="x",
        condition="crop",
        parse_ok=ok,
        target={"material": "ceramic"},
        derived=derived,
        meta=meta,
    )


V_TRAY, V_BOOK = "sim_realistic/tray/front/crop", "sim_realistic/book/front/crop"
# the model calls the (ceramic) tray metal and the book paper in Experiment 1.0
LABELS = identification_labels(
    [
        rec(V_TRAY, {"predicted": "metal"}, {}),
        rec(V_BOOK, {"predicted": "book_paper_cover"}, {}),
        rec("sim_realistic/box/front/crop", {"predicted": None}, {}, ok=False),
    ]
)


def test_identification_labels_keep_unparsed_as_none() -> None:
    assert LABELS == {
        V_TRAY: "metal",
        V_BOOK: "book_paper_cover",
        "sim_realistic/box/front/crop": None,
    }


def test_yesno_consistency_follows_the_models_own_label() -> None:
    scored = [
        rec(
            "q1", {"reply": "yes"}, {"view": V_TRAY, "asked": "metal"}
        ),  # consistent (wrong though)
        rec("q2", {"reply": "no"}, {"view": V_TRAY, "asked": "ceramic"}),  # consistent
        rec("q3", {"reply": "yes"}, {"view": V_TRAY, "asked": "ceramic"}),  # inconsistent
        rec("q4", {"reply": None}, {"view": V_TRAY, "asked": "metal"}, ok=False),  # skipped
        rec(
            "q5", {"reply": "yes"}, {"view": "sim_realistic/box/front/crop", "asked": "metal"}
        ),  # no label
    ]
    assert yesno_consistency(LABELS, scored) == {"n": 3, "consistency": 2 / 3}


def test_choice_consistency_only_where_the_label_is_an_option() -> None:
    scored = [
        rec("c1", {"chosen": "metal"}, {"view": V_TRAY, "first": "metal", "second": "ceramic"}),
        rec("c2", {"chosen": "ceramic"}, {"view": V_TRAY, "first": "ceramic", "second": "metal"}),
        rec("c3", {"chosen": "ceramic"}, {"view": V_TRAY, "first": "ceramic", "second": "plastic"}),
    ]
    assert choice_consistency(LABELS, scored) == {"n": 2, "consistency": 0.5}


def test_matching_consistency_needs_exactly_one_object_with_the_label() -> None:
    meta = {"view_a": V_TRAY, "view_b": V_BOOK}
    scored = [
        rec("m1", {"chosen": "A"}, {**meta, "asked": "metal"}),  # 1.0 says tray=metal: consistent
        rec(
            "m2", {"chosen": "A"}, {**meta, "asked": "book_paper_cover"}
        ),  # book is paper: inconsistent
        rec(
            "m3", {"chosen": "B"}, {**meta, "asked": "ceramic"}
        ),  # neither labelled ceramic: skipped
        rec(
            "m4", {"chosen": "B"}, {"view_a": V_BOOK, "view_b": V_TRAY, "asked": "metal"}
        ),  # consistent
    ]
    assert matching_consistency(LABELS, scored) == {"n": 3, "consistency": 2 / 3}


def test_no_labels_gives_no_consistency() -> None:
    assert yesno_consistency(
        {}, [rec("q", {"reply": "yes"}, {"view": V_TRAY, "asked": "metal"})]
    ) == {
        "n": 0,
        "consistency": None,
    }
