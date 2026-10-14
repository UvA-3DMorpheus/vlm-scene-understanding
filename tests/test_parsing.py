"""JSON extraction copes with messy model text; failures are recorded, not dropped."""

from __future__ import annotations

import pytest

from vsu.schemas import ComparativeAnswer, MaterialAnswer, PropertiesAnswer, SceneInitAnswer
from vsu.utils.parsing import (
    JSONNotFound,
    extract_json,
    parse_answer,
    strip_reasoning,
)

# ---------------------------------------------------------------- extract_json


@pytest.mark.parametrize(
    "text",
    [
        '{"material": "metal", "confidence": 0.8}',
        '  \n {"material": "metal", "confidence": 0.8} \n',
        'Sure! Here is the answer:\n```json\n{"material": "metal", "confidence": 0.8}\n```\n'
        "Let me know.",
        '```\n{"material": "metal", "confidence": 0.8}\n```',
        'The object looks shiny. {"material": "metal", "confidence": 0.8} I am fairly sure.',
        '{"material": "metal", "confidence": 0.8,}',
        "{'material': 'metal', 'confidence': 0.8}",
        '{"material": "metal", "confidence": 0.8, "extra": None, "flag": True}',
    ],
)
def test_extracts_object_from_messy_text(text: str) -> None:
    data = extract_json(text)
    assert data["material"] == "metal"
    assert data["confidence"] == 0.8


def test_braces_inside_strings_do_not_break_balancing() -> None:
    text = 'Answer: {"reasoning": "the {bracket} shape and a } sign", "material": "wood"} done'
    data = extract_json(text)
    assert data["material"] == "wood"
    assert "{bracket}" in data["reasoning"]


@pytest.mark.parametrize(
    "text",
    [
        'I\'d say it\'s metal: {"material": "metal"}',
        'The label reads "steel", so {"material": "metal"} is my answer, isn\'t it?',
        "Don't quote me, but {'material': 'metal'}",
    ],
)
def test_quotes_in_surrounding_prose_do_not_swallow_the_object(text: str) -> None:
    assert extract_json(text)["material"] == "metal"


def test_escaped_quotes_inside_strings() -> None:
    text = r'{"reasoning": "it says \"steel\" on the label", "material": "metal"}'
    assert extract_json(text)["material"] == "metal"


def test_nested_objects_returned_whole() -> None:
    text = (
        'Result:\n{"friction": {"value": 0.3, "range": {"low": 0.2, "high": 0.4}}, "mass_kg": null}'
    )
    data = extract_json(text)
    assert data["friction"]["range"]["high"] == 0.4


def test_first_valid_object_wins_and_broken_ones_are_skipped() -> None:
    text = '{"broken": } then {"material": "ceramic"} and later {"material": "glass"}'
    assert extract_json(text)["material"] == "ceramic"


def test_top_level_list_is_not_an_object() -> None:
    with pytest.raises(JSONNotFound):
        extract_json('[{"material": "metal"}]'.replace("{", "<").replace("}", ">"))


def test_truncated_json_fails() -> None:
    with pytest.raises(JSONNotFound):
        extract_json('{"material": "metal", "confidence": 0.')


@pytest.mark.parametrize("text", ["", "   ", "The object is made of metal.", "metal"])
def test_no_json_raises(text: str) -> None:
    with pytest.raises(JSONNotFound):
        extract_json(text)


def test_fenced_block_preferred_over_prose_braces() -> None:
    text = 'Note {not json}\n```json\n{"material": "plastic"}\n```'
    assert extract_json(text)["material"] == "plastic"


# ---------------------------------------------------------------- parse_answer


def test_parse_answer_success() -> None:
    r = parse_answer('```json\n{"material": "Metal", "confidence": 0.9}\n```', MaterialAnswer, "q1")
    assert r.ok and r.error is None
    assert r.answer is not None and r.answer.material == "metal"


def test_parse_answer_records_missing_json() -> None:
    r = parse_answer(
        "I think it is probably made of some kind of metal, hard to say.", MaterialAnswer, "q2"
    )
    assert not r.ok and r.answer is None
    assert r.error is not None and "no JSON" in r.error


def test_parse_answer_records_schema_violation_with_field_name() -> None:
    r = parse_answer('{"material": "metal", "confidence": 7}', MaterialAnswer, "q3")
    assert not r.ok
    assert r.error is not None and "confidence" in r.error


def test_parse_answer_records_empty_response() -> None:
    r = parse_answer("", MaterialAnswer, "q4")
    assert not r.ok and r.error == "empty response"


