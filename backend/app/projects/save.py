import os
import json
import logging
from typing import Dict, Any
from .project import Project

logger = logging.getLogger(__name__)


def save_project(project: Project, storage_dir: str = "storage/projects") -> str:
    """
    Saves project definition JSON to persistent storage.
    """
    os.makedirs(storage_dir, exist_ok=True)
    filename = f"{project.name.lower().replace(' ', '_')}.json"
    filepath = os.path.join(storage_dir, filename)

    with open(filepath, "w") as f:
        json.dump(project.to_dict(), f, indent=2)

    logger.info(f"Project saved successfully: {filepath}")
    return filepath
