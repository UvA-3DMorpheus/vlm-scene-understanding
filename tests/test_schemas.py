"""Scene and answer schemas validate what they should and reject what they should not."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from vsu.schemas import (
    MATERIAL_CLASSES,
    SCENARIO_TO_PHENOMENON,
    ComparativeAnswer,
    GroundTruth,
    MaterialAnswer,
    ObjectConfig,
    ParsedAnswer,
    PropertiesAnswer,
    PropertyRange,
    SceneConfig,
    SceneInitAnswer,
    normalize_label,
)


def sliding_gt(**overrides: object) -> dict:
    """A sliding scene in our internal layout, with the values Emil's pipeline writes."""
    base = {
        "scene_id": "sliding_book",
        "schema_version": "2.0",
        "scenario": "sliding_with_friction",
        "phenomenon": "sliding",
        "trajectory_mode": "analytic",
        "fps": 24,
        "physics_timestep": 1 / 2400,
        "gravity": [0, 0, -9.81],
        "objects": [
            {
                "id": "object",
                "name": "Eat_to_Live_Book",
                "key": "book",
                "shape": "mesh",
                "material_class": "book_paper_cover",
                "bbox_body_frame_m": [0.209, 0.139, 0.050],
                "volume_m3": 0.00056,
                "density_kg_m3": 800.0,
                "density_basis": "effective_density",
                "mass_kg": 0.45,
                "segmentation_geom_id": 7,
                "dataset": "Google Scanned Objects",
                "license": "CC-BY 4.0",
            }
        ],
        "surface": {
            "name": "finished_wood",
            "label": "finished (varnished) wood, tabletop / ramp",
            "ramp_angle_deg": 30.0,
            "ramp_azimuth_deg": 30.0,
            "ramp_normal": [0.433, 0.25, 0.866],
            "ramp_downhill_direction": [0.75, 0.433, -0.5],
        },
        "contact": {
            "object_material": "book_paper_cover",
            "surface": "finished_wood",
            "model": "Coulomb kinetic friction, analytic (no rotation)",
            "mu_kinetic": 0.45,
            "mu_static": 0.55,
            "restitution": None,
            "source": "illustrative value within published ranges",
        },
        "expected": {"formula": "s(t) = 0.5 a t^2", "acceleration_magnitude_mps2": 1.082},
        "initial_position": [0.0, 0.0, 0.8],
        "initial_velocity": [0.0, 0.0, 0.0],
        "params": {"ramp_angle_deg": 30.0, "mu": 0.45},
        "frames": [
            {"t": 0.0, "com_position": [0, 0, 0.8], "com_velocity": [0, 0, 0]},
            {
                "t": 1 / 24,
                "com_position": [0.001, 0.0005, 0.799],
                "com_velocity": [0.03, 0.02, -0.02],
            },
        ],
        "provenance": {"git_commit": "05c0043", "renderer": "mujoco", "unknown_field": 1},
        "cameras": ["front", "left", "right", "high", "low"],
        "checks_pass": True,
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------- GroundTruth


def test_ground_truth_round_trips_and_ignores_unknown_fields() -> None:
    gt = GroundTruth.model_validate(sliding_gt())
    assert gt.obj.material_class == "book_paper_cover"
    assert gt.contact is not None and gt.contact.restitution is None
    assert gt.provenance is not None and not hasattr(gt.provenance, "unknown_field")
    again = GroundTruth.model_validate(gt.model_dump())
    assert again == gt


def test_ground_truth_derived_values() -> None:
    gt = GroundTruth.model_validate(sliding_gt())
    assert gt.num_frames == 2
    assert gt.duration_s == pytest.approx(1 / 24)
    assert gt.positions()[1] == [0.001, 0.0005, 0.799]


def test_scenario_mapping_covers_all_pipeline_scenarios() -> None:
    assert set(SCENARIO_TO_PHENOMENON.values()) == {"free_fall", "projectile", "rolling", "sliding"}


def test_free_flight_scene_has_no_surface() -> None:
    gt = GroundTruth.model_validate(
        sliding_gt(
            scenario="free_fall_no_contact",
            phenomenon="free_fall",
            trajectory_mode="simulated",
            surface=None,
            contact={"model": "none: no contact during the clip"},
            objects=[{"id": "ball", "name": "ball", "shape": "sphere", "radius_m": 0.3}],
        )
    )
    assert gt.surface is None
    assert gt.obj.radius_m == 0.3 and gt.obj.material_class is None


@pytest.mark.parametrize(
    "bad",
    [
        {"objects": []},
        {"frames": []},
        {"phenomenon": "teleport"},
        {"trajectory_mode": "guessed"},
        {"fps": 0},
        {
            "frames": [
                {"t": 0.0, "com_position": [0, 0, 0], "com_velocity": [0, 0, 0]},
                {"t": 0.0, "com_position": [0, 0, 0], "com_velocity": [0, 0, 0]},
            ]
        },
        {"initial_position": [0, 0]},
    ],
)
def test_ground_truth_rejects_invalid(bad: dict) -> None:
    with pytest.raises(ValidationError):
        GroundTruth.model_validate(sliding_gt(**bad))


def test_duplicate_object_ids_rejected() -> None:
    obj = sliding_gt()["objects"][0]
    with pytest.raises(ValidationError, match="duplicate"):
        GroundTruth.model_validate(sliding_gt(objects=[obj, dict(obj)]))


def test_contact_bounds() -> None:
    with pytest.raises(ValidationError):
        GroundTruth.model_validate(sliding_gt(contact={"restitution": 1.5}))
    with pytest.raises(ValidationError):
        GroundTruth.model_validate(sliding_gt(contact={"mu_kinetic": -0.1}))


# ---------------------------------------------------------------- SceneConfig


def test_scene_config_from_ground_truth_copies_physics_and_geometry() -> None:
    gt = GroundTruth.model_validate(sliding_gt())
    cfg = SceneConfig.from_ground_truth(gt)
    o = cfg.objects[0]
    assert cfg.phenomenon == "sliding"
    assert o.geometry_source == "ground_truth"
    assert o.size_m == [0.209, 0.139, 0.050]
    assert o.mass_kg == 0.45 and o.friction == 0.45 and o.restitution is None
    assert o.initial_position_m == [0.0, 0.0, 0.8]
    assert cfg.surface is not None
    assert cfg.surface.material == "finished_wood" and cfg.surface.ramp_angle_deg == 30.0
    assert cfg.duration_s == pytest.approx(1 / 24)


def test_scene_config_from_free_flight_has_no_surface() -> None:
    gt = GroundTruth.model_validate(
        sliding_gt(
            phenomenon="free_fall",
            surface=None,
            contact=None,
            objects=[{"id": "ball", "name": "ball", "shape": "sphere", "radius_m": 0.3}],
        )
    )
    cfg = SceneConfig.from_ground_truth(gt)
    assert cfg.surface is None
    assert cfg.objects[0].radius_m == 0.3


def test_scene_config_from_single_frame_ground_truth_has_no_duration() -> None:
    gt = GroundTruth.model_validate(
        sliding_gt(frames=[{"t": 0.0, "com_position": [0, 0, 0.8], "com_velocity": [0, 0, 0]}])
    )
    assert SceneConfig.from_ground_truth(gt).duration_s is None


def test_object_config_fills_missing_dimension_from_the_other() -> None:
    sphere = ObjectConfig(name="ball", shape="sphere", size_m=[0.2, 0.2, 0.2])
    assert sphere.radius_m == pytest.approx(0.1)
    box = ObjectConfig(name="cube", shape="box", radius_m=0.05)
    assert box.size_m == [0.1, 0.1, 0.1]


def test_scene_config_from_model_json_like_dict() -> None:
    """The shape a model is asked to emit, with extra chatter keys ignored."""
    cfg = SceneConfig.model_validate(
        {
            "phenomenon": "free_fall",
            "objects": [
                {
                    "name": "red ball",
                    "shape": "sphere",
                    "radius_m": 0.3,
                    "material_class": "plastic",
                    "mass_kg": 0.5,
                    "initial_position_m": [0, 0, 4.5],
                    "comment": "ignored",
                }
            ],
            "surface": None,
        }
    )
    assert cfg.objects[0].geometry_source == "vlm"
    assert cfg.gravity == [0.0, 0.0, -9.81]


@pytest.mark.parametrize(
    "bad",
    [
        {"phenomenon": "free_fall", "objects": []},
        {"phenomenon": "free_fall", "objects": [{"name": "x", "shape": "blob"}]},
        {"phenomenon": "free_fall", "objects": [{"name": "x", "shape": "box", "mass_kg": -1}]},
        {
            "phenomenon": "sliding",
            "objects": [{"name": "x", "shape": "box"}],
            "surface": {"ramp_angle_deg": 95},
        },
    ],
)
def test_scene_config_rejects_invalid(bad: dict) -> None:
    with pytest.raises(ValidationError):
        SceneConfig.model_validate(bad)


# ---------------------------------------------------------------- answers


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Metal", "metal"),
        (" Book Paper-Cover ", "book_paper_cover"),
        ("CARDBOARD\n", "cardboard"),
        ("glazed  ceramic", "glazed_ceramic"),
    ],
)
def test_normalize_label(raw: str, expected: str) -> None:
    assert normalize_label(raw) == expected


