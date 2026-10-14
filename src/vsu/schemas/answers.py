"""Typed answers per experiment, plus the record produced by the single parsing step.

Scoring reads these models only, never raw model text. A model's JSON is validated into
one of them by ``vsu.utils.parsing``; what does not validate becomes a ``ParsedAnswer``
with ``ok=False`` and an error, so parse failures are counted rather than dropped.
"""

from __future__ import annotations

import re
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from vsu.schemas.scene import SceneConfig

Confidence = float | None


def normalize_label(text: str) -> str:
    """Lower case, trimmed, inner whitespace and hyphens turned into single underscores.

    ``" Book Paper-Cover "`` becomes ``"book_paper_cover"`` so that labels compare equal
    to materials.json keys regardless of how the model typed them.
    """
    return re.sub(r"[\s\-]+", "_", text.strip().lower())


class MaterialAnswer(BaseModel):
    """Experiment 1: what the object is made of."""

    model_config = ConfigDict(extra="ignore")

    material: str = Field(description="Normalized label; closed set key or free text.")
    confidence: Confidence = Field(default=None, ge=0, le=1)
    reasoning: str | None = None

    @field_validator("material")
    @classmethod
    def _normalize(cls, value: str) -> str:
        value = normalize_label(value)
        if not value:
            raise ValueError("material label is empty")
        return value


class PropertyRange(BaseModel):
    """A low-high interval for one property."""

    low: float
    high: float

    @model_validator(mode="after")
    def _ordered(self) -> PropertyRange:
        if self.high < self.low:
            raise ValueError(f"range high {self.high} is below low {self.low}")
        return self

    @property
    def width(self) -> float:
        return self.high - self.low

    def contains(self, value: float) -> bool:
        return self.low <= value <= self.high


class PropertyEstimate(BaseModel):
    """Point estimate, optional range and confidence for one physical property."""

    model_config = ConfigDict(extra="ignore")

    value: float | None = None
    range: PropertyRange | None = None
    confidence: Confidence = Field(default=None, ge=0, le=1)

    @model_validator(mode="after")
    def _something_given(self) -> PropertyEstimate:
        if self.value is None and self.range is None:
            raise ValueError("estimate needs a value or a range")
        return self


class PropertiesAnswer(BaseModel):
    """Experiment 2: restitution, friction and density or mass of one object.

    Every property is optional because prompts ask for subsets; scoring reports
    coverage per property.
    """

    model_config = ConfigDict(extra="ignore")

    restitution: PropertyEstimate | None = None
    friction: PropertyEstimate | None = None
    density_kg_m3: PropertyEstimate | None = None
    mass_kg: PropertyEstimate | None = None
    reasoning: str | None = None

    @model_validator(mode="after")
    def _at_least_one(self) -> PropertiesAnswer:
        if all(
            getattr(self, k) is None
            for k in ("restitution", "friction", "density_kg_m3", "mass_kg")
        ):
            raise ValueError("no property estimated")
        return self


Choice = Literal["A", "B", "same"]


class ComparativeAnswer(BaseModel):
    """Experiment 3: which of two objects (A or B) has more of the asked property."""

    model_config = ConfigDict(extra="ignore")

    choice: Choice
    confidence: Confidence = Field(default=None, ge=0, le=1)
    reasoning: str | None = None

    @field_validator("choice", mode="before")
    @classmethod
    def _normalize_choice(cls, value: object) -> object:
        if isinstance(value, str):
            v = value.strip().strip(".").lower()
            aliases = {
                "a": "A",
                "object a": "A",
                "left": "A",
                "first": "A",
                "b": "B",
                "object b": "B",
                "right": "B",
                "second": "B",
                "same": "same",
                "equal": "same",
                "both": "same",
                "neither": "same",
                "tie": "same",
            }
            return aliases.get(v, value)
        return value


class SceneInitAnswer(SceneConfig):
    """Experiment 4: the scene config the model wrote, with its optional reasoning."""

    reasoning: str | None = None


T = TypeVar("T", bound=BaseModel)


class ParsedAnswer(BaseModel, Generic[T]):
    """Outcome of parsing one model response: the typed answer or the failure reason."""

    question_id: str
    ok: bool
    answer: T | None = None
    error: str | None = Field(default=None, description="Why parsing failed; None when ok.")

    @model_validator(mode="after")
    def _consistent(self) -> ParsedAnswer[T]:
        if self.ok and self.answer is None:
            raise ValueError("ok=True requires an answer")
        if not self.ok and self.error is None:
            raise ValueError("ok=False requires an error")
        return self
