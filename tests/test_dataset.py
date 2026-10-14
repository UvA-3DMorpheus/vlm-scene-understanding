"""The scene loader converts Emil's folders into our models and serves frames and masks."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from vsu.data.dataset import (
    Scene,
    checks_pass,
    convert_ground_truth,
    discover_scenes,
    expand_bbox,
    load_depth,
    load_scene,
    load_seg,
    mask_bbox,
)
from vsu.data.frames import encode_frames, extract_frames, ffmpeg_executable
from vsu.settings import Settings

W, H, F = 64, 48, 3
OBJ_ID = 5
CAMS = ["front", "high"]


def raw_ground_truth(scenario: str = "sliding_with_friction") -> dict:
    """A ground_truth.json as the pipeline writes it (schema 2.0, single ``object``)."""
    frames = [
        {
            "t": k / 24,
            "com_position": [0.01 * k, 0.0, 0.8 - 0.005 * k],
            "com_velocity": [0.24, 0.0, -0.12],
            "quaternion": [1, 0, 0, 0],
            "angular_velocity": [0, 0, 0],
            "mesh_origin_position": None,
            "mesh_quaternion": None,
        }
        for k in range(F)
    ]
    return {
        "schema_version": "2.0",
        "scenario": scenario,
        "trajectory_mode": "analytic",
        "conventions": {"units": "SI"},
        "provenance": {
            "git_commit": "05c0043a",
            "git_uncommitted_changes": False,
            "materials_json_version": "1.0.0",
            "materials_json_sha256": "b575",
            "renderer": "blender",
            "renderer_version": "Blender 5.0.1",
            "simulator_version": "MuJoCo 3.14.0",
            "renderer_settings": {"duration_s": 1.0, "fps": 24, "look": "realistic"},
        },
        "fps": 24,
        "physics_timestep": 1 / 2400,
        "gravity": [0, 0, -9.81],
        "air_drag": "none (vacuum)",
        "object": {
            "dataset": "Google Scanned Objects",
            "name": "Vans_Cereal_Honey_Nut_Crunch_11_oz_box",
            "key": "cereal_box",
            "license": "CC-BY 4.0",
            "attribution": "Google Scanned Objects (Downs et al., 2022)",
            "shape": "mesh",
            "geom_name": "object",
            "segmentation_geom_id": OBJ_ID,
            "material_class": "cardboard",
            "scale": 1.0,
            "radius_m": None,
            "size_m": None,
            "bbox_body_frame_m": [0.268, 0.190, 0.056],
            "bbox_mesh_frame_m": [0.19, 0.268, 0.056],
            "volume_m3": 0.0028,
            "density_kg_m3": 132.0,
            "density_basis": "effective_density",
            "mass_kg": 0.37,
            "inertia_kg_m2": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "com_offset_from_mesh_origin_m": [0, 0, 0],
            "rotation_mesh_to_body": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        },
        "surface": {
            "name": "finished_wood",
            "label": "finished (varnished) wood, tabletop / ramp",
            "density_kg_m3": 700,
            "ramp_angle_deg": 30.0,
            "ramp_azimuth_deg": 30.0,
            "ramp_top_edge_centre_m": [0, 0, 1],
            "ramp_bottom_edge_centre_m": [1, 0, 0.5],
            "ramp_width_m": 0.3,
            "ramp_normal": [0.433, 0.25, 0.866],
            "ramp_downhill_direction": [0.75, 0.433, -0.5],
        },
        "contact": {
            "object_material": "cardboard",
            "surface": "finished_wood",
            "model": "Coulomb kinetic friction, analytic (no rotation)",
            "mu_kinetic": 0.4,
            "mu_static": 0.5,
            "restitution": None,
            "source": "illustrative value within published ranges",
        },
        "expected": {
            "description": "sliding from rest",
            "formula": "s(t) = 0.5 a t^2",
            "acceleration_world_mps2": [1.0, 0.5, -0.6],
            "acceleration_magnitude_mps2": 1.3,
        },
        "initial_position": [0.0, 0.0, 0.8],
        "initial_velocity": [0.0, 0.0, 0.0],
        "params": {"ramp_angle_deg": 30.0, "mu": 0.4},
        "frames": frames,
    }


def raw_checks(ok: bool = True) -> dict:
    return {
        "renderer": "mujoco",
        "max_error_vs_analytic_m": 1e-12,
        "contact_ok": True,
        "stays_on_ramp": ok,
        "cameras": {
            cam: {
                "object_visible_every_frame": True,
                "object_touches_image_edge": False,
                "projection_vs_segmentation_px_max": 0.1,
            }
            for cam in CAMS
        },
    }


def make_scene_dir(root: Path, scene_id: str = "sliding_cereal_box", ok: bool = True) -> Path:
    """Write a complete synthetic scene folder: json files, npz arrays and real mp4 clips."""
    d = root / scene_id
    d.mkdir(parents=True)
    (d / "ground_truth.json").write_text(json.dumps(raw_ground_truth()))
    (d / "checks.json").write_text(json.dumps(raw_checks(ok)))
    cameras = {
        cam: {
            "K": [[60.0, 0, W / 2], [0, 60.0, H / 2], [0, 0, 1]],
            "width": W,
            "height": H,
            "position": [0.0, -3.0, 1.0],
            "rotation_cam_to_world": [[1, 0, 0], [0, 0, 1], [0, -1, 0]],
        }
        for cam in CAMS
    }
    (d / "cameras.json").write_text(json.dumps(cameras))
    for cam in CAMS:
        (d / cam).mkdir()
        seg = np.full((F, H, W), 255, np.uint8)  # background
        seg[:, 30:, :] = 1  # ground geom
        depth = np.zeros((F, H, W), np.uint16)
        depth[:, 30:, :] = 3000
        pngs = []
        for k in range(F):
            x0 = 10 + 4 * k  # object moves right by 4 px per frame
            seg[k, 8:20, x0 : x0 + 16] = OBJ_ID
            depth[k, 8:20, x0 : x0 + 16] = 2500
            img = np.full((H, W, 3), 200, np.uint8)
            img[30:] = (90, 60, 30)
            img[8:20, x0 : x0 + 16] = (220, 40, 40)  # red object
            png = d / cam / f"src_{k:06d}.png"
            Image.fromarray(img).save(png)
            pngs.append(png)
        np.savez_compressed(d / cam / "seg.npz", seg=seg)
        np.savez_compressed(d / cam / "depth.npz", depth_mm=depth)
        # encode from a %06d pattern: copy sources to the expected names in a temp folder
        enc = d / cam / "enc"
        enc.mkdir()
        for k, png in enumerate(pngs):
            (enc / f"{k:06d}.png").write_bytes(png.read_bytes())
        encode_frames(sorted(enc.glob("*.png")), d / cam / "rgb.mp4", fps=24)
    return d


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(data_root=tmp_path / "data", cache_root=tmp_path / "cache", _env_file=None)


@pytest.fixture
def scene(settings: Settings) -> Scene:
    d = make_scene_dir(settings.sim_dir)
    return load_scene(d, settings=settings)


# ---------------------------------------------------------------- conversion


def test_convert_ground_truth_maps_their_fields_onto_ours() -> None:
    gt = convert_ground_truth(
        raw_ground_truth(), "sliding_cereal_box", cameras=CAMS, checks=raw_checks()
    )
    assert gt.scene_id == "sliding_cereal_box"
    assert gt.phenomenon == "sliding" and gt.scenario == "sliding_with_friction"
    assert len(gt.objects) == 1
    assert gt.obj.id == "object" and gt.obj.key == "cereal_box"
    assert gt.obj.material_class == "cardboard" and gt.obj.mass_kg == 0.37
    assert gt.obj.segmentation_geom_id == OBJ_ID
    assert gt.contact is not None and gt.contact.mu_kinetic == 0.4
    assert gt.surface is not None and gt.surface.ramp_angle_deg == 30.0
    assert gt.provenance is not None and gt.provenance.look == "realistic"
    assert gt.provenance.renderer == "blender"
    assert gt.cameras == CAMS and gt.checks_pass is True
    assert gt.num_frames == F and gt.duration_s == pytest.approx(2 / 24)


@pytest.mark.parametrize(
    ("scenario", "phenomenon"),
    [
        ("free_fall_no_contact", "free_fall"),
        ("projectile_no_contact", "projectile"),
        ("rolling_without_slipping", "rolling"),
        ("sliding_with_friction", "sliding"),
    ],
)
def test_every_pipeline_scenario_converts(scenario: str, phenomenon: str) -> None:
    gt = convert_ground_truth(raw_ground_truth(scenario), "x")
    assert gt.phenomenon == phenomenon


def test_unknown_scenario_is_an_error() -> None:
    with pytest.raises(ValueError, match="unknown scenario"):
        convert_ground_truth(raw_ground_truth("teleport_no_contact"), "x")


def test_checks_pass_rule_matches_the_pipeline() -> None:
    assert checks_pass(raw_checks(True))
    assert not checks_pass(raw_checks(False))
    edge = raw_checks(True)
    edge["cameras"]["front"]["object_touches_image_edge"] = True
    assert not checks_pass(edge)
    no_bools = {"renderer": "mujoco", "max_error_vs_analytic_m": 0.1, "cameras": {}}
    assert checks_pass(no_bools)


# ---------------------------------------------------------------- arrays


def test_load_seg_and_depth_conventions(tmp_path: Path) -> None:
    seg = np.array([[[255, 3], [0, 7]]], np.uint8)
    np.savez_compressed(tmp_path / "seg.npz", seg=seg)
    loaded = load_seg(tmp_path / "seg.npz")
    assert loaded.dtype == np.int16 and loaded[0, 0, 0] == -1 and loaded[0, 1, 1] == 7
    seg16 = np.array([[[65535, 300]]], np.uint16)
    np.savez_compressed(tmp_path / "seg16.npz", seg=seg16)
    assert load_seg(tmp_path / "seg16.npz")[0, 0, 0] == -1
    depth = np.array([[[0, 1500], [2000, 1]]], np.uint16)
    np.savez_compressed(tmp_path / "depth.npz", depth_mm=depth)
    d = load_depth(tmp_path / "depth.npz")
    assert np.isnan(d[0, 0, 0]) and d[0, 0, 1] == pytest.approx(1.5) and d.dtype == np.float32


def test_mask_bbox_and_expand() -> None:
    mask = np.zeros((10, 10), bool)
    assert mask_bbox(mask) is None
    mask[2:5, 3:8] = True
    assert mask_bbox(mask) == (3, 2, 8, 5)
    assert expand_bbox((3, 2, 8, 5), (10, 10), margin=0.0, min_size=0) == (3, 2, 8, 5)
    assert expand_bbox((3, 2, 8, 5), (10, 10), margin=0.5, min_size=0) == (0, 0, 10, 7)
    assert expand_bbox((4, 4, 6, 6), (10, 10), margin=0.0, min_size=8) == (1, 1, 9, 9)


# ---------------------------------------------------------------- scenes on disk


def test_load_scene_reads_everything(scene: Scene) -> None:
    assert scene.scene_id == "sliding_cereal_box"
    assert sorted(scene.cameras) == sorted(CAMS)
    assert scene.cameras["front"].width == W and scene.cameras["front"].K[0][2] == W / 2
    assert scene.gt.checks_pass is True
    assert scene.phenomenon == "sliding"


def test_frames_are_decoded_into_the_cache_and_reused(scene: Scene, settings: Settings) -> None:
    paths = scene.frame_paths("front")
    assert len(paths) == F
    assert (
        paths[0] == settings.cache_root / "frames" / "sim" / scene.scene_id / "front" / "000000.png"
    )
    assert not (paths[0].parent.parent / "front.partial").exists()
    first = scene.frame("front", 0)
    assert first.size == (W, H) and first.mode == "RGB"
    mtime = paths[0].stat().st_mtime
    assert scene.frame_paths("front")[0].stat().st_mtime == mtime  # no re-decode
    with pytest.raises(IndexError):
        scene.frame_path("front", F)


def test_decoded_frame_has_the_object_where_the_mask_says(scene: Scene) -> None:
    img = np.asarray(scene.frame("front", 1))
    mask = scene.mask("front", 1)
    assert mask.shape == (H, W) and mask.sum() == 12 * 16
    inside = img[mask].mean(axis=0)
    outside = img[~mask].mean(axis=0)
    assert inside[0] > 150 and inside[1] < 110  # red-ish after H.264 round trip
    assert outside[0] < inside[0]


def test_bbox_and_crop_follow_the_object(scene: Scene) -> None:
    assert scene.bbox("front", 0) == (10, 8, 26, 20)
    assert scene.bbox("front", 2) == (18, 8, 34, 20)
    crop = scene.crop("front", 0, margin=0.0, min_size=0)
    assert crop.size == (16, 12)
    padded = scene.crop("front", 0, margin=0.25, min_size=0)
    assert padded.size == (24, 18)


def test_same_scene_name_under_two_roots_gets_two_caches(settings: Settings) -> None:
    a = load_scene(make_scene_dir(settings.sim_dir, "high_drop"), settings=settings)
    b = load_scene(
        make_scene_dir(settings.data_root / "sim_realistic", "high_drop"), settings=settings
    )
    assert a.scene_id == b.scene_id == "high_drop"
    assert a.frames_cache != b.frames_cache
    assert a.frames_cache == settings.cache_root / "frames" / "sim" / "high_drop"
    outside = load_scene(
        make_scene_dir(settings.data_root.parent / "elsewhere", "high_drop"), settings=settings
    )
    assert outside.frames_cache.parent == settings.cache_root / "frames"
    assert outside.frames_cache.name.startswith("high_drop-")


def test_unknown_object_id_is_a_key_error(scene: Scene) -> None:
    with pytest.raises(KeyError, match="not 'ghost'"):
        scene.mask("front", 0, object_id="ghost")


def test_unknown_camera_and_missing_segmentation_id(scene: Scene) -> None:
    with pytest.raises(KeyError):
        scene.frame_paths("back")
    scene.gt.obj.segmentation_geom_id = None
    with pytest.raises(ValueError, match="segmentation id"):
        scene.mask("front", 0)


def test_depth_of_object_pixels(scene: Scene) -> None:
    depth = scene.depth("front")
    mask = scene.mask("front", 0)
    assert np.allclose(depth[0][mask], 2.5)
    assert np.isnan(depth[0][0, 0])


def test_discover_scenes_recursive_filters(settings: Settings) -> None:
    make_scene_dir(settings.sim_dir, "sliding_a", ok=True)
    make_scene_dir(settings.sim_dir / "realistic", "sliding_b", ok=False)
    scenes = discover_scenes(settings=settings)
    assert [s.scene_id for s in scenes] == ["sliding_b", "sliding_a"] or sorted(
        s.scene_id for s in scenes
    ) == ["sliding_a", "sliding_b"]
    assert [s.scene_id for s in discover_scenes(only_passing=True, settings=settings)] == [
        "sliding_a"
    ]
    assert discover_scenes(phenomenon="free_fall", settings=settings) == []
    assert discover_scenes(settings.data_root / "nowhere", settings=settings) == []


def test_load_scene_rejects_folder_without_ground_truth(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_scene(tmp_path)


def test_extract_frames_overwrite_and_missing_video(tmp_path: Path, scene: Scene) -> None:
    assert Path(ffmpeg_executable()).exists() or ffmpeg_executable()
    out = tmp_path / "again"
    first = extract_frames(scene.video("high"), out)
    again = extract_frames(scene.video("high"), out, overwrite=True)
    assert [p.name for p in first] == [p.name for p in again]
    with pytest.raises(FileNotFoundError):
        extract_frames(tmp_path / "missing.mp4", out)


def test_interrupted_extraction_is_not_reused(tmp_path: Path, scene: Scene) -> None:
    out = tmp_path / "cache"
    partial = tmp_path / "cache.partial"
    partial.mkdir()
    (partial / "000000.png").write_bytes(b"garbage")  # leftover from a killed run
    frames = extract_frames(scene.video("front"), out)
    assert len(frames) == F and not partial.exists()
    assert frames[0].stat().st_size > 100
