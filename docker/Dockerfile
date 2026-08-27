# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# Hugging Face Spaces Docker template for Kimodo Virtual Stage.
# Runs BOTH:
# - kimodo_textencoder (Gradio on 9550, internal)
# - kimodo_demo        (Viser UI on 7860, public)
#
FROM nvcr.io/nvidia/pytorch:24.10-py3

# Avoid interactive prompts + make pip reproducible/quieter
ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Persist HF caches on Spaces when /data is enabled.
    HF_HOME=/data/.huggingface \
    XDG_CACHE_HOME=/data/.cache \
    PIP_CACHE_DIR=/data/.cache/pip

# Where code lives inside container
WORKDIR /workspace

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
      git curl ca-certificates \
      cmake build-essential \
    && rm -rf /var/lib/apt/lists/*

# Remove broken system cmake shim if present
RUN rm -f /usr/local/bin/cmake || true

# Copy pinned requirements
COPY requirements.txt /workspace/requirements.txt

ARG GITHUB_TOKEN=

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=secret,id=GITHUB_TOKEN,mode=0444,required=false \
    python -m pip install --upgrade pip \
 && python -m pip install -r requirements.txt;

COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 7860
ENTRYPOINT ["/start.sh"]
