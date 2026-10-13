#!/usr/bin/env bash
# Download the open model weights configured in configs/models/*.yaml into HF_HOME.
# Run once on a node with network (login node, or a job if the proxy works), after
# setup_env.sh.
#
#     bash scripts/snellius/download_models.sh                   # every hf backend config
#     bash scripts/snellius/download_models.sh Qwen/Qwen3-VL-8B-Instruct   # explicit repos
#
# Consumes: model configs (fields `backend: hf` and `hf_id`) or explicit repo ids.
# Produces: weights under HF_HOME/hub, shared by both owners.
set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/env.sh"
unset HF_HUB_OFFLINE
cd "${VSU_REPO_DIR}"

if [[ $# -gt 0 ]]; then
  repos=("$@")
else
  mapfile -t repos < <(uv run python - <<'PY'
import glob
import yaml

seen = set()
for path in sorted(glob.glob("configs/models/*.yaml")):
    cfg = yaml.safe_load(open(path)) or {}
    repo = cfg.get("hf_id")
    if cfg.get("backend") == "hf" and repo and repo not in seen:
        seen.add(repo)
        print(repo)
PY
)
fi

if [[ ${#repos[@]} -eq 0 ]]; then
  echo "No hf models configured in configs/models/; pass repo ids explicitly." >&2
  exit 1
fi

# `hf` is the current CLI name in huggingface_hub; `huggingface-cli` is the older alias.
if uv run hf --help >/dev/null 2>&1; then
  dl=(uv run hf download)
else
  dl=(uv run huggingface-cli download)
fi

for repo in "${repos[@]}"; do
  echo "Downloading ${repo} into ${HF_HOME}"
  "${dl[@]}" "${repo}"
done
echo "Done. Disk use of HF_HOME:"
du -sh "${HF_HOME}"
