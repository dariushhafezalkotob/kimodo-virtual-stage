from typing import Dict, Any, List
from ..actors.actor import Actor


class MasterTimeline:
    """
    Computes per-actor frame evaluation and master clock synchronization.
    """

    def __init__(self, duration: float = 15.0, fps: int = 30):
        self.duration = duration
        self.fps = fps

    def evaluate_actor_frame(self, actor: Actor, master_time: float) -> Dict[str, Any]:
        """
        Evaluates local frame index for an actor based on master_time and timeline_start offset.
        """
        local_time = master_time - actor.timeline_start
        if local_time < 0:
            return {"active": False, "frame": 0, "local_time": local_time}

        local_frame = int(local_time * self.fps)
        return {
            "active": True,
            "frame": local_frame,
            "local_time": local_time,
        }
