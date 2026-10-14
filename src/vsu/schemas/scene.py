"""Internal scene representation: ``GroundTruth`` and ``SceneConfig``.

``GroundTruth`` mirrors the simulation team's ``ground_truth.json`` (schema 2.0 of the
3D-Simulations repository) field for field, so the two teams speak one language. The one
deliberate difference is ``objects``: their scenes hold a single ``object``; we keep a list
that currently has one entry, so a future two-object scene needs no rewrite. Conversion
from their files lives in ``vsu.data.dataset``; nothing else reads their format.

``SceneConfig`` is the structured output of Experiment 4: the subset of the ground truth a
vision language model can fill from a first frame, which the simulator then runs.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Vec3 = Annotated[list[float], Field(min_length=3, max_length=3)]
Quat = Annotated[list[float], Field(min_length=4, max_length=4)]

Phenomenon = Literal["free_fall", "projectile", "rolling", "sliding", "bouncing"]
Shape = Literal["sphere", "box", "mesh"]
TrajectoryMode = Literal["simulated", "analytic"]
GeometrySource = Literal["vlm", "ground_truth", "reconstruction"]

#: Scenario ids written by the simulation pipeline, mapped onto our phenomenon names.
SCENARIO_TO_PHENOMENON: dict[str, Phenomenon] = {
    "free_fall_no_contact": "free_fall",
    "projectile_no_contact": "projectile",
    "rolling_without_slipping": "rolling",
    "sliding_with_friction": "sliding",
}

#: Object material classes in the simulation team's materials.json (its ``materials`` keys).
MATERIAL_CLASSES: tuple[str, ...] = ("ceramic", "metal", "plastic", "cardboard", "book_paper_cover")

#: Camera names every scene is rendered from; ``front`` is the Morpheus style level side view.
CAMERA_NAMES: tuple[str, ...] = ("front", "left", "right", "high", "low")

GRAVITY_DEFAULT: list[float] = [0.0, 0.0, -9.81]


class SceneObject(BaseModel):
    """One rigid object in a scene, as the simulation team describes it.

    Field names follow ``ground_truth.json`` ``object``. Fields that do not apply to a
    shape are ``None`` (a sphere has ``radius_m`` and no ``size_m``).
    """

    model_config = ConfigDict(extra="ignore")

    id: str = Field(description="Unique id inside the scene; the simulator geom name.")
    name: str
    key: str | None = Field(default=None, description="Short library key (tray, book, ...).")
    shape: Shape
    material_class: str | None = Field(
        default=None, description="Key in materials.json, None for unlabelled primitives."
    )
    radius_m: float | None = Field(default=None, gt=0)
    size_m: Vec3 | None = Field(default=None, description="Box edge lengths (x, y, z).")
    bbox_body_frame_m: Vec3 | None = None
    volume_m3: float | None = Field(default=None, gt=0)
    density_kg_m3: float | None = Field(default=None, gt=0)
    density_basis: str | None = None
    mass_kg: float | None = Field(default=None, gt=0)
    segmentation_geom_id: int | None = Field(
        default=None, description="Pixel value of this object in <camera>/seg.npz."
    )
    dataset: str | None = None
    license: str | None = None
    attribution: str | None = None


class Surface(BaseModel):
    """The surface the object rests on. All fields are ``None`` for free flight scenes."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = Field(default=None, description="Surface key in materials.json.")
    label: str | None = None
    density_kg_m3: float | None = None
    ramp_angle_deg: float | None = Field(default=None, ge=0, lt=90)
    ramp_azimuth_deg: float | None = None
    ramp_width_m: float | None = None
    ramp_normal: Vec3 | None = None
    ramp_downhill_direction: Vec3 | None = None
    ramp_top_edge_centre_m: Vec3 | None = None
    ramp_bottom_edge_centre_m: Vec3 | None = None


class Contact(BaseModel):
    """Contact parameters of the object-surface pair used by the simulation."""

    model_config = ConfigDict(extra="ignore")

    object_material: str | None = None
    surface: str | None = None
    model: str | None = Field(default=None, description="Contact model in words.")
    mu_kinetic: float | None = Field(default=None, ge=0)
    mu_static: float | None = Field(default=None, ge=0)
    restitution: float | None = Field(default=None, ge=0, le=1)
    source: str | None = None


class Expected(BaseModel):
    """The closed form motion the trajectory follows."""

    model_config = ConfigDict(extra="ignore")

    description: str | None = None
    formula: str | None = None
    acceleration_world_mps2: Vec3 | None = None
    acceleration_magnitude_mps2: float | None = None


class FrameState(BaseModel):
    """Rigid body state of the object at one video frame (world frame, SI units)."""

    model_config = ConfigDict(extra="ignore")

    t: float = Field(ge=0)
    com_position: Vec3
    com_velocity: Vec3
    quaternion: Quat | None = Field(default=None, description="w, x, y, z; body to world.")
    angular_velocity: Vec3 | None = None


class Provenance(BaseModel):
    """How the scene was produced; copied from the simulation team's record."""

    model_config = ConfigDict(extra="ignore")

    git_commit: str | None = None
    git_uncommitted_changes: bool | None = None
    materials_json_version: str | None = None
    materials_json_sha256: str | None = None
    renderer: str | None = Field(default=None, description="mujoco or blender.")
    renderer_version: str | None = None
    simulator_version: str | None = None
    look: str | None = Field(
        default=None, description="Blender look (placeholder, realistic); None for MuJoCo."
    )


class Camera(BaseModel):
    """Pinhole camera a scene was rendered from (MuJoCo/OpenGL convention: looks along -z, y up)."""

    model_config = ConfigDict(extra="ignore")

    name: str
    K: Annotated[list[Vec3], Field(min_length=3, max_length=3)] = Field(
        description="3x3 intrinsics in pixels, principal point at the image centre."
    )
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    position: Vec3
    rotation_cam_to_world: Annotated[list[Vec3], Field(min_length=3, max_length=3)]


