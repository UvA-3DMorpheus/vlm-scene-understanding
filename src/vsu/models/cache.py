"""Disk cache for model responses under ``VSU_CACHE_ROOT/responses``.

The key is a SHA-256 over the backend model identifier, the decoding parameters, the
prompt text, the image bytes and the answer schema. Same request, same key, so a rerun
at temperature 0 reproduces ``raw.jsonl`` byte for byte without calling the model again.
Entries are JSON files, one per response, under a two character prefix directory to keep
directories small.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from vsu.utils.io import tmp_path

if TYPE_CHECKING:
    from vsu.models.base import Response

KEY_VERSION = "v1"


def cache_key(
    *,
    model: str,
    decoding: dict[str, Any],
    prompt: str,
    images: list[bytes],
    schema: dict[str, Any] | None,
) -> str:
    """Deterministic key for one request. Any change to any input changes the key."""
    h = hashlib.sha256()
    h.update(KEY_VERSION.encode())
    h.update(b"\0model\0" + model.encode())
    h.update(b"\0decoding\0" + json.dumps(decoding, sort_keys=True, default=str).encode())
    h.update(b"\0prompt\0" + prompt.encode())
    h.update(b"\0schema\0" + (json.dumps(schema, sort_keys=True).encode() if schema else b""))
    for data in images:
        h.update(b"\0image\0" + hashlib.sha256(data).digest())
    return h.hexdigest()


class ResponseCache:
    """Read and write ``Response`` records by key."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root) / "responses"

    def path(self, key: str) -> Path:
        return self.root / key[:2] / f"{key}.json"

    def get(self, key: str) -> Response | None:
        """The cached response marked ``cached=True``, or None."""
        from vsu.models.base import Response

        path = self.path(key)
        if not path.is_file():
            return None
        try:
            data = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            return None
        data["cached"] = True
        return Response.model_validate(data)

    def put(self, key: str, response: Response) -> Path:
        """Write a response atomically (temp file then rename)."""
        path = self.path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = tmp_path(path)
        tmp.write_text(json.dumps(response.model_dump(mode="json"), indent=1, sort_keys=True))
        tmp.replace(path)
        return path

    def __contains__(self, key: str) -> bool:
        return self.path(key).is_file()

    def __len__(self) -> int:
        return sum(1 for _ in self.root.glob("*/*.json")) if self.root.is_dir() else 0
