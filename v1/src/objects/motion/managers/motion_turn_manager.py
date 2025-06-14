from typing import TYPE_CHECKING, Union

from enums.glyph_enum
 import Turns
from data.constants import BLUE, RED

if TYPE_CHECKING:
    from objects.motion.motion import Motion


class MotionTurnsManager:
    def __init__(self, motion: "Motion") -> None:
        self.motion = motion

    def adjust_turns(self, adjustment: float) -> None:
        """Adjust the turns of a given motion object"""
        new_turns = MotionTurnsManager.clamp_turns(self.motion.state.turns + adjustment)
        self.motion.state.turns_manager.set_motion_turns(new_turns)

    def set_turns(self, new_turns: Turns) -> None:
        """set the turns for a given motion object"""
        clamped_turns = MotionTurnsManager.clamp_turns(new_turns)
        self.motion.state.turns_manager.set_motion_turns(clamped_turns)

    @staticmethod
    def clamp_turns(turns: Turns) -> Turns:
        """Clamp the turns value to be within allowable range"""
        return max(0, min(3, turns))

    @staticmethod
    def convert_turn_floats_to_ints(turns: Turns) -> Turns:
        """Convert turn values that are whole numbers from float to int"""
        return int(turns) if turns in [0.0, 1.0, 2.0, 3.0] else turns

    def add_half_turn(self) -> None:
        """Add half a turn to the motion"""
        self.adjust_turns(self.motion, 0.5)

    def subtract_half_turn(self) -> None:
        """Subtract half a turn from the motion"""
        self.adjust_turns(self.motion, -0.5)

    def add_turn(self) -> None:
        """Add a full turn to the motion"""
        self.adjust_turns(self.motion, 1)

    def subtract_turn(self) -> None:
        """Subtract a full turn from the motion"""
        self.adjust_turns(self.motion, -1)

    def set_motion_turns(self, turns: Union[str, int, float]) -> None:
        self.motion.state.turns = turns
        self.motion.arrow.motion.state.turns = turns
        other_motion_color = RED if self.motion.state.color == BLUE else BLUE
        other_motion = self.motion.pictograph.managers.get.other_motion(self.motion)
        arrow_data = {
            f"{self.motion.state.color}_attributes": {TURNS: turns},
            f"{other_motion_color}_attributes": {TURNS: other_motion.state.turns},
        }
        self.motion.arrow.updater.update_arrow(arrow_data)
