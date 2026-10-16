"""``DummyModel``: canned answers so the whole pipeline runs without GPUs or API keys.

Given a ``schema``, it writes a valid instance of that answer type, chosen
deterministically from the request content (same question, same answer; different
questions, different answers). Without a schema it echoes the prompt. A configurable
``failure_rate`` returns unparseable text for a deterministic subset of requests, so the
failure counting of the scoring stage is exercised in tests.
"""

from __future__ import annotations

import hashlib
import json
import random
from typing import Any

from pydantic import BaseModel

from vsu.models.base import VLM, Decoding, ImageData, Usage
from vsu.models.cache import ResponseCache
from vsu.models.registry import ModelConfig
from vsu.schemas.scene import MATERIAL_CLASSES
from vsu.settings import Settings


def _rng(images: list[ImageData], prompt: str) -> random.Random:
    h = hashlib.sha256(prompt.encode())
    for im in images:
        h.update(im.data)
    return random.Random(int.from_bytes(h.digest()[:8], "big"))


def _estimate(rng: random.Random, low: float, high: float, log_scale: bool = False) -> dict:
    if log_scale:
        import math

        value = math.exp(rng.uniform(math.log(low), math.log(high)))
    else:
        value = rng.uniform(low, high)
    spread = 0.5 * value if log_scale else 0.25 * (high - low)
    return {
        "value": round(value, 4),
        "range": {"low": round(max(value - spread, low), 4), "high": round(value + spread, 4)},
        "confidence": round(rng.uniform(0.3, 0.9), 2),
    }


def canned_answer(schema_name: str, rng: random.Random) -> dict[str, Any] | None:
    """A plausible answer dictionary for a known answer schema, or None."""
    if schema_name == "MaterialAnswer":
        return {
            "material": rng.choice(MATERIAL_CLASSES),
            "confidence": round(rng.uniform(0.3, 0.95), 2),
            "reasoning": "dummy: picked at random",
        }
    if schema_name == "PropertiesAnswer":
        return {
            "restitution": _estimate(rng, 0.1, 0.9),
            "friction": _estimate(rng, 0.1, 0.8),
            "density_kg_m3": _estimate(rng, 100, 8000, log_scale=True),
            "mass_kg": _estimate(rng, 0.05, 5.0, log_scale=True),
            "reasoning": "dummy: numbers drawn at random",
        }
    if schema_name == "YesNoAnswer":
        return {"answer": rng.choice(["yes", "no"]), "confidence": round(rng.uniform(0.3, 0.9), 2)}
    if schema_name == "ChoiceAnswer":
        return {
            "material": rng.choice(MATERIAL_CLASSES),
            "confidence": round(rng.uniform(0.3, 0.9), 2),
        }
    if schema_name == "PairChoiceAnswer":
        return {"choice": rng.choice(["A", "B"]), "confidence": round(rng.uniform(0.3, 0.9), 2)}
    if schema_name == "ComparativeAnswer":
        return {
            "choice": rng.choice(["A", "B", "same"]),
            "confidence": round(rng.uniform(0.3, 0.9), 2),
        }
    if schema_name in ("SceneConfig", "SceneInitAnswer"):
        return {
            "phenomenon": rng.choice(["free_fall", "projectile", "rolling", "sliding"]),
            "objects": [
                {
                    "name": "object",
                    "shape": rng.choice(["sphere", "box"]),
                    "material_class": rng.choice(MATERIAL_CLASSES),
                    "radius_m": round(rng.uniform(0.05, 0.4), 3),
                    "size_m": [round(rng.uniform(0.05, 0.5), 3) for _ in range(3)],
                    "mass_kg": round(rng.uniform(0.1, 3.0), 3),
                    "restitution": round(rng.uniform(0.1, 0.9), 2),
                    "friction": round(rng.uniform(0.1, 0.6), 2),
                    "initial_position_m": [0.0, 0.0, round(rng.uniform(0.5, 3.0), 2)],
                    "initial_velocity_m_s": [0.0, 0.0, 0.0],
                }
            ],
            "surface": {
                "material": "finished_wood",
                "ramp_angle_deg": round(rng.uniform(0, 40), 1),
            },
            "reasoning": "dummy: scene guessed at random",
        }
    return None


class DummyModel(VLM):
    """Returns canned, schema conforming answers without any model."""

    backend = "dummy"

    def __init__(
        self,
        config: ModelConfig | str = "dummy",
        *,
        cache: ResponseCache | None = None,
        settings: Settings | None = None,
        decoding: Decoding | None = None,
        failure_rate: float | None = None,
    ) -> None:
        if isinstance(config, str):
            config = ModelConfig(name=config, backend="dummy")
        super().__init__(config.name, decoding=decoding or config.decoding, cache=cache)
        self.config = config
        rate = config.options.get("failure_rate", 0.0) if failure_rate is None else failure_rate
        self.failure_rate = float(rate)

    @property
    def backend_model(self) -> str:
        return self.config.backend_model

    def _generate(
        self,
        images: list[ImageData],
        prompt: str,
        schema: type[BaseModel] | None,
        decoding: Decoding,
    ) -> tuple[str, Usage, str | None, dict[str, Any]]:
        rng = _rng(images, prompt)
        extra = {"image_sizes": [im.pil.size for im in images], "backend": "dummy"}
        if self.failure_rate > 0 and rng.random() < self.failure_rate:
            return "I am not sure what you are asking.", Usage(), "stop", extra
        answer = canned_answer(schema.__name__, rng) if schema is not None else None
        if answer is None:
            text = f"dummy response to: {prompt[:60]}"
        else:
            text = "```json\n" + json.dumps(answer, indent=1) + "\n```"
        usage = Usage(
            prompt_tokens=len(prompt.split()) + 256 * len(images),
            completion_tokens=len(text.split()),
        )
        return text, usage, "stop", extra
