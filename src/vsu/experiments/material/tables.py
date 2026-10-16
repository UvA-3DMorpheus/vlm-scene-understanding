"""Report tables of the material recognition experiments (1.0, 1.1, 1.2).

Row builders turn the summaries of finished runs into table rows, one dataset at a time;
the ``report_*`` functions write them as csv and markdown, the benchmark first.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from pathlib import Path

from vsu.experiments.material.consistency import overview_rows
from vsu.experiments.reporting import (
    ROLE_TITLES,
    FinishedRun,
    Row,
    dataset_sections,
    finished_runs,
    markdown_table,
    rounded,
    run_provenance_rows,
    write_csv,
)
from vsu.scoring.classification import agreement
from vsu.settings import Settings

# ---------------------------------------------------------------- experiment 1.0 tables


def exp1_accuracy_rows(runs: Iterable[FinishedRun], dataset: str) -> list[Row]:
    """One row per model and variant for one dataset: accuracy per condition, macro F1, failures."""
    rows = []
    for fr in runs:
        s = fr.summary
        d = s.get("datasets", {}).get(dataset)
        if d is None:
            continue
        row: Row = {
            "model": fr.model,
            "variant": fr.variant,
            "n": d["n"],
            "accuracy": rounded(d["accuracy"]),
            "exact_label_rate": rounded(d.get("exact_label_rate")),
            "parse_failures": d["n_parse_failures"],
        }
        for group, g in sorted(s["groups"].items()):
            if group.startswith(f"{dataset}/"):
                condition = group.split("/", 1)[1]
                row[f"{condition} acc"] = rounded(g["accuracy"])
                row[f"{condition} macro_f1"] = rounded(g["macro_f1"])
        row["mean_latency_s"] = rounded(s.get("mean_latency_s"), 2)
        row["run"] = fr.run.path.name
        rows.append(row)
    return rows


def exp1_camera_rows(runs: Iterable[FinishedRun], dataset: str) -> list[Row]:
    """One row per model and variant: accuracy per camera (viewpoint robustness)."""
    rows = []
    for fr in runs:
        d = fr.summary.get("datasets", {}).get(dataset) or {}
        by_camera = d.get("by_camera") or {}
        if not by_camera:
            continue
        row: Row = {"model": fr.model, "variant": fr.variant}
        for camera, c in by_camera.items():
            row[f"{camera} (n={c['n']})"] = rounded(c["accuracy"])
        rows.append(row)
    return rows


def exp1_per_material_rows(runs: Iterable[FinishedRun], dataset: str) -> list[Row]:
    """One row per model, variant, condition and material of a dataset."""
    rows = []
    for fr in runs:
        for group, g in sorted(fr.summary["groups"].items()):
            if not group.startswith(f"{dataset}/"):
                continue
            for material, pc in g["per_class"].items():
                if not pc["support"]:
                    continue
                rows.append(
                    {
                        "model": fr.model,
                        "variant": fr.variant,
                        "condition": group.split("/", 1)[1],
                        "material": material,
                        "support": pc["support"],
                        "recall": rounded(pc["recall"]),
                        "precision": rounded(pc["precision"]),
                        "f1": rounded(pc["f1"]),
                    }
                )
    return rows


def exp1_confusion_tables(runs: Iterable[FinishedRun], dataset: str) -> dict[str, list[Row]]:
    """``"<model>/<variant>/<condition>" -> rows`` of the confusion matrix (true label per row)."""
    tables: dict[str, list[Row]] = {}
    for fr in runs:
        for group, g in sorted(fr.summary["groups"].items()):
            if not group.startswith(f"{dataset}/"):
                continue
            cm = g["confusion"]
            rows = [
                {"true \\ predicted": t, **{c: cm["matrix"][t][c] for c in cm["columns"]}}
                for t in cm["labels"]
            ]
            tables[f"{fr.model}/{fr.variant}/{group.split('/', 1)[1]}"] = rows
    return tables


def exp1_agreement_rows(runs: Sequence[FinishedRun], dataset: str) -> list[Row]:
    """One row per model: agreement of its variants on the dataset's questions they all answered."""
    by_model: dict[str, dict[str, dict[str, str | None]]] = {}
    for fr in runs:
        preds = {
            s.question_id: (s.derived.get("predicted") if s.parse_ok else None)
            for s in fr.scored
            if s.dataset == dataset
        }
        by_model.setdefault(fr.model, {})[fr.variant] = preds
    rows = []
    for model, variants in sorted(by_model.items()):
        a = agreement(variants)
        row: Row = {
            "model": model,
            "variants": ",".join(a["variants"]),
            "n_common": a["n_common"],
            "all_agree": rounded(a["all_agree"]),
            "fleiss_kappa": rounded(a["fleiss_kappa"]),
        }
        for pair, value in sorted(a["pairwise"].items()):
            row[f"agree {pair}"] = rounded(value)
        rows.append(row)
    return rows


