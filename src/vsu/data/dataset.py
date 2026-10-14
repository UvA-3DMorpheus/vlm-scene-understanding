"""Scene access and the single conversion point from the simulation team's format.

A scene folder is what Emil's 3D-Simulations pipeline writes (``docs/data_format.md``
there, schema 2.0)::

    <scene_id>/
      ground_truth.json      object, surface, contact, expected motion, per frame states
      cameras.json           intrinsics and extrinsics per camera
      checks.json            automatic validation results
      <camera>/rgb.mp4       front, left, right, high, low
      <camera>/depth.npz     uint16 millimetres, 0 = no surface
      <camera>/seg.npz       geom id per pixel, max value = background

This module reads those files into our ``GroundTruth`` and ``Camera`` models and
serves frames, masks and crops. Nothing downstream touches their files directly, so a
format change is absorbed here. Frames are decoded once into ``VSU_CACHE_ROOT/frames``.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

from vsu.data.frames import extract_frames
from vsu.schemas.scene import (
    SCENARIO_TO_PHENOMENON,
    Camera,
    GroundTruth,
    Phenomenon,
    SceneObject,
)
from vsu.settings import Settings, get_settings

GROUND_TRUTH_FILE = "ground_truth.json"
CAMERAS_FILE = "cameras.json"
CHECKS_FILE = "checks.json"

BBox = tuple[int, int, int, int]
log = logging.getLogger(__name__)


# ---------------------------------------------------------------- their arrays


def load_seg(path: Path) -> np.ndarray:
    """Segmentation per frame as int16 geom ids with -1 for background, shape (F, H, W)."""
    raw = np.load(path)["seg"]
    background = np.iinfo(raw.dtype).max
    return np.where(raw == background, -1, raw.astype(np.int16))


def load_depth(path: Path) -> np.ndarray:
    """Depth per frame in metres as float32 with NaN where no surface, shape (F, H, W)."""
    mm = np.load(path)["depth_mm"]
    return np.where(mm > 0, mm / 1000.0, np.nan).astype(np.float32)


# ---------------------------------------------------------------- their json


def checks_pass(checks: dict[str, Any]) -> bool:
    """Apply the pipeline's own rule: every boolean check true, except the image edge ones."""

    def bad(key: str, value: object) -> bool:
        return isinstance(value, bool) and value != (not key.endswith("touches_image_edge"))

    if any(bad(k, v) for k, v in checks.items()):
        return False
    return not any(
        bad(k, v) for cam in checks.get("cameras", {}).values() for k, v in cam.items()
    )


def phenomenon_of(scenario: str) -> Phenomenon:
    """Map a pipeline scenario id onto our phenomenon name."""
    try:
        return SCENARIO_TO_PHENOMENON[scenario]
    except KeyError as exc:
        raise ValueError(f"unknown scenario {scenario!r}; extend SCENARIO_TO_PHENOMENON") from exc


def convert_ground_truth(
    raw: dict[str, Any],
    scene_id: str,
    *,
    cameras: list[str] | None = None,
    checks: dict[str, Any] | None = None,
) -> GroundTruth:
    """Convert a schema 2.0 ``ground_truth.json`` dictionary into our ``GroundTruth``.

    Their single ``object`` becomes a one element ``objects`` list with ``id`` taken from
    the geom name; the Blender look is lifted out of ``renderer_settings``; the checks
    result is reduced to one boolean. Fields we do not model are ignored by the schema.
    """
    obj = dict(raw["object"])
    obj["id"] = obj.get("geom_name") or obj.get("key") or "object"
    provenance = dict(raw.get("provenance") or {})
    provenance["look"] = (provenance.get("renderer_settings") or {}).get("look")
    return GroundTruth(
        scene_id=scene_id,
        schema_version=str(raw.get("schema_version", "")),
        scenario=raw["scenario"],
        phenomenon=phenomenon_of(raw["scenario"]),
        trajectory_mode=raw["trajectory_mode"],
        fps=raw["fps"],
        physics_timestep=raw.get("physics_timestep"),
        gravity=raw.get("gravity") or [0.0, 0.0, -9.81],
        objects=[obj],
        surface=raw.get("surface"),
        contact=raw.get("contact"),
        expected=raw.get("expected"),
        initial_position=raw["initial_position"],
        initial_velocity=raw["initial_velocity"],
        params=raw.get("params"),
        frames=raw["frames"],
        provenance=provenance,
        cameras=list(cameras or []),
        checks_pass=None if checks is None else checks_pass(checks),
    )


