"""Experiment 1 builds the right questions, maps answers onto label sets, and summarizes."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from tests.test_dataset import make_scene_dir
from vsu.experiments.base import ExperimentConfig, Question, load_experiment_config
from vsu.experiments.exp1_material import MaterialExperiment
from vsu.models.dummy_backend import DummyModel
from vsu.models.registry import ModelConfig
from vsu.prompts import loader
from vsu.schemas import MaterialAnswer
from vsu.schemas.scene import MATERIAL_CLASSES
from vsu.settings import Settings

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    data = tmp_path / "data"
    shutil.copytree(REPO / "data" / "smoke", data / "smoke")
    shutil.copytree(REPO / "data" / "materials", data / "materials")
    make_scene_dir(data / "sim", "sliding_cereal_box")  # material cardboard, cameras front + high
    return Settings(
        data_root=data,
        results_root=tmp_path / "runs",
        cache_root=tmp_path / "cache",
        _env_file=None,
    )


@pytest.fixture
def exp(settings: Settings) -> MaterialExperiment:
    return MaterialExperiment(load_experiment_config("exp1", settings), settings=settings)


def test_templates_exist_for_every_configured_variant(exp: MaterialExperiment) -> None:
    assert loader.list_variants("exp1") == ["v1", "v2", "v3"] == exp.variants()
    q = Question(
        id="x",
        dataset="smoke",
        item_id="x",
        images=["a.png"],
        context={"labels": ["metal", "wood"], "focus": "the main object in this photo"},
    )
    v1 = exp.render_prompt(q, "v1")
    assert "metal, wood" in v1 and "exactly one label" in v1
    assert '"material"' in exp.render_prompt(q, "v2") and "reasoning" in exp.render_prompt(q, "v3")


def test_questions_cover_smoke_and_labelled_sim_scenes(exp: MaterialExperiment) -> None:
    questions = exp.build_questions()
    smoke = [q for q in questions if q.dataset == "smoke"]
    sim = [q for q in questions if q.dataset == "sim"]
    assert len(smoke) == 18 and all(q.condition == "photo" for q in smoke)
    assert (
        smoke[0].context["labels"] == exp.table.keys and smoke[0].meta["labels"] == exp.table.keys
    )
    assert all(Path(q.images[0]).is_file() for q in questions)
    assert sorted(q.id for q in sim) == [
        "sim/sliding_cereal_box/front/crop",
        "sim/sliding_cereal_box/front/frame",
        "sim/sliding_cereal_box/high/crop",
        "sim/sliding_cereal_box/high/frame",
    ]
    crop = next(q for q in sim if q.condition == "crop")
    assert crop.target == {"material": "cardboard"} and crop.context["labels"] == list(
        MATERIAL_CLASSES
    )
    assert "crop_000000_object" in crop.images[0] and crop.meta["camera"] == "front"
    assert len({q.id for q in questions}) == len(questions)


def test_unlabelled_scenes_and_missing_cameras_are_skipped(settings: Settings) -> None:
    import json

    d = settings.sim_dir / "sliding_cereal_box"
    gt = json.loads((d / "ground_truth.json").read_text())
    gt["object"]["material_class"] = None
    (d / "ground_truth.json").write_text(json.dumps(gt))
    cfg = ExperimentConfig(
        name="exp1",
        variants=["v1"],
        options={"datasets": ["sim"], "sim_cameras": ["front", "left"]},
    )
    assert MaterialExperiment(cfg, settings=settings).build_questions() == []


def test_score_record_maps_open_set_answers(exp: MaterialExperiment) -> None:
    smoke_q = Question(
        id="s",
        dataset="smoke",
        item_id="s",
        images=["a"],
        context={"labels": exp.table.keys},
        target={"material": "metal"},
        meta={"labels": exp.table.keys},
    )
    sim_q = Question(
        id="m",
        dataset="sim",
        item_id="m",
        images=["a"],
        context={"labels": list(MATERIAL_CLASSES)},
        target={"material": "cardboard"},
        meta={"labels": list(MATERIAL_CLASSES)},
    )
    r = exp.score_record(
        smoke_q, MaterialAnswer(material="brushed stainless steel", confidence=0.7), "v2"
    )
    assert (
        r["predicted"] == "metal" and r["correct"] and r["in_label_set"] and r["confidence"] == 0.7
    )
    r = exp.score_record(smoke_q, MaterialAnswer(material="Aluminum"), "v2")
    assert r["predicted"] == "aluminium" and not r["correct"] and r["in_label_set"]
    r = exp.score_record(smoke_q, MaterialAnswer(material="unobtainium"), "v2")
    assert r["predicted"] == "unobtainium" and not r["in_label_set"] and not r["correct"]
    r = exp.score_record(sim_q, MaterialAnswer(material="corrugated cardboard box"), "v2")
    assert r["predicted"] == "cardboard" and r["correct"]
    r = exp.score_record(
        sim_q, MaterialAnswer(material="wood"), "v2"
    )  # resolves, but not in this label set
    assert r["predicted"] == "wood" and not r["in_label_set"] and not r["correct"]
    unparsed = exp.score_record(sim_q, None, "v1")
    assert (
        unparsed["correct"] is None and unparsed["predicted"] is None and unparsed["exact"] is None
    )


@pytest.mark.parametrize("variant", ["v1", "v2", "v3"])
def test_dummy_pipeline_end_to_end(exp: MaterialExperiment, variant: str) -> None:
    cfg = ModelConfig(name="dummy", backend="dummy")
    model = DummyModel(cfg)
    questions = exp.build_questions()
    run = exp.start_run(cfg, variant, questions)
    assert exp.run(run, model, variant) == 22
    scored = exp.score(run, variant)
    assert len(scored) == 22 and all(s.parse_ok for s in scored)
    summary = exp.report(run, variant)
    assert set(summary["groups"]) == {"smoke/photo", "sim/crop", "sim/frame"}
    sim = summary["groups"]["sim/frame"]
    assert sim["n"] == 2 and sim["confusion"]["labels"] == list(MATERIAL_CLASSES)
    assert set(summary["datasets"]["sim"]["by_camera"]) == {"front", "high"}
    assert summary["datasets"]["sim"]["by_camera"]["front"]["n"] == 2
    assert summary["datasets"]["smoke"]["by_camera"] == {}
    smoke = summary["groups"]["smoke/photo"]
    assert smoke["n"] == 18 and set(smoke["per_class"]) >= {"metal", "wood", "glass"}
    assert summary["primary_dataset"] == "sim" and summary["sanity_datasets"] == ["smoke"]
    assert summary["datasets"]["sim"]["role"] == "primary" and summary["datasets"]["sim"]["n"] == 4
    assert (
        summary["datasets"]["smoke"]["role"] == "sanity" and summary["datasets"]["smoke"]["n"] == 18
    )
    assert 0.0 <= summary["datasets"]["smoke"]["accuracy"] <= 1.0
    assert (
        summary["datasets"]["sim"]["exact_label_rate"] == 1.0
    )  # the dummy always uses a listed label
    assert "overall" not in summary
    assert summary["num_parse_failures"] == 0


def test_failures_flow_into_the_summary(exp: MaterialExperiment) -> None:
    cfg = ModelConfig(name="dummy", backend="dummy", options={"failure_rate": 0.5})
    run = exp.start_run(cfg, "v3", exp.build_questions())
    exp.run(run, DummyModel(cfg), "v3")
    exp.score(run, "v3")
    summary = exp.report(run, "v3")
    assert 0 < summary["num_parse_failures"] < 22
    smoke = summary["groups"]["smoke/photo"]
    assert smoke["n"] == 18 and smoke["n_parsed"] < 18
    assert (
        sum(row["<unparsed>"] for row in smoke["confusion"]["matrix"].values())
        == 18 - smoke["n_parsed"]
    )
