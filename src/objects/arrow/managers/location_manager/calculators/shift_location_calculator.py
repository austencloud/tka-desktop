from data.constants import *
from .base_location_calculator import BaseLocationCalculator


class ShiftLocationCalculator(BaseLocationCalculator):
    def calculate_location(self) -> str:
        direction_pairs = {
            frozenset({NORTH, EAST}): NORTHEAST,
            frozenset({EAST, SOUTH}): SOUTHEAST,
            frozenset({SOUTH, WEST}): SOUTHWEST,
            frozenset({WEST, NORTH}): NORTHWEST,
            frozenset({NORTHEAST, NORTHWEST}): NORTH,
            frozenset({NORTHEAST, SOUTHEAST}): EAST,
            frozenset({SOUTHWEST, SOUTHEAST}): SOUTH,
            frozenset({NORTHWEST, SOUTHWEST}): WEST,
        }
        return direction_pairs.get(
            frozenset(
                {self.arrow.motion.state.start_loc, self.arrow.motion.state.end_loc}
            ),
            "",
        )
