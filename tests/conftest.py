"""Shared pytest fixtures.

Tests must pass with no network, no GPU and no Snellius. The fixtures here keep the
settings environment clean so a developer's local ``.env`` never leaks into tests.
"""

from __future__ import annotations

import pytest

VSU_ENV_VARS = ("VSU_DATA_ROOT", "VSU_RESULTS_ROOT", "VSU_CACHE_ROOT", "HF_HOME")


@pytest.fixture
def clean_env(monkeypatch: pytest.MonkeyPatch) -> pytest.MonkeyPatch:
    """Remove every variable the settings read, then return the monkeypatch for overrides."""
    for name in VSU_ENV_VARS:
        monkeypatch.delenv(name, raising=False)
    return monkeypatch
