#!/usr/bin/env bash
# The material recognition experiments for one model in one allocation.
#
#     sbatch scripts/snellius/run_material.slurm <model> <exp>:<variant>[,<variant>...] ...
#     sbatch scripts/snellius/run_material.slurm qwen3vl-8b exp1:v1,v2,v3 exp1_1:yesno_v1,choice_v1 exp1_2:v1
#     sbatch --partition=gpu_h100 --cpus-per-task=16 scripts/snellius/run_material.slurm gemma4-31b exp1:v1
#
# Each <exp>:<variants> runs scripts/run.py once. Answers already in the response cache cost
# nothing, and a resubmitted job resumes each experiment from its raw.jsonl.
#
#SBATCH --job-name=vsu-material
#SBATCH --partition=gpu_a100
#SBATCH --gpus=1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=18
#SBATCH --time=01:00:00
#SBATCH --output=/projects/prjs2306/morpheus/logs/vlm-scene-understanding/%x-%j.out
#SBATCH --error=/projects/prjs2306/morpheus/logs/vlm-scene-understanding/%x-%j.err
set -euo pipefail
if [[ $# -lt 2 ]]; then
  echo "usage: sbatch run_material.slurm <model> <exp>:<variants> ..." >&2
  exit 2
fi
model="$1"; shift
repo="${VSU_REPO_DIR:-${SLURM_SUBMIT_DIR:-$PWD}}"
# shellcheck disable=SC1091
source "${repo}/scripts/snellius/env.sh"
export HF_HUB_OFFLINE="${HF_HUB_OFFLINE:-1}"
cd "${VSU_REPO_DIR}"
echo "job ${SLURM_JOB_ID:-local} on $(hostname), $(date -Is): ${model} $*"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || true
status=0
for spec in "$@"; do
  exp="${spec%%:*}"
  IFS=',' read -r -a variants <<< "${spec#*:}"
  echo; echo "=== ${exp}: ${variants[*]}  ($(date -Is))"
  uv run --no-sync python scripts/run.py "${exp}" --models "${model}" --variants "${variants[@]}" || status=1
done
echo "finished $(date -Is), status ${status}"
exit "${status}"
