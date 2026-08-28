#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

cd /workspace

export PYTHONPATH="/workspace:${PYTHONPATH:-}"

# Export HF tokens
export HF_TOKEN="${HF_TOKEN:-${HUGGING_FACE_HUB_TOKEN:-}}"
export HUGGING_FACE_HUB_TOKEN="${HF_TOKEN}"

# Pre-download checkpoints
python - <<'PY'
import os
from huggingface_hub import snapshot_download
token = os.environ.get("HF_TOKEN") or None
snapshot_download("nvidia/Kimodo-SOMA-RP-v1", token=token)
snapshot_download("nvidia/Kimodo-G1-RP-v1", token=token)
print("Checkpoint download complete.")
PY

# Launch ungated text encoder on port 9550
echo "Starting ungated text-encoder on :9550 ..."
python3 run_ungated_text_encoder.py &
TEXT_ENCODER_PID=$!

cleanup() {
  echo "Shutting down text-encoder (pid=${TEXT_ENCODER_PID}) ..."
  kill "${TEXT_ENCODER_PID}" >/dev/null 2>&1 || true
}
trap cleanup EXIT

# Wait for text encoder readiness
echo "Waiting for text-encoder health ..."
for i in $(seq 1 1200); do
  if curl -fsS "http://127.0.0.1:9550/" >/dev/null 2>&1; then
    echo "Text-encoder is up."
    break
  fi
  sleep 1
  if [[ $i -eq 1200 ]]; then
    echo "ERROR: text-encoder did not become healthy on http://127.0.0.1:9550/ within 1200s" >&2
    exit 1
  fi
done

# Launch public Viser demo
echo "Starting demo on :7860 ..."
exec kimodo_demo
