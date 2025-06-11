# domain/arrow_placement_context.py
from dataclasses import dataclass

from enums.letter.letter import Letter


@dataclass
class ArrowPlacementContext:
    grid_mode: str  # e.g. DIAMOND or BOX
    motion_type: str  # e.g. PRO, ANTI, FLOAT, DASH, or STATIC
    letter: Letter  # the letter associated with the pictograph
    arrow_color: str  # color of the arrow (from state)
    turns: float  # number of turns in the motion
    start_ori: str  # orientation of the arrow at the start of the motion
