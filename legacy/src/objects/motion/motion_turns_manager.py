from typing import TYPE_CHECKING, Union

from data.constants import BLUE, RED

Turns = Union[int, float, str]
if TYPE_CHECKING:
    from objects.motion.motion import Motion


class MotionTurnsManager:
    def __init__(self, motion: "Motion") -> None:
        self.motion = motion

    @staticmethod
    def clamp_turns(turns: Turns) -> Turns:
        """Clamp the turns value to be within allowable range"""
        # if turns is 'fl', just return 'fl'
        if turns == "fl":
            return turns
        return max(0, min(3, turns))

    def set_motion_turns(self, turns: Union[str, int, float]) -> None:
        self.motion.state.turns = turns
