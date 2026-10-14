#!/usr/bin/env bash
# One short GPU job that sends one smoke image through a model and checks the answer parses.
# Also the first place a new model, driver or torch build gets exercised.
#
#     sbatch scripts/snellius/smoke_model.slurm qwen3vl-8b
#     sbatch scripts/snellius/smoke_model.slurm qwen3vl-4b internvl3_5-8b -- --no-cache
# Several models run one after the other in the same allocation.
#
#SBATCH --job-name=vsu-smoke
#SBATCH --partition=gpu_a100
#SBATCH --gpus=1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=18
#SBATCH --time=00:20:00
#SBATCH --output=/projects/prjs2306/morpheus/logs/vlm-scene-understanding/%x-%j.out
#SBATCH --error=/projects/prjs2306/morpheus/logs/vlm-scene-understanding/%x-%j.err
set -euo pipefail
models=()
while [[ $# -gt 0 && "$1" != "--" ]]; do models+=("$1"); shift; done
[[ "${1:-}" == "--" ]] && shift
[[ ${#models[@]} -eq 0 ]] && models=(qwen3vl-8b)
repo="${VSU_REPO_DIR:-${SLURM_SUBMIT_DIR:-$PWD}}"
# shellcheck disable=SC1091
source "${repo}/scripts/snellius/env.sh"
export HF_HUB_OFFLINE="${HF_HUB_OFFLINE:-1}"
cd "${VSU_REPO_DIR}"
echo "job ${SLURM_JOB_ID:-local} on $(hostname), $(date -Is), models ${models[*]}"
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader || true
uv run --no-sync python -c "import torch; print('torch', torch.__version__, 'cuda', torch.version.cuda, 'available', torch.cuda.is_available())"
status=0
for model in "${models[@]}"; do
  echo; echo "=== ${model}"
  uv run --no-sync python scripts/smoke_model.py --model "${model}" --verbose "$@" || status=1
done
echo "finished $(date -Is), status ${status}"
exit "${status}"
