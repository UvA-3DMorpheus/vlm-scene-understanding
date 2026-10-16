"""Paths and environment configuration.

Every location the package reads or writes comes from here; nothing else in the
code base hardcodes a path. Values come from environment variables, or from a
``.env`` file in the working directory, and fall back to laptop friendly defaults
relative to the working directory. ``scripts/snellius/env.sh`` exports the
Snellius values.

Variables read:

- ``VSU_DATA_ROOT``: datasets (default ``./data``)
- ``VSU_RESULTS_ROOT``: run outputs (default ``./results/runs``)
- ``VSU_CACHE_ROOT``: model response cache (default ``./.cache``)
- ``HF_HOME``: Hugging Face cache, optional and passed through unchanged
- ``VSU_CONFIGS_ROOT``: yaml configs (default: the repository's ``configs/``)
"""

from __future__ import annotations

import os
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

#: The repository root when running from a checkout (src/vsu/settings.py -> three levels up).
REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Resolved absolute roots for data, results, cache and model weights.

    Construct with ``Settings()`` to read the environment and ``.env``, or pass
    keyword overrides (``Settings(data_root=...)``). Tests pass ``_env_file=None``
    to ignore any local ``.env``.
    """

    model_config = SettingsConfigDict(
        env_prefix="VSU_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    data_root: Path = Field(default=Path("data"), description="Datasets root.")
    results_root: Path = Field(default=Path("results/runs"), description="Run outputs root.")
    cache_root: Path = Field(default=Path(".cache"), description="Model response cache root.")
    hf_home: Path | None = Field(
        default=None,
        validation_alias="HF_HOME",
        description="Hugging Face cache directory; None means the Hugging Face default.",
    )
    configs_root: Path = Field(
        default=REPO_ROOT / "configs", description="Model and experiment yaml configs."
    )

    @field_validator("hf_home", mode="before")
    @classmethod
    def _empty_is_none(cls, value: object) -> object:
        """Treat an empty ``HF_HOME`` (as left in a copied .env.example) as unset."""
        return None if value in ("", None) else value

    @field_validator("data_root", "results_root", "cache_root", "hf_home", "configs_root")
    @classmethod
    def _absolute(cls, value: Path | None) -> Path | None:
        """Expand ``~`` and make the path absolute so run records are portable.

        Symlinks are kept (``/projects/...`` stays ``/projects/...`` on Snellius rather
        than becoming the physical ``/gpfs/work5/...`` path), so records stay readable.
        """
        return None if value is None else Path(os.path.abspath(Path(value).expanduser()))

    # Derived dataset locations (PLAN.md Section 2.1). Kept here so the layout is defined once.

    @property
    def sim_dir(self) -> Path:
        """Simulation team output, one folder per look: ``sim/preview``, ``sim/realistic``."""
        return self.data_root / "sim"

    def sim_collection_dir(self, collection: str) -> Path:
        """Scenes rendered with one look (``preview`` = MuJoCo, ``realistic`` = Blender)."""
        return self.sim_dir / collection

    @property
    def physion_pp_dir(self) -> Path:
        """Physion++ fallback set."""
        return self.data_root / "physion_pp"

    @property
    def smoke_dir(self) -> Path:
        """Tiny labelled image set used by tests and smoke runs."""
        return self.data_root / "smoke"

    @property
    def materials_dir(self) -> Path:
        """Directory holding ``material_table.yaml``."""
        return self.data_root / "materials"

    @property
    def annotations_dir(self) -> Path:
        """Hand boxes and synonym tables."""
        return self.data_root / "annotations"

    @property
    def model_configs_dir(self) -> Path:
        """One yaml per model."""
        return self.configs_root / "models"

    @property
    def experiment_configs_dir(self) -> Path:
        """One yaml per experiment."""
        return self.configs_root / "experiments"

    def resolved_roots(self) -> dict[str, str | None]:
        """Return the resolved roots as strings, for inclusion in a run's config record."""
        return {
            "VSU_DATA_ROOT": str(self.data_root),
            "VSU_RESULTS_ROOT": str(self.results_root),
            "VSU_CACHE_ROOT": str(self.cache_root),
            "HF_HOME": None if self.hf_home is None else str(self.hf_home),
            "VSU_CONFIGS_ROOT": str(self.configs_root),
        }


def get_settings(**overrides: object) -> Settings:
    """Build a :class:`Settings` from the environment, with optional keyword overrides.

    Not cached on purpose: callers that need one instance pass it around explicitly,
    and tests can change the environment between calls.
    """
    return Settings(**overrides)  # type: ignore[arg-type]
