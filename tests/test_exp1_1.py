"""Experiment 1.1 builds balanced yes/no and swapped two-option questions and scores them."""

from __future__ import annotations

import shutil
from collections import Counter
from pathlib import Path

import pytest

from tests.test_dataset import make_scene_dir
from vsu.experiments.base import Question, load_experiment_config
from vsu.experiments.material.verify import VerificationExperiment, task_of
from vsu.models.dummy_backend import DummyModel
from vsu.models.registry import ModelConfig
from vsu.prompts import loader
from vsu.schemas import ChoiceAnswer, YesNoAnswer
from vsu.settings import Settings

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    data = tmp_path / "data"
    shutil.copytree(REPO / "data" / "smoke", data / "smoke")
    shutil.copytree(REPO / "data" / "materials", data / "materials")
    make_scene_dir(
        data / "sim" / "realistic", "sliding_cereal_box"
    )  # cardboard, cameras front + high
    return Settings(
        data_root=data,
        results_root=tmp_path / "runs",
        cache_root=tmp_path / "cache",
        _env_file=None,
    )


@pytest.fixture
def exp(settings: Settings) -> VerificationExperiment:
    return VerificationExperiment(load_experiment_config("exp1_1", settings), settings=settings)


def test_variants_have_templates_and_tasks(exp: VerificationExperiment) -> None:
    assert loader.list_variants("exp1_1") == ["choice_v1", "choice_v2", "yesno_v1", "yesno_v2"]
    assert [task_of(v) for v in exp.variants()] == ["yesno", "yesno", "choice", "choice"]
    assert exp.schema_for("yesno_v2") is YesNoAnswer and exp.schema_for("choice_v1") is ChoiceAnswer
    assert exp.bare_label_field_for("yesno_v1") == "answer"
    assert exp.bare_label_field_for("choice_v1") == "material"
    assert exp.bare_label_field_for("choice_v2") is None
    with pytest.raises(ValueError):
        task_of("v1")


def test_question_counts_and_balance(exp: VerificationExperiment) -> None:
    questions = exp.build_questions()
    counts = Counter((q.dataset, q.meta["task"]) for q in questions)
    # scene: yesno on 2 cameras x (frame, crop) x (1 true + 4 wrong); choice on crops, 4 x 2 orders
    assert counts[("sim_realistic", "yesno")] == 2 * 2 * 5
    assert counts[("sim_realistic", "choice")] == 2 * 1 * 4 * 2
    # photos: 18 x 5 yes/no and 18 x 8 choices (4 sampled wrong materials of 11)
    assert counts[("smoke", "yesno")] == 18 * 5 and counts[("smoke", "choice")] == 18 * 8
    assert len({q.id for q in questions}) == len(questions)
    yesno = [q for q in questions if q.meta["task"] == "yesno" and q.dataset == "sim_realistic"]
    assert sum(q.meta["asked"] == q.target["material"] for q in yesno) == 4  # one positive per view
    choices = [q for q in questions if q.meta["task"] == "choice" and q.dataset == "sim_realistic"]
    assert all(q.condition == "crop" for q in choices)
    pairs = Counter(frozenset((q.meta["first"], q.meta["second"])) for q in choices)
    assert set(pairs.values()) == {4}  # each pair twice per view (two orders), two views


def test_smoke_distractors_are_seeded_and_stable(settings: Settings) -> None:
    a = VerificationExperiment(load_experiment_config("exp1_1", settings), settings=settings)
    b = VerificationExperiment(load_experiment_config("exp1_1", settings), settings=settings)
    assert [q.id for q in a.build_questions()] == [q.id for q in b.build_questions()]


def test_prompts_use_readable_material_names(exp: VerificationExperiment) -> None:
    questions = exp.build_questions()
    q = next(
        q for q in questions if q.meta["task"] == "yesno" and q.meta["asked"] == "book_paper_cover"
    )
    prompt = exp.render_prompt(q, "yesno_v1")
    assert "made of book paper?" in prompt and "book_paper_cover" not in prompt
    c = next(q for q in questions if q.meta["task"] == "choice" and q.dataset == "sim_realistic")
    text = exp.render_prompt(c, "choice_v1")
    assert f"{c.context['first']} or of {c.context['second']}" in text


def test_questions_for_selects_the_task(exp: VerificationExperiment) -> None:
    questions = exp.build_questions()
    assert all(q.meta["task"] == "yesno" for q in exp.questions_for("yesno_v2", questions))
    assert all(q.meta["task"] == "choice" for q in exp.questions_for("choice_v1", questions))


def _q(**meta: str) -> Question:
    return Question(
        id="x",
        dataset="sim_realistic",
        item_id="x",
        images=["a"],
        target={"material": "metal"},
        meta=meta,
    )


def test_score_record_yesno_and_choice_mapping(exp: VerificationExperiment) -> None:
    pos = _q(task="yesno", asked="metal")
    assert exp.score_record(pos, YesNoAnswer(answer="Yes."), "yesno_v1") == {
        "reply": "yes",
        "positive": True,
        "correct": True,
    }
    assert (
        exp.score_record(_q(task="yesno", asked="ceramic"), YesNoAnswer(answer="yes"), "yesno_v1")[
            "correct"
        ]
        is False
    )
    assert exp.score_record(pos, None, "yesno_v1")["correct"] is False
    choice = _q(task="choice", first="book_paper_cover", second="metal")
    r = exp.score_record(choice, ChoiceAnswer(material="Book paper"), "choice_v1")
    assert r["chosen"] == "book_paper_cover" and r["first_chosen"] and not r["correct"]
    r = exp.score_record(choice, ChoiceAnswer(material="stainless steel"), "choice_v1")
    assert r["chosen"] == "metal" and r["correct"] and r["valid"]
    r = exp.score_record(choice, ChoiceAnswer(material="wood"), "choice_v1")
    assert r["chosen"] == "wood" and not r["valid"] and not r["correct"]


@pytest.mark.parametrize("variant", ["yesno_v1", "yesno_v2", "choice_v1", "choice_v2"])
def test_dummy_pipeline_end_to_end(exp: VerificationExperiment, variant: str) -> None:
    cfg = ModelConfig(name="dummy", backend="dummy")
    questions = exp.questions_for(variant, exp.build_questions())
    run = exp.start_run(cfg, variant, questions)
    assert exp.run(run, DummyModel(cfg), variant) == len(questions)
    scored = exp.score(run, variant)
    assert all(s.parse_ok for s in scored)
    summary = exp.report(run, variant)
    assert summary["task"] == task_of(variant)
    sim = summary["datasets"]["sim_realistic"]
    assert sim["role"] == "primary" and summary["datasets"]["smoke"]["role"] == "sanity"
    assert set(sim["by_camera"]) == {"front", "high"}
    if task_of(variant) == "yesno":
        assert sim["n"] == 20 and 0 <= sim["balanced_accuracy"] <= 1 and sim["yes_rate"] is not None
    else:
        assert sim["n"] == 16 and sim["n_swapped_pairs"] <= 8 and "first_option_rate" in sim
        assert set(summary["groups"]) == {"sim_realistic/crop", "smoke/photo"}


def test_smoke_never_asks_an_overlapping_material_as_wrong(exp: VerificationExperiment) -> None:
    for q in exp.build_questions():
        if q.meta["task"] == "yesno" and q.meta["asked"] != q.target["material"]:
            assert {q.meta["asked"], q.target["material"]} not in (
                {"plastic", "ping_pong_plastic"},
                {"metal", "aluminium"},
            )
