"""Generate the simulated scene set with the simulation team's pipeline.

Runs the scenarios of Emil Halliday's ``3D-Simulations`` repository from a pinned checkout,
headless. Two renderers: ``mujoco`` (fast preview look, into ``VSU_DATA_ROOT/sim/preview/``) and
``blender`` (Cycles, realistic look, into ``VSU_DATA_ROOT/sim/realistic/``; needs the
Blender binary named by ``BLENDER`` and a GPU, see ``scripts/snellius/generate_sim.slurm``).
Physics, ground truth, depth and segmentation are identical between the two; only the
pixels differ.

    python scripts/generate_sim.py                       # all scenes, preview look, skip existing
    python scripts/generate_sim.py --scenes high_drop sliding_book --force
    python scripts/generate_sim.py --renderer blender    # realistic look, 1280x960
    python scripts/generate_sim.py --dry-run             # print the commands only

Consumes: the checkout (``--repo`` or ``VSU_SIM_REPO``, default ``~/3D-Simulations``),
the scene table below and the ``sim`` extra (``uv sync --extra sim``). Produces: one
folder per scene exactly as the pipeline writes it, plus ``MANIFEST.json`` recording the
pipeline commit, MuJoCo version, options and which scenes passed their own checks. The
pipeline output is deterministic for a given commit, MuJoCo version and options.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

from vsu.data.dataset import CHECKS_FILE, GROUND_TRUTH_FILE, checks_pass
from vsu.settings import get_settings

#: The commit of 3D-Simulations the scenes are generated from. Bump deliberately.
PINNED_COMMIT = "05c0043a1a9b67e71478868abeab79d7d363c2fd"

#: Renderer -> (collection under VSU_DATA_ROOT/sim, default width, default height).
RENDERERS: dict[str, tuple[str, int, int]] = {
    "mujoco": ("preview", 640, 480),
    "blender": ("realistic", 1280, 960),
}

#: scene id -> (scenario module, extra arguments). Resolution and fps are added by the script.
SCENES: dict[str, tuple[str, list[str]]] = {
    "high_drop": ("scenarios.high_drop", []),
    "projectile": ("scenarios.projectile", []),
    "rolling": ("scenarios.rolling", []),
    "rolling_hollow": ("scenarios.rolling", ["--hollow"]),
    "sliding_block": ("scenarios.sliding", ["--object", "block"]),
    "sliding_tray": ("scenarios.sliding", ["--object", "tray"]),
    "sliding_organiser": ("scenarios.sliding", ["--object", "organiser"]),
    "sliding_board_game": ("scenarios.sliding", ["--object", "board_game"]),
    "sliding_book": ("scenarios.sliding", ["--object", "book"]),
    "sliding_cereal_box": ("scenarios.sliding", ["--object", "cereal_box"]),
}
SCANNED_OBJECT_SCENES = {k for k, (_, a) in SCENES.items() if "--object" in a and a[-1] != "block"}


def default_repo() -> Path:
    env = os.environ.get("VSU_SIM_REPO")
    return Path(env).expanduser() if env else Path.home() / "3D-Simulations"


def repo_commit(repo: Path) -> tuple[str, bool]:
    """Return (HEAD commit, dirty) of the checkout."""
    head = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
    dirty = bool(
        subprocess.run(
            ["git", "-C", str(repo), "status", "--porcelain", "--untracked-files=no"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    )
    return head, dirty


def scene_command(
    scene_id: str,
    out_dir: Path,
    *,
    width: int,
    height: int,
    fps: int,
    renderer: str = "mujoco",
    blender: str | None = None,
    python: str = sys.executable,
) -> list[str]:
    """The pipeline invocation for one scene."""
    module, extra = SCENES[scene_id]
    cmd = [
        python,
        "-m",
        module,
        "--out",
        str(out_dir / scene_id),
        "--width",
        str(width),
        "--height",
        str(height),
        "--fps",
        str(fps),
        *extra,
    ]
    if renderer == "blender":
        cmd += ["--renderer", "blender", "--blender-look", "realistic"]
        if blender:
            cmd += ["--blender", blender]
    return cmd


def scenes_to_run(requested: list[str] | None, out_dir: Path, *, force: bool) -> list[str]:
    """Requested (or all) scene ids, minus those already generated unless ``force``."""
    ids = list(SCENES) if not requested else list(requested)
    unknown = [s for s in ids if s not in SCENES]
    if unknown:
        raise SystemExit(f"unknown scenes {unknown}; known: {sorted(SCENES)}")
    if force:
        return ids
    return [s for s in ids if not (out_dir / s / GROUND_TRUTH_FILE).is_file()]


def ensure_assets(repo: Path, python: str, env: dict[str, str]) -> None:
    """Download the scanned objects and textures once (needs network)."""
    if (repo / "assets" / "scanned_objects").is_dir():
        return
    print("fetching assets (scanned objects, textures) into", repo / "assets")
    subprocess.run([python, "fetch_assets.py"], cwd=repo, env=env, check=True)


def write_manifest(out_dir: Path, *, commit: str, dirty: bool, args: argparse.Namespace) -> dict:
    mujoco_version = subprocess.run(
        [sys.executable, "-c", "import mujoco; print(mujoco.__version__)"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    scenes = {}
    for scene_id in SCENES:
        checks = out_dir / scene_id / CHECKS_FILE
        if checks.is_file():
            scenes[scene_id] = {"checks_pass": checks_pass(json.loads(checks.read_text()))}
    manifest = {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "pipeline_repo": "github.com/UvA-3DMorpheus/3D-Simulations",
        "pipeline_commit": commit,
        "pipeline_uncommitted_changes": dirty,
        "blender": os.environ.get("BLENDER_REAL") if args.renderer == "blender" else None,
        "cycles_device": os.environ.get("BLENDER_COMPUTE_DEVICE")
        if args.renderer == "blender"
        else None,
        "mujoco_version": mujoco_version,
        "renderer": args.renderer,
        "look": "realistic" if args.renderer == "blender" else "preview",
        "options": {"width": args.width, "height": args.height, "fps": args.fps},
        "scenes": scenes,
    }
    (out_dir / "MANIFEST.json").write_text(json.dumps(manifest, indent=1) + "\n")
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--repo", type=Path, default=default_repo(), help="3D-Simulations checkout")
    parser.add_argument("--out", type=Path, default=None, help="default VSU_DATA_ROOT/sim/<look>")
    parser.add_argument("--scenes", nargs="*", default=None, help=f"subset of {sorted(SCENES)}")
    parser.add_argument("--renderer", choices=sorted(RENDERERS), default="mujoco")
    parser.add_argument("--width", type=int, default=None, help="default per renderer")
    parser.add_argument("--height", type=int, default=None, help="default per renderer")
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--force", action="store_true", help="regenerate existing scenes")
    parser.add_argument("--allow-dirty", action="store_true", help="accept a modified checkout")
    parser.add_argument("--allow-other-commit", action="store_true", help="accept HEAD != pinned")
    parser.add_argument("--dry-run", action="store_true", help="print commands, run nothing")
    args = parser.parse_args(argv)

    repo = Path(os.path.abspath(args.repo.expanduser()))
    if not (repo / "pipeline.py").is_file():
        raise SystemExit(f"{repo} is not a 3D-Simulations checkout (set --repo or VSU_SIM_REPO)")
    commit, dirty = repo_commit(repo)
    if commit != PINNED_COMMIT and not args.allow_other_commit:
        raise SystemExit(
            f"checkout is at {commit[:8]}, pinned {PINNED_COMMIT[:8]}; pass --allow-other-commit"
        )
    if dirty and not args.allow_dirty:
        raise SystemExit("checkout has uncommitted changes; pass --allow-dirty to proceed")

    folder, default_w, default_h = RENDERERS[args.renderer]
    args.width = args.width or default_w
    args.height = args.height or default_h
    out_dir = Path(os.path.abspath(args.out or get_settings().sim_collection_dir(folder)))
    blender = os.environ.get("BLENDER") if args.renderer == "blender" else None
    if (
        args.renderer == "blender"
        and not (blender and Path(blender).is_file())
        and not args.dry_run
    ):
        raise SystemExit("set BLENDER to the Blender executable (scripts/snellius/env.sh does)")
    todo = scenes_to_run(args.scenes, out_dir, force=args.force)
    env = {**os.environ, "MUJOCO_GL": os.environ.get("MUJOCO_GL", "egl"), "PYTHONPATH": str(repo)}
    state = " (dirty)" if dirty else ""
    print(f"repo {repo} @ {commit[:8]}{state}; out {out_dir}; scenes {todo or 'none'}")
    if args.dry_run:
        for scene_id in todo:
            cmd = scene_command(
                scene_id,
                out_dir,
                width=args.width,
                height=args.height,
                fps=args.fps,
                renderer=args.renderer,
                blender=blender,
            )
            print(" ".join(cmd))
        return 0
    if not todo:
        write_manifest(out_dir, commit=commit, dirty=dirty, args=args)
        return 0
    out_dir.mkdir(parents=True, exist_ok=True)
    if SCANNED_OBJECT_SCENES & set(todo):
        ensure_assets(repo, sys.executable, env)
    failed: list[str] = []
    for scene_id in todo:
        cmd = scene_command(
            scene_id,
            out_dir,
            width=args.width,
            height=args.height,
            fps=args.fps,
            renderer=args.renderer,
            blender=blender,
        )
        print(f"\n=== {scene_id}: {' '.join(cmd[1:])}", flush=True)
        result = subprocess.run(cmd, cwd=repo, env=env)
        if result.returncode != 0:
            failed.append(scene_id)
            print(f"!!! {scene_id} failed with exit code {result.returncode}", flush=True)
    manifest = write_manifest(out_dir, commit=commit, dirty=dirty, args=args)
    print("\nchecks:", {k: v["checks_pass"] for k, v in manifest["scenes"].items()})
    if failed:
        print("failed:", failed)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
