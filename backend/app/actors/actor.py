from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class Actor:
    """
    SOMA 3D Actor representation in virtual stage.
    """

    id: str
    name: str
    visible: bool = True
    position: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    rotation: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    scale: float = 1.0
    selected: bool = False
    motion_id: Optional[str] = None
    timeline_start: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "visible": self.visible,
            "position": self.position,
            "rotation": self.rotation,
            "scale": self.scale,
            "selected": self.selected,
            "motion_id": self.motion_id,
            "timeline_start": self.timeline_start,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Actor":
        return cls(
            id=data["id"],
            name=data["name"],
            visible=data.get("visible", True),
            position=data.get("position", [0.0, 0.0, 0.0]),
            rotation=data.get("rotation", [0.0, 0.0, 0.0]),
            scale=data.get("scale", 1.0),
            selected=data.get("selected", False),
            motion_id=data.get("motion_id"),
            timeline_start=data.get("timeline_start", 0.0),
        )
