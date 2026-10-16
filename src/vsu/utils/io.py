"""Small file helpers: jsonl, json and yaml, with the conventions every stage shares."""

from __future__ import annotations

import json
import os
from collections.abc import Iterable, Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


def tmp_path(path: Path) -> Path:
    """A temporary sibling of ``path``, unique per process, for write-then-rename.

    Several jobs may write the same cached file at once; each writes its own temporary file
    and renames it into place, so none can remove or truncate another's.
    """
    path = Path(path)
    return path.with_name(f".{path.name}.{os.getpid()}.tmp")


def utc_timestamp() -> str:
    """``YYYYmmddTHHMMSSZ``: sortable, filesystem safe, used as run directory name."""
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def read_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    """Yield one dictionary per non-empty line. A missing file yields nothing."""
    path = Path(path)
    if not path.is_file():
        return
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    """Append one record and flush, so a killed job keeps every finished line."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")
        f.flush()


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    """Write all records, replacing the file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = tmp_path(path)
    with tmp.open("w") as f:
        for record in records:
            f.write(json.dumps(record, sort_keys=True) + "\n")
    tmp.replace(path)


def read_json(path: Path) -> Any:
    return json.loads(Path(path).read_text())


def write_json(path: Path, data: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = tmp_path(path)
    tmp.write_text(json.dumps(data, indent=1, sort_keys=True, default=str) + "\n")
    tmp.replace(path)


def read_yaml(path: Path) -> Any:
    return yaml.safe_load(Path(path).read_text())


def write_yaml(path: Path, data: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=True, default_flow_style=False))
