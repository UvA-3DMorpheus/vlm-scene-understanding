#!/usr/bin/env bash
# Generic experiment job: one (experiment, model) per job, variants loop inside so the
# model is loaded once.
#
#     sbatch scripts/snellius/run_exp.slurm <exp> <model> [variant ...] [-- extra run.py args]
#     sbatch scripts/snellius/run_exp.slurm exp1 qwen3vl-8b v1 v2 v3
#     sbatch --partition=gpu_h100 --time=04:00:00 scripts/snellius/run_exp.slurm exp1 qwen3vl-32b
#
# Submit from the repository root (or export VSU_REPO_DIR). Logs go to the project logs
# directory; the literal path in the SBATCH lines below is the only place it appears
# because SBATCH directives cannot expand variables (override with sbatch --output/--error).
# Results stream directly to VSU_RESULTS_ROOT, so a timed out job keeps its partial
# raw.jsonl and a resubmission resumes from it.
#
#SBATCH --job-name=vsu
#SBATCH --partition=gpu_a100
#SBATCH --gpus=1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=18
#SBATCH --time=02:00:00
#SBATCH --output=/projects/prjs2306/morpheus/logs/vlm-scene-understanding/%x-%j.out
#SBATCH --error=/projects/prjs2306/morpheus/logs/vlm-scene-understanding/%x-%j.err
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: sbatch run_exp.slurm <exp> <model> [variant ...] [-- extra run.py args]" >&2
  exit 2
fi
exp="$1"; model="$2"; shift 2
variants=()
while [[ $# -gt 0 && "$1" != "--" ]]; do variants+=("$1"); shift; done
[[ "${1:-}" == "--" ]] && shift
extra=("$@")

repo="${VSU_REPO_DIR:-${SLURM_SUBMIT_DIR:-$PWD}}"
# shellcheck disable=SC1091
source "${repo}/scripts/snellius/env.sh"
export HF_HUB_OFFLINE="${HF_HUB_OFFLINE:-1}"   # weights are pre-downloaded by download_models.sh
cd "${VSU_REPO_DIR}"

echo "job ${SLURM_JOB_ID:-local} on $(hostname), $(date -Is)"
echo "exp=${exp} model=${model} variants=${variants[*]:-<all>} extra=${extra[*]:-}"
echo "commit $(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || true

args=("${exp}" --models "${model}")
if [[ ${#variants[@]} -gt 0 ]]; then args+=(--variants "${variants[@]}"); fi
args+=("${extra[@]}")

uv run --no-sync python scripts/run.py "${args[@]}"
echo "finished $(date -Is)"
