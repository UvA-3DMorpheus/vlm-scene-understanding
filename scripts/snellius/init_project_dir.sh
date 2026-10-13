#!/usr/bin/env bash
# Create the shared project layout (PLAN.md Section 2.1) once, with group permissions:
# the whole prjs2306 group can read everything, and results and logs are group writable
# so both owners can write run outputs and SLURM logs.
#
#     bash scripts/snellius/init_project_dir.sh
#
# Also copies the small versioned data (smoke set, material table, annotations) from the
# repository into the project space, since runs read the project copy (VSU_DATA_ROOT).
# Safe to rerun: it only creates what is missing and reapplies permissions.
set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/env.sh"

root="${VSU_PROJECT_DIR}"
echo "Initializing ${root} for group ${VSU_GROUP}"

dirs=(
  data/sim
  data/physion_pp
  data/smoke
  data/materials
  data/annotations
  models/hf
  models/vllm
  results/vlm-scene-understanding
  results/vlm-scene-understanding/.cache
  envs
  logs/vlm-scene-understanding
)
for d in "${dirs[@]}"; do
  mkdir -p "${root}/${d}"
done

# Versioned small data: repo -> project space. rsync keeps reruns cheap.
for sub in smoke materials annotations; do
  if [[ -d "${VSU_REPO_DIR}/data/${sub}" ]]; then
    rsync -a --exclude '.gitkeep' "${VSU_REPO_DIR}/data/${sub}/" "${root}/data/${sub}/"
  fi
done
if [[ -f "${VSU_REPO_DIR}/data/README.md" ]]; then
  cp "${VSU_REPO_DIR}/data/README.md" "${root}/data/README.md"
fi

# Group ownership and permissions. setgid on directories makes new files inherit the group.
chgrp -R "${VSU_GROUP}" "${root}"
chmod -R g+rX "${root}"
find "${root}" -type d -exec chmod g+s {} +
chmod -R g+w "${root}/results" "${root}/logs"
# The uv environment, caches and model weights are also shared so one download serves both owners.
chmod -R g+w "${root}/envs" "${root}/models"

echo "Done. Layout:"
find "${root}" -maxdepth 2 -type d | sort
