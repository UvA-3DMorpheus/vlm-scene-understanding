"""Experiment 1.0: material identification from a single image.

The model sees one view of an object and names its material from the dataset's closed set
(or in free words, for the open set variant). Objects and views come from
:mod:`vsu.experiments.material.items`, shared with Experiments 1.1 and 1.2, so all three ask
about the same images.

Variants (templates ``exp1_<variant>.jinja``): ``v1`` closed set, one label; ``v2`` open
set free text, mapped onto the label set through the material table aliases; ``v3``
closed set with a short reasoning step before the label.
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel

from vsu.data.materials import MaterialTable, load_material_table
from vsu.experiments.base import Experiment, Question, ScoredRecord
from vsu.experiments.material.items import FOCUS, MaterialItem, dataset_roles, load_items
from vsu.schemas.answers import MaterialAnswer
from vsu.scoring.classification import classification_summary, label_counts

log = logging.getLogger(__name__)


class MaterialExperiment(Experiment):
    """Experiment 1.0. See the module docstring."""

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

    def items(self) -> list[MaterialItem]:
        return load_items(self.config.options, self.settings, self.table)

    def build_questions(self) -> list[Question]:
        """One question per item and view."""
        questions = [question_for_view(item, view) for item in self.items() for view in item.views]
        log.info(
            "exp1: %d questions (%s)", len(questions), label_counts(q.dataset for q in questions)
        )
        return questions

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

        ``datasets`` holds one entry per dataset with its role (``primary``: the benchmark;
        ``secondary``: reported beside it; ``sanity``: reported apart), its accuracy over
        all its conditions and the mean macro F1 over its conditions. ``groups`` holds the
        full classification summary per ``<dataset>/<condition>``. No number mixes datasets.
        """
        roles = dataset_roles(self.config.options)
        groups: dict[str, list[ScoredRecord]] = {}
        for s in scored:
            groups.setdefault(f"{s.dataset}/{s.condition}", []).append(s)
        out: dict[str, Any] = {"dataset_roles": roles, "groups": {}, "datasets": {}}
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
                "role": roles.get(dataset, "other"),
                "n": len(records),
                "n_parse_failures": sum(not r.parse_ok for r in records),
                "accuracy": (correct / len(records)) if records else None,
                "exact_label_rate": (exact / len(records)) if records else None,
                "macro_f1_mean_over_conditions": _mean(f1s),
                "by_camera": _accuracy_by(records, "camera"),
            }
        return out


def question_for_view(item: MaterialItem, view: Any) -> Question:
    """The identification question for one object in one view."""
    labels = list(item.labels)
    return Question(
        id=item.view_id(view),
        dataset=item.dataset,
        item_id=item.item_id,
        condition=view.condition,
        images=list(view.images),
        context={"labels": labels, "focus": FOCUS[view.condition]},
        target={"material": item.material},
        meta={"labels": labels, **({"camera": view.camera} if view.camera else {}), **item.meta},
    )


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
