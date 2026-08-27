import os
import json
import logging
from typing import Optional
from .project import Project

logger = logging.getLogger(__name__)


def load_project(filepath: str) -> Optional[Project]:
    """
    Loads project definition JSON from file path.
    """
    if not os.path.exists(filepath):
        logger.error(f"Project file not found: {filepath}")
        return None

    with open(filepath, "r") as f:
        data = json.load(f)

    logger.info(f"Loaded project: {filepath}")
    return Project.from_dict(data)
