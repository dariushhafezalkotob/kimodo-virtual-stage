import os
import json
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


class MotionCacheManager:
    """
    Handles serialization and deserialization of accepted Kimodo motion arrays
    and metadata to persistent storage (.npz / .json).
    Guarantees zero GPU inference requirement during timeline playback.
    """

    def __init__(self, cache_dir: str = "storage/motions"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def get_motion_filepath(self, motion_id: str) -> str:
        ext = ".npz" if HAS_NUMPY else ".json"
        return os.path.join(self.cache_dir, f"{motion_id}{ext}")

    def get_meta_filepath(self, motion_id: str) -> str:
        return os.path.join(self.cache_dir, f"{motion_id}_meta.json")

    def save_motion(self, motion_id: str, motion_data: Dict[str, Any]) -> str:
        """
        Saves motion arrays and metadata.
        """
        motion_path = self.get_motion_filepath(motion_id)
        meta_path = self.get_meta_filepath(motion_id)

        poses = motion_data.get("poses")
        root_trans = motion_data.get("root_trans")

        if HAS_NUMPY:
            if poses is None:
                poses = np.zeros((150, 24, 3), dtype=np.float32)
            if root_trans is None:
                root_trans = np.zeros((150, 3), dtype=np.float32)
            np.savez_compressed(motion_path, poses=poses, root_trans=root_trans)
        else:
            payload = {
                "poses": poses if poses is not None else [],
                "root_trans": root_trans if root_trans is not None else [],
            }
            with open(motion_path, "w") as f:
                json.dump(payload, f)

        metadata = {
            "motion_id": motion_id,
            "prompt": motion_data.get("prompt", ""),
            "duration": motion_data.get("duration", 5.0),
            "fps": motion_data.get("fps", 30),
            "constraints": motion_data.get("constraints", {}),
        }

        with open(meta_path, "w") as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"Saved motion cache: {motion_path}")
        return motion_path

    def load_motion(self, motion_id: str) -> Optional[Dict[str, Any]]:
        """
        Loads cached motion arrays and metadata from disk.
        """
        motion_path = self.get_motion_filepath(motion_id)
        meta_path = self.get_meta_filepath(motion_id)

        if not os.path.exists(motion_path) or not os.path.exists(meta_path):
            logger.warning(f"Motion cache not found: {motion_id}")
            return None

        with open(meta_path, "r") as f:
            metadata = json.load(f)

        if HAS_NUMPY and motion_path.endswith(".npz"):
            arrays = np.load(motion_path)
            metadata["poses"] = arrays["poses"]
            metadata["root_trans"] = arrays["root_trans"]
        else:
            with open(motion_path, "r") as f:
                payload = json.load(f)
            metadata["poses"] = payload.get("poses")
            metadata["root_trans"] = payload.get("root_trans")

        return metadata
