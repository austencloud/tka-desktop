from typing import Literal
from data.constants import BOX, DIAMOND
from objects.motion.managers.handpath_calculator import (
    HandpathCalculator,
)
from objects.motion.motion import Motion


class BaseDirectionalGenerator:
    def __init__(self, motion: Motion) -> None:
        self.motion = motion
        self.other_motion = motion.pictograph.get.other_motion(motion)
        self.hand_rot_dir_calculator = HandpathCalculator()

    def generate_directional_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        raise NotImplementedError("Subclasses must implement this method.")

    def _get_grid_mode(self) -> Literal["box"] | Literal["diamond"]:
        if self.motion.prop.loc in ["ne", "nw", "se", "sw"]:
            grid_mode = BOX
        elif self.motion.prop.loc in ["n", "s", "e", "w"]:
            grid_mode = DIAMOND
        return grid_mode
