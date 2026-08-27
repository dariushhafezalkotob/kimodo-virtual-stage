---
title: Kimodo AI Virtual Stage
emoji: 🏃
colorFrom: blue
colorTo: green
sdk: docker
pinned: true
license: apache-2.0
short_description: "Official NVIDIA Kimodo Viser UI & AI Virtual Stage"
models:
- nvidia/Kimodo-SOMA-RP-v1
- nvidia/Kimodo-G1-RP-v1
---

# Kimodo AI Virtual Stage

AI-powered virtual stage application built on official NVIDIA Kimodo (`nv-tlabs/kimodo`), NVIDIA Viser (`nv-tlabs/kimodo-viser`), and NVIDIA SOMA-X (`NVlabs/SOMA-X`).

## Architecture & Official NVIDIA UI

This repository deploys the **exact official NVIDIA Kimodo Viser interface** ([https://huggingface.co/spaces/nvidia/Kimodo](https://huggingface.co/spaces/nvidia/Kimodo) & [https://research.nvidia.com/labs/sil/projects/kimodo/](https://research.nvidia.com/labs/sil/projects/kimodo/)):
- **3D Canvas & Renderer**: Official Viser WebGL canvas with SOMA human character meshes.
- **Interactive Controls**: End-effector 3D pose handles (hands, feet), 2D root path drawing, full-body keyframes, text prompt inputs, and timeline controls.
- **Port 7860**: Public Viser Web UI (`kimodo_demo`).
- **Port 9550**: Internal Text Encoder service (`kimodo_textencoder`).

## Hugging Face Docker Space Deployment

1. Create a Space on Hugging Face using **Docker** SDK and **NVIDIA L40S** GPU.
2. In Space Settings -> Secrets, configure:
   - `HF_TOKEN`: Hugging Face User Access Token with permission for `meta-llama/Meta-Llama-3-8B-Instruct`.
3. The Space will launch `docker/start.sh`, initializing `kimodo_textencoder` on port 9550 and serving `kimodo_demo` on port 7860.

## Local / Container Execution

```bash
# Clone repository
git clone https://github.com/dariushhafezalkotob/kimodo-virtual-stage.git
cd kimodo-virtual-stage

# Install dependencies
pip install -r requirements.txt

# Launch demo
python3 run_demo.py
```
