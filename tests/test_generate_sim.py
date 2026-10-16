"""The scene generation script builds the right commands and skips what exists."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "generate_sim.py"
spec = importlib.util.spec_from_file_location("generate_sim", SCRIPT)
assert spec is not None and spec.loader is not None
generate_sim = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_sim)


def test_scene_table_has_one_entry_per_pipeline_variant() -> None:
    assert set(generate_sim.SCENES) >= {
        "high_drop",
        "projectile",
        "rolling",
        "sliding_block",
        "sliding_book",
    }
    expected = {
        "sliding_tray",
        "sliding_organiser",
        "sliding_board_game",
        "sliding_book",
        "sliding_cereal_box",
    }
    assert expected == generate_sim.SCANNED_OBJECT_SCENES


def test_scene_command_targets_the_scene_folder(tmp_path: Path) -> None:
    cmd = generate_sim.scene_command(
        "sliding_book", tmp_path, width=640, height=480, fps=24, python="py"
    )
    assert cmd[:3] == ["py", "-m", "scenarios.sliding"]
    assert cmd[cmd.index("--out") + 1] == str(tmp_path / "sliding_book")
    assert cmd[-2:] == ["--object", "book"]
    assert "--width" in cmd and "640" in cmd


def test_scenes_to_run_skips_existing_unless_forced(tmp_path: Path) -> None:
    (tmp_path / "high_drop").mkdir()
    (tmp_path / "high_drop" / "ground_truth.json").write_text("{}")
    assert "high_drop" not in generate_sim.scenes_to_run(None, tmp_path, force=False)
    assert "high_drop" in generate_sim.scenes_to_run(None, tmp_path, force=True)
    assert generate_sim.scenes_to_run(["projectile"], tmp_path, force=False) == ["projectile"]
    with pytest.raises(SystemExit, match="unknown scenes"):
        generate_sim.scenes_to_run(["nope"], tmp_path, force=False)


def test_dry_run_refuses_a_non_checkout(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="not a 3D-Simulations checkout"):
        generate_sim.main(["--repo", str(tmp_path), "--dry-run"])


def test_dry_run_on_a_fake_pinned_checkout(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    import subprocess

    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "pipeline.py").write_text("")
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@t",
            "commit",
            "-q",
            "--allow-empty",
            "-m",
            "x",
        ],
        cwd=repo,
        check=True,
    )
    out = tmp_path / "out"
    code = generate_sim.main(
        [
            "--repo",
            str(repo),
            "--out",
            str(out),
            "--scenes",
            "high_drop",
            "--dry-run",
            "--allow-other-commit",
        ]
    )
    assert code == 0
    printed = capsys.readouterr().out
    assert "scenarios.high_drop" in printed and str(out / "high_drop") in printed
    with pytest.raises(SystemExit, match="pinned"):
        generate_sim.main(["--repo", str(repo), "--out", str(out), "--dry-run"])


def test_script_does_not_import_mujoco_itself() -> None:
    source = SCRIPT.read_text()
    assert "import mujoco" not in source.replace("import mujoco; print", "")
    assert "mujoco" not in sys.modules


def test_blender_renderer_adds_look_and_binary(tmp_path: Path) -> None:
    cmd = generate_sim.scene_command(
        "high_drop",
        tmp_path,
        width=1280,
        height=960,
        fps=24,
        renderer="blender",
        blender="/x/blender",
        python="py",
    )
    assert cmd[cmd.index("--renderer") + 1] == "blender"
    assert cmd[cmd.index("--blender-look") + 1] == "realistic"
    assert cmd[cmd.index("--blender") + 1] == "/x/blender"
    plain = generate_sim.scene_command(
        "high_drop", tmp_path, width=640, height=480, fps=24, python="py"
    )
    assert "--renderer" not in plain
    assert generate_sim.RENDERERS["blender"][0] == "realistic"
