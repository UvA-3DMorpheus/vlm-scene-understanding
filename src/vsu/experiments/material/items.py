"""The labelled objects shared by the material recognition experiments (1.0, 1.1, 1.2).

Every material experiment asks about the same things: an object of known material, seen
in one or more views. This module builds that list once, so the three experiments ask
about identical objects and images and their answers can be compared question by question.

Datasets:

- ``smoke``: the labelled photos under ``VSU_DATA_ROOT/smoke`` (a sanity check).
- ``sim_<collection>``: simulated scenes under ``VSU_DATA_ROOT/sim/<collection>``, whose object
  has a material class: ``sim_realistic`` (Blender renders, the benchmark) and
  ``sim_preview`` (MuJoCo renders).

A view is one way of showing an object: a camera plus an input condition (``frame`` the
whole first frame, ``crop`` the object cut along its mask, ``outline`` the frame with the
mask boundary drawn in red, ``multiview`` the first frame of every camera at once). Photos
have a single ``photo`` view.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from vsu.data.dataset import Scene, discover_scenes
from vsu.data.materials import MaterialTable
from vsu.data.smoke import load_smoke_set
from vsu.schemas.scene import MATERIAL_CLASSES
from vsu.settings import Settings

log = logging.getLogger(__name__)

SIM_PREFIX = "sim_"
MULTIVIEW_CAMERA = "all"
SIM_CONDITIONS = ("frame", "crop", "outline")

#: How a prompt refers to the object in each condition.
FOCUS = {
    "photo": "the main object in this photo",
    "frame": "the main movable object in this image (not the surface it rests on)",
    "crop": "the object shown in this close crop",
    "outline": "the object outlined in red in this image",
    "multiview": (
        "the main movable object (not the surface it rests on), shown from five different "
        "cameras in these images"
    ),
}


#: How a material key reads in a sentence ("Is it made of <text>?"). Keys not listed read as
#: themselves with spaces for underscores.
#: "book paper", not "paper": a cardboard box is made of paper too, so "Is it made of paper?"
#: would have no clear answer for it.
LABEL_TEXT = {
    "book_paper_cover": "book paper",
    "ping_pong_plastic": "thin plastic (a ping pong ball)",
    "plastic": "plastic",
}

#: Label pairs where one material is a kind of the other. An object of one is truly also made
#: of the other ("is this ping pong ball made of plastic?" is yes), so verification and matching
#: never use one as the wrong option for the other.
OVERLAPPING: frozenset[frozenset[str]] = frozenset(
    {frozenset({"plastic", "ping_pong_plastic"}), frozenset({"metal", "aluminium"})}
)


def label_text(key: str) -> str:
    """The words a prompt uses for a material key."""
    return LABEL_TEXT.get(key, key.replace("_", " "))


def distinct_materials(a: str, b: str) -> bool:
    """True when ``a`` and ``b`` are different materials and neither is a kind of the other."""
    return a != b and frozenset({a, b}) not in OVERLAPPING


@dataclass(frozen=True)
class MaterialView:
    """One way of showing an object: its images, in prompt order."""

    condition: str
    images: tuple[str, ...]
    camera: str | None = None  # None for photos

    @property
    def key(self) -> str:
        """``<camera>/<condition>`` for scenes, ``<condition>`` for photos."""
        return self.condition if self.camera is None else f"{self.camera}/{self.condition}"


@dataclass(frozen=True)
class MaterialItem:
    """An object of known material and the views it can be shown in."""

    dataset: str
    item_id: str
    material: str
    labels: tuple[str, ...]  # the closed set offered for this dataset
    views: tuple[MaterialView, ...]
    meta: dict[str, Any] = field(default_factory=dict)

    def view_id(self, view: MaterialView) -> str:
        """Stable id of one object in one view: ``<dataset>/<item>/<view key>``."""
        return f"{self.dataset}/{self.item_id}/{view.key}"

    def view(self, key: str) -> MaterialView | None:
        return next((v for v in self.views if v.key == key), None)


def sim_collection(dataset: str) -> str:
    """``sim_realistic`` -> ``realistic``; raises for a non-simulation dataset."""
    if not dataset.startswith(SIM_PREFIX):
        raise ValueError(f"{dataset!r} is not a simulation dataset")
    return dataset[len(SIM_PREFIX) :]


def smoke_items(settings: Settings, table: MaterialTable) -> list[MaterialItem]:
    """One item per smoke photo, with the material table keys as closed set."""
    try:
        images = load_smoke_set(settings=settings)
    except FileNotFoundError as exc:
        log.warning("smoke set skipped: %s", exc)
        return []
    labels = tuple(table.keys)
    return [
        MaterialItem(
            dataset="smoke",
            item_id=img.image_id,
            material=img.material,
            labels=labels,
            views=(MaterialView("photo", (str(img.path),)),),
            meta={"object": img.object, "license": img.license},
        )
        for img in images
    ]


def sim_items(
    settings: Settings,
    dataset: str,
    *,
    cameras: list[str],
    conditions: list[str],
    multiview: bool = False,
    frame_index: int = 0,
    crop_margin: float = 0.2,
    only_passing: bool = False,
) -> list[MaterialItem]:
    """One item per simulated scene with a labelled object, with every requested view.

    Images are written on first use into the frame cache, so building items is cheap after
    the first run. Scenes without a material class are skipped; so are cameras a scene lacks.
    """
    collection = sim_collection(dataset)
    scenes = discover_scenes(collection=collection, only_passing=only_passing, settings=settings)
    if not scenes:
        log.warning("no scenes under %s", settings.sim_collection_dir(collection))
    items = []
    for scene in scenes:
        material = scene.gt.obj.material_class
        if material is None:
            continue
        present = [c for c in cameras if c in scene.cameras]
        for missing in sorted(set(cameras) - set(present)):
            log.warning("%s has no camera %s", scene.scene_id, missing)
        views: list[MaterialView] = []
        if multiview and len(present) >= 2:
            frames = tuple(str(scene.frame_path(c, frame_index)) for c in present)
            views.append(MaterialView("multiview", frames, MULTIVIEW_CAMERA))
        for camera in present:
            for condition in conditions:
                image = _scene_image(scene, camera, frame_index, condition, crop_margin)
                views.append(MaterialView(condition, (str(image),), camera))
        provenance = scene.gt.provenance
        items.append(
            MaterialItem(
                dataset=dataset,
                item_id=scene.scene_id,
                material=material,
                labels=tuple(MATERIAL_CLASSES),
                views=tuple(views),
                meta={
                    "object": scene.gt.obj.name,
                    "object_key": scene.gt.obj.key,
                    "phenomenon": scene.phenomenon,
                    "look": provenance.look if provenance else None,
                    "renderer": provenance.renderer if provenance else None,
                },
            )
        )
    return items


def load_items(
    options: dict[str, Any], settings: Settings, table: MaterialTable
) -> list[MaterialItem]:
    """Every item of the datasets listed in an experiment's ``options``.

    Options read: ``datasets`` (``smoke``, ``sim_realistic``, ``sim_preview``), ``sim_cameras``,
    ``sim_conditions``, ``sim_multiview``, ``frame_index``, ``crop_margin``,
    ``only_passing_scenes``.
    """
    items: list[MaterialItem] = []
    for dataset in options.get("datasets", ["smoke", "sim_realistic"]):
        if dataset == "smoke":
            items += smoke_items(settings, table)
        elif dataset.startswith(SIM_PREFIX):
            items += sim_items(
                settings,
                dataset,
                cameras=list(options.get("sim_cameras", ["front"])),
                conditions=list(options.get("sim_conditions", ["frame", "crop"])),
                multiview=bool(options.get("sim_multiview", False)),
                frame_index=int(options.get("frame_index", 0)),
                crop_margin=float(options.get("crop_margin", 0.2)),
                only_passing=bool(options.get("only_passing_scenes", False)),
            )
        else:
            raise ValueError(f"unknown dataset {dataset!r}")
    return items


def dataset_roles(options: dict[str, Any]) -> dict[str, str]:
    """``dataset -> role`` (``primary``, ``secondary``, ``sanity``) from experiment options.

    The primary dataset is the benchmark and the only one quoted as a headline; secondary
    datasets are reported next to it for comparison; sanity datasets only show the
    pipeline works and are reported apart.
    """
    roles = dict(options.get("dataset_roles") or {})
    unknown = set(roles.values()) - {"primary", "secondary", "sanity"}
    if unknown:
        raise ValueError(f"unknown dataset roles {sorted(unknown)}")
    if list(roles.values()).count("primary") > 1:
        raise ValueError("only one dataset can be primary")
    return roles


def _scene_image(scene: Scene, camera: str, index: int, condition: str, margin: float) -> Path:
    if condition == "frame":
        return scene.frame_path(camera, index)
    if condition == "crop":
        return scene.crop_path(camera, index, margin=margin)
    if condition == "outline":
        return scene.outline_path(camera, index)
    raise ValueError(f"unknown sim condition {condition!r}")
