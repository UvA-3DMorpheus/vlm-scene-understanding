"""Model configs (``configs/models/<name>.yaml``) and the name to backend mapping.

A config names a backend and what it needs: the Hugging Face id and dtype for open
models, the API model name for closed ones, default decoding parameters and free
``options`` the backend understands. ``build_model(name)`` turns a config into a ready
``VLM`` with the response cache attached. Backend modules are imported lazily so that
listing configs or using the dummy never imports torch.
"""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

from vsu.models.base import VLM, Decoding
from vsu.models.cache import ResponseCache
from vsu.settings import Settings, get_settings

Backend = Literal["dummy", "hf", "openai", "gemini"]

#: backend name -> (module, class). Modules import their heavy dependencies on load.
BACKENDS: dict[str, tuple[str, str]] = {
    "dummy": ("vsu.models.dummy_backend", "DummyModel"),
    "hf": ("vsu.models.hf_backend", "HFModel"),
    "openai": ("vsu.models.openai_backend", "OpenAIModel"),
    "gemini": ("vsu.models.gemini_backend", "GeminiModel"),
}


class ModelConfig(BaseModel):
    """One model yaml, validated."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="Config name, the file stem; used as model_id everywhere.")
    backend: Backend
    hf_id: str | None = Field(default=None, description="Hugging Face repository (hf backend).")
    api_model: str | None = Field(default=None, description="Model name sent to an API backend.")
    dtype: str | None = Field(default=None, description="torch dtype name for open models.")
    decoding: Decoding = Field(default_factory=Decoding)
    options: dict[str, Any] = Field(default_factory=dict, description="Backend specific settings.")
    notes: str | None = None

    @model_validator(mode="after")
    def _backend_has_what_it_needs(self) -> ModelConfig:
        if self.backend == "hf" and not self.hf_id:
            raise ValueError(f"{self.name}: hf backend needs hf_id")
        if self.backend in ("openai", "gemini") and not self.api_model:
            raise ValueError(f"{self.name}: {self.backend} backend needs api_model")
        return self

    @property
    def backend_model(self) -> str:
        """The identifier the backend uses, for cache keys and records."""
        return self.hf_id or self.api_model or f"{self.backend}:{self.name}"


def list_models(settings: Settings | None = None) -> list[str]:
    """Config names available, sorted."""
    d = (settings or get_settings()).model_configs_dir
    return sorted(p.stem for p in d.glob("*.yaml")) if d.is_dir() else []


def load_model_config(name: str, settings: Settings | None = None) -> ModelConfig:
    """Read and validate ``configs/models/<name>.yaml``."""
    settings = settings or get_settings()
    path = settings.model_configs_dir / f"{name}.yaml"
    if not path.is_file():
        raise FileNotFoundError(f"no model config {path}; known: {list_models(settings)}")
    raw = yaml.safe_load(path.read_text()) or {}
    return ModelConfig(name=name, **raw)


def build_model(
    name: str | ModelConfig,
    *,
    settings: Settings | None = None,
    use_cache: bool = True,
    cache_root: Path | None = None,
) -> VLM:
    """Instantiate the backend of a config, with the disk cache attached unless disabled."""
    settings = settings or get_settings()
    config = name if isinstance(name, ModelConfig) else load_model_config(name, settings)
    module_name, class_name = BACKENDS[config.backend]
    cls = getattr(import_module(module_name), class_name)
    cache = ResponseCache(cache_root or settings.cache_root) if use_cache else None
    return cls(config, cache=cache, settings=settings)
