"""Registry and dummy backend: configs load, models build, answers parse, caching works."""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image
from pydantic import ValidationError

from vsu.models.dummy_backend import DummyModel
from vsu.models.registry import ModelConfig, build_model, list_models, load_model_config
from vsu.schemas import ComparativeAnswer, MaterialAnswer, PropertiesAnswer, SceneInitAnswer
from vsu.settings import Settings
from vsu.utils.parsing import parse_answer

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(cache_root=tmp_path / "cache", data_root=REPO / "data", _env_file=None)


@pytest.fixture
def image(tmp_path: Path) -> Path:
    p = tmp_path / "a.png"
    Image.new("RGB", (16, 16), (120, 120, 120)).save(p)
    return p


# ---------------------------------------------------------------- registry


def test_repository_configs_all_validate(settings: Settings) -> None:
    names = list_models(settings)
    assert {"dummy", "qwen3vl-8b", "internvl3_5-8b", "llava-onevision-7b"} <= set(names)
    for name in names:
        cfg = load_model_config(name, settings)
        assert cfg.name == name and cfg.backend_model


def test_hf_config_fields(settings: Settings) -> None:
    cfg = load_model_config("qwen3vl-8b", settings)
    assert cfg.backend == "hf" and cfg.hf_id == "Qwen/Qwen3-VL-8B-Instruct"
    assert cfg.dtype == "bfloat16" and cfg.decoding.temperature == 0.0
    assert cfg.options["max_pixels"] > 0 and cfg.backend_model == cfg.hf_id


def test_unknown_config_and_invalid_configs(settings: Settings) -> None:
    with pytest.raises(FileNotFoundError, match="known"):
        load_model_config("nope", settings)
    with pytest.raises(ValidationError, match="needs hf_id"):
        ModelConfig(name="x", backend="hf")
    with pytest.raises(ValidationError, match="needs api_model"):
        ModelConfig(name="x", backend="openai")
    with pytest.raises(ValidationError):
        ModelConfig(name="x", backend="dummy", bogus=1)
    with pytest.raises(ValidationError):
        ModelConfig(name="x", backend="dummy", decoding={"beam": 3})


def test_build_model_attaches_cache_under_cache_root(settings: Settings, image: Path) -> None:
    model = build_model("dummy", settings=settings)
    assert isinstance(model, DummyModel) and model.cache is not None
    model.generate([image], "hello")
    assert (settings.cache_root / "responses").is_dir()
    assert build_model("dummy", settings=settings, use_cache=False).cache is None


def test_build_model_does_not_import_torch_for_dummy(settings: Settings) -> None:
    import sys

    before = "torch" in sys.modules
    build_model("dummy", settings=settings)
    assert ("torch" in sys.modules) == before
    assert "vsu.models.hf_backend" not in sys.modules or before


# ---------------------------------------------------------------- dummy answers


@pytest.mark.parametrize(
    "schema",
    [MaterialAnswer, PropertiesAnswer, ComparativeAnswer, SceneInitAnswer],
)
def test_dummy_answers_validate_against_each_schema(image: Path, schema: type) -> None:
    model = DummyModel()
    r = model.generate([image], f"question for {schema.__name__}", schema=schema)
    parsed = parse_answer(r.text, schema, "q")
    assert parsed.ok, parsed.error
    assert r.usage.prompt_tokens and r.extra["image_sizes"] == [(16, 16)]


def test_dummy_is_deterministic_per_request_and_varies_across_requests(image: Path) -> None:
    model = DummyModel()
    a = model.generate([image], "what material?", schema=MaterialAnswer, use_cache=False)
    b = model.generate([image], "what material?", schema=MaterialAnswer, use_cache=False)
    assert a.text == b.text
    texts = {
        model.generate([image], f"question {i}", schema=MaterialAnswer, use_cache=False).text
        for i in range(12)
    }
    assert len(texts) > 1


def test_dummy_without_schema_echoes(image: Path) -> None:
    r = DummyModel().generate([image], "describe this")
    assert r.text.startswith("dummy response to: describe this")


def test_dummy_failure_rate_produces_unparseable_subset(image: Path) -> None:
    model = DummyModel(failure_rate=0.5)
    results = [
        parse_answer(
            model.generate([image], f"q{i}", schema=MaterialAnswer, use_cache=False).text,
            MaterialAnswer,
            f"q{i}",
        ).ok
        for i in range(40)
    ]
    assert 5 < sum(results) < 35
    assert all(
        parse_answer(
            DummyModel(failure_rate=0.0).generate([image], f"q{i}", schema=MaterialAnswer).text,
            MaterialAnswer,
            "q",
        ).ok
        for i in range(10)
    )


def test_dummy_failure_rate_from_config_options(settings: Settings) -> None:
    cfg = ModelConfig(name="flaky", backend="dummy", options={"failure_rate": 0.25})
    assert build_model(cfg, settings=settings, use_cache=False).failure_rate == 0.25
