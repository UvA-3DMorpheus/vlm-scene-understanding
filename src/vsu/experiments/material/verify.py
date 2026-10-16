"""Experiment 1.1: material verification from a single image.

Two tasks on the same objects and views as Experiment 1.0:

- ``yesno``: "Is it made of <material>?", asked for the true material (positive) and for a
  few wrong ones (negatives). Scored with balanced accuracy, since most questions are
  negatives, and with the yes rate, which exposes a bias towards agreeing.
- ``choice``: "Is it made of <A> or of <B>?", the true material against each wrong one,
  asked in both orders. Scored with accuracy, the rate of picking the first-named option
  (0.5 is unbiased) and order consistency over the swapped pairs.

A variant is ``<task>_<version>``: ``v1`` asks for the answer only (a bare word is
accepted), ``v2`` asks for a short reasoning step and a JSON answer. Each variant asks only
its own task's questions (:meth:`questions_for`).
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel

from vsu.data.materials import MaterialTable, load_material_table
from vsu.experiments.base import Experiment, Question, ScoredRecord
from vsu.experiments.material.items import (
    FOCUS,
    MaterialItem,
    MaterialView,
    dataset_roles,
    distinct_materials,
    label_text,
    load_items,
)
from vsu.schemas.answers import ChoiceAnswer, YesNoAnswer, normalize_label
from vsu.scoring.binary import ChoiceRecord, YesNoRecord, choice_summary, group_by, yesno_summary
from vsu.scoring.classification import label_counts
from vsu.utils.seeding import rng

log = logging.getLogger(__name__)

TASKS: dict[str, type[BaseModel]] = {"yesno": YesNoAnswer, "choice": ChoiceAnswer}
BARE_FIELDS = {"yesno": "answer", "choice": "material"}


def task_of(variant: str) -> str:
    """``choice_v2`` -> ``choice``; raises for a variant of no known task."""
    task = variant.split("_", 1)[0]
    if task not in TASKS:
        raise ValueError(f"variant {variant!r} belongs to no task of {sorted(TASKS)}")
    return task


class VerificationExperiment(Experiment):
    """Experiment 1.1. See the module docstring."""

    name = "exp1_1"
    answer_schema = YesNoAnswer  # per variant: see schema_for

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._table: MaterialTable | None = None

    @property
    def table(self) -> MaterialTable:
        if self._table is None:
            self._table = load_material_table(settings=self.settings)
        return self._table

    # ---- per variant

    def schema_for(self, variant: str) -> type[BaseModel]:
        return TASKS[task_of(variant)]

    def bare_label_field_for(self, variant: str) -> str | None:
        return BARE_FIELDS[task_of(variant)] if variant.endswith("_v1") else None

    def questions_for(self, variant: str, questions: list[Question]) -> list[Question]:
        task = task_of(variant)
        return [q for q in questions if q.meta["task"] == task]

    # ---- questions

    def build_questions(self) -> list[Question]:
        """Every yes/no and two-option question of every item and view (both tasks)."""
        opts = self.config.options
        n_wrong = opts.get("distractors")
        questions: list[Question] = []
        for item in load_items(opts, self.settings, self.table):
            wrong = self._distractors(item, n_wrong)
            for view in item.views:
                if _asks(view, opts.get("yesno_conditions")):
                    questions += [
                        self._yesno(item, view, asked) for asked in [item.material, *wrong]
                    ]
                if _asks(view, opts.get("choice_conditions")):
                    for other in wrong:
                        questions.append(self._choice(item, view, item.material, other))
                        questions.append(self._choice(item, view, other, item.material))
        log.info(
            "exp1_1: %d questions (%s)",
            len(questions),
            label_counts(f"{q.dataset}/{q.meta['task']}" for q in questions),
        )
        return questions

    def _distractors(self, item: MaterialItem, n: int | None) -> list[str]:
        """The wrong materials asked about this item: all, or a seeded sample of ``n``.

        A label overlapping the true material (plastic for a ping pong ball) is never wrong.
        """
        wrong = [label for label in item.labels if distinct_materials(label, item.material)]
        if n is None or n >= len(wrong):
            return wrong
        picked = rng(self.config.seed, item.dataset, item.item_id).sample(wrong, n)
        return [label for label in wrong if label in picked]  # keep the label set's order

    @staticmethod
    def _yesno(item: MaterialItem, view: MaterialView, asked: str) -> Question:
        return Question(
            id=f"{item.view_id(view)}/yesno/{asked}",
            dataset=item.dataset,
            item_id=item.item_id,
            condition=view.condition,
            images=list(view.images),
            context={"focus": FOCUS[view.condition], "asked": label_text(asked)},
            target={"material": item.material},
            meta={"task": "yesno", "asked": asked, **_view_meta(item, view)},
        )

    @staticmethod
    def _choice(item: MaterialItem, view: MaterialView, first: str, second: str) -> Question:
        return Question(
            id=f"{item.view_id(view)}/choice/{first}-{second}",
            dataset=item.dataset,
            item_id=item.item_id,
            condition=view.condition,
            images=list(view.images),
            context={
                "focus": FOCUS[view.condition],
                "first": label_text(first),
                "second": label_text(second),
            },
            target={"material": item.material},
            meta={"task": "choice", "first": first, "second": second, **_view_meta(item, view)},
        )

    # ---- scoring

    def score_record(
        self, question: Question, answer: BaseModel | None, variant: str
    ) -> dict[str, Any]:
        truth = question.target["material"]
        if question.meta["task"] == "yesno":
            reply = answer.answer if isinstance(answer, YesNoAnswer) else None
            record = YesNoRecord(question.meta["asked"], truth, reply)
            return {"reply": reply, "positive": record.positive, "correct": record.correct}
        chosen = self._chosen_option(answer, question) if answer is not None else None
        record = ChoiceRecord(question.meta["first"], question.meta["second"], truth, chosen, "")
        return {
            "chosen": chosen,
            "valid": record.valid,
            "first_chosen": chosen == record.first,
            "correct": record.correct,
        }

    def _chosen_option(self, answer: BaseModel, question: Question) -> str:
        """Map a two-option reply onto ``first`` or ``second``; anything else is kept as is."""
        assert isinstance(answer, ChoiceAnswer)
        reply = answer.material
        for key in (question.meta["first"], question.meta["second"]):
            if reply in (key, normalize_label(label_text(key))):
                return key
        resolved = self.table.resolve(reply)
        if resolved in (question.meta["first"], question.meta["second"]):
            return resolved
        return reply

    def summarize(self, scored: list[ScoredRecord], variant: str) -> dict[str, Any]:
        """The task's summary per dataset and per ``<dataset>/<condition>`` group."""
        roles = dataset_roles(self.config.options)
        task = task_of(variant)
        out: dict[str, Any] = {"task": task, "dataset_roles": roles, "groups": {}, "datasets": {}}
        for name, records in group_by(scored, lambda s: f"{s.dataset}/{s.condition}").items():
            out["groups"][name] = _task_summary(task, records)
        for dataset, records in group_by(scored, lambda s: s.dataset).items():
            out["datasets"][dataset] = {
                "role": roles.get(dataset, "other"),
                "n_parse_failures": sum(not r.parse_ok for r in records),
                "by_camera": {
                    camera: _task_summary(task, rs)["accuracy"]
                    for camera, rs in group_by(
                        [r for r in records if r.meta.get("camera")], lambda r: r.meta["camera"]
                    ).items()
                },
                **_task_summary(task, records),
            }
        return out


def _asks(view: MaterialView, conditions: list[str] | None) -> bool:
    """Photos are always asked; scene views only in the task's listed conditions."""
    return view.camera is None or conditions is None or view.condition in conditions


def _view_meta(item: MaterialItem, view: MaterialView) -> dict[str, Any]:
    return {
        **({"camera": view.camera} if view.camera else {}),
        "view": item.view_id(view),
        **item.meta,
    }


def _task_summary(task: str, records: list[ScoredRecord]) -> dict[str, Any]:
    if task == "yesno":
        return yesno_summary(
            [
                YesNoRecord(r.meta["asked"], r.target["material"], r.derived.get("reply"))
                for r in records
            ]
        )
    return choice_summary(
        [
            ChoiceRecord(
                r.meta["first"],
                r.meta["second"],
                r.target["material"],
                r.derived.get("chosen"),
                r.meta["view"],
            )
            for r in records
        ]
    )
