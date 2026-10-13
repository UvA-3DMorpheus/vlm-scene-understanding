#!/usr/bin/env bash
# Create or update the Python environment in the project space with uv.
#
#     bash scripts/snellius/setup_env.sh            # core + dev + hf + api extras
#     bash scripts/snellius/setup_env.sh --no-gpu   # core + dev + api only (login node tests)
#
# Installs uv into VSU_PROJECT_DIR/envs/bin if missing, lets uv install the managed
# CPython 3.11 from .python-version into VSU_PROJECT_DIR/envs/python, and syncs the
# locked dependencies into VSU_PROJECT_DIR/envs/vsu. Needs outbound network (login node).
set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/env.sh"
unset HF_HUB_OFFLINE

mkdir -p "${UV_INSTALL_DIR}" "${UV_CACHE_DIR}" "${UV_PYTHON_INSTALL_DIR}"

if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv into ${UV_INSTALL_DIR}"
  curl -sSfL https://astral.sh/uv/install.sh | UV_NO_MODIFY_PATH=1 sh
fi
uv --version

cd "${VSU_REPO_DIR}"
uv python install            # version from .python-version, into UV_PYTHON_INSTALL_DIR

if [[ "${1:-}" == "--no-gpu" ]]; then
  uv sync --extra api
else
  uv sync --extra api --extra hf
fi

echo "Environment ready at ${UV_PROJECT_ENVIRONMENT}"
echo "Checking: $(uv run python -c 'import sys, vsu; print(sys.version.split()[0], "vsu", vsu.__version__)')"
