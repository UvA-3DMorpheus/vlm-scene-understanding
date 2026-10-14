"""Experiment 1: material recognition from a first frame or a photo.

Questions come from the smoke photos and from simulated scenes whose object carries a
material class. Each simulated scene yields one question per camera and input condition:
``frame`` shows the whole first frame, ``crop`` shows the object cut out along its
segmentation mask. The label set offered in closed set prompts is the dataset's own: the
material table keys for photos, the five materials.json classes for simulated scenes.

Variants (templates ``exp1_<variant>.jinja``): ``v1`` closed set, one label; ``v2`` open
set free text, mapped onto the label set through the material table aliases; ``v3``
closed set with a short reasoning step before the label.
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel

from vsu.data.dataset import Scene, discover_scenes
from vsu.data.materials import MaterialTable, load_material_table
from vsu.data.smoke import load_smoke_set
from vsu.experiments.base import Experiment, Question, ScoredRecord
from vsu.schemas.answers import MaterialAnswer
from vsu.schemas.scene import MATERIAL_CLASSES
from vsu.scoring.classification import classification_summary, label_counts

log = logging.getLogger(__name__)

FOCUS = {
    "photo": "the main object in this photo",
    "frame": "the main movable object in this image (not the surface it rests on)",
    "crop": "the object shown in this close crop",
}


class MaterialExperiment(Experiment):
    """Experiment 1. See the module docstring."""

    name = "exp1"
    answer_schema = MaterialAnswer
    bare_label_field = "material"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._table: MaterialTable | None = None

    @property
    def table(self) -> MaterialTable:
        if self._table is None:
            self._table = load_material_table(settings=self.settings)
        return self._table

    def uses_bare_label(self, variant: str) -> bool:
        return variant == "v1"

    # ---- questions

    def build_questions(self) -> list[Question]:
        opts = self.config.options
        questions: list[Question] = []
        datasets = opts.get("datasets", ["smoke", "sim"])
        if "smoke" in datasets:
            questions += self._smoke_questions()
        if "sim" in datasets:
            questions += self._sim_questions()
        log.info(
            "exp1: %d questions (%s)", len(questions), label_counts(q.dataset for q in questions)
        )
        return questions

    def _smoke_questions(self) -> list[Question]:
        labels = self.table.keys
        out = []
        try:
            images = load_smoke_set(settings=self.settings)
        except FileNotFoundError as exc:
            log.warning("smoke set skipped: %s", exc)
            return out
        for img in images:
            out.append(
                Question(
                    id=f"smoke/{img.image_id}/photo",
                    dataset="smoke",
                    item_id=img.image_id,
                    condition="photo",
                    images=[str(img.path)],
                    context={"labels": labels, "focus": FOCUS["photo"]},
                    target={"material": img.material},
                    meta={"labels": labels, "object": img.object, "license": img.license},
                )
            )
        return out

    def _sim_questions(self) -> list[Question]:
        opts = self.config.options
        cameras = list(opts.get("sim_cameras", ["front"]))
        conditions = list(opts.get("sim_conditions", ["frame", "crop"]))
        index = int(opts.get("frame_index", 0))
        margin = float(opts.get("crop_margin", 0.2))
        labels = list(MATERIAL_CLASSES)
        out = []
        scenes = discover_scenes(
            only_passing=bool(opts.get("only_passing_scenes", False)), settings=self.settings
        )
        for scene in scenes:
            material = scene.gt.obj.material_class
            if material is None:
                continue
            for camera in cameras:
                if camera not in scene.cameras:
                    log.warning("%s has no camera %s", scene.scene_id, camera)
                    continue
                for condition in conditions:
                    image = self._sim_image(scene, camera, index, condition, margin)
                    out.append(
                        Question(
                            id=f"sim/{scene.scene_id}/{camera}/{condition}",
                            dataset="sim",
                            item_id=scene.scene_id,
                            condition=condition,
                            images=[str(image)],
                            context={"labels": labels, "focus": FOCUS[condition]},
                            target={"material": material},
                            meta={
                                "labels": labels,
                                "camera": camera,
                                "object": scene.gt.obj.name,
                                "object_key": scene.gt.obj.key,
                                "phenomenon": scene.phenomenon,
                                "look": scene.gt.provenance.look if scene.gt.provenance else None,
                                "renderer": scene.gt.provenance.renderer
                                if scene.gt.provenance
                                else None,
                            },
                        )
                    )
        return out

    @staticmethod
    def _sim_image(scene: Scene, camera: str, index: int, condition: str, margin: float):  # noqa: ANN205
        if condition == "frame":
            return scene.frame_path(camera, index)
        if condition == "crop":
            return scene.crop_path(camera, index, margin=margin)
        raise ValueError(f"unknown sim condition {condition!r}")

    # ---- scoring

    def score_record(
        self, question: Question, answer: BaseModel | None, variant: str
    ) -> dict[str, Any]:
        """Map the answer onto the question's label set and compare with the target.

        ``exact`` says whether the raw label was one of the offered labels; an alias
        ("steel" for metal) still counts as correct through the material table, which is
        what makes the open set variant scorable. Closed set prompts can be judged on
        ``exact`` as well.
        """
        if answer is None:
            return {
                "predicted_raw": None,
                "predicted": None,
                "exact": None,
                "in_label_set": None,
                "correct": None,
            }
        assert isinstance(answer, MaterialAnswer)
        labels: list[str] = question.context["labels"]
        raw = answer.material
        exact = raw in labels
        predicted = raw if exact else self.table.resolve(raw)
        if predicted is not None and predicted not in labels:
            predicted = None  # resolved to a material outside this dataset's label set
        return {
            "predicted_raw": raw,
            "predicted": predicted if predicted is not None else raw,
            "exact": exact,
            "in_label_set": predicted is not None,
            "correct": predicted == question.target["material"],
            "confidence": answer.confidence,
        }

    def summarize(self, scored: list[ScoredRecord], variant: str) -> dict[str, Any]:
        """Classification metrics per dataset and condition, kept apart by dataset role.

        ``datasets`` holds one entry per dataset with its role (``primary`` for the
        simulated scenes, ``sanity`` for the smoke photos), its accuracy over all its
        conditions and the mean macro F1 over its conditions. ``groups`` holds the full
        classification summary per ``<dataset>/<condition>``. There is no number that
        mixes datasets.
        """
        primary = self.config.options.get("primary_dataset", "sim")
        sanity = list(self.config.options.get("sanity_datasets", ["smoke"]))
        groups: dict[str, list[ScoredRecord]] = {}
        for s in scored:
            groups.setdefault(f"{s.dataset}/{s.condition}", []).append(s)
        out: dict[str, Any] = {
            "primary_dataset": primary,
            "sanity_datasets": sanity,
            "groups": {},
            "datasets": {},
        }
        for name, records in sorted(groups.items()):
            labels = _labels_of(records)
            y_true = [r.target["material"] for r in records]
            y_pred = [r.derived["predicted"] if r.parse_ok else None for r in records]
            out["groups"][name] = classification_summary(y_true, y_pred, labels)
        for dataset in sorted({s.dataset for s in scored}):
            records = [s for s in scored if s.dataset == dataset]
            correct = sum(r.parse_ok and r.derived["correct"] for r in records)
            f1s = [
                g["macro_f1"]
                for name, g in out["groups"].items()
                if name.startswith(f"{dataset}/") and g["macro_f1"] is not None
            ]
            exact = sum(bool(r.parse_ok and r.derived.get("exact")) for r in records)
            out["datasets"][dataset] = {
                "role": "primary"
                if dataset == primary
                else ("sanity" if dataset in sanity else "other"),
                "n": len(records),
                "n_parse_failures": sum(not r.parse_ok for r in records),
                "accuracy": (correct / len(records)) if records else None,
                "exact_label_rate": (exact / len(records)) if records else None,
                "macro_f1_mean_over_conditions": _mean(f1s),
                "by_camera": _accuracy_by(records, "camera"),
            }
        return out


def _accuracy_by(records: list[ScoredRecord], key: str) -> dict[str, dict[str, Any]]:
    """Accuracy split by a question meta field (camera, phenomenon); empty if absent."""
    groups: dict[str, list[ScoredRecord]] = {}
    for r in records:
        value = r.meta.get(key)
        if value is not None:
            groups.setdefault(str(value), []).append(r)
    return {
        name: {
            "n": len(rs),
            "accuracy": sum(bool(r.parse_ok and r.derived["correct"]) for r in rs) / len(rs),
        }
        for name, rs in sorted(groups.items())
    }


def _labels_of(records: list[ScoredRecord]) -> list[str]:
    """The label set of a group: the closed set the prompt offered, recorded in question meta."""
    labels: list[str] = list(records[0].meta.get("labels", [])) if records else []
    missing = sorted({r.target["material"] for r in records} - set(labels))
    return labels + missing


def _mean(values: list[float]) -> float | None:
    return (sum(values) / len(values)) if values else None
