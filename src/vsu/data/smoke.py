"""The smoke set: a handful of labelled photos committed under ``data/smoke/``.

Consumes ``labels.csv`` (columns ``file, material, object, notes`` plus attribution) and
produces ``SmokeImage`` records. Used by tests and by Experiment 1 smoke runs; the
materials are keys of ``material_table.yaml``.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from vsu.settings import Settings, get_settings

LABELS_FILE = "labels.csv"


@dataclass(frozen=True)
class SmokeImage:
    """One labelled photo."""

    path: Path
    material: str
    object: str
    notes: str
    license: str
    source_url: str

    @property
    def image_id(self) -> str:
        return self.path.stem


def load_smoke_set(root: Path | None = None, *, settings: Settings | None = None) -> list[SmokeImage]:
    """Read the smoke set under ``root`` (default ``VSU_DATA_ROOT/smoke``), in csv order."""
    root = Path(root) if root is not None else (settings or get_settings()).smoke_dir
    labels = root / LABELS_FILE
    if not labels.is_file():
        raise FileNotFoundError(f"{labels} missing; the smoke set is versioned under data/smoke")
    images: list[SmokeImage] = []
    with labels.open(newline="") as f:
        for row in csv.DictReader(f):
            path = root / row["file"]
            if not path.is_file():
                raise FileNotFoundError(f"{labels} lists {row['file']} but it is missing")
            images.append(
                SmokeImage(
                    path=path,
                    material=row["material"],
                    object=row.get("object", ""),
                    notes=row.get("notes", ""),
                    license=row.get("license", ""),
                    source_url=row.get("source_url", ""),
                )
            )
    return images
