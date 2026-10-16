#!/usr/bin/env bash
# Render simulated scenes with the simulation team's pipeline on one GPU (Blender Cycles realistic look).
#
#     sbatch scripts/snellius/generate_sim.slurm --renderer blender --scenes high_drop
#     sbatch --time=08:00:00 scripts/snellius/generate_sim.slurm --renderer blender
#
# Arguments are passed to scripts/generate_sim.py. Output goes to VSU_DATA_ROOT/sim/realistic
# (for the Blender renderer) and is resumable per scene: finished scenes are skipped.
#
#SBATCH --job-name=vsu-render
#SBATCH --partition=gpu_a100
#SBATCH --gpus=1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=18
#SBATCH --time=04:00:00
#SBATCH --output=/projects/prjs2306/morpheus/logs/vlm-scene-understanding/%x-%j.out
#SBATCH --error=/projects/prjs2306/morpheus/logs/vlm-scene-understanding/%x-%j.err
set -euo pipefail
repo="${VSU_REPO_DIR:-${SLURM_SUBMIT_DIR:-$PWD}}"
# shellcheck disable=SC1091
source "${repo}/scripts/snellius/env.sh"
cd "${VSU_REPO_DIR}"
echo "job ${SLURM_JOB_ID:-local} on $(hostname), $(date -Is): generate_sim $*"
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader || true
uv run --no-sync python scripts/generate_sim.py "$@"
echo "finished $(date -Is)"