def convert_cameras(raw: dict[str, Any]) -> dict[str, Camera]:
    """Convert ``cameras.json`` (name -> entry) into ``Camera`` models."""
    return {name: Camera(name=name, **entry) for name, entry in raw.items()}


# ---------------------------------------------------------------- scenes


@dataclass
class Scene:
    """One scene folder: ground truth, cameras and lazy access to pixels."""

    root: Path
    gt: GroundTruth
    cameras: dict[str, Camera]
    frames_cache: Path
    _seg: dict[str, np.ndarray] = field(default_factory=dict, repr=False)

    @property
    def scene_id(self) -> str:
        return self.gt.scene_id

    @property
    def phenomenon(self) -> Phenomenon:
        return self.gt.phenomenon

    def video(self, camera: str = "front") -> Path:
        self._check_camera(camera)
        return self.root / camera / "rgb.mp4"

    def frame_paths(self, camera: str = "front") -> list[Path]:
        """All frame PNGs of a camera, decoding the video into the cache on first use."""
        paths = extract_frames(self.video(camera), self.frames_cache / camera)
        if len(paths) != self.gt.num_frames:
            log.warning(
                "%s/%s: video has %d frames, ground truth %d",
                self.scene_id,
                camera,
                len(paths),
                self.gt.num_frames,
            )
        return paths

    def frame_path(self, camera: str = "front", index: int = 0) -> Path:
        paths = self.frame_paths(camera)
        if index >= len(paths):
            raise IndexError(f"{self.scene_id}/{camera} has {len(paths)} frames, asked {index}")
        return paths[index]

    def frame(self, camera: str = "front", index: int = 0) -> Image.Image:
        """One frame as an RGB PIL image."""
        return Image.open(self.frame_path(camera, index)).convert("RGB")

    def seg(self, camera: str = "front") -> np.ndarray:
        """Segmentation array (F, H, W) of a camera, loaded once."""
        self._check_camera(camera)
        if camera not in self._seg:
            self._seg[camera] = load_seg(self.root / camera / "seg.npz")
        return self._seg[camera]

    def depth(self, camera: str = "front") -> np.ndarray:
        """Depth array (F, H, W) in metres of a camera."""
        self._check_camera(camera)
        return load_depth(self.root / camera / "depth.npz")

    def mask(self, camera: str = "front", index: int = 0, object_id: str | None = None) -> np.ndarray:
        """Boolean (H, W) mask of an object in one frame, from the segmentation ids."""
        obj = self.gt.obj if object_id is None else self._object(object_id)
        if obj.segmentation_geom_id is None:
            raise ValueError(f"{self.scene_id}: object {obj.id} has no segmentation id")
        return self.seg(camera)[index] == obj.segmentation_geom_id

    def bbox(self, camera: str = "front", index: int = 0, object_id: str | None = None) -> BBox | None:
        """Pixel box (x0, y0, x1, y1), exclusive upper bounds, or None if the object is unseen."""
        return mask_bbox(self.mask(camera, index, object_id))

    def crop(
        self,
        camera: str = "front",
        index: int = 0,
        object_id: str | None = None,
        *,
        margin: float = 0.2,
        min_size: int = 32,
    ) -> Image.Image:
        """The object cut out of a frame, with ``margin`` of its box size added on each side."""
        box = self.bbox(camera, index, object_id)
        if box is None:
            raise ValueError(f"{self.scene_id}: object not visible in {camera} frame {index}")
        image = self.frame(camera, index)
        return image.crop(expand_bbox(box, image.size, margin=margin, min_size=min_size))

    def _object(self, object_id: str) -> SceneObject:
        for o in self.gt.objects:
            if o.id == object_id:
                return o
        raise KeyError(f"{self.scene_id} has objects {[o.id for o in self.gt.objects]}, not {object_id!r}")

    def _check_camera(self, camera: str) -> None:
        if camera not in self.cameras:
            raise KeyError(f"{self.scene_id} has cameras {sorted(self.cameras)}, not {camera!r}")


