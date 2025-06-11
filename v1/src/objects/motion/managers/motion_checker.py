from data.constants import ANTI, DASH, FLOAT, PRO, STATIC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.motion.motion import Motion


class MotionChecker:
    def __init__(self, motion: "Motion") -> None:
        self.motion = motion

    def is_shift(self) -> bool:
        return self.motion.state.motion_type in [PRO, ANTI, FLOAT]

    def is_dash(self) -> bool:
        return self.motion.state.motion_type == DASH

    def is_float(self) -> bool:
        return self.motion.state.motion_type == FLOAT

    def is_static(self) -> bool:
        return self.motion.state.motion_type == STATIC

    def is_dash_or_static(self) -> bool:
        return self.motion.state.motion_type in [DASH, STATIC]
