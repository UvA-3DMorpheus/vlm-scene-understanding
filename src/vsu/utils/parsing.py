"""Robust extraction of a JSON object from free form model text, and the one parsing step.

Models wrap JSON in markdown fences, put prose before and after it, leave trailing
commas, use single quotes or Python literals, or answer with a bare label. This module
turns such text into a validated answer model, or into a recorded failure. Scoring never
sees raw text: it consumes the ``ParsedAnswer`` records produced by :func:`parse_answer`.
"""

from __future__ import annotations

import json
import re
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

from vsu.schemas.answers import ParsedAnswer

T = TypeVar("T", bound=BaseModel)

_FENCE = re.compile(r"```(?:json|JSON|javascript|js)?\s*\n?(.*?)```", re.DOTALL)
_TRAILING_COMMA = re.compile(r",\s*([}\]])")
_PY_LITERALS = {r"\bTrue\b": "true", r"\bFalse\b": "false", r"\bNone\b": "null", r"\bNaN\b": "null"}
_MAX_BARE_LABEL_CHARS = 80
_THINK_BLOCK = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
_OPEN_THINK = re.compile(r"<think>.*\Z", re.DOTALL | re.IGNORECASE)
_BOX_MARKERS = re.compile(r"<\|begin_of_box\|>|<\|end_of_box\|>")
_BOX_CONTENT = re.compile(r"<\|begin_of_box\|>(.*?)<\|end_of_box\|>", re.DOTALL)


class JSONNotFound(ValueError):
    """Raised when no JSON object can be recovered from the text."""


def strip_reasoning(text: str) -> str:
    """Remove a reasoning model's scratch work so only the final answer is parsed.

    Drops ``<think>…</think>`` blocks (and an unterminated ``<think>`` tail, which means
    the token budget ran out mid-thought). GLM-4.xV marks its final answer with
    ``<|begin_of_box|>…<|end_of_box|>``: when such a box is present, its content is the
    answer and the sentence around it ("The answer is …") is dropped; the last box wins.
    Plain text passes through unchanged.
    """
    if not text:
        return text
    cleaned = _THINK_BLOCK.sub("", text)
    cleaned = _OPEN_THINK.sub("", cleaned)
    boxes = _BOX_CONTENT.findall(cleaned)
    if boxes:
        return boxes[-1].strip()
    cleaned = _BOX_MARKERS.sub("", cleaned)
    return cleaned.strip()


def _balanced_objects(text: str) -> list[str]:
    """Return every top level ``{...}`` substring whose braces balance.

    Braces inside string literals and escaped quotes are ignored, so an object whose
    values contain ``{`` is returned whole. Quotes are only tracked inside braces, so an
    apostrophe in the surrounding prose (``I'd say {...}``) cannot swallow the object.
    Candidates come in text order.
    """
    out: list[str] = []
    depth = 0
    start = -1
    in_string = False
    quote = ""
    escaped = False
    for i, ch in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                in_string = False
            continue
        if depth > 0 and ch in ('"', "'"):
            in_string, quote = True, ch
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}" and depth > 0:
            depth -= 1
            if depth == 0:
                out.append(text[start : i + 1])
    return out


def _repair(candidate: str) -> str:
    """Apply cheap fixes for the most common deviations from strict JSON."""
    fixed = _TRAILING_COMMA.sub(r"\1", candidate)
    for pattern, replacement in _PY_LITERALS.items():
        fixed = re.sub(pattern, replacement, fixed)
    if '"' not in fixed and "'" in fixed:
        fixed = fixed.replace("'", '"')
    return fixed


def _try_load(candidate: str) -> dict[str, Any] | None:
    for attempt in (candidate, _repair(candidate)):
        try:
            value = json.loads(attempt)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def extract_json(text: str) -> dict[str, Any]:
    """Return the first JSON object found in ``text``.

    Search order: fenced code blocks, then the whole text, then every balanced
    ``{...}`` substring. Each candidate is tried strictly and then with repairs
    (trailing commas, Python literals, single quotes). Raises :class:`JSONNotFound`
    when nothing yields a JSON object.
    """
    if not text or not text.strip():
        raise JSONNotFound("empty response")
    candidates: list[str] = [m.group(1).strip() for m in _FENCE.finditer(text)]
    candidates.append(text.strip())
    for chunk in list(candidates):
        candidates.extend(_balanced_objects(chunk))
    seen: set[str] = set()
    for candidate in candidates:
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        loaded = _try_load(candidate)
        if loaded is not None:
            return loaded
    raise JSONNotFound("no JSON object found in response")


def _summarize_validation_error(exc: ValidationError) -> str:
    """One line per error: ``field: message``, enough to see why a parse failed."""
    parts = []
    for err in exc.errors()[:3]:
        loc = ".".join(str(p) for p in err["loc"]) or "<root>"
        parts.append(f"{loc}: {err['msg']}")
    extra = len(exc.errors()) - 3
    return "; ".join(parts) + (f"; and {extra} more" if extra > 0 else "")


def parse_answer(
    text: str,
    model: type[T],
    question_id: str,
    *,
    bare_label_field: str | None = None,
) -> ParsedAnswer[T]:
    """Turn one model response into a ``ParsedAnswer`` of ``model``.

    Consumes the raw text, the answer model to validate against and the question id.
    Reasoning blocks and answer markers are stripped first (:func:`strip_reasoning`).
    Produces a record with ``ok=True`` and the typed answer, or ``ok=False`` and a short
    error. With ``bare_label_field`` set (for example ``"material"``), a response that
    contains no JSON but is a single short line is accepted as ``{field: line}``, which
    is what a closed set prompt asking for one word produces.
    """
    text = strip_reasoning(text or "")
    data: dict[str, Any] | None = None
    try:
        data = extract_json(text)
    except JSONNotFound as exc:
        stripped = text.strip().strip("`*_\"' ").strip()
        if (
            bare_label_field is not None
            and stripped
            and "\n" not in stripped
            and len(stripped) <= _MAX_BARE_LABEL_CHARS
        ):
            data = {bare_label_field: stripped.rstrip(".")}
        else:
            return ParsedAnswer[model](question_id=question_id, ok=False, error=str(exc))  # type: ignore[valid-type]
    try:
        answer = model.model_validate(data)
    except ValidationError as exc:
        return ParsedAnswer[model](  # type: ignore[valid-type]
            question_id=question_id, ok=False, error=_summarize_validation_error(exc)
        )
    return ParsedAnswer[model](question_id=question_id, ok=True, answer=answer)  # type: ignore[valid-type]
