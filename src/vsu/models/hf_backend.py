"""Hugging Face transformers backend for open models (Qwen3-VL, InternVL3.5).

Loads any image-text-to-text model through ``AutoModelForImageTextToText`` and its
``AutoProcessor``, builds a chat message with the images and the prompt, and decodes the
newly generated tokens. The model is loaded on first use and freed by ``close``, so an
experiment job loads it once and loops variants inside. The ``schema`` argument is not
used for constrained decoding here; the prompt template describes the JSON shape.

Config ``options`` understood: ``attn_implementation`` (sdpa, eager, flash_attention_2),
``max_pixels`` and ``min_pixels`` (Qwen image processors), ``device_map`` (default auto,
which also spreads a model over every GPU of the job), ``trust_remote_code`` (default
false), ``chat_template_kwargs`` (extra variables for the chat template, for example
``enable_thinking: false`` for models that reason by default). FP8 checkpoints in the
compressed-tensors format load as they are; they need a Hopper GPU (gpu_h100).
"""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from typing import Any

from pydantic import BaseModel

from vsu.models.base import VLM, Decoding, ImageData, TransientError, Usage
from vsu.models.cache import ResponseCache
from vsu.models.registry import ModelConfig
from vsu.settings import Settings

log = logging.getLogger(__name__)

Loader = Callable[[], tuple[Any, Any]]


def load_transformers_model(config: ModelConfig, settings: Settings | None) -> tuple[Any, Any]:
    """Load (model, processor) for ``config`` with transformers; imports torch here only."""
    import torch
    from transformers import AutoModelForImageTextToText, AutoProcessor

    opts = dict(config.options)
    dtype = getattr(torch, config.dtype or "bfloat16")
    trust = bool(opts.pop("trust_remote_code", False))
    processor_kwargs: dict[str, Any] = {}
    for key in ("min_pixels", "max_pixels"):
        if key in opts:
            processor_kwargs[key] = opts.pop(key)
    model_kwargs: dict[str, Any] = {
        "dtype": dtype,
        "device_map": opts.pop("device_map", "auto"),
        "trust_remote_code": trust,
    }
    if "attn_implementation" in opts:
        model_kwargs["attn_implementation"] = opts.pop("attn_implementation")
    opts.pop("chat_template_kwargs", None)  # used at generation time, not at load time
    if opts:
        log.warning("%s: unused options %s", config.name, sorted(opts))
    log.info("loading %s (%s, %s)", config.hf_id, config.dtype, model_kwargs["device_map"])
    processor = AutoProcessor.from_pretrained(
        config.hf_id, trust_remote_code=trust, **processor_kwargs
    )
    model = AutoModelForImageTextToText.from_pretrained(config.hf_id, **model_kwargs)
    model.eval()
    return model, processor


def build_messages(images: list[ImageData], prompt: str) -> list[dict[str, Any]]:
    """One user turn: every image first, then the prompt text (chat template format)."""
    content: list[dict[str, Any]] = [{"type": "image", "image": im.pil} for im in images]
    content.append({"type": "text", "text": prompt})
    return [{"role": "user", "content": content}]


def generation_kwargs(decoding: Decoding) -> dict[str, Any]:
    """Map our decoding parameters onto ``model.generate`` arguments."""
    kwargs: dict[str, Any] = {"max_new_tokens": decoding.max_tokens}
    if decoding.temperature > 0:
        kwargs.update(do_sample=True, temperature=decoding.temperature, top_p=decoding.top_p)
    else:
        kwargs.update(do_sample=False)
    return kwargs


class HFModel(VLM):
    """Open models through transformers. See the module docstring for the options."""

    backend = "hf"

    def __init__(
        self,
        config: ModelConfig,
        *,
        cache: ResponseCache | None = None,
        settings: Settings | None = None,
        decoding: Decoding | None = None,
        loader: Loader | None = None,
    ) -> None:
        super().__init__(config.name, decoding=decoding or config.decoding, cache=cache)
        self.config = config
        self.settings = settings
        self._loader: Loader = loader or (lambda: load_transformers_model(config, settings))
        self._model: Any = None
        self._processor: Any = None

    @property
    def backend_model(self) -> str:
        return self.config.backend_model

    @property
    def cache_identity(self) -> str:
        """Model id plus dtype and options: a different pixel budget is a different model."""
        opts = json.dumps(self.config.options, sort_keys=True)
        return f"{self.backend_model}|dtype={self.config.dtype}|options={opts}"

    @property
    def loaded(self) -> bool:
        return self._model is not None

    def prepare(self) -> None:
        """Load the model now, so latency measurements exclude the load."""
        self._ensure_loaded()

    def _ensure_loaded(self) -> tuple[Any, Any]:
        if self._model is None:
            self._model, self._processor = self._loader()
        return self._model, self._processor

    def _generate(
        self,
        images: list[ImageData],
        prompt: str,
        schema: type[BaseModel] | None,
        decoding: Decoding,
    ) -> tuple[str, Usage, str | None, dict[str, Any]]:
        import torch

        model, processor = self._ensure_loaded()
        messages = build_messages(images, prompt)
        inputs = processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
            **dict(self.config.options.get("chat_template_kwargs") or {}),
        )
        inputs = inputs.to(model.device)
        prompt_len = int(inputs["input_ids"].shape[1])
        kwargs = generation_kwargs(decoding)
        if kwargs.get("do_sample") and decoding.seed is not None:
            torch.manual_seed(decoding.seed)
        try:
            with torch.inference_mode():
                output = model.generate(**inputs, **kwargs)
        except torch.cuda.OutOfMemoryError as exc:  # pragma: no cover - GPU only
            torch.cuda.empty_cache()
            raise TransientError(f"CUDA out of memory: {exc}") from exc
        new_tokens = output[0, prompt_len:]
        text = processor.batch_decode([new_tokens], skip_special_tokens=True)[0]
        completion = int(new_tokens.shape[0])
        finish = "length" if completion >= decoding.max_tokens else "stop"
        extra = {
            "device": str(model.device),
            "dtype": str(getattr(model, "dtype", "")),
            "image_sizes": [im.pil.size for im in images],
        }
        return (
            text.strip(),
            Usage(prompt_tokens=prompt_len, completion_tokens=completion),
            finish,
            extra,
        )

    def close(self) -> None:
        """Free the model and the GPU memory it held."""
        if self._model is None:
            return
        self._model = None
        self._processor = None
        try:
            import gc

            import torch

            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except ImportError:  # pragma: no cover
            pass
