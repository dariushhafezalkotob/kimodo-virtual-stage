# Official NVIDIA Kimodo Viser UI Guide

This guide details launching and running the official **NVIDIA Kimodo Viser Web Application** ([https://huggingface.co/spaces/nvidia/Kimodo](https://huggingface.co/spaces/nvidia/Kimodo)).

---

## 🏃 Running the Official Kimodo Viser Application

### Option A: Hugging Face Docker Space (Recommended)
1. Push this repository to your Hugging Face Docker Space with **NVIDIA L40S** GPU.
2. Add your secret `HF_TOKEN` in Space Settings (with access to `meta-llama/Meta-Llama-3-8B-Instruct`).
3. The Space will automatically build the environment and serve the official NVIDIA Kimodo Viser web application on port `7860`.

### Option B: Local / Docker Instance
```bash
docker build -f docker/Dockerfile -t kimodo-virtual-stage .
docker run --gpus all -p 7860:7860 -e HF_TOKEN="your_hf_token" kimodo-virtual-stage
```

---

## 🎨 Official UI Capabilities & Features

When `kimodo_demo` launches on port `7860`, the official Viser client renders:

1. **Official 3D Canvas**:
   - SOMA human character meshes rendered with realistic joint articulation.
   - Interactive 3D Orbit & Pan controls.

2. **3D Constraint Controls**:
   - **Hand & Foot End-Effectors**: 3D interactive handles to set target keyframe locations for left hand, right hand, left foot, and right foot.
   - **Full-Body Keyframe Widgets**: Pose keyframe controls.
   - **Root Waypoints & 2D Root Path**: Draw 2D trajectory paths for the character to follow.

3. **Motion Generation & Timeline**:
   - Text prompt input box for diffusion guidance.
   - Sample generation selector.
   - Keyframe timeline track view for scrubbing and playing back generated motion sequences.
