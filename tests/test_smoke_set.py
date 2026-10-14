"""The versioned smoke set is complete, small and labelled with known materials."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from vsu.data.materials import load_material_table
from vsu.data.smoke import load_smoke_set
from vsu.settings import Settings

REPO_DATA = Path(__file__).resolve().parents[1] / "data"


def test_smoke_set_loads_and_is_labelled_with_table_keys() -> None:
    settings = Settings(data_root=REPO_DATA, _env_file=None)
    images = load_smoke_set(settings=settings)
    table = load_material_table(settings=settings)
    assert 8 <= len(images) < 20
    assert len({i.image_id for i in images}) == len(images)
    for img in images:
        assert img.material in table, img.material
        assert img.license and img.source_url.startswith("https://commons.wikimedia.org/")
        with Image.open(img.path) as im:
            assert max(im.size) <= 800 and im.mode == "RGB"
        assert img.path.stat().st_size < 400_000
    assert len({i.material for i in images}) >= 8
