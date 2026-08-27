# Deployment Guide: Kimodo AI Virtual Stage (Phase 0)

## Hugging Face Docker Space Deployment

1. **Create Space**:
   - Create a new Space on Hugging Face.
   - Select **Docker** SDK.
   - Select hardware instance: **NVIDIA L40S** (48GB VRAM) or **L4** (24GB VRAM).

2. **Configure Secrets**:
   In Hugging Face Space Settings -> **Secrets**, add:
   - `HF_TOKEN`: Your Hugging Face Access Token. Ensure your HF account has accepted the license for `meta-llama/Meta-Llama-3-8B-Instruct`.
   - `GITHUB_TOKEN` *(optional)*: GitHub personal access token if cloning private repositories during build.

3. **Persistent Storage**:
   - Enable Space Persistent Storage mounted at `/data`.
   - Caches for Hugging Face models (`/data/.huggingface`), XDG (`/data/.cache`), and pip (`/data/.cache/pip`) will automatically persist across container restarts.

## Local Docker Execution

```bash
cd /Users/macpro/.gemini/antigravity/scratch/kimodo-virtual-stage

# Build the container
docker build -f docker/Dockerfile -t kimodo-virtual-stage .

# Run container with GPU access and Hugging Face token secret
docker run --gpus all \
  -p 7860:7860 \
  -e HF_TOKEN="your_hf_token" \
  kimodo-virtual-stage
```

## Runtime Architecture & Services
1. **Text Encoder Service**: `kimodo_textencoder` starts internally on port `9550`.
2. **Health Check**: `docker/start.sh` polls `http://127.0.0.1:9550/` until ready.
3. **Public Interface**: `kimodo_demo` launches Viser server bound to port `7860`.
