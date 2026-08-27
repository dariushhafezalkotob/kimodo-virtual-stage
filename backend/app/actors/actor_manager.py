from typing import Dict, List, Optional, Any
import copy
from .actor import Actor


class ActorManager:
    """
    Manages actor registry, selection state, transformations, and motion assignments.
    """

    def __init__(self):
        self.actors: Dict[str, Actor] = {}
        self.active_actor_id: Optional[str] = None
        self._counter = 1

    def create_actor(
        self,
        name: Optional[str] = None,
        position: Optional[List[float]] = None,
        rotation: Optional[List[float]] = None,
    ) -> Actor:
        actor_id = f"actor_{self._counter:03d}"
        actor_name = name or f"Actor {self._counter:02d}"
        self._counter += 1

        actor = Actor(
            id=actor_id,
            name=actor_name,
            position=position or [0.0, 0.0, 0.0],
            rotation=rotation or [0.0, 0.0, 0.0],
        )

        self.actors[actor_id] = actor

        # If it's the first actor created, select it by default
        if len(self.actors) == 1:
            self.select_actor(actor_id)

        return actor

    def select_actor(self, actor_id: Optional[str]) -> Optional[Actor]:
        """Sets active actor selection and unselects previous actors."""
        for a_id, actor in self.actors.items():
            actor.selected = (a_id == actor_id)

        if actor_id and actor_id in self.actors:
            self.active_actor_id = actor_id
            return self.actors[actor_id]
        
        self.active_actor_id = None
        return None

    def get_active_actor(self) -> Optional[Actor]:
        if self.active_actor_id and self.active_actor_id in self.actors:
            return self.actors[self.active_actor_id]
        return None

    def update_transform(
        self,
        actor_id: str,
        position: Optional[List[float]] = None,
        rotation: Optional[List[float]] = None,
        scale: Optional[float] = None,
    ) -> Optional[Actor]:
        actor = self.actors.get(actor_id)
        if not actor:
            return None

        if position is not None:
            actor.position = position
        if rotation is not None:
            actor.rotation = rotation
        if scale is not None:
            actor.scale = scale

        return actor

    def assign_motion(
        self, actor_id: str, motion_id: str, timeline_start: float = 0.0
    ) -> Optional[Actor]:
        actor = self.actors.get(actor_id)
        if not actor:
            return None

        actor.motion_id = motion_id
        actor.timeline_start = timeline_start
        return actor

    def duplicate_actor(self, actor_id: str) -> Optional[Actor]:
        original = self.actors.get(actor_id)
        if not original:
            return None

        new_actor = self.create_actor(
            name=f"{original.name} (Copy)",
            position=[original.position[0] + 0.5, original.position[1], original.position[2]],
            rotation=copy.deepcopy(original.rotation),
        )
        new_actor.motion_id = original.motion_id
        new_actor.timeline_start = original.timeline_start
        return new_actor

    def delete_actor(self, actor_id: str) -> bool:
        if actor_id in self.actors:
            del self.actors[actor_id]
            if self.active_actor_id == actor_id:
                remaining_ids = list(self.actors.keys())
                self.select_actor(remaining_ids[0] if remaining_ids else None)
            return True
        return False

    def list_actors(self) -> List[Dict[str, Any]]:
        return [actor.to_dict() for actor in self.actors.values()]
