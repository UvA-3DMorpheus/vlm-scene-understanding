"""Classification metrics against hand computed values."""

from __future__ import annotations

import pytest

from vsu.scoring.classification import (
    OTHER,
    UNPARSED,
    accuracy,
    agreement,
    classification_summary,
    confusion_matrix,
    fleiss_kappa,
    label_counts,
    macro_f1,
    per_class,
)

LABELS = ["a", "b", "c"]
TRUE = ["a", "a", "b", "b", "c"]
PRED = ["a", "b", "b", "b", None]  # one wrong, one unparsed


def test_accuracy_counts_failures_as_wrong_and_reports_parsed_separately() -> None:
    r = accuracy(TRUE, PRED)
    assert r == {"n": 5, "n_parsed": 4, "accuracy": 3 / 5, "accuracy_parsed": 3 / 4}
    assert accuracy([], []) == {"n": 0, "n_parsed": 0, "accuracy": None, "accuracy_parsed": None}
    with pytest.raises(ValueError):
        accuracy(["a"], [])


def test_confusion_matrix_has_other_and_unparsed_columns() -> None:
    cm = confusion_matrix(TRUE, [*PRED[:4], "zzz"], LABELS)
    assert cm["columns"] == ["a", "b", "c", OTHER, UNPARSED]
    assert cm["matrix"]["a"] == {"a": 1, "b": 1, "c": 0, OTHER: 0, UNPARSED: 0}
    assert cm["matrix"]["b"] == {"a": 0, "b": 2, "c": 0, OTHER: 0, UNPARSED: 0}
    assert cm["matrix"]["c"] == {"a": 0, "b": 0, "c": 0, OTHER: 1, UNPARSED: 0}
    assert confusion_matrix(TRUE, PRED, LABELS)["matrix"]["c"][UNPARSED] == 1
    with pytest.raises(ValueError):
        confusion_matrix(["q"], ["a"], LABELS)


def test_per_class_and_macro_f1() -> None:
    rows = per_class(TRUE, PRED, LABELS)
    # a: tp 1, fp 0, fn 1 -> p 1, r 0.5, f1 2/3
    assert rows["a"] == {"support": 2, "precision": 1.0, "recall": 0.5, "f1": pytest.approx(2 / 3)}
    # b: tp 2, fp 1, fn 0 -> p 2/3, r 1, f1 0.8
    assert rows["b"]["precision"] == pytest.approx(2 / 3) and rows["b"]["f1"] == pytest.approx(0.8)
    # c: never predicted -> precision undefined, recall 0, f1 0
    assert rows["c"] == {"support": 1, "precision": None, "recall": 0.0, "f1": 0.0}
    assert macro_f1(rows) == pytest.approx((2 / 3 + 0.8 + 0.0) / 3)


def test_macro_f1_ignores_labels_absent_from_ground_truth() -> None:
    rows = per_class(["a", "a"], ["a", "a"], ["a", "b"])
    assert rows["b"] == {"support": 0, "precision": None, "recall": None, "f1": None}
    assert macro_f1(rows) == 1.0
    assert macro_f1({}) is None


def test_summary_is_json_shaped() -> None:
    s = classification_summary(TRUE, PRED, LABELS)
    assert set(s) == {
        "n",
        "n_parsed",
        "accuracy",
        "accuracy_parsed",
        "macro_f1",
        "per_class",
        "confusion",
    }
    assert s["confusion"]["labels"] == LABELS


# ---------------------------------------------------------------- agreement


def test_fleiss_kappa_hand_example() -> None:
    # two raters, three subjects: agree, agree, disagree -> P_bar 2/3, P_e 0.5, kappa 1/3
    assert fleiss_kappa([["a", "a"], ["b", "b"], ["a", "b"]]) == pytest.approx(1 / 3)
    assert fleiss_kappa([["a", "a", "a"], ["b", "b", "b"]]) == 1.0
    assert fleiss_kappa([["a", "a"], ["a", "a"]]) == 1.0  # one category only: defined as perfect
    assert fleiss_kappa([]) is None
    assert fleiss_kappa([["a"]]) is None
    assert fleiss_kappa([["a", "b"], ["a"]]) is None


def test_agreement_across_variants() -> None:
    preds = {
        "v1": {"q1": "a", "q2": "b", "q3": "a", "q4": "c"},
        "v2": {"q1": "a", "q2": "b", "q3": "b", "q4": "c"},
        "v3": {"q1": "a", "q2": None, "q3": "b", "q5": "c"},  # q4 missing, q5 extra
    }
    r = agreement(preds)
    assert r["variants"] == ["v1", "v2", "v3"] and r["n_common"] == 3
    assert r["all_agree"] == pytest.approx(1 / 3)  # only q1
    assert r["pairwise"] == {
        "v1-v2": pytest.approx(2 / 3),
        "v1-v3": pytest.approx(1 / 3),
        "v2-v3": pytest.approx(2 / 3),
    }
    assert r["fleiss_kappa"] is not None and -1 <= r["fleiss_kappa"] < 1


def test_agreement_edge_cases() -> None:
    assert agreement({})["all_agree"] is None
    one = agreement({"v1": {"q": "a"}})
    assert one["fleiss_kappa"] is None and one["pairwise"] == {} and one["all_agree"] == 1.0
    disjoint = agreement({"v1": {"q1": "a"}, "v2": {"q2": "a"}})
    assert disjoint["n_common"] == 0 and disjoint["all_agree"] is None


def test_label_counts() -> None:
    assert label_counts(["a", "a", None, "b"]) == {"a": 2, UNPARSED: 1, "b": 1}
