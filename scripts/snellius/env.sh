#!/usr/bin/env bash
# Snellius environment for vlm-scene-understanding. Source it, do not execute it:
#
#     source scripts/snellius/env.sh
#
# It loads modules, puts uv on PATH, exports the VSU_* roots and HF_HOME pointing at
# the shared project space, and sources the private secrets file. Every SLURM script
# sources this file. On a laptop you source nothing and get the local defaults.
#
# Module names below were checked on the login node on 2026-10-13 (`module -t avail`).
# The 2024 stack ships Python 3.12.3 and no Python 3.11, so the interpreter comes from
# uv (managed CPython 3.11 installed into the project space by setup_env.sh); the modules
# provide only CUDA, cuDNN and FFmpeg. Re-verify after a software stack update.

# Shared project directory (PLAN.md Section 2.1). Override only for testing the scripts.
export VSU_PROJECT_DIR="${VSU_PROJECT_DIR:-/projects/prjs2306/morpheus}"
export VSU_GROUP="${VSU_GROUP:-prjs2306}"

# Repository root, derived from this file's location so the scripts work from any cwd.
_vsu_env_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export VSU_REPO_DIR="${VSU_REPO_DIR:-$(cd "${_vsu_env_dir}/../.." && pwd)}"
unset _vsu_env_dir

# --- Modules (names to re-verify after a stack update) ---------------------------------
# Non login shells (some sbatch and tool contexts) lack the `module` function; load Lmod.
if ! command -v module >/dev/null 2>&1 && [[ -f /usr/share/lmod/lmod/init/bash ]]; then
  # shellcheck disable=SC1091
  source /usr/share/lmod/lmod/init/bash
fi
module purge
module load 2024
module load CUDA/12.6.0
module load cuDNN/9.5.0.50-CUDA-12.6.0
module load FFmpeg/7.0.2-GCCcore-13.3.0

# --- Paths read by src/vsu/settings.py ------------------------------------------------
export VSU_DATA_ROOT="${VSU_PROJECT_DIR}/data"
export VSU_RESULTS_ROOT="${VSU_PROJECT_DIR}/results/vlm-scene-understanding"
export VSU_CACHE_ROOT="${VSU_RESULTS_ROOT}/.cache"
export VSU_LOGS_ROOT="${VSU_PROJECT_DIR}/logs/vlm-scene-understanding"
export HF_HOME="${VSU_PROJECT_DIR}/models/hf"
export VLLM_CACHE_ROOT="${VSU_PROJECT_DIR}/models/vllm"
# Pinned checkout of the simulation team's 3D-Simulations repository (scripts/generate_sim.py).
export VSU_SIM_REPO="${VSU_SIM_REPO:-${VSU_PROJECT_DIR}/envs/3D-Simulations}"
# Headless rendering for MuJoCo (EGL works on login and GPU nodes).
export MUJOCO_GL="${MUJOCO_GL:-egl}"

# --- uv: binary, download cache, managed Python and the project environment -------------
# Everything uv writes goes to the project space, never to home (200 GB quota, shared quota
# with everything else) and never into the repository.
export UV_INSTALL_DIR="${VSU_PROJECT_DIR}/envs/bin"
export UV_CACHE_DIR="${VSU_PROJECT_DIR}/envs/uv-cache"
export UV_PYTHON_INSTALL_DIR="${VSU_PROJECT_DIR}/envs/python"
export UV_PROJECT_ENVIRONMENT="${VSU_PROJECT_DIR}/envs/vsu"
case ":${PATH}:" in
  *":${UV_INSTALL_DIR}:"*) ;;
  *) export PATH="${UV_INSTALL_DIR}:${PATH}" ;;
esac
# Activate the project environment when it exists so `python` and `pytest` resolve to it.
if [[ -f "${UV_PROJECT_ENVIRONMENT}/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "${UV_PROJECT_ENVIRONMENT}/bin/activate"
fi

# --- Hugging Face: tokenizers parallelism warning off, offline by default in jobs -------
export TOKENIZERS_PARALLELISM=false
# Jobs set HF_HUB_OFFLINE=1 (weights are pre-downloaded); download_models.sh unsets it.

# --- Secrets: API keys live in a mode 600 file under home, never in the repo -----------
export VSU_SECRETS_FILE="${VSU_SECRETS_FILE:-${HOME}/.config/vsu/secrets.env}"
if [[ -f "${VSU_SECRETS_FILE}" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "${VSU_SECRETS_FILE}"
  set +a
fi
