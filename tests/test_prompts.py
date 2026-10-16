"""Templates are found by experiment and variant, rendered strictly, and hashed."""

from __future__ import annotations

from pathlib import Path

import pytest
from jinja2 import UndefinedError

from vsu.prompts import loader


@pytest.fixture
def templates(tmp_path: Path) -> Path:
    (tmp_path / "expx_v1.jinja").write_text(
        "Material of {{ object }}? Options: {{ labels | join(', ') }}\n"
    )
    (tmp_path / "expx_v2.jinja").write_text(
        "{% for l in labels %}- {{ l }}\n{% endfor %}Free text about {{ object }}."
    )
    (tmp_path / "other_v1.jinja").write_text("x")
    return tmp_path


def test_list_variants_per_experiment(templates: Path) -> None:
    assert loader.list_variants("expx", templates) == ["v1", "v2"]
    assert loader.list_variants("other", templates) == ["v1"]
    assert loader.list_variants("none", templates) == []


def test_render_strips_and_joins(templates: Path) -> None:
    text = loader.render("expx", "v1", templates, object="ball", labels=["metal", "wood"])
    assert text == "Material of ball? Options: metal, wood"
    text = loader.render("expx", "v2", templates, object="ball", labels=["a", "b"])
    assert text == "- a\n- b\nFree text about ball."


def test_missing_context_is_an_error(templates: Path) -> None:
    with pytest.raises(UndefinedError):
        loader.render("expx", "v1", templates, object="ball")


def test_missing_template_lists_known_variants(templates: Path) -> None:
    with pytest.raises(FileNotFoundError, match=r"\['v1', 'v2'\]"):
        loader.template_path("expx", "v9", templates)


def test_hash_changes_with_the_file(templates: Path) -> None:
    before = loader.template_hash("expx", "v1", templates)
    (templates / "expx_v1.jinja").write_text("changed {{ object }} {{ labels }}")
    assert loader.template_hash("expx", "v1", templates) != before
    assert len(before) == 64


def test_real_templates_dir_exists() -> None:
    assert loader.TEMPLATES_DIR.is_dir()


def test_longer_experiment_names_do_not_leak_into_variants(templates: Path) -> None:
    (templates / "expx_1_yesno_v1.jinja").write_text("x")
    assert loader.list_variants("expx", templates) == ["v1", "v2"]
    assert loader.list_variants("expx_1", templates) == ["yesno_v1"]
