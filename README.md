---
title: Kimodo AI Virtual Stage
emoji: 🏃
colorFrom: blue
colorTo: green
sdk: docker
pinned: true
license: apache-2.0
short_description: "Browser-based multi-actor AI virtual stage powered by NVIDIA Kimodo"
models:
- nvidia/Kimodo-SOMA-RP-v1
- nvidia/Kimodo-G1-RP-v1
---

# Kimodo AI Virtual Stage - Phase 0

AI-powered browser-based virtual stage and virtual cinematography application based on NVIDIA Kimodo.

## Phase 0 Status

Phase 0 reproduces NVIDIA's official baseline interactive Kimodo demo running inside a Hugging Face Docker Space environment.

### Ports
- `7860`: Public Viser 3D Web UI
- `9550`: Internal Text Encoder (`kimodo_textencoder`)

### Requirements
- **Hugging Face Secret**: `HF_TOKEN` with granted access to `meta-llama/Meta-Llama-3-8B-Instruct`.
- **GPU**: Recommended NVIDIA L40S (48 GB VRAM), minimum ~17 GB VRAM.

## Verification / Acceptance Test
Prompt to verify:
> "A person walks forward and waves with the right hand."
