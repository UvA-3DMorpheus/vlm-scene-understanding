"""Experiment 1.2 builds four forms per pair and presentation, composites, and scores pairs."""

from __future__ import annotations

import json
import shutil
from collections import Counter
from pathlib import Path

import pytest
from PIL import Image

from tests.test_dataset import make_scene_dir
from vsu.experiments.base import load_experiment_config
from vsu.experiments.material.match import MatchingExperiment, side_by_side
from vsu.models.dummy_backend import DummyModel
from vsu.models.registry import ModelConfig
from vsu.prompts import loader
from vsu.schemas import PairChoiceAnswer
from vsu.settings import Settings

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    data = tmp_path / "data"
    shutil.copytree(REPO / "data" / "smoke", data / "smoke")
    shutil.copytree(REPO / "data" / "materials", data / "materials")
    root = data / "sim" / "realistic"
    make_scene_dir(root, "sliding_cereal_box")  # cardboard
    tray = make_scene_dir(root, "sliding_tray")
    gt = json.loads((tray / "ground_truth.json").read_text())
    gt["object"]["material_class"] = "ceramic"
    (tray / "ground_truth.json").write_text(json.dumps(gt))
    make_scene_dir(root, "sliding_board_game")  # cardboard again: no pair with the cereal box
    return Settings(
        data_root=data,
        results_root=tmp_path / "runs",
        cache_root=tmp_path / "cache",
        _env_file=None,
    )


@pytest.fixture
def exp(settings: Settings) -> MatchingExperiment:
    return MatchingExperiment(load_experiment_config("exp1_2", settings), settings=settings)


def test_templates_and_answer_aliases() -> None:
    assert loader.list_variants("exp1_2") == ["v1", "v2"]
    assert PairChoiceAnswer(choice="b.").choice == "B"
    assert PairChoiceAnswer(choice="The first one").choice == "A"
    assert PairChoiceAnswer(choice="right").choice == "B"


def test_pairs_forms_and_balance(exp: MatchingExperiment) -> None:
    questions = exp.build_questions()
    sim = [q for q in questions if q.dataset == "sim_realistic"]
    # tray (ceramic) with each cardboard object: 2 pairs x 2 cameras x 2 presentations x 4 forms
    assert len(sim) == 2 * 2 * 2 * 4
    assert {q.meta["materials"][0] + "|" + q.meta["materials"][1] for q in sim} == {
        "cardboard|ceramic"
    }
    assert set(Counter(q.meta["pair"] for q in sim).values()) == {4}
    assert Counter(q.target["object"] == q.meta["image_a"] for q in sim) == {True: 16, False: 16}
    smoke = [q for q in questions if q.dataset == "smoke"]
    assert len(smoke) == 20 * 2 * 4  # sampled pairs x presentations x forms
    assert len({q.id for q in questions}) == len(questions)


def test_presentations_use_two_images_or_one_composite(exp: MatchingExperiment) -> None:
    questions = exp.build_questions()
    sep = next(q for q in questions if q.condition == "separate" and q.dataset == "sim_realistic")
    sbs = next(q for q in questions if q.condition == "sidebyside" and q.dataset == "sim_realistic")
    assert len(sep.images) == 2 and len(sbs.images) == 1 and "pair_" in sbs.images[0]
    prompt = exp.render_prompt(sep, "v1")
    assert "first image shows object A" in prompt and "A or B" in prompt
    assert "left" in exp.render_prompt(sbs, "v2") and '"choice"' in exp.render_prompt(sbs, "v2")
    assert (
        f"made of {sep.context['asked']} and the other is made of {sep.context['other']}" in prompt
    )


def test_side_by_side_is_deterministic(tmp_path: Path) -> None:
    for name, colour in (("l.png", (200, 0, 0)), ("r.png", (0, 0, 200))):
        Image.new("RGB", (40, 20), colour).save(tmp_path / name)
    a = side_by_side(str(tmp_path / "l.png"), str(tmp_path / "r.png"), tmp_path / "out", height=60)
    b = side_by_side(str(tmp_path / "l.png"), str(tmp_path / "r.png"), tmp_path / "out", height=60)
    c = side_by_side(str(tmp_path / "r.png"), str(tmp_path / "l.png"), tmp_path / "out", height=60)
    assert a == b and a != c
    im = Image.open(a)
    assert im.size == (120 + 24 + 120, 60 + 64)
    assert im.getpixel((10, 100))[0] > 150 and im.getpixel((200, 100))[2] > 150


def test_score_record(exp: MatchingExperiment) -> None:
    q = next(q for q in exp.build_questions() if q.dataset == "sim_realistic")
    right = "A" if q.target["object"] == q.meta["image_a"] else "B"
    wrong = "B" if right == "A" else "A"
    assert exp.score_record(q, PairChoiceAnswer(choice=right), "v1")["correct"] is True
    r = exp.score_record(q, PairChoiceAnswer(choice=wrong), "v1")
    assert r["correct"] is False and r["chosen_object"] != q.target["object"]
    assert exp.score_record(q, None, "v1")["chosen"] is None


@pytest.mark.parametrize("variant", ["v1", "v2"])
def test_dummy_pipeline_end_to_end(exp: MatchingExperiment, variant: str) -> None:
    cfg = ModelConfig(name="dummy", backend="dummy")
    questions = exp.build_questions()
    run = exp.start_run(cfg, variant, questions)
    assert exp.run(run, DummyModel(cfg), variant) == len(questions)
    assert all(s.parse_ok for s in exp.score(run, variant))
    summary = exp.report(run, variant)
    sim = summary["datasets"]["sim_realistic"]
    assert sim["role"] == "primary" and sim["n"] == 32 and sim["n_pairs"] == 8
    assert set(sim["by_camera"]) == {"front", "high"} and set(sim["by_material_pair"]) == {
        "cardboard|ceramic"
    }
    assert set(summary["groups"]) >= {"sim_realistic/separate", "sim_realistic/sidebyside"}
    assert 0 <= sim["a_rate"] <= 1 and sim["solved_rate"] is not None
