#!/usr/bin/env bash
# Verify the material experiments' scoring on the benchmark, then submit the model runs.
#
#     sbatch --dependency=afterok:<render job> scripts/snellius/verify_then_run_material.slurm
#
# 1. scripts/verify_scoring.py with simulated perfect and biased models on the realistic
#    scenes and the photos (no GPU). Any mismatch stops here: nothing is submitted.
# 2. One run_material.slurm job per model (A100 or H100), then one CPU job that writes the
#    report tables once all model jobs have ended.
#
#SBATCH --job-name=vsu-verify
#SBATCH --partition=rome
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=00:30:00
#SBATCH --output=/projects/prjs2306/morpheus/logs/vlm-scene-understanding/%x-%j.out
#SBATCH --error=/projects/prjs2306/morpheus/logs/vlm-scene-understanding/%x-%j.err
set -euo pipefail
repo="${VSU_REPO_DIR:-${SLURM_SUBMIT_DIR:-$PWD}}"
# shellcheck disable=SC1091
source "${repo}/scripts/snellius/env.sh"
cd "${VSU_REPO_DIR}"
echo "job ${SLURM_JOB_ID:-local} on $(hostname), $(date -Is)"

check_dir="${VSU_RESULTS_ROOT}/verify/${SLURM_JOB_ID:-local}"
if ! uv run --no-sync python scripts/verify_scoring.py --out "${check_dir}"; then
  echo "scoring check FAILED: no model runs submitted" >&2
  exit 1
fi

specs=(exp1:v1,v2,v3 exp1_1:yesno_v1,choice_v1 exp1_2:v1)
a100=(qwen3vl-8b internvl3_5-8b llava-onevision-7b internvl3_5-14b glm-4.6v-flash)
h100=(qwen3.8-27b gemma4-31b)
jobs=()
for model in "${a100[@]}"; do
  jobs+=("$(sbatch --parsable --job-name="vsu-mat-${model}" scripts/snellius/run_material.slurm "${model}" "${specs[@]}")")
done
for model in "${h100[@]}"; do
  jobs+=("$(sbatch --parsable --job-name="vsu-mat-${model}" --partition=gpu_h100 --cpus-per-task=16 \
    scripts/snellius/run_material.slurm "${model}" "${specs[@]}")")
done
echo "model jobs: ${jobs[*]}"
deps="$(IFS=:; echo "${jobs[*]}")"
report="$(sbatch --parsable --job-name=vsu-report --partition=rome --cpus-per-task=4 --time=00:20:00 \
  --dependency="afterany:${deps}" \
  --output="${VSU_LOGS_ROOT}/%x-%j.out" --error="${VSU_LOGS_ROOT}/%x-%j.err" \
  --wrap="source ${VSU_REPO_DIR}/scripts/snellius/env.sh && cd ${VSU_REPO_DIR} && uv run --no-sync python scripts/report.py")"
echo "report job: ${report}"