def mask_bbox(mask: np.ndarray) -> BBox | None:
    """Tight pixel box (x0, y0, x1, y1) around the true pixels of a mask, or None if empty."""
    rows = np.flatnonzero(mask.any(axis=1))
    cols = np.flatnonzero(mask.any(axis=0))
    if rows.size == 0:
        return None
    return int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1


def expand_bbox(box: BBox, image_size: tuple[int, int], *, margin: float, min_size: int) -> BBox:
    """Grow a box by a fraction of its size and to a minimum size, clipped to the image."""
    width, height = image_size
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    pad_x = max(margin * w, (min_size - w) / 2, 0)
    pad_y = max(margin * h, (min_size - h) / 2, 0)
    return (
        max(0, math.floor(x0 - pad_x)),
        max(0, math.floor(y0 - pad_y)),
        min(width, math.ceil(x1 + pad_x)),
        min(height, math.ceil(y1 + pad_y)),
    )


def is_scene_dir(path: Path) -> bool:
    return (path / GROUND_TRUTH_FILE).is_file()


def frames_cache_dir(root: Path, settings: Settings) -> Path:
    """Where a scene's decoded frames live: ``VSU_CACHE_ROOT/frames/<path under data root>``.

    Two scenes with the same folder name under different roots (``sim/high_drop`` and
    ``sim_realistic/high_drop``) must not share a cache. Outside the data root the key is
    the folder name plus a short hash of its absolute path.
    """
    base = settings.cache_root / "frames"
    try:
        return base / root.relative_to(settings.data_root)
    except ValueError:
        digest = hashlib.sha1(str(root).encode()).hexdigest()[:8]
        return base / f"{root.name}-{digest}"


def load_scene(root: Path, *, settings: Settings | None = None) -> Scene:
    """Read one scene folder. ``scene_id`` is the folder name."""
    root = Path(os.path.abspath(root))
    if not is_scene_dir(root):
        raise FileNotFoundError(f"{root} has no {GROUND_TRUTH_FILE}")
    settings = settings or get_settings()
    raw_gt = json.loads((root / GROUND_TRUTH_FILE).read_text())
    cameras_path = root / CAMERAS_FILE
    cameras = convert_cameras(json.loads(cameras_path.read_text())) if cameras_path.is_file() else {}
    checks_path = root / CHECKS_FILE
    checks = json.loads(checks_path.read_text()) if checks_path.is_file() else None
    gt = convert_ground_truth(raw_gt, root.name, cameras=sorted(cameras), checks=checks)
    return Scene(root=root, gt=gt, cameras=cameras, frames_cache=frames_cache_dir(root, settings))


def discover_scenes(
    sim_root: Path | None = None,
    *,
    phenomenon: Phenomenon | None = None,
    only_passing: bool = False,
    settings: Settings | None = None,
) -> list[Scene]:
    """Load every scene folder under ``sim_root`` (default ``VSU_DATA_ROOT/sim``), sorted.

    Folders are found recursively, so ``sim/<scene>`` and ``sim/<look>/<scene>`` both work.
    """
    settings = settings or get_settings()
    sim_root = Path(sim_root) if sim_root is not None else settings.sim_dir
    if not sim_root.is_dir():
        return []
    scenes = [
        load_scene(p.parent, settings=settings) for p in sorted(sim_root.rglob(GROUND_TRUTH_FILE))
    ]
    if phenomenon is not None:
        scenes = [s for s in scenes if s.phenomenon == phenomenon]
    if only_passing:
        scenes = [s for s in scenes if s.gt.checks_pass]
    return scenes
