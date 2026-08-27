from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from ..actors.actor_manager import ActorManager


@dataclass
class Scene:
    """
    Master Scene state representation.
    """

    id: str = "scene_001"
    name: str = "Master Scene"
    duration: float = 15.0
    fps: int = 30
    loop: bool = False
    master_time: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "duration": self.duration,
            "fps": self.fps,
            "loop": self.loop,
            "master_time": self.master_time,
        }
