"""Fixed seeds for every random choice (pair sampling, frame sampling, dummy answers)."""

from __future__ import annotations

import random

import numpy as np


def seed_everything(seed: int) -> None:
    """Seed Python, numpy and torch (if installed)."""
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch

        torch.manual_seed(seed)
    except ImportError:
        pass


def rng(seed: int, *salt: str) -> random.Random:
    """An independent generator derived from ``seed`` and a few labels, for reproducible
    sampling that does not depend on call order elsewhere."""
    import hashlib

    h = hashlib.sha256(f"{seed}|{'|'.join(salt)}".encode()).digest()
    return random.Random(int.from_bytes(h[:8], "big"))
