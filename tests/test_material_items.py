"""Shared material items: datasets, views, ids and roles used by Experiments 1.0 to 1.2."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from tests.test_dataset import make_scene_dir
from vsu.data.materials import load_material_table
from vsu.experiments.material.items import (
    MaterialView,
    dataset_roles,
    load_items,
    sim_collection,
)
from vsu.schemas.scene import MATERIAL_CLASSES
from vsu.settings import Settings

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    data = tmp_path / "data"
    shutil.copytree(REPO / "data" / "smoke", data / "smoke")
    shutil.copytree(REPO / "data" / "materials", data / "materials")
    make_scene_dir(data / "sim" / "realistic", "sliding_cereal_box")
    make_scene_dir(data / "sim" / "preview", "sliding_cereal_box")
    return Settings(data_root=data, cache_root=tmp_path / "cache", _env_file=None)


OPTIONS = {
    "datasets": ["sim_realistic", "sim_preview", "smoke"],
    "sim_cameras": ["front", "high"],
    "sim_conditions": ["frame", "crop"],
    "sim_multiview": True,
}


def test_collections_are_separate_datasets_with_their_own_images(settings: Settings) -> None:
    items = load_items(OPTIONS, settings, load_material_table(settings=settings))
    by_dataset = {}
    for item in items:
        by_dataset.setdefault(item.dataset, []).append(item)
    assert set(by_dataset) == {"sim_realistic", "sim_preview", "smoke"}
    real, prev = by_dataset["sim_realistic"][0], by_dataset["sim_preview"][0]
    assert real.item_id == prev.item_id == "sliding_cereal_box"
    assert real.material == "cardboard" and real.labels == tuple(MATERIAL_CLASSES)
    assert [v.key for v in real.views] == [
        "all/multiview",
        "front/frame",
        "front/crop",
        "high/frame",
        "high/crop",
    ]
    assert real.view("front/crop") is not None and real.view("low/crop") is None
    assert "/sim/realistic/" in real.view("front/frame").images[0]
    assert "/sim/preview/" in prev.view("front/frame").images[0]
    assert real.view_id(real.views[1]) == "sim_realistic/sliding_cereal_box/front/frame"
    smoke = by_dataset["smoke"][0]
    assert smoke.views == (MaterialView("photo", smoke.views[0].images),)
    assert smoke.view_id(smoke.views[0]) == f"smoke/{smoke.item_id}/photo"


def test_missing_collection_gives_no_items(settings: Settings) -> None:
    shutil.rmtree(settings.sim_collection_dir("realistic"))
    items = load_items(
        {"datasets": ["sim_realistic"]}, settings, load_material_table(settings=settings)
    )
    assert items == []


def test_unknown_dataset_and_bad_roles() -> None:
    with pytest.raises(ValueError, match="not a simulation dataset"):
        sim_collection("smoke")
    assert sim_collection("sim_realistic") == "realistic"
    with pytest.raises(ValueError, match="unknown dataset"):
        load_items({"datasets": ["imagenet"]}, Settings(_env_file=None), None)  # type: ignore[arg-type]
    assert dataset_roles({"dataset_roles": {"a": "primary", "b": "sanity"}}) == {
        "a": "primary",
        "b": "sanity",
    }
    with pytest.raises(ValueError, match="unknown dataset roles"):
        dataset_roles({"dataset_roles": {"a": "headline"}})
    with pytest.raises(ValueError, match="only one"):
        dataset_roles({"dataset_roles": {"a": "primary", "b": "primary"}})


def test_overlapping_materials_are_not_distinct() -> None:
    from vsu.experiments.material.items import distinct_materials, label_text

    assert not distinct_materials("plastic", "ping_pong_plastic")
    assert not distinct_materials("aluminium", "metal") and not distinct_materials("metal", "metal")
    assert distinct_materials("cardboard", "book_paper_cover")
    assert label_text("book_paper_cover") == "book paper"
