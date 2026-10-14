"""The VLM interface: image normalization, cache keys, caching, retries, decoding merge."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from PIL import Image
from pydantic import BaseModel, ValidationError

from vsu.models import (
    VLM,
    Decoding,
    ImageData,
    Response,
    ResponseCache,
    TransientError,
    Usage,
    cache_key,
    to_image_data,
)


class FakeVLM(VLM):
    """Counts calls and answers with a canned text; can fail transiently first."""

    backend = "fake"

    def __init__(self, *args: Any, fail_first: int = 0, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.calls: list[tuple[list[ImageData], str, Decoding]] = []
        self.fail_first = fail_first
        self.retry_wait_s = 0.0

    @property
    def backend_model(self) -> str:
        return "fake/model-1"

    def _generate(self, images, prompt, schema, decoding):  # type: ignore[no-untyped-def]
        self.calls.append((images, prompt, decoding))
        if self.fail_first > 0:
            self.fail_first -= 1
            raise TransientError("rate limited")
        return (
            f"answer to: {prompt}",
            Usage(prompt_tokens=10, completion_tokens=3),
            "stop",
            {"k": 1},
        )


class Answer(BaseModel):
    material: str


@pytest.fixture
def png(tmp_path: Path) -> Path:
    path = tmp_path / "img.png"
    Image.new("RGB", (8, 8), (200, 30, 30)).save(path)
    return path


@pytest.fixture
def jpg(tmp_path: Path) -> Path:
    path = tmp_path / "img.jpg"
    Image.new("RGB", (8, 8), (30, 200, 30)).save(path, quality=90)
    return path


# ---------------------------------------------------------------- images


def test_path_inputs_keep_file_bytes(png: Path, jpg: Path) -> None:
    a = to_image_data(png)
    assert a.mime == "image/png" and a.data == png.read_bytes()
    b = to_image_data(str(jpg))
    assert b.mime == "image/jpeg" and b.data == jpg.read_bytes()
    assert b.pil.size == (8, 8)


def test_pil_and_raw_bytes_inputs(png: Path) -> None:
    im = Image.new("RGB", (4, 4), (0, 0, 255))
    a = to_image_data(im)
    assert a.mime == "image/png" and a.pil.getpixel((0, 0)) == (0, 0, 255)
    b = to_image_data(png.read_bytes())
    assert b.mime == "image/png" and b.data == png.read_bytes()
    assert to_image_data(a) is a
    with pytest.raises(TypeError):
        to_image_data(42)


def test_unknown_extension_is_re_encoded(tmp_path: Path) -> None:
    path = tmp_path / "img.bmp"
    Image.new("RGB", (4, 4), (9, 9, 9)).save(path)
    data = to_image_data(path)
    assert data.mime == "image/png" and data.pil.getpixel((1, 1)) == (9, 9, 9)


# ---------------------------------------------------------------- keys


def test_cache_key_is_deterministic_and_sensitive() -> None:
    base = dict(model="m", decoding={"temperature": 0.0}, prompt="p", images=[b"a"], schema=None)
    k = cache_key(**base)
    assert k == cache_key(**base) and len(k) == 64
    assert k != cache_key(**{**base, "model": "m2"})
    assert k != cache_key(**{**base, "decoding": {"temperature": 0.5}})
    assert k != cache_key(**{**base, "prompt": "p "})
    assert k != cache_key(**{**base, "images": [b"b"]})
    assert k != cache_key(**{**base, "images": [b"a", b"a"]})
    assert k != cache_key(**{**base, "schema": {"type": "object"}})
    assert cache_key(**{**base, "decoding": {"b": 1, "a": 2}}) == cache_key(
        **{**base, "decoding": {"a": 2, "b": 1}}
    )


# ---------------------------------------------------------------- cache


def test_cache_roundtrip(tmp_path: Path) -> None:
    cache = ResponseCache(tmp_path)
    r = Response(
        text="x",
        model_id="id",
        backend_model="bm",
        decoding=Decoding(),
        latency_s=0.5,
        request_hash="k" * 64,
    )
    assert cache.get("k" * 64) is None and ("k" * 64) not in cache and len(cache) == 0
    path = cache.put("k" * 64, r)
    assert path.is_file() and path.parent.name == "kk" and len(cache) == 1
    hit = cache.get("k" * 64)
    assert hit is not None and hit.cached and hit.text == "x" and hit.latency_s == 0.5


def test_cache_ignores_corrupt_entry(tmp_path: Path) -> None:
    cache = ResponseCache(tmp_path)
    p = cache.path("a" * 64)
    p.parent.mkdir(parents=True)
    p.write_text("{not json")
    assert cache.get("a" * 64) is None


# ---------------------------------------------------------------- generate


def test_generate_calls_backend_once_then_serves_cache(tmp_path: Path, png: Path) -> None:
    model = FakeVLM("fake", cache=ResponseCache(tmp_path))
    r1 = model.generate([png], "what?")
    r2 = model.generate([png], "what?")
    assert len(model.calls) == 1
    assert not r1.cached and r2.cached and r1.text == r2.text == "answer to: what?"
    assert r1.request_hash == r2.request_hash
    assert r1.usage.prompt_tokens == 10 and r1.finish_reason == "stop" and r1.extra == {"k": 1}
    assert r1.model_id == "fake" and r1.backend_model == "fake/model-1"
    assert r1.latency_s >= 0


def test_generate_without_cache_calls_every_time(tmp_path: Path, png: Path) -> None:
    model = FakeVLM("fake", cache=ResponseCache(tmp_path))
    model.generate([png], "q")
    model.generate([png], "q", use_cache=False)
    assert len(model.calls) == 2
    no_cache = FakeVLM("fake")
    no_cache.generate([png], "q")
    no_cache.generate([png], "q")
    assert len(no_cache.calls) == 2


def test_decoding_defaults_and_overrides(tmp_path: Path, png: Path) -> None:
    model = FakeVLM(
        "fake", decoding=Decoding(temperature=0.7, max_tokens=64), cache=ResponseCache(tmp_path)
    )
    r = model.generate([png], "q", max_tokens=32)
    assert r.decoding.temperature == 0.7 and r.decoding.max_tokens == 32
    again = model.generate([png], "q", max_tokens=32)
    assert again.cached
    other = model.generate([png], "q", temperature=0.0, max_tokens=32)
    assert not other.cached and len(model.calls) == 2
    with pytest.raises(ValidationError):
        model.generate([png], "q", beam_width=3)


def test_schema_and_images_are_part_of_the_key(tmp_path: Path, png: Path, jpg: Path) -> None:
    model = FakeVLM("fake", cache=ResponseCache(tmp_path))
    a = model.generate([png], "q")
    b = model.generate([png], "q", schema=Answer)
    c = model.generate([jpg], "q")
    d = model.generate([png, jpg], "q")
    assert len({a.request_hash, b.request_hash, c.request_hash, d.request_hash}) == 4
    assert len(model.calls) == 4
    assert model.calls[3][0][1].mime == "image/jpeg"


def test_transient_errors_are_retried_then_raised(png: Path) -> None:
    model = FakeVLM("fake", fail_first=2, max_retries=3)
    r = model.generate([png], "q")
    assert len(model.calls) == 3 and r.extra["retries"] == 2
    hopeless = FakeVLM("fake", fail_first=5, max_retries=2)
    with pytest.raises(TransientError):
        hopeless.generate([png], "q")
    assert len(hopeless.calls) == 3


def test_context_manager_closes() -> None:
    closed = []

    class Closing(FakeVLM):
        def close(self) -> None:
            closed.append(True)

    with Closing("fake") as m:
        assert m.model_id == "fake"
    assert closed == [True]


def test_response_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        Response(
            text="x",
            model_id="i",
            backend_model="b",
            decoding=Decoding(),
            latency_s=0,
            request_hash="h",
            bogus=1,
        )
