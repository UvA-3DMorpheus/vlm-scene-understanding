"""The one interface every vision language model is called through.

``VLM.generate(images, prompt, schema=None, **decoding)`` is the only entry point the
experiments use. It normalizes the images, merges decoding parameters with the model's
defaults, consults the disk cache, retries transient backend errors, logs one line per
call and returns a ``Response``. Backends implement ``_generate`` only, so caching,
retries, token counting and logging are uniform across closed and open models.
"""

from __future__ import annotations

import io
import logging
import mimetypes
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image
from pydantic import BaseModel, ConfigDict, Field

from vsu.models.cache import ResponseCache, cache_key

log = logging.getLogger(__name__)


class Decoding(BaseModel):
    """Decoding parameters. Every one of them is part of the cache key and the run record."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    temperature: float = Field(default=0.0, ge=0)
    max_tokens: int = Field(default=1024, gt=0)
    top_p: float = Field(default=1.0, gt=0, le=1)
    seed: int | None = Field(default=0, description="Sampling seed; irrelevant at temperature 0.")

    def merged(self, **overrides: Any) -> Decoding:
        """A copy with ``overrides`` applied; unknown names raise."""
        return Decoding(**{**self.model_dump(), **overrides})


class Usage(BaseModel):
    """Token counts as the backend reports them; ``None`` when unavailable."""

    prompt_tokens: int | None = None
    completion_tokens: int | None = None


class Response(BaseModel):
    """What a model call returns, as stored in the cache and in ``raw.jsonl``."""

    model_config = ConfigDict(extra="forbid")

    text: str
    model_id: str = Field(description="Config name of the model that answered.")
    backend_model: str = Field(description="The actual model identifier the backend used.")
    decoding: Decoding
    latency_s: float = Field(ge=0)
    cached: bool = False
    usage: Usage = Field(default_factory=Usage)
    finish_reason: str | None = None
    request_hash: str = Field(description="Cache key of the request.")
    extra: dict[str, Any] = Field(
        default_factory=dict, description="Backend specific, JSON serializable details."
    )


@dataclass(frozen=True)
class ImageData:
    """An image as bytes plus its media type, the form every backend consumes."""

    data: bytes
    mime: str

    @property
    def pil(self) -> Image.Image:
        return Image.open(io.BytesIO(self.data)).convert("RGB")


def to_image_data(image: object) -> ImageData:
    """Normalize any supported image input to ``ImageData``.

    Paths are read as they are on disk, so the cache key follows the file bytes. PIL
    images and raw bytes without a known type are encoded as PNG.
    """
    if isinstance(image, ImageData):
        return image
    if isinstance(image, str | Path):
        path = Path(image)
        mime = mimetypes.guess_type(path.name)[0]
        if mime not in ("image/jpeg", "image/png", "image/webp"):
            with Image.open(path) as im:
                return _encode_png(im)
        return ImageData(path.read_bytes(), mime)
    if isinstance(image, bytes):
        with Image.open(io.BytesIO(image)) as im:
            fmt = (im.format or "").lower()
            if fmt in ("jpeg", "png", "webp"):
                return ImageData(image, f"image/{fmt}")
            return _encode_png(im)
    if isinstance(image, Image.Image):
        return _encode_png(image)
    raise TypeError(f"unsupported image input {type(image).__name__}")


def _encode_png(im: Image.Image) -> ImageData:
    buf = io.BytesIO()
    im.convert("RGB").save(buf, format="PNG", optimize=False)
    return ImageData(buf.getvalue(), "image/png")


class TransientError(RuntimeError):
    """A backend failure worth retrying: rate limit, timeout, temporary server error."""


class VLM(ABC):
    """Base class of every backend. Subclasses implement ``_generate`` and ``backend_model``.

    ``model_id`` is the config name (``qwen3vl-8b``), ``backend_model`` the identifier the
    backend loads or calls (``Qwen/Qwen3-VL-8B-Instruct``).
    """

    backend: str = "abstract"

    def __init__(
        self,
        model_id: str,
        *,
        decoding: Decoding | None = None,
        cache: ResponseCache | None = None,
        max_retries: int = 3,
        retry_wait_s: float = 2.0,
    ) -> None:
        self.model_id = model_id
        self.default_decoding = decoding or Decoding()
        self.cache = cache
        self.max_retries = max_retries
        self.retry_wait_s = retry_wait_s

    @property
    @abstractmethod
    def backend_model(self) -> str:
        """The identifier the backend actually uses."""

    @property
    def cache_identity(self) -> str:
        """What identifies this model in cache keys. Backends whose outputs depend on
        settings beyond the model id (dtype, image resolution) append them here."""
        return self.backend_model

    @abstractmethod
    def _generate(
        self,
        images: list[ImageData],
        prompt: str,
        schema: type[BaseModel] | None,
        decoding: Decoding,
    ) -> tuple[str, Usage, str | None, dict[str, Any]]:
        """Run one request. Returns (text, usage, finish_reason, extra). Raise
        ``TransientError`` for failures that a retry may fix."""

    def generate(
        self,
        images: list[object],
        prompt: str,
        schema: type[BaseModel] | None = None,
        *,
        use_cache: bool = True,
        **decoding: Any,
    ) -> Response:
        """Answer ``prompt`` about ``images``.

        Consumes image paths, PIL images or bytes, the prompt text, an optional answer
        schema (passed to backends that support constrained output, and part of the cache
        key) and decoding overrides. Produces a ``Response``; identical requests return
        the cached one unless ``use_cache`` is false.
        """
        params = self.default_decoding.merged(**decoding)
        image_data = [to_image_data(im) for im in images]
        key = cache_key(
            model=self.cache_identity,
            decoding=params.model_dump(),
            prompt=prompt,
            images=[im.data for im in image_data],
            schema=schema.model_json_schema() if schema is not None else None,
        )
        if use_cache and self.cache is not None:
            hit = self.cache.get(key)
            if hit is not None:
                log.info("%s cached %s", self.model_id, key[:12])
                return hit
        text, usage, finish_reason, extra = self._call_with_retries(
            image_data, prompt, schema, params
        )
        response = Response(
            text=text,
            model_id=self.model_id,
            backend_model=self.backend_model,
            decoding=params,
            latency_s=extra.pop("_latency_s"),
            cached=False,
            usage=usage,
            finish_reason=finish_reason,
            request_hash=key,
            extra=extra,
        )
        log.info(
            "%s %.2fs tokens=%s/%s %s",
            self.model_id,
            response.latency_s,
            usage.prompt_tokens,
            usage.completion_tokens,
            key[:12],
        )
        if self.cache is not None:
            self.cache.put(key, response)
        return response

    def _call_with_retries(
        self,
        images: list[ImageData],
        prompt: str,
        schema: type[BaseModel] | None,
        params: Decoding,
    ) -> tuple[str, Usage, str | None, dict[str, Any]]:
        self.prepare()
        attempt = 0
        while True:
            start = time.perf_counter()
            try:
                text, usage, finish_reason, extra = self._generate(images, prompt, schema, params)
            except TransientError as exc:
                attempt += 1
                if attempt > self.max_retries:
                    raise
                wait = self.retry_wait_s * 2 ** (attempt - 1)
                log.warning(
                    "%s transient error (%s), retry %d in %.0fs", self.model_id, exc, attempt, wait
                )
                time.sleep(wait)
                continue
            extra = dict(extra)
            extra["_latency_s"] = time.perf_counter() - start
            if attempt:
                extra["retries"] = attempt
            return text, usage, finish_reason, extra

    def prepare(self) -> None:
        """Load weights or open sessions before the first timed call. Backends override."""
        return None

    def close(self) -> None:
        """Release resources (GPU memory, HTTP sessions). Backends override as needed."""
        return None

    def __enter__(self) -> VLM:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
