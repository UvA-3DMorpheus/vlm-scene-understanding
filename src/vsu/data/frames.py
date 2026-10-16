"""Frame extraction from rendered videos with ffmpeg.

Consumes an ``rgb.mp4`` and produces numbered PNG frames (``000000.png`` is frame 0, at
t = 0) in a cache directory. The ffmpeg binary comes from ``VSU_FFMPEG``, the PATH, or
the one bundled with the ``imageio-ffmpeg`` package, in that order, so laptops need no
system install and Snellius can use the FFmpeg module.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

FRAME_GLOB = "[0-9][0-9][0-9][0-9][0-9][0-9].png"


def ffmpeg_executable() -> str:
    """Return the path of an ffmpeg binary, or raise ``FileNotFoundError``."""
    explicit = os.environ.get("VSU_FFMPEG")
    if explicit:
        return explicit
    on_path = shutil.which("ffmpeg")
    if on_path:
        return on_path
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as exc:  # pragma: no cover - depends on the install
        raise FileNotFoundError("no ffmpeg found: set VSU_FFMPEG or install ffmpeg") from exc


def extract_frames(video: Path, out_dir: Path, *, overwrite: bool = False) -> list[Path]:
    """Decode every frame of ``video`` into ``out_dir/%06d.png`` and return the paths.

    Existing frames are reused unless ``overwrite`` is set, so repeated scene loads cost
    nothing. Frame numbering starts at 0 to match ``frames[k].t = k / fps``. ffmpeg writes
    into a per-process ``.partial.<pid>`` folder that is renamed when it finishes, so an interrupted
    extraction is never mistaken for a complete one.
    """
    video = Path(video)
    out_dir = Path(out_dir)
    if not video.is_file():
        raise FileNotFoundError(video)
    existing = sorted(out_dir.glob(FRAME_GLOB))
    if existing and not overwrite:
        return existing
    partial = out_dir.with_name(f"{out_dir.name}.partial.{os.getpid()}")  # one per process
    if partial.exists():
        shutil.rmtree(partial)
    partial.mkdir(parents=True)
    cmd = [
        ffmpeg_executable(),
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(video),
        "-start_number",
        "0",
        str(partial / "%06d.png"),
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    if not any(partial.glob(FRAME_GLOB)):
        shutil.rmtree(partial)
        raise RuntimeError(f"ffmpeg produced no frames from {video}")
    if overwrite and out_dir.exists():
        shutil.rmtree(out_dir)
    try:
        os.replace(partial, out_dir)
    except OSError:
        # another process finished the same extraction first: keep its frames, drop ours
        shutil.rmtree(partial, ignore_errors=True)
    return sorted(out_dir.glob(FRAME_GLOB))


def encode_frames(frames: list[Path], video: Path, fps: int) -> Path:
    """Encode PNG frames into an H.264 mp4 (used by tests and for side by side clips)."""
    video = Path(video)
    video.parent.mkdir(parents=True, exist_ok=True)
    pattern_dir = frames[0].parent
    cmd = [
        ffmpeg_executable(),
        "-loglevel",
        "error",
        "-y",
        "-framerate",
        str(fps),
        "-start_number",
        frames[0].stem,
        "-i",
        str(pattern_dir / "%06d.png"),
        "-frames:v",
        str(len(frames)),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        str(video),
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    return video
