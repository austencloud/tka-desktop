from typing import TYPE_CHECKING, Union

from data.constants import BLUE, RED, TURNS

Turns = Union[int, float]

if TYPE_CHECKING:
    from objects.motion.motion import Motion


class MotionTurnsManager:
    def __init__(self, motion: "Motion") -> None:
        self.motion = motion

    def adjust_turns(self, adjustment: float) -> None:
        """Adjust the turns of a given motion object"""
        current_turns = self.motion.state.turns
        if isinstance(current_turns, str):
            current_turns = (
                float(current_turns) if current_turns.replace(".", "").isdigit() else 0
            )
        new_turns = MotionTurnsManager.clamp_turns(current_turns + adjustment)
        self.set_motion_turns(new_turns)

    def set_turns(self, new_turns: Turns) -> None:
        """set the turns for a given motion object"""
        clamped_turns = MotionTurnsManager.clamp_turns(new_turns)
        self.set_motion_turns(clamped_turns)

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
        self.adjust_turns(0.5)

    def subtract_half_turn(self) -> None:
        """Subtract half a turn from the motion"""
        self.adjust_turns(-0.5)

    def add_turn(self) -> None:
        """Add a full turn to the motion"""
        self.adjust_turns(1)

    def subtract_turn(self) -> None:
        """Subtract a full turn from the motion"""
        self.adjust_turns(-1)

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
