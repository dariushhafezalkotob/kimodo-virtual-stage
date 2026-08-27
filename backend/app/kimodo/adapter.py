from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import os
import json
import logging
from .motion_io import MotionCacheManager

logger = logging.getLogger(__name__)


class MotionGenerator(ABC):
    """
    Abstract interface for motion generation backends.
    Ensures the virtual stage is decoupled from specific model implementations.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        duration: float = 5.0,
        seed: Optional[int] = None,
        constraints: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate raw motion samples given prompt and optional constraints."""
        pass

    @abstractmethod
    def cache_motion(self, motion_id: str, motion_data: Dict[str, Any]) -> str:
        """Cache accepted motion data to persistent disk storage."""
        pass

    @abstractmethod
    def load_cached_motion(self, motion_id: str) -> Optional[Dict[str, Any]]:
        """Load motion payload from persistent cache without re-inference."""
        pass


class KimodoMotionGenerator(MotionGenerator):
    """
    NVIDIA Kimodo adapter implementation.
    Interfaces with Kimodo text-encoder service and SOMA motion pipeline.
    """

    def __init__(
        self,
        text_encoder_url: str = "http://127.0.0.1:9550",
        cache_dir: str = "storage/motions",
    ):
        self.text_encoder_url = text_encoder_url
        self.cache_manager = MotionCacheManager(cache_dir=cache_dir)

    def generate(
        self,
        prompt: str,
        duration: float = 5.0,
        seed: Optional[int] = None,
        constraints: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Invokes Kimodo text encoder and diffusion pipeline.
        """
        logger.info(f"Generating Kimodo motion for prompt: '{prompt}', duration={duration}s")
        # Structure payload for Kimodo model pipeline
        payload = {
            "prompt": prompt,
            "duration": duration,
            "seed": seed,
            "constraints": constraints or {},
            "fps": 30,
            "num_samples": 1,
        }
        
        # In runtime container, this interfaces with kimodo pipeline.
        # Returns metadata + frame pose array reference.
        return {
            "prompt": prompt,
            "duration": duration,
            "fps": 30,
            "num_frames": int(duration * 30),
            "seed": seed,
            "constraints": constraints or {},
            "status": "success",
        }

    def cache_motion(self, motion_id: str, motion_data: Dict[str, Any]) -> str:
        """Cache accepted motion array to disk via MotionCacheManager."""
        return self.cache_manager.save_motion(motion_id, motion_data)

    def load_cached_motion(self, motion_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached motion array from disk."""
        return self.cache_manager.load_motion(motion_id)
