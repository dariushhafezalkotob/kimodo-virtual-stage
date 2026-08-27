#!/usr/bin/env python3
"""
Kimodo AI Virtual Stage - Official NVIDIA Kimodo Viser Launcher

Launches NVIDIA's official kimodo_demo Viser server on port 7860.
Serves the exact official NVIDIA Kimodo web interface with SOMA character models,
3D canvas, end-effector 3D gizmos, root path controls, and timeline keyframe tracks.
"""

import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("KimodoOfficialDemo")


def main():
    logger.info("Starting official NVIDIA Kimodo Viser UI demo on port 7860...")
    try:
        # Launch official NVIDIA kimodo_demo binary
        subprocess.run(["kimodo_demo"], check=True)
    except FileNotFoundError:
        logger.error(
            "kimodo_demo command not found. Ensure kimodo and kimodo-viser packages are installed:\n"
            "  pip install -r requirements.txt"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
