from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Project:
    """
    Project data representation matching Master Build Specification.
    """

    name: str = "Untitled Stage Project"
    version: int = 1
    duration: float = 15.0
    fps: int = 30
    actors: List[Dict[str, Any]] = field(default_factory=list)
    timeline: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_format_version": self.version,
            "name": self.name,
            "duration": self.duration,
            "fps": self.fps,
            "actors": self.actors,
            "timeline": self.timeline,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        return cls(
            name=data.get("name", "Untitled Stage Project"),
            version=data.get("project_format_version", 1),
            duration=data.get("duration", 15.0),
            fps=data.get("fps", 30),
            actors=data.get("actors", []),
            timeline=data.get("timeline", {}),
        )
