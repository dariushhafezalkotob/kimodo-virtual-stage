from typing import Dict, Any, Optional
import logging
from .scene import Scene
from ..actors.actor_manager import ActorManager

logger = logging.getLogger(__name__)


class SceneManager:
    """
    Master Scene Manager for Kimodo AI Virtual Stage.
    Synchronizes multi-actor states, master timeline playback, and 3D stage rendering.
    """

    def __init__(self):
        self.scene = Scene()
        self.actor_manager = ActorManager()
        self.is_playing: bool = False
        self.master_clock: float = 0.0

    def play(self):
        """Starts master timeline playback across all actors synchronously."""
        self.is_playing = True
        logger.info("Master timeline playback started.")

    def pause(self):
        """Pauses master timeline playback."""
        self.is_playing = False
        logger.info("Master timeline playback paused.")

    def stop(self):
        """Stops master timeline playback and resets clock to 0."""
        self.is_playing = False
        self.master_clock = 0.0
        logger.info("Master timeline playback stopped.")

    def seek(self, timecode: float):
        """Seeks master timeline clock to specific second timestamp."""
        self.master_clock = max(0.0, min(timecode, self.scene.duration))
        logger.info(f"Master timeline seeked to: {self.master_clock:.2f}s")

    def get_scene_state(self) -> Dict[str, Any]:
        """Returns unified master scene state payload."""
        return {
            "scene": self.scene.to_dict(),
            "actors": self.actor_manager.list_actors(),
            "active_actor_id": self.actor_manager.active_actor_id,
            "is_playing": self.is_playing,
            "master_clock": self.master_clock,
        }
