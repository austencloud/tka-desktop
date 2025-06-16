from collections import defaultdict
from typing import Dict, Tuple
from data.constants import (
    CCW_HANDPATH,
    CW_HANDPATH,
    DASH,
    STATIC,
    SOUTH,
    WEST,
    NORTH,
    EAST,
    NORTHEAST,
    NORTHWEST,
    SOUTHEAST,
    SOUTHWEST,
)


class HandpathCalculator:
    """Calculates the hand rotation direction based on the start and end locations."""

    def __init__(self):
        """Initialize hand rotation direction mapping."""
        self.hand_rot_dir_map: defaultdict[Tuple[str, str], str]

        clockwise_pairs = [(SOUTH, WEST), (WEST, NORTH), (NORTH, EAST), (EAST, SOUTH)]
        counter_clockwise_pairs = [
            (WEST, SOUTH),
            (NORTH, WEST),
            (EAST, NORTH),
            (SOUTH, EAST),
        ]
        diagonal_clockwise = [
            (NORTHEAST, SOUTHEAST),
            (SOUTHEAST, SOUTHWEST),
            (SOUTHWEST, NORTHWEST),
            (NORTHWEST, NORTHEAST),
        ]
        diagonal_counter_clockwise = [
            (NORTHEAST, NORTHWEST),
            (NORTHWEST, SOUTHWEST),
            (SOUTHWEST, SOUTHEAST),
            (SOUTHEAST, NORTHEAST),
        ]
        dash_pairs = [
            (SOUTH, NORTH),
            (WEST, EAST),
            (NORTH, SOUTH),
            (EAST, WEST),
            (NORTHEAST, SOUTHWEST),
            (SOUTHEAST, NORTHWEST),
            (SOUTHWEST, NORTHEAST),
            (NORTHWEST, SOUTHEAST),
        ]
        static_pairs = [
            (NORTH, NORTH),
            (EAST, EAST),
            (SOUTH, SOUTH),
            (WEST, WEST),
            (NORTHEAST, NORTHEAST),
            (SOUTHEAST, SOUTHEAST),
            (SOUTHWEST, SOUTHWEST),
            (NORTHWEST, NORTHWEST),
        ]

        # Properly define as an instance variable
        self.hand_rot_dir_map = defaultdict(
            lambda: "NO HAND ROTATION FOUND",
            {
                **{pair: CW_HANDPATH for pair in clockwise_pairs + diagonal_clockwise},
                **{
                    pair: CCW_HANDPATH
                    for pair in counter_clockwise_pairs + diagonal_counter_clockwise
                },
                **{pair: DASH for pair in dash_pairs},
                **{pair: STATIC for pair in static_pairs},
            },
        )

    def get_hand_rot_dir(self, start_loc: str, end_loc: str) -> str:
        """
        Returns the hand rotation direction based on the start and end locations.

        :param start_loc: The starting location.
        :param end_loc: The ending location.
        :return: The hand rotation direction (CLOCKWISE, COUNTER_CLOCKWISE, DASH, or STATIC).
        """
        if not isinstance(start_loc, str) or not isinstance(end_loc, str):
            return "NO HAND ROTATION FOUND"
        return self.hand_rot_dir_map[(start_loc, end_loc)]
