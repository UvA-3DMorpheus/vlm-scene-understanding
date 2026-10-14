"""run.py and report.py drive the whole pipeline on the dummy and write the tables."""

from __future__ import annotations

import csv
import importlib.util
import shutil
from pathlib import Path

import pytest

from tests.test_dataset import make_scene_dir

REPO = Path(__file__).resolve().parents[1]


def load_script(name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, REPO / "scripts" / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    data = tmp_path / "data"
    shutil.copytree(REPO / "data" / "smoke", data / "smoke")
    shutil.copytree(REPO / "data" / "materials", data / "materials")
    make_scene_dir(data / "sim", "sliding_cereal_box")
    monkeypatch.setenv("VSU_DATA_ROOT", str(data))
    monkeypatch.setenv("VSU_RESULTS_ROOT", str(tmp_path / "runs"))
    monkeypatch.setenv("VSU_CACHE_ROOT", str(tmp_path / "cache"))
    monkeypatch.chdir(tmp_path)  # no .env of the repo
    return tmp_path


def test_run_then_report(env: Path, capsys: pytest.CaptureFixture[str]) -> None:
    run = load_script("run")
    assert run.main(["exp1", "--models", "dummy", "--variants", "v1", "v2", "v3"]) == 0
    runs = env / "runs" / "exp1" / "dummy"
    assert sorted(p.name for p in runs.iterdir()) == ["v1", "v2", "v3"]
    for variant in ("v1", "v2", "v3"):
        (run_dir,) = list((runs / variant).iterdir())
        assert {p.name for p in run_dir.iterdir()} >= {
            "config.yaml",
            "questions.jsonl",
            "raw.jsonl",
            "scored.jsonl",
            "summary.json",
        }
    out = capsys.readouterr().out
    assert "sim (benchmark):" in out and "smoke (sanity check):" in out
    assert out.count("| dummy |") == 6

    report = load_script("report")
    tables = env / "tables"
    assert report.main(["--experiment", "exp1", "--out", str(tables)]) == 0
    names = {p.name for p in tables.iterdir()}
    assert names >= {
        "exp1_sim_accuracy.csv",
        "exp1_sim_agreement.csv",
        "exp1_sim_per_material.csv",
        "exp1_smoke_accuracy.csv",
        "exp1_runs.csv",
        "exp1_report.md",
    }
    with (tables / "exp1_sim_accuracy.csv").open() as f:
        rows = list(csv.DictReader(f))
    assert [r["variant"] for r in rows] == ["v1", "v2", "v3"] and all(r["n"] == "7" for r in rows)
    assert set(rows[0]) >= {"frame acc", "crop acc", "frame macro_f1"}
    with (tables / "exp1_smoke_accuracy.csv").open() as f:
        smoke_rows = list(csv.DictReader(f))
    assert all(r["n"] == "18" for r in smoke_rows)
    with (tables / "exp1_sim_agreement.csv").open() as f:
        (agree,) = list(csv.DictReader(f))
    assert (
        agree["model"] == "dummy" and agree["n_common"] == "7" and agree["variants"] == "v1,v2,v3"
    )
    text = (tables / "exp1_report.md").read_text()
    assert text.index("## sim (benchmark)") < text.index("## smoke (sanity check)")
    assert "dummy/v1/frame" in text and "never mixed" in text


def test_score_and_report_stages_reuse_latest_run(env: Path) -> None:
    run = load_script("run")
    run.main(["exp1", "--models", "dummy", "--variants", "v1", "--limit", "3"])
    (run_dir,) = list((env / "runs" / "exp1" / "dummy" / "v1").iterdir())
    assert run.main(["exp1", "--models", "dummy", "--variants", "v1", "--stage", "score"]) == 0
    assert run.main(["exp1", "--models", "dummy", "--variants", "v1", "--stage", "report"]) == 0
    assert list((env / "runs" / "exp1" / "dummy" / "v1").iterdir()) == [run_dir]
    with pytest.raises(SystemExit, match="no run"):
        run.main(["exp1", "--models", "dummy", "--variants", "v2", "--stage", "score"])


def test_unknown_variant_or_experiment(env: Path) -> None:
    run = load_script("run")
    with pytest.raises(SystemExit, match="unknown variants"):
        run.main(["exp1", "--models", "dummy", "--variants", "v9"])
    with pytest.raises(KeyError, match="unknown experiment"):
        run.main(["exp9", "--models", "dummy"])


def test_questions_stage_creates_run_without_answers(env: Path) -> None:
    run = load_script("run")
    assert run.main(["exp1", "--models", "dummy", "--variants", "v1", "--stage", "questions"]) == 0
    (run_dir,) = list((env / "runs" / "exp1" / "dummy" / "v1").iterdir())
    assert (run_dir / "questions.jsonl").is_file() and not (run_dir / "raw.jsonl").exists()


def test_report_with_no_runs(env: Path, capsys: pytest.CaptureFixture[str]) -> None:
    report = load_script("report")
    assert report.main(["--out", str(env / "tables")]) == 0
    assert "no finished runs" in capsys.readouterr().out