# ---------------------------------------------------------------- experiment 1.1 tables

YESNO_COLUMNS = (
    "balanced_accuracy",
    "accuracy",
    "true_positive_rate",
    "true_negative_rate",
    "yes_rate",
)
CHOICE_COLUMNS = ("accuracy", "first_option_rate", "order_consistency", "invalid_rate")


def exp1_1_rows(runs: Iterable[FinishedRun], dataset: str, task: str | None = None) -> list[Row]:
    """One row per model and variant of one dataset (optionally one task): the task's
    headline metrics, then accuracy per input condition."""
    rows = []
    for fr in runs:
        s = fr.summary
        d = s.get("datasets", {}).get(dataset)
        if d is None or (task is not None and s.get("task") != task):
            continue
        columns = YESNO_COLUMNS if s["task"] == "yesno" else CHOICE_COLUMNS
        row: Row = {"model": fr.model, "variant": fr.variant, "n": d["n"]}
        row.update({c: rounded(d.get(c)) for c in columns})
        row["parse_failures"] = d["n_parse_failures"]
        for group, g in sorted(s["groups"].items()):
            if group.startswith(f"{dataset}/"):
                row[f"{group.split('/', 1)[1]} acc"] = rounded(g["accuracy"])
        row["run"] = fr.run.path.name
        rows.append(row)
    return rows


def exp1_1_material_rows(runs: Iterable[FinishedRun], dataset: str) -> list[Row]:
    """Per material, per model and variant: for yes/no how often the true material is
    confirmed and how often it is wrongly accepted when it is not the truth; for two options,
    accuracy against each distractor."""
    rows = []
    for fr in runs:
        s = fr.summary
        d = s.get("datasets", {}).get(dataset)
        if d is None:
            continue
        if s["task"] == "yesno":
            confirmed, accepted = d["true_yes_by_truth"], d["false_yes_by_asked"]
            for material in sorted(set(confirmed) | set(accepted)):
                rows.append(
                    {
                        "model": fr.model,
                        "variant": fr.variant,
                        "material": material,
                        "confirmed when true": rounded(confirmed.get(material)),
                        "accepted when false": rounded(accepted.get(material)),
                    }
                )
        else:
            for material, acc in d["accuracy_by_distractor"].items():
                rows.append(
                    {
                        "model": fr.model,
                        "variant": fr.variant,
                        "distractor": material,
                        "accuracy": rounded(acc),
                    }
                )
    return rows


# ---------------------------------------------------------------- experiment 1.2 tables

PAIR_COLUMNS = ("accuracy", "solved_rate", "a_rate", "image_order_consistency", "label_consistency")


def exp1_2_rows(runs: Iterable[FinishedRun], dataset: str) -> list[Row]:
    """One row per model and variant of one dataset: pair metrics, then accuracy per
    presentation (separate images, side by side)."""
    rows = []
    for fr in runs:
        s = fr.summary
        d = s.get("datasets", {}).get(dataset)
        if d is None:
            continue
        row: Row = {"model": fr.model, "variant": fr.variant, "n": d["n"], "pairs": d["n_pairs"]}
        row.update({c: rounded(d.get(c)) for c in PAIR_COLUMNS})
        row["parse_failures"] = d["n_parse_failures"]
        for group, g in sorted(s["groups"].items()):
            if group.startswith(f"{dataset}/"):
                row[f"{group.split('/', 1)[1]} acc"] = rounded(g["accuracy"])
        row["run"] = fr.run.path.name
        rows.append(row)
    return rows


