"""Settings resolve roots from the environment with local defaults."""

from __future__ import annotations

from pathlib import Path

import pytest

from vsu.settings import Settings, get_settings


def test_defaults_are_absolute_and_relative_to_cwd(
    clean_env: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    cwd = tmp_path
    clean_env.chdir(cwd)
    s = Settings(_env_file=None)
    assert s.data_root == cwd / "data"
    assert s.results_root == cwd / "results" / "runs"
    assert s.cache_root == cwd / ".cache"
    assert s.hf_home is None
    assert all(p.is_absolute() for p in (s.data_root, s.results_root, s.cache_root))


def test_environment_overrides_defaults(clean_env: pytest.MonkeyPatch, tmp_path: Path) -> None:
    root = tmp_path
    clean_env.setenv("VSU_DATA_ROOT", str(root / "d"))
    clean_env.setenv("VSU_RESULTS_ROOT", str(root / "r"))
    clean_env.setenv("VSU_CACHE_ROOT", str(root / "c"))
    clean_env.setenv("HF_HOME", str(root / "hf"))
    s = Settings(_env_file=None)
    assert s.data_root == root / "d"
    assert s.results_root == root / "r"
    assert s.cache_root == root / "c"
    assert s.hf_home == root / "hf"


def test_empty_hf_home_means_unset(clean_env: pytest.MonkeyPatch) -> None:
    clean_env.setenv("HF_HOME", "")
    assert Settings(_env_file=None).hf_home is None


def test_tilde_is_expanded(clean_env: pytest.MonkeyPatch, tmp_path: Path) -> None:
    home = tmp_path
    clean_env.setenv("HOME", str(home))
    clean_env.setenv("VSU_DATA_ROOT", "~/data")
    assert Settings(_env_file=None).data_root == home / "data"


def test_keyword_overrides(clean_env: pytest.MonkeyPatch, tmp_path: Path) -> None:
    s = get_settings(data_root=tmp_path / "x", _env_file=None)
    assert s.data_root == tmp_path / "x"


def test_derived_dirs_follow_data_root(clean_env: pytest.MonkeyPatch, tmp_path: Path) -> None:
    s = Settings(data_root=tmp_path, _env_file=None)
    root = tmp_path
    assert s.sim_dir == root / "sim"
    assert s.physion_pp_dir == root / "physion_pp"
    assert s.smoke_dir == root / "smoke"
    assert s.materials_dir == root / "materials"
    assert s.annotations_dir == root / "annotations"


def test_symlinks_are_not_followed(clean_env: pytest.MonkeyPatch, tmp_path: Path) -> None:
    target = tmp_path / "real"
    target.mkdir()
    link = tmp_path / "link"
    link.symlink_to(target)
    assert Settings(data_root=link, _env_file=None).data_root == link


def test_resolved_roots_are_plain_strings(clean_env: pytest.MonkeyPatch, tmp_path: Path) -> None:
    s = Settings(data_root=tmp_path, _env_file=None)
    record = s.resolved_roots()
    assert set(record) == {
        "VSU_DATA_ROOT",
        "VSU_RESULTS_ROOT",
        "VSU_CACHE_ROOT",
        "HF_HOME",
        "VSU_CONFIGS_ROOT",
    }
    assert record["VSU_DATA_ROOT"] == str(tmp_path)
    assert record["HF_HOME"] is None
    assert all(v is None or isinstance(v, str) for v in record.values())


def test_dotenv_file_in_cwd_is_read(clean_env: pytest.MonkeyPatch, tmp_path: Path) -> None:
    cwd = tmp_path
    clean_env.chdir(cwd)
    (cwd / ".env").write_text("VSU_RESULTS_ROOT=./from_dotenv\nOPENAI_API_KEY=ignored\n")
    s = Settings()
    assert s.results_root == cwd / "from_dotenv"


def test_environment_beats_dotenv(clean_env: pytest.MonkeyPatch, tmp_path: Path) -> None:
    cwd = tmp_path
    clean_env.chdir(cwd)
    (cwd / ".env").write_text("VSU_CACHE_ROOT=./from_dotenv\n")
    clean_env.setenv("VSU_CACHE_ROOT", str(cwd / "from_env"))
    assert Settings().cache_root == cwd / "from_env"


def test_configs_root_defaults_to_the_repository(clean_env: pytest.MonkeyPatch) -> None:
    s = Settings(_env_file=None)
    assert s.configs_root.name == "configs" and (s.model_configs_dir / "dummy.yaml").is_file()
    clean_env.setenv("VSU_CONFIGS_ROOT", "/elsewhere/cfg")
    assert Settings(_env_file=None).experiment_configs_dir == Path("/elsewhere/cfg/experiments")
