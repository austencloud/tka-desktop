"""
Domain model for the Codex Exporter.
"""
from enum import StrEnum
from dataclasses import dataclass


class GridMode(StrEnum):
    """Grid mode for pictograph rendering."""
    DIAMOND = "diamond"
    BOX = "box"


@dataclass(slots=True)
class TurnConfig:
    """Configuration for pictograph turns."""
    red: float = 0.0
    blue: float = 0.0
    generate_all: bool = False
    grid_mode: GridMode = GridMode.DIAMOND
