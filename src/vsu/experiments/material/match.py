"""Experiment 1.2: material matching between two objects.

Two objects of different materials are shown together, from the same camera, and the model
is told both materials and asked which object has one of them: "One of the two objects is
made of metal and the other of paper. Which object is made of metal, A or B?". This is the
comparative form of material recognition: a model may fail to name a material on its own
and still tell two apart.

Every pair is asked in four forms, both image orders times both asked materials, which
separates accuracy from a bias towards a letter and from inconsistent answers (see
:mod:`vsu.scoring.pairwise`). Two presentations: ``separate`` (two images, A then B) and
``sidebyside`` (one composite image, A on the left, B on the right, each labelled).

Objects and images come from :mod:`vsu.experiments.material.items`, shared with 1.0 and 1.1.
Variants: ``v1`` answer only (a bare letter is accepted), ``v2`` a short comparison of the
visual cues and a JSON answer.
"""

from __future__ import annotations

import hashlib
import logging
from itertools import combinations
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel

from vsu.data.materials import MaterialTable, load_material_table
from vsu.experiments.base import Experiment, Question, ScoredRecord
from vsu.experiments.material.items import (
    MaterialItem,
    MaterialView,
    dataset_roles,
    distinct_materials,
    label_text,
    load_items,
)
from vsu.schemas.answers import PairChoiceAnswer
from vsu.scoring.binary import group_by
from vsu.scoring.classification import label_counts
from vsu.scoring.pairwise import PairRecord, pair_summary
from vsu.utils.io import tmp_path
from vsu.utils.seeding import rng

log = logging.getLogger(__name__)

PRESENTATIONS = ("separate", "sidebyside")


class MatchingExperiment(Experiment):
    """Experiment 1.2. See the module docstring."""

    name = "exp1_2"
    answer_schema = PairChoiceAnswer
    bare_label_field = "choice"

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
        """Four forms per pair, view and presentation."""
        opts = self.config.options
        presentations = list(opts.get("presentations", PRESENTATIONS))
        unknown = set(presentations) - set(PRESENTATIONS)
        if unknown:
            raise ValueError(f"unknown presentations {sorted(unknown)}")
        items = load_items(opts, self.settings, self.table)
        questions: list[Question] = []
        for dataset, group in group_by(items, lambda i: i.dataset).items():
            for a, b, view_key in self._pairs(dataset, group):
                for presentation in presentations:
                    questions += self._forms(a, b, view_key, presentation)
        log.info(
            "exp1_2: %d questions (%s)",
            len(questions),
            label_counts(f"{q.dataset}/{q.condition}" for q in questions),
        )
        return questions

    def _pairs(
        self, dataset: str, items: list[MaterialItem]
    ) -> list[tuple[MaterialItem, MaterialItem, str]]:
        """Every two items of distinct materials (not overlapping, see ``OVERLAPPING``), per
        view both have; optionally a seeded sample."""
        pairs = [
            (a, b, view.key)
            for a, b in combinations(items, 2)
            if distinct_materials(a.material, b.material)
            for view in a.views
            if b.view(view.key) is not None
        ]
        limit = (self.config.options.get("max_pairs") or {}).get(dataset)
        if limit is not None and len(pairs) > limit:
            picked = set(rng(self.config.seed, dataset, "pairs").sample(range(len(pairs)), limit))
            pairs = [p for i, p in enumerate(pairs) if i in picked]
        return pairs

    def _forms(
        self, a: MaterialItem, b: MaterialItem, view_key: str, presentation: str
    ) -> list[Question]:
        """Both image orders times both asked materials."""
        out = []
        pair_id = f"{a.dataset}/{a.item_id}+{b.item_id}/{view_key}/{presentation}"
        for first, second in ((a, b), (b, a)):
            images = self._images(first.view(view_key), second.view(view_key), presentation)
            for asked, other in ((first, second), (second, first)):
                view = first.view(view_key)
                assert view is not None
                out.append(
                    Question(
                        id=(
                            f"{a.dataset}/{first.item_id}+{second.item_id}/{view_key}/"
                            f"{presentation}/{asked.material}"
                        ),
                        dataset=a.dataset,
                        item_id=f"{a.item_id}+{b.item_id}",
                        condition=presentation,
                        images=images,
                        context={
                            "presentation": presentation,
                            "asked": label_text(asked.material),
                            "other": label_text(other.material),
                        },
                        target={"material": asked.material, "object": asked.item_id},
                        meta={
                            "pair": pair_id,
                            "image_a": first.item_id,
                            "image_b": second.item_id,
                            # the same object and view in Experiments 1.0 and 1.1
                            "view_a": first.view_id(view),
                            "view_b": second.view_id(view),
                            "materials": sorted((a.material, b.material)),
                            "asked": asked.material,
                            **({"camera": view.camera} if view.camera else {}),
                            "view_condition": view.condition,
                        },
                    )
                )
        return out

    def _images(
        self, first: MaterialView | None, second: MaterialView | None, presentation: str
    ) -> list[str]:
        assert first is not None and second is not None
        if presentation == "separate":
            return [*first.images, *second.images]
        out = self.settings.cache_root / "composites"
        return [str(side_by_side(first.images[0], second.images[0], out))]

    # ---- scoring

    def score_record(
        self, question: Question, answer: BaseModel | None, variant: str
    ) -> dict[str, Any]:
        record = _pair_record(question.meta, question.target, answer)
        return {
            "chosen": record.chosen,
            "truth": record.truth,
            "correct": record.correct,
            "chosen_object": record.chosen_object,
        }

    def summarize(self, scored: list[ScoredRecord], variant: str) -> dict[str, Any]:
        """Pair metrics per dataset and per ``<dataset>/<presentation>`` group."""
        roles = dataset_roles(self.config.options)
        out: dict[str, Any] = {"dataset_roles": roles, "groups": {}, "datasets": {}}
        records = {s.question_id: _scored_pair(s) for s in scored}
        for name, group in group_by(scored, lambda s: f"{s.dataset}/{s.condition}").items():
            out["groups"][name] = pair_summary([records[s.question_id] for s in group])
        for dataset, group in group_by(scored, lambda s: s.dataset).items():
            by_camera = group_by(
                [s for s in group if s.meta.get("camera")], lambda s: s.meta["camera"]
            )
            by_materials = group_by(group, lambda s: "|".join(s.meta["materials"]))
            out["datasets"][dataset] = {
                "role": roles.get(dataset, "other"),
                "n_parse_failures": sum(not s.parse_ok for s in group),
                "by_camera": {
                    c: pair_summary([records[s.question_id] for s in ss])["accuracy"]
                    for c, ss in by_camera.items()
                },
                "by_material_pair": {
                    m: pair_summary([records[s.question_id] for s in ss])["accuracy"]
                    for m, ss in by_materials.items()
                },
                **pair_summary([records[s.question_id] for s in group]),
            }
        return out


