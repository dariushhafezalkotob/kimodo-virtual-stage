# NVIDIA Dependency Version Pinning

This document tracks the exact commits, base images, and models used for Kimodo AI Virtual Stage.

| Component | Pinned Specification |
| :--- | :--- |
| **Kimodo Commit** | `1aece8c124d73d255ceff5086d983b844c9f4e94` (`git+https://github.com/nv-tlabs/kimodo.git@1aece8c124d73d255ceff5086d983b844c9f4e94`) |
| **Kimodo-Viser Commit** | `7c82ad8f8640bad9dff8ded5c5eee908eeb08f11` (`git+https://github.com/nv-tlabs/kimodo-viser.git@7c82ad8f8640bad9dff8ded5c5eee908eeb08f11`) |
| **SOMA-X Commit** | `9afc124d1adfbc4ba73a747a94fbd5172188a385` (`git+https://github.com/NVlabs/SOMA-X.git@9afc124d1adfbc4ba73a747a94fbd5172188a385`) |
| **Docker Base Image** | `nvcr.io/nvidia/pytorch:24.10-py3` |
| **Target GPU** | NVIDIA L40S (48 GB VRAM) |
| **Models** | `nvidia/Kimodo-SOMA-RP-v1`, `nvidia/Kimodo-G1-RP-v1` |
| **Text Encoder Model** | `meta-llama/Meta-Llama-3-8B-Instruct` |
