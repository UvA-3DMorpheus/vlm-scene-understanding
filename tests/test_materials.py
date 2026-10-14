"""The materials files load, agree with each other, and resolve free text labels."""

from __future__ import annotations

from pathlib import Path

import pytest

from vsu.data.materials import (
    contact_values,
    load_material_table,
    load_materials_json,
    materials_json_sha256,
)
from vsu.schemas.scene import MATERIAL_CLASSES
from vsu.settings import Settings

REPO_DATA = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture
def settings() -> Settings:
    return Settings(data_root=REPO_DATA, _env_file=None)


def test_materials_json_is_the_simulation_teams_file(settings: Settings) -> None:
    table = load_materials_json(settings=settings)
    assert table["version"] == "1.0.0"
    assert set(table["materials"]) == set(MATERIAL_CLASSES)
    assert contact_values(table, "cardboard")["mu_kinetic"] == 0.40
    assert contact_values(table, "ceramic")["restitution"] is None
    assert len(materials_json_sha256(settings=settings)) == 64


def test_material_table_covers_every_simulation_class_with_sources(settings: Settings) -> None:
    table = load_material_table(settings=settings)
    for key in MATERIAL_CLASSES:
        assert key in table, key
        row = table[key]
        assert row.sources, f"{key} has no sources"
        assert all(s in table.sources for s in row.sources)


def test_simulator_point_values_lie_inside_our_ranges(settings: Settings) -> None:
    """Their illustrative values must be covered by our ranges, or E2b cannot be right."""
    sim = load_materials_json(settings=settings)
    table = load_material_table(settings=settings)
    for key in MATERIAL_CLASSES:
        row = table[key]
        density = sim["materials"][key]["density_kg_m3"]
        assert row.density_kg_m3[0] <= density <= row.density_kg_m3[1], (key, density)
        contact = contact_values(sim, key)
        lo, hi = row.friction_kinetic_on_wood
        assert lo <= contact["mu_kinetic"] <= hi, (key, contact["mu_kinetic"])
        lo, hi = row.friction_static_on_wood
        assert lo <= contact["mu_static"] <= hi, (key, contact["mu_static"])


def test_ranges_are_ordered_and_restitution_bounded(settings: Settings) -> None:
    table = load_material_table(settings=settings)
    for row in table.rows.values():
        for name in (
            "density_kg_m3",
            "restitution",
            "friction_static_on_wood",
            "friction_kinetic_on_wood",
            "friction_static_on_steel",
            "friction_kinetic_on_steel",
        ):
            lo, hi = row.range_of(name)
            assert 0 <= lo <= hi, (row.key, name)
        assert row.restitution[1] <= 1.0
        assert row.midpoint("friction") == pytest.approx(sum(row.friction_kinetic_on_wood) / 2)


@pytest.mark.parametrize(
    ("label", "key"),
    [
        ("metal", "metal"),
        ("Stainless steel", "metal"),
        ("brushed stainless steel", "metal"),
        ("Aluminum", "aluminium"),
        ("ping-pong ball", "ping_pong_plastic"),
        ("glazed porcelain", "ceramic"),
        ("a paperback book", "book_paper_cover"),
        ("corrugated cardboard box", "cardboard"),
        ("wooden", "wood"),
        ("unobtainium", None),
    ],
)
def test_resolve_free_text_labels(settings: Settings, label: str, key: str | None) -> None:
    table = load_material_table(settings=settings)
    assert table.resolve(label) == key


def test_bad_table_is_rejected(tmp_path: Path) -> None:
    bad = tmp_path / "material_table.yaml"
    bad.write_text(
        "version: 1\nsources: {}\nmaterials:\n  x:\n    label: x\n    density_kg_m3: [5, 1]\n"
        "    restitution: [0, 1]\n    friction_static_on_wood: [0, 1]\n"
        "    friction_kinetic_on_wood: [0, 1]\n"
        "    friction_static_on_steel: [0, 1]\n    friction_kinetic_on_steel: [0, 1]\n"
    )
    with pytest.raises(ValueError, match="below low"):
        load_material_table(bad)
    bad.write_text(bad.read_text().replace("[5, 1]", "[1, 5]") + "    sources: [nope]\n")
    with pytest.raises(ValueError, match="unknown sources"):
        load_material_table(bad)