@pytest.mark.parametrize(
    ("text", "label"),
    [
        ("metal", "metal"),
        ("Metal.", "metal"),
        ("`cardboard`", "cardboard"),
        ("  Book paper cover \n", "book_paper_cover"),
    ],
)
def test_bare_label_accepted_when_enabled(text: str, label: str) -> None:
    r = parse_answer(text, MaterialAnswer, "q5", bare_label_field="material")
    assert r.ok and r.answer is not None and r.answer.material == label


def test_bare_label_rejected_for_long_or_multiline_text() -> None:
    prose = "It looks like metal.\nBut it could also be painted wood."
    r = parse_answer(prose, MaterialAnswer, "q6", bare_label_field="material")
    assert not r.ok
    r = parse_answer("x" * 200, MaterialAnswer, "q7", bare_label_field="material")
    assert not r.ok


def test_bare_label_not_used_without_opt_in() -> None:
    assert not parse_answer("metal", MaterialAnswer, "q8").ok


def test_parse_comparative_with_alias() -> None:
    r = parse_answer('{"choice": "object b", "confidence": 0.6}', ComparativeAnswer, "pair1")
    assert r.ok and r.answer is not None and r.answer.choice == "B"


def test_parse_properties_partial_answer() -> None:
    text = (
        'Estimates:\n{"friction": {"value": 0.35, "range": {"low": 0.3, "high": 0.5}, '
        '"confidence": 0.5}}'
    )
    r = parse_answer(text, PropertiesAnswer, "p1")
    assert r.ok and r.answer is not None
    assert r.answer.friction is not None and r.answer.friction.value == 0.35
    assert r.answer.mass_kg is None


def test_parse_scene_config_from_model_output() -> None:
    text = (
        "Here is the scene config:\n```json\n"
        '{"phenomenon": "sliding", "objects": [{"name": "book", "shape": "box", '
        '"size_m": [0.2, 0.14, 0.05], "material_class": "book_paper_cover", "friction": 0.4}], '
        '"surface": {"material": "finished_wood", "ramp_angle_deg": 30}, '
        '"reasoning": "a paperback on a tilted wooden board"}\n```'
    )
    r = parse_answer(text, SceneInitAnswer, "s1")
    assert r.ok and r.answer is not None
    assert r.answer.objects[0].material_class == "book_paper_cover"
    assert r.answer.surface is not None and r.answer.surface.ramp_angle_deg == 30
    assert r.answer.reasoning is not None and r.answer.reasoning.startswith("a paperback")


def test_parse_scene_config_invalid_angle_fails_with_location() -> None:
    text = (
        '{"phenomenon": "sliding", "objects": [{"name": "b", "shape": "box"}], '
        '"surface": {"ramp_angle_deg": 120}}'
    )
    r = parse_answer(text, SceneInitAnswer, "s2")
    assert not r.ok and r.error is not None and "surface.ramp_angle_deg" in r.error


# ---------------------------------------------------------------- reasoning models


def test_strip_reasoning_removes_think_blocks_and_box_markers() -> None:
    text = "<think>Got it, a bearing, so metal.</think>\n<|begin_of_box|>metal<|end_of_box|>"
    assert strip_reasoning(text) == "metal"
    boxed_json = (
        '<think>x</think>\n<|begin_of_box|>{"material": "steel", "confidence": 0.95}<|end_of_box|>'
    )
    assert strip_reasoning(boxed_json) == '{"material": "steel", "confidence": 0.95}'
    assert strip_reasoning("<think>never closed because the budget ran out") == ""
    assert strip_reasoning("plain answer") == "plain answer"
    assert strip_reasoning("") == ""


def test_parse_answer_handles_reasoning_model_output() -> None:
    v1 = "<think>Got it, a bearing, so metal.</think>\n<|begin_of_box|>metal<|end_of_box|>"
    r = parse_answer(v1, MaterialAnswer, "q", bare_label_field="material")
    assert r.ok and r.answer is not None and r.answer.material == "metal"
    v2 = (
        "<think>steel, high confidence</think>\n"
        '<|begin_of_box|>{"material": "steel", "confidence": 0.95}<|end_of_box|>'
    )
    r = parse_answer(v2, MaterialAnswer, "q")
    assert r.ok and r.answer is not None and r.answer.material == "steel"
    truncated = "<think>" + "thinking " * 50
    r = parse_answer(truncated, MaterialAnswer, "q", bare_label_field="material")
    assert not r.ok and r.error == "empty response"