def test_material_answer_normalizes_and_bounds_confidence() -> None:
    a = MaterialAnswer(material="Metal ", confidence=0.8)
    assert a.material == "metal" and a.material in MATERIAL_CLASSES
    with pytest.raises(ValidationError):
        MaterialAnswer(material="metal", confidence=1.2)
    with pytest.raises(ValidationError):
        MaterialAnswer(material="   ")


def test_property_range_and_estimate() -> None:
    r = PropertyRange(low=0.2, high=0.5)
    assert r.width == pytest.approx(0.3) and r.contains(0.5) and not r.contains(0.51)
    with pytest.raises(ValidationError, match="below"):
        PropertyRange(low=0.5, high=0.2)
    with pytest.raises(ValidationError, match="value or a range"):
        PropertiesAnswer(friction={"confidence": 0.5})
    with pytest.raises(ValidationError, match="no property"):
        PropertiesAnswer(reasoning="nothing")


def test_properties_answer_partial_is_fine() -> None:
    a = PropertiesAnswer(density_kg_m3={"value": 800, "range": {"low": 600, "high": 1000}})
    assert a.restitution is None
    assert a.density_kg_m3 is not None and a.density_kg_m3.range is not None
    assert a.density_kg_m3.range.contains(800)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("A", "A"),
        ("b", "B"),
        (" Object A. ", "A"),
        ("same", "same"),
        ("Equal", "same"),
        ("left", "A"),
    ],
)
def test_comparative_choice_aliases(raw: str, expected: str) -> None:
    assert ComparativeAnswer(choice=raw).choice == expected


def test_comparative_rejects_unknown_choice() -> None:
    with pytest.raises(ValidationError):
        ComparativeAnswer(choice="C")


def test_scene_init_answer_is_a_scene_config_with_reasoning() -> None:
    a = SceneInitAnswer(
        phenomenon="sliding",
        objects=[{"name": "box", "shape": "box", "size_m": [0.6, 0.4, 0.3]}],
        reasoning="blue box on a wooden ramp",
    )
    assert isinstance(a, SceneConfig)


def test_parsed_answer_consistency() -> None:
    ok = ParsedAnswer[MaterialAnswer](
        question_id="q1", ok=True, answer=MaterialAnswer(material="metal")
    )
    assert ok.answer is not None and ok.answer.material == "metal"
    failed = ParsedAnswer[MaterialAnswer](question_id="q2", ok=False, error="no json found")
    assert failed.answer is None
    with pytest.raises(ValidationError):
        ParsedAnswer[MaterialAnswer](question_id="q3", ok=True)
    with pytest.raises(ValidationError):
        ParsedAnswer[MaterialAnswer](question_id="q4", ok=False)