class GroundTruth(BaseModel):
    """Everything we know about a simulated scene, independent of how it was stored."""

    model_config = ConfigDict(extra="ignore")

    scene_id: str
    schema_version: str
    scenario: str = Field(description="Scenario id as written by the simulation pipeline.")
    phenomenon: Phenomenon
    trajectory_mode: TrajectoryMode
    fps: float = Field(gt=0)
    physics_timestep: float | None = Field(default=None, gt=0)
    gravity: Vec3 = Field(default_factory=lambda: list(GRAVITY_DEFAULT))
    objects: list[SceneObject] = Field(min_length=1)
    surface: Surface | None = None
    contact: Contact | None = None
    expected: Expected | None = None
    initial_position: Vec3
    initial_velocity: Vec3
    params: dict[str, Any] | None = None
    frames: list[FrameState] = Field(min_length=1)
    provenance: Provenance | None = None
    cameras: list[str] = Field(default_factory=list, description="Camera names rendered.")
    checks_pass: bool | None = Field(
        default=None, description="Result of the pipeline's automatic checks, if present."
    )

    @model_validator(mode="after")
    def _unique_object_ids(self) -> GroundTruth:
        ids = [o.id for o in self.objects]
        if len(ids) != len(set(ids)):
            raise ValueError(f"duplicate object ids: {ids}")
        return self

    @model_validator(mode="after")
    def _frames_in_time_order(self) -> GroundTruth:
        times = [f.t for f in self.frames]
        if any(b <= a for a, b in zip(times, times[1:], strict=False)):
            raise ValueError("frame times must increase strictly")
        return self

    @property
    def obj(self) -> SceneObject:
        """The tracked object. Scenes currently have exactly one."""
        return self.objects[0]

    @property
    def num_frames(self) -> int:
        return len(self.frames)

    @property
    def duration_s(self) -> float:
        """Time of the last frame."""
        return self.frames[-1].t

    def positions(self) -> list[Vec3]:
        """Centre of mass position per frame, in frame order."""
        return [f.com_position for f in self.frames]


class ObjectConfig(BaseModel):
    """One object as a vision language model (or an injected ground truth) describes it."""

    model_config = ConfigDict(extra="ignore")

    name: str
    shape: Shape
    material_class: str | None = None
    radius_m: float | None = Field(default=None, gt=0)
    size_m: Vec3 | None = None
    mass_kg: float | None = Field(default=None, gt=0)
    density_kg_m3: float | None = Field(default=None, gt=0)
    restitution: float | None = Field(default=None, ge=0, le=1)
    friction: float | None = Field(default=None, ge=0, description="Kinetic friction coefficient.")
    initial_position_m: Vec3 | None = None
    initial_velocity_m_s: Vec3 | None = None
    geometry_source: GeometrySource = Field(
        default="vlm", description="Where position and size came from (Experiment 4 conditions)."
    )

    @model_validator(mode="after")
    def _shape_has_dimensions(self) -> ObjectConfig:
        if self.shape == "sphere" and self.radius_m is None and self.size_m is not None:
            self.radius_m = max(self.size_m) / 2
        if self.shape == "box" and self.size_m is None and self.radius_m is not None:
            self.size_m = [2 * self.radius_m] * 3
        return self


class SurfaceConfig(BaseModel):
    """The resting surface as the model describes it."""

    model_config = ConfigDict(extra="ignore")

    material: str | None = None
    ramp_angle_deg: float | None = Field(default=None, ge=0, lt=90)
    friction: float | None = Field(default=None, ge=0, description="Kinetic friction coefficient.")
    restitution: float | None = Field(default=None, ge=0, le=1)


class SceneConfig(BaseModel):
    """Structured scene description that initializes a simulator (Experiment 4 output)."""

    model_config = ConfigDict(extra="ignore")

    phenomenon: Phenomenon
    objects: list[ObjectConfig] = Field(min_length=1)
    surface: SurfaceConfig | None = None
    gravity: Vec3 = Field(default_factory=lambda: list(GRAVITY_DEFAULT))
    fps: float | None = Field(default=None, gt=0)
    duration_s: float | None = Field(default=None, gt=0)

    @classmethod
    def from_ground_truth(cls, gt: GroundTruth) -> SceneConfig:
        """Build the config a perfect model would write for ``gt``.

        Used to inject ground truth geometry (Experiment 4 condition C2), to generate
        synthetic test cases, and as the reference the scoring compares against.
        """
        contact = gt.contact or Contact()
        objects = [
            ObjectConfig(
                name=o.name,
                shape=o.shape,
                material_class=o.material_class,
                radius_m=o.radius_m,
                size_m=o.size_m if o.size_m is not None else o.bbox_body_frame_m,
                mass_kg=o.mass_kg,
                density_kg_m3=o.density_kg_m3,
                restitution=contact.restitution,
                friction=contact.mu_kinetic,
                initial_position_m=gt.initial_position,
                initial_velocity_m_s=gt.initial_velocity,
                geometry_source="ground_truth",
            )
            for o in gt.objects
        ]
        surface = None
        if gt.surface is not None and gt.surface.name is not None:
            surface = SurfaceConfig(
                material=gt.surface.name,
                ramp_angle_deg=gt.surface.ramp_angle_deg,
                friction=contact.mu_kinetic,
                restitution=contact.restitution,
            )
        return cls(
            phenomenon=gt.phenomenon,
            objects=objects,
            surface=surface,
            gravity=list(gt.gravity),
            fps=gt.fps,
            duration_s=gt.duration_s or None,
        )
