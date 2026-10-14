# vlm-scene-understanding

Can vision language models recognize materials, infer physical properties, make
comparative physical judgments, and write a structured scene description that initializes
a physics simulator from a first frame? This repository holds the VLM side of the
simulator-first extension of the Morpheus benchmark (arXiv 2504.02918). It never runs
video generation models; those are the thing under test elsewhere in the project.

The proposed data contract for the simulation team is in [data/README.md](data/README.md).

## Layout

```
src/vsu/           package: settings, models (one VLM interface), prompts, schemas, data,
                   experiments, sim, scoring, utils
configs/           yaml configs for models and experiments
data/              local data root (gitignored except smoke/, materials/, annotations/)
results/runs/      local run outputs (gitignored); results/tables/ is committed
scripts/           CLI entry points; scripts/snellius/ holds SLURM and environment scripts
tests/             pytest, runs on the dummy backend without network or GPUs
```

## Local use (laptop or login node)

Requires [uv](https://docs.astral.sh/uv/). Python 3.11 is pinned in `.python-version`
and uv installs it if missing.

```bash
uv sync                       # core dependencies plus dev tools (pytest, ruff, pre-commit)
uv run pre-commit install     # ruff lint and format on every commit
uv run pytest                 # all tests use the dummy backend
uv run ruff check . && uv run ruff format --check .
```

Optional extras: `uv sync --extra api` for the OpenAI compatible and Gemini backends,
`uv sync --extra hf` for Qwen3-VL and InternVL through transformers (GPU).

Paths come from `src/vsu/settings.py`, which reads `VSU_DATA_ROOT`, `VSU_RESULTS_ROOT`,
`VSU_CACHE_ROOT` and `HF_HOME` with defaults `./data`, `./results/runs`, `./.cache`.
Copy `.env.example` to `.env` for API keys; `.env` is gitignored.

Running an experiment:

```bash
uv run python scripts/run.py exp1 --models dummy --variants v1 v2 v3   # whole pipeline
uv run python scripts/run.py exp1 --models dummy --stage score         # re-score the latest runs
uv run python scripts/report.py --experiment exp1                      # tables into results/tables
uv run python scripts/smoke_model.py --model dummy                     # one image, one question
```

Each run writes `VSU_RESULTS_ROOT/<exp>/<model>/<variant>/<timestamp>/` with `config.yaml`
(resolved settings, git commit, package versions, template hash), `questions.jsonl`,
`raw.jsonl`, `scored.jsonl` and `summary.json`. A resubmitted job resumes from `raw.jsonl`.
Experiments are configured in `configs/experiments/`, models in `configs/models/`, prompts are
jinja templates in `src/vsu/prompts/templates/` named `<exp>_<variant>.jinja`.

Experiment 1 (material recognition) asks the material of the object in the simulated scenes
(the benchmark) and of the smoke photos (a sanity check, reported apart). Reports under
`results/tables/` give accuracy, macro F1, per material recall, confusion matrices and the
agreement between prompt variants.

## Snellius

Everything large lives in the shared project space `/projects/prjs2306/morpheus`
(data, model weights, results, logs, the Python environment). The repository and your
home directory stay small. `scripts/snellius/env.sh` is the only place that knows the
project path; it loads the modules and exports the `VSU_*` variables and `HF_HOME`.

One time setup, on a login node:

```bash
source scripts/snellius/env.sh
bash scripts/snellius/init_project_dir.sh    # layout with group prjs2306 permissions
bash scripts/snellius/setup_env.sh           # uv + Python 3.11 + dependencies in the project space
bash scripts/snellius/download_models.sh     # open model weights into HF_HOME
mkdir -p ~/.config/vsu && touch ~/.config/vsu/secrets.env && chmod 600 ~/.config/vsu/secrets.env
# put OPENAI_API_KEY=... and GEMINI_API_KEY=... lines in that file
uv run pytest                                # must pass on the login node
```

Every session:

```bash
source scripts/snellius/env.sh
sbatch scripts/snellius/run_exp.slurm exp1 qwen3vl-8b v1 v2 v3
# defaults: gpu_a100, 1 GPU, 2 hours; override with sbatch flags, for example
sbatch --partition=gpu_h100 --time=04:00:00 scripts/snellius/run_exp.slurm exp1 qwen3vl-32b
```

Logs land in `/projects/prjs2306/morpheus/logs/vlm-scene-understanding/`. A timed out
job is resubmitted with the same command; `run` resumes from the existing `raw.jsonl`.

Module names in `env.sh` were verified on 2026-10-13. The 2024 software stack has no
Python 3.11, so uv provides the interpreter and the modules provide CUDA, cuDNN and FFmpeg.
Re-check `module -t avail` after a stack update. The torch wheel brings its own CUDA runtime
(currently a CUDA 13.0 build), so the node driver must support it; the first GPU smoke job
in Step 3 confirms this. uv's download cache under `envs/uv-cache` is about 5 GB and can be
cleared with `uv cache clean` after a sync.
