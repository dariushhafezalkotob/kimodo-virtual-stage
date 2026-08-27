"""
Generation pipeline utilities and parameter configuration for NVIDIA Kimodo.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List


@dataclass
class GenerationConfig:
    prompt: str
    duration: float = 5.0
    fps: int = 30
    seed: Optional[int] = None
    num_samples: int = 1
    diffusion_steps: int = 50
    guidance_scale: float = 7.5
    transition_frames: int = 10
    constraints: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "prompt": self.prompt,
            "duration": self.duration,
            "fps": self.fps,
            "seed": self.seed,
            "num_samples": self.num_samples,
            "diffusion_steps": self.diffusion_steps,
            "guidance_scale": self.guidance_scale,
            "transition_frames": self.transition_frames,
            "constraints": self.constraints,
        }
