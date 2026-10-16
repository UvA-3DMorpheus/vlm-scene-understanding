"""Verification metrics against hand computed values."""

from __future__ import annotations

import pytest

from vsu.scoring.binary import ChoiceRecord, YesNoRecord, choice_summary, group_by, yesno_summary


def test_yesno_balanced_accuracy_and_bias() -> None:
    # object is metal; asked metal (positive) twice, wood and glass (negatives)
    records = [
        YesNoRecord("metal", "metal", "yes"),  # TP
        YesNoRecord("metal", "metal", None),  # unparsed positive: wrong
        YesNoRecord("wood", "metal", "no"),  # TN
        YesNoRecord("glass", "metal", "yes"),  # FP
        YesNoRecord("glass", "metal", "no"),  # TN
    ]
    s = yesno_summary(records)
    assert s["n"] == 5 and s["n_positive"] == 2 and s["n_negative"] == 3 and s["n_parsed"] == 4
    assert s["accuracy"] == pytest.approx(3 / 5)
    assert s["true_positive_rate"] == pytest.approx(1 / 2)
    assert s["true_negative_rate"] == pytest.approx(2 / 3)
    assert s["balanced_accuracy"] == pytest.approx((1 / 2 + 2 / 3) / 2)
    assert s["yes_rate"] == pytest.approx(2 / 4)
    assert s["false_yes_by_asked"] == {"glass": 0.5, "wood": 0.0}
    assert s["true_yes_by_truth"] == {"metal": 0.5}


def test_always_no_has_high_accuracy_but_chance_balanced_accuracy() -> None:
    records = [YesNoRecord("metal", "metal", "no")] + [
        YesNoRecord(m, "metal", "no") for m in ("wood", "glass", "plastic", "ceramic")
    ]
    s = yesno_summary(records)
    assert s["accuracy"] == pytest.approx(0.8) and s["balanced_accuracy"] == pytest.approx(0.5)
    assert s["yes_rate"] == 0.0


def test_yesno_empty_and_one_sided() -> None:
    assert yesno_summary([])["accuracy"] is None
    s = yesno_summary([YesNoRecord("wood", "metal", "no")])
    assert s["true_positive_rate"] is None and s["balanced_accuracy"] is None


def test_choice_first_option_rate_and_order_consistency() -> None:
    g = ("obj", "front/crop")
    records = [
        ChoiceRecord("metal", "wood", "metal", "metal", g),  # correct, picked first
        ChoiceRecord("wood", "metal", "metal", "wood", g),  # wrong, picked first: inconsistent
        ChoiceRecord("metal", "glass", "metal", "metal", g),  # correct, first
        ChoiceRecord("glass", "metal", "metal", "metal", g),  # correct, second: consistent
        ChoiceRecord("metal", "plastic", "metal", "rubber", g),  # named neither: invalid, wrong
        ChoiceRecord("plastic", "metal", "metal", None, g),  # unparsed
    ]
    s = choice_summary(records)
    assert s["n"] == 6 and s["n_valid"] == 4
    assert s["accuracy"] == pytest.approx(3 / 6)
    assert s["invalid_rate"] == pytest.approx(2 / 6)
    assert s["first_option_rate"] == pytest.approx(3 / 4)
    assert s["n_swapped_pairs"] == 2
    assert s["order_consistency"] == pytest.approx(1 / 2)
    assert s["accuracy_by_distractor"] == {"glass": 1.0, "plastic": 0.0, "wood": 0.5}


def test_swapped_pairs_need_the_same_group() -> None:
    records = [
        ChoiceRecord("metal", "wood", "metal", "metal", "a"),
        ChoiceRecord("wood", "metal", "metal", "metal", "b"),
    ]
    assert choice_summary(records)["n_swapped_pairs"] == 0
    assert choice_summary(records)["order_consistency"] is None


def test_group_by_sorts_keys() -> None:
    assert list(group_by([3, 1, 2, 1], lambda x: x % 2)) == [0, 1]
