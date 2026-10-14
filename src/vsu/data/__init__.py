"""Dataset access: scenes, frames, ground truth, materials and fallback loaders."""

from vsu.data.dataset import Scene, convert_ground_truth, discover_scenes, load_scene
from vsu.data.materials import MaterialTable, load_material_table, load_materials_json
from vsu.data.smoke import SmokeImage, load_smoke_set

__all__ = [
    "MaterialTable",
    "Scene",
    "SmokeImage",
    "convert_ground_truth",
    "discover_scenes",
    "load_material_table",
    "load_materials_json",
    "load_scene",
    "load_smoke_set",
]
