"""Material lookups: the simulation team's ``materials.json`` and our ranged material table.

``materials.json`` is a verbatim copy of the simulation team's file (its SHA-256 is
recorded in every scene's provenance, so the copy can be verified). It gives the point
values the simulator used. ``material_table.yaml`` is ours: typical ranges per material
with sources, used by the material first estimator of Experiment 2 and by the synonym
mapping of Experiment 1's open set variant.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from vsu.schemas.answers import normalize_label
from vsu.settings import Settings, get_settings

MATERIALS_JSON = "materials.json"
MATERIAL_TABLE = "material_table.yaml"

Range = tuple[float, float]


def _materials_dir(settings: Settings | None) -> Path:
    return (settings or get_settings()).materials_dir


def load_materials_json(path: Path | None = None, *, settings: Settings | None = None) -> dict[str, Any]:
    """The simulation team's materials file as a dictionary."""
    path = path or _materials_dir(settings) / MATERIALS_JSON
    return json.loads(Path(path).read_text())


def materials_json_sha256(path: Path | None = None, *, settings: Settings | None = None) -> str:
    """SHA-256 of the raw file, comparable with ``provenance.materials_json_sha256``."""
    path = path or _materials_dir(settings) / MATERIALS_JSON
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def contact_values(table: dict[str, Any], material: str, surface: str = "finished_wood") -> dict[str, Any]:
    """Friction and restitution the simulator uses for ``material`` on ``surface``."""
    return table["contacts"][surface][material]


@dataclass(frozen=True)
class MaterialRow:
    """Typical ranges for one material class, with the sources they come from."""

    key: str
    label: str
    aliases: tuple[str, ...]
    density_kg_m3: Range
    restitution: Range
    friction_static_on_wood: Range
    friction_kinetic_on_wood: Range
    friction_static_on_steel: Range
    friction_kinetic_on_steel: Range
    hardness: str
    notes: str
    sources: tuple[str, ...]

    def range_of(self, property_name: str) -> Range:
        """Range for ``density_kg_m3``, ``restitution``, ``friction`` (kinetic on wood) or a full name."""
        if property_name == "friction":
            property_name = "friction_kinetic_on_wood"
        return getattr(self, property_name)

    def midpoint(self, property_name: str) -> float:
        low, high = self.range_of(property_name)
        return 0.5 * (low + high)


@dataclass(frozen=True)
class MaterialTable:
    """The ranged table plus alias resolution."""

    version: int
    rows: dict[str, MaterialRow]
    sources: dict[str, str]

    def __getitem__(self, key: str) -> MaterialRow:
        return self.rows[key]

    def __contains__(self, key: str) -> bool:
        return key in self.rows

    @property
    def keys(self) -> list[str]:
        return list(self.rows)

    def resolve(self, label: str) -> str | None:
        """Map a free text label onto a table key through its aliases, or None.

        Exact key match first, then alias match, then the longest key or alias contained
        in the label (``"brushed stainless steel"`` resolves to ``metal``; ``"paperback
        book"`` resolves to ``book_paper_cover`` through ``paperback``, not to
        ``cardboard`` through ``paper``).
        """
        text = normalize_label(label)
        if text in self.rows:
            return text
        for key, row in self.rows.items():
            if text in row.aliases:
                return key
        best: tuple[int, str] | None = None
        for key, row in self.rows.items():
            for candidate in (key, *row.aliases):
                if candidate in text and (best is None or len(candidate) > best[0]):
                    best = (len(candidate), key)
        return None if best is None else best[1]


def _as_range(value: Any, where: str) -> Range:
    if not (isinstance(value, list | tuple) and len(value) == 2):
        raise ValueError(f"{where}: expected [low, high], got {value!r}")
    low, high = float(value[0]), float(value[1])
    if high < low:
        raise ValueError(f"{where}: high {high} below low {low}")
    return low, high


def load_material_table(path: Path | None = None, *, settings: Settings | None = None) -> MaterialTable:
    """Parse ``material_table.yaml`` and validate every range."""
    path = path or _materials_dir(settings) / MATERIAL_TABLE
    raw = yaml.safe_load(Path(path).read_text())
    sources = dict(raw.get("sources") or {})
    rows: dict[str, MaterialRow] = {}
    for key, entry in raw["materials"].items():
        where = f"material_table[{key}]"
        unknown = set(entry.get("sources", [])) - set(sources)
        if unknown:
            raise ValueError(f"{where}: unknown sources {sorted(unknown)}")
        rows[key] = MaterialRow(
            key=key,
            label=entry["label"],
            aliases=tuple(normalize_label(a) for a in entry.get("aliases", [])),
            density_kg_m3=_as_range(entry["density_kg_m3"], where),
            restitution=_as_range(entry["restitution"], where),
            friction_static_on_wood=_as_range(entry["friction_static_on_wood"], where),
            friction_kinetic_on_wood=_as_range(entry["friction_kinetic_on_wood"], where),
            friction_static_on_steel=_as_range(entry["friction_static_on_steel"], where),
            friction_kinetic_on_steel=_as_range(entry["friction_kinetic_on_steel"], where),
            hardness=str(entry.get("hardness", "")),
            notes=str(entry.get("notes", "")),
            sources=tuple(entry.get("sources", [])),
        )
    return MaterialTable(version=int(raw.get("version", 1)), rows=rows, sources=sources)
