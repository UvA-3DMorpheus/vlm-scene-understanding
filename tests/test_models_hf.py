"""The transformers backend, exercised with a fake model and processor (no torch weights)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from PIL import Image

torch = pytest.importorskip("torch")

from vsu.models.base import Decoding, ImageData  # noqa: E402
from vsu.models.hf_backend import HFModel, build_messages, generation_kwargs  # noqa: E402
from vsu.models.registry import ModelConfig  # noqa: E402


class FakeInputs(dict):
    def to(self, device: Any) -> FakeInputs:
        self["device"] = device
        return self


class FakeProcessor:
    def __init__(self) -> None:
        self.calls: list[Any] = []

    def apply_chat_template(self, messages, **kwargs):  # type: ignore[no-untyped-def]
        self.calls.append((messages, kwargs))
        n_images = sum(1 for part in messages[0]["content"] if part["type"] == "image")
        return FakeInputs(input_ids=torch.zeros((1, 5 + 10 * n_images), dtype=torch.long))

    def batch_decode(self, tokens, skip_special_tokens=True):  # type: ignore[no-untyped-def]
        return ["".join(chr(65 + int(t)) for t in tokens[0]) + "  "]


class FakeModel:
    device = "cpu"
    dtype = "float32"

    def __init__(self, reply_len: int = 3) -> None:
        self.reply_len = reply_len
        self.generate_kwargs: dict[str, Any] = {}

    def generate(self, **kwargs):  # type: ignore[no-untyped-def]
        self.generate_kwargs = kwargs
        n = min(self.reply_len, kwargs["max_new_tokens"])
        reply = torch.arange(n, dtype=torch.long)
        return torch.cat([kwargs["input_ids"][0], reply]).unsqueeze(0)


@pytest.fixture
def image(tmp_path: Path) -> Path:
    p = tmp_path / "a.png"
    Image.new("RGB", (10, 6), (1, 2, 3)).save(p)
    return p


def make_model(reply_len: int = 3, **options: Any) -> tuple[HFModel, FakeModel, FakeProcessor]:
    fake_model, fake_proc = FakeModel(reply_len), FakeProcessor()
    cfg = ModelConfig(name="fake-hf", backend="hf", hf_id="org/model", options=options)
    model = HFModel(cfg, loader=lambda: (fake_model, fake_proc))
    return model, fake_model, fake_proc


def test_messages_put_images_before_text(image: Path) -> None:
    msgs = build_messages([], "hello")
    assert msgs == [{"role": "user", "content": [{"type": "text", "text": "hello"}]}]
    data = ImageData(image.read_bytes(), "image/png")
    content = build_messages([data, data], "hi")[0]["content"]
    assert [p["type"] for p in content] == ["image", "image", "text"]
    assert content[0]["image"].size == (10, 6)


def test_generation_kwargs_follow_temperature() -> None:
    assert generation_kwargs(Decoding(temperature=0.0, max_tokens=7)) == {
        "max_new_tokens": 7,
        "do_sample": False,
    }
    sampled = generation_kwargs(Decoding(temperature=0.7, top_p=0.9, max_tokens=7))
    assert sampled["do_sample"] and sampled["temperature"] == 0.7 and sampled["top_p"] == 0.9


def test_lazy_load_generate_and_close(image: Path) -> None:
    model, fake_model, fake_proc = make_model()
    assert not model.loaded
    model.prepare()
    assert model.loaded
    r = model.generate([image, image], "what?")
    messages, kwargs = fake_proc.calls[0]
    content = messages[0]["content"]
    assert [p["type"] for p in content] == ["image", "image", "text"]
    assert content[0]["image"].size == (10, 6) and content[2]["text"] == "what?"
    assert kwargs["add_generation_prompt"] and kwargs["return_tensors"] == "pt"
    assert r.text == "ABC" and r.usage.prompt_tokens == 25 and r.usage.completion_tokens == 3
    assert r.finish_reason == "stop" and r.extra["image_sizes"] == [(10, 6), (10, 6)]
    assert fake_model.generate_kwargs["do_sample"] is False
    model.close()
    assert not model.loaded


def test_finish_reason_length_when_budget_exhausted(image: Path) -> None:
    model, _, _ = make_model(reply_len=100)
    r = model.generate([image], "q", max_tokens=4)
    assert r.usage.completion_tokens == 4 and r.finish_reason == "length" and r.text == "ABCD"


def test_sampling_seeds_torch(image: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    seeds: list[int] = []
    monkeypatch.setattr(torch, "manual_seed", lambda s: seeds.append(s))
    model, fake_model, _ = make_model()
    model.generate([image], "q", temperature=0.5, seed=123)
    assert seeds == [123] and fake_model.generate_kwargs["temperature"] == 0.5


def test_loader_receives_config_options() -> None:
    model, _, _ = make_model(max_pixels=1000, attn_implementation="sdpa")
    assert model.config.options == {"max_pixels": 1000, "attn_implementation": "sdpa"}
    assert model.backend_model == "org/model"


def test_cache_identity_includes_dtype_and_options(image: Path) -> None:
    a, _, _ = make_model(max_pixels=1000)
    b, _, _ = make_model(max_pixels=2000)
    assert a.backend_model == b.backend_model
    assert a.cache_identity != b.cache_identity
    assert a.generate([image], "q").request_hash != b.generate([image], "q").request_hash
