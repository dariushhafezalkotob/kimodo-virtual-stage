#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

cd /workspace

export PYTHONUNBUFFERED=1
export PYTHONPATH="/workspace:${PYTHONPATH:-}"

# Optimize PyTorch CUDA memory allocation
export PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True"

# Run text encoder on CPU to preserve 100% of GPU VRAM for Kimodo motion diffusion model
export TEXT_ENCODER_DEVICE="cpu"

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
print("Checkpoint download complete.", flush=True)
PY

# Launch ungated text encoder on CPU on port 9550
echo "Starting ungated text-encoder on CPU :9550 ..."
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
    echo "Text-encoder is up and healthy on port 9550."
    break
  fi
  sleep 1
  if [[ $i -eq 1200 ]]; then
    echo "ERROR: text-encoder did not become healthy on http://127.0.0.1:9550/ within 1200s" >&2
    exit 1
  fi
done

# Launch public Viser demo on GPU
echo "Starting demo on :7860 ..."
exec kimodo_demo