def exp1_2_material_pair_rows(runs: Iterable[FinishedRun], dataset: str) -> list[Row]:
    """Accuracy per pair of materials, per model and variant: which materials are told apart."""
    rows = []
    for fr in runs:
        d = fr.summary.get("datasets", {}).get(dataset)
        if d is None:
            continue
        for materials, acc in d["by_material_pair"].items():
            rows.append(
                {
                    "model": fr.model,
                    "variant": fr.variant,
                    "materials": materials.replace("|", " vs "),
                    "accuracy": rounded(acc),
                }
            )
    return rows


# ---------------------------------------------------------------- report writers


def report_exp1(out: Path, settings: Settings) -> list[Path]:
    """Experiment 1.0 tables: accuracy, cameras, agreement, per material, confusion."""
    runs = finished_runs("exp1", settings=settings)
    if not runs:
        return []
    sections = dataset_sections(runs)
    benchmark = [d for d, role in sections if role == "primary"]
    written: list[Path] = []
    parts = [
        "# Experiment 1.0: material identification\n",
        f"Latest finished run per model and variant under `{settings.results_root}`.\n",
        (
            f"The **{benchmark[0]}** dataset is the benchmark and the only one to quote. "
            if benchmark
            else ""
        )
        + "Comparison datasets are reported beside it; sanity checks show the pipeline works on "
        "real photos. No number mixes datasets.\n",
    ]
    for dataset, role in sections:
        title = f"{dataset} ({ROLE_TITLES[role]})"
        acc = exp1_accuracy_rows(runs, dataset)
        if not acc:
            continue
        agree = exp1_agreement_rows(runs, dataset)
        per_material = exp1_per_material_rows(runs, dataset)
        confusion = exp1_confusion_tables(runs, dataset)
        for name, rows in (("accuracy", acc), ("agreement", agree), ("per_material", per_material)):
            path = out / f"exp1_{dataset}_{name}.csv"
            write_csv(path, rows)
            written.append(path)
        cameras = exp1_camera_rows(runs, dataset)
        parts += [
            f"## {title}\n",
            "### Accuracy and macro F1 per condition\n",
            markdown_table(acc),
        ]
        if cameras:
            write_csv(out / f"exp1_{dataset}_cameras.csv", cameras)
            written.append(out / f"exp1_{dataset}_cameras.csv")
            parts += ["### Accuracy per camera (viewpoint robustness)\n", markdown_table(cameras)]
        parts += [
            "### Agreement across prompt variants\n",
            markdown_table(agree),
            "### Per material recall (which materials are recognisable at all)\n",
            markdown_table(per_material),
            "### Confusion matrices\n",
        ]
        for key, rows in confusion.items():
            parts += [f"#### {key}\n", markdown_table(rows)]
    prov = run_provenance_rows(runs)
    write_csv(out / "exp1_runs.csv", prov)
    written.append(out / "exp1_runs.csv")
    parts += ["## Runs\n", markdown_table(prov)]
    report = out / "exp1_report.md"
    report.write_text("\n".join(parts))
    written.append(report)
    return written


