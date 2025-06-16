from typing import TYPE_CHECKING

from data.constants import *
from objects.motion.handpath_calculator import HandpathCalculator
from objects.motion.motion import Motion


class LeadStateDeterminer:
    def __init__(self, red_motion: Motion, blue_motion: Motion) -> None:
        self.red_motion = red_motion
        self.blue_motion = blue_motion
        self.handpath_calculator = HandpathCalculator()

    def trailing_motion(self) -> Motion:
        """Returns the trailing motion."""
        return self._determine_motion_order(trailing=True)

    def leading_motion(self) -> Motion:
        """Returns the leading motion."""
        return self._determine_motion_order(trailing=False)

    def _determine_motion_order(self, trailing: bool) -> Motion:
        """Determine leading or trailing motion based on positions and direction."""
        red_start, red_end = (
            self.red_motion.state.start_loc,
            self.red_motion.state.end_loc,
        )
        blue_start, blue_end = (
            self.blue_motion.state.start_loc,
            self.blue_motion.state.end_loc,
        )
        red_handpath, blue_handpath = (
            self.handpath_calculator.get_hand_rot_dir(red_start, red_end),
            self.handpath_calculator.get_hand_rot_dir(blue_start, blue_end),
        )

        # If directions are different, determine based on the direction alone
        if red_handpath != blue_handpath:
            raise ValueError(
                "Motions have different directions, cannot determine lead/follow relationship accurately."
            )

        # Special case: if one motion ends where the other starts, the one that starts at that position is leading
        if red_end == blue_start:
            return self.red_motion if trailing else self.blue_motion
        if blue_end == red_start:
            return self.blue_motion if trailing else self.red_motion

        # If both motions are moving in the same direction, evaluate their relative position
        if red_handpath == CW_HANDPATH:
            if self._is_clockwise_ahead(blue_start, red_start):
                return self.blue_motion if trailing else self.red_motion
            else:
                return self.red_motion if trailing else self.blue_motion
        elif red_handpath == CCW_HANDPATH:
            if self._is_counter_clockwise_ahead(blue_start, red_start):
                return self.blue_motion if trailing else self.red_motion
            else:
                return self.red_motion if trailing else self.blue_motion

    def _is_clockwise_ahead(self, start_a: str, start_b: str) -> bool:
        """Check if start_a is ahead of start_b in a clockwise direction."""
        circular_order = ["nw", "n", "ne", "e", "se", "s", "sw", "w"]
        idx_a = circular_order.index(start_a)
        idx_b = circular_order.index(start_b)
        return (idx_a - idx_b) % len(circular_order) > 0

    def _is_counter_clockwise_ahead(self, start_a: str, start_b: str) -> bool:
        """Check if start_a is ahead of start_b in a counter-clockwise direction."""
        circular_order = ["nw", "n", "ne", "e", "se", "s", "sw", "w"]
        idx_a = circular_order.index(start_a)
        idx_b = circular_order.index(start_b)
        return (idx_b - idx_a) % len(circular_order) > 0