def _pair_record(
    meta: dict[str, Any], target: dict[str, Any], answer: BaseModel | None
) -> PairRecord:
    chosen = answer.choice if isinstance(answer, PairChoiceAnswer) else None
    return PairRecord(
        pair=meta["pair"],
        image_a=meta["image_a"],
        image_b=meta["image_b"],
        asked=meta["asked"],
        answer_object=target["object"],
        chosen=chosen,
    )


def _scored_pair(s: ScoredRecord) -> PairRecord:
    return PairRecord(
        pair=s.meta["pair"],
        image_a=s.meta["image_a"],
        image_b=s.meta["image_b"],
        asked=s.meta["asked"],
        answer_object=s.target["object"],
        chosen=s.derived.get("chosen") if s.parse_ok else None,
    )


def side_by_side(left: str, right: str, out_dir: Path, *, height: int = 448) -> Path:
    """One image with ``left`` and ``right`` scaled to the same height, labelled A and B.

    Written once into ``out_dir`` under a name hashed from both source files' bytes, so
    the same pair always gives the same file (and the same cached answers).
    """
    digest = hashlib.sha256(Path(left).read_bytes() + b"|" + Path(right).read_bytes()).hexdigest()
    path = Path(out_dir) / f"pair_{digest[:20]}.png"
    if path.is_file():
        return path
    panels = []
    for source in (left, right):
        with Image.open(source) as im:
            im = im.convert("RGB")
            width = max(1, round(im.width * height / im.height))
            panels.append(im.resize((width, height), Image.Resampling.LANCZOS))
    gap, band = 24, 64
    canvas = Image.new(
        "RGB", (panels[0].width + gap + panels[1].width, height + band), (255, 255, 255)
    )
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=44)
    x = 0
    for letter, panel in zip("AB", panels, strict=True):
        canvas.paste(panel, (x, band))
        box = draw.textbbox((0, 0), letter, font=font)
        draw.text(
            (x + (panel.width - (box[2] - box[0])) / 2, 6), letter, fill=(20, 20, 20), font=font
        )
        x += panel.width + gap
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = tmp_path(path)
    canvas.save(tmp, "PNG")
    tmp.replace(path)
    return path