def report_exp1_1(out: Path, settings: Settings) -> list[Path]:
    """Experiment 1.1 tables: yes/no and two-option results per dataset, benchmark first."""
    runs = finished_runs("exp1_1", settings=settings)
    if not runs:
        return []
    written: list[Path] = []
    parts = [
        "# Experiment 1.1: material verification\n",
        f"Latest finished run per model and variant under `{settings.results_root}`.\n",
        "Yes/no: balanced accuracy is the headline (most questions are negatives); the yes rate "
        "shows a bias towards agreeing. Two options: chance is 0.5; a first-option rate away "
        "from 0.5 is an order bias. No number mixes datasets.\n",
    ]
    for dataset, role in dataset_sections(runs):
        parts.append(f"## {dataset} ({ROLE_TITLES[role]})\n")
        for task, title in (("yesno", "Yes or no"), ("choice", "Two options")):
            rows = exp1_1_rows(runs, dataset, task)
            if not rows:
                continue
            path = out / f"exp1_1_{dataset}_{task}.csv"
            write_csv(path, rows)
            written.append(path)
            parts += [f"### {title}\n", markdown_table(rows)]
        materials = exp1_1_material_rows(runs, dataset)
        if materials:
            path = out / f"exp1_1_{dataset}_per_material.csv"
            write_csv(path, materials)
            written.append(path)
            parts += ["### Per material\n", markdown_table(materials)]
    prov = run_provenance_rows(runs)
    write_csv(out / "exp1_1_runs.csv", prov)
    written.append(out / "exp1_1_runs.csv")
    parts += ["## Runs\n", markdown_table(prov)]
    report = out / "exp1_1_report.md"
    report.write_text("\n".join(parts))
    written.append(report)
    return written


def report_exp1_2(out: Path, settings: Settings) -> list[Path]:
    """Experiment 1.2 tables: pair metrics and accuracy per material pair, benchmark first."""
    runs = finished_runs("exp1_2", settings=settings)
    if not runs:
        return []
    written: list[Path] = []
    parts = [
        "# Experiment 1.2: material matching between two objects\n",
        f"Latest finished run per model and variant under `{settings.results_root}`.\n",
        "Each pair is asked in four forms (both image orders, both asked materials). Chance "
        "accuracy is 0.5; the solved rate counts pairs with all four forms right; an A rate "
        "away from 0.5 is a position bias. No number mixes datasets.\n",
    ]
    for dataset, role in dataset_sections(runs):
        rows = exp1_2_rows(runs, dataset)
        if not rows:
            continue
        pairs = exp1_2_material_pair_rows(runs, dataset)
        for name, table in (("pairs", rows), ("per_material_pair", pairs)):
            path = out / f"exp1_2_{dataset}_{name}.csv"
            write_csv(path, table)
            written.append(path)
        parts += [
            f"## {dataset} ({ROLE_TITLES[role]})\n",
            markdown_table(rows),
            "### Accuracy per pair of materials\n",
            markdown_table(pairs),
        ]
    prov = run_provenance_rows(runs)
    write_csv(out / "exp1_2_runs.csv", prov)
    written.append(out / "exp1_2_runs.csv")
    parts += ["## Runs\n", markdown_table(prov)]
    report = out / "exp1_2_report.md"
    report.write_text("\n".join(parts))
    written.append(report)
    return written


def report_material(out: Path, settings: Settings) -> list[Path]:
    """The combined material recognition overview: every task and cross-task consistency."""
    runs = [
        r for name in ("exp1", "exp1_1", "exp1_2") for r in finished_runs(name, settings=settings)
    ]
    if not runs:
        return []
    written: list[Path] = []
    parts = [
        "# Material recognition: overview of Experiments 1.0, 1.1 and 1.2\n",
        "Per model and answer mode (direct: answer only; reasoning: a short reasoning step "
        "first). Identification (1.0) names the material; yes/no and two options (1.1) verify "
        "a named material; matching (1.2) tells two objects apart. Consistency columns compare "
        "a task's answers with the model's own 1.0 label for the same object and view, right "
        "or wrong. Chance: identification 0.2 (five labels), yes/no balanced accuracy 0.5, "
        "two options 0.5, matching 0.5. Views: identification is over all its views (frame, "
        "crop, outline, multiview), yes/no over frames and crops, two options and matching "
        "over crops.\n",
    ]
    for dataset, role in dataset_sections(runs):
        rows = overview_rows(settings, dataset)
        if not rows:
            continue
        path = out / f"material_{dataset}_overview.csv"
        write_csv(path, rows)
        written.append(path)
        parts += [f"## {dataset} ({ROLE_TITLES[role]})\n", markdown_table(rows)]
    report = out / "material_report.md"
    report.write_text("\n".join(parts))
    written.append(report)
    return written
