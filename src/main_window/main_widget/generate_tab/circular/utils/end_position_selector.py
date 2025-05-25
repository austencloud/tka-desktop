from typing import TYPE_CHECKING
import random
from data.positions_maps import (
    half_position_map,
    quarter_position_map_cw,
    quarter_position_map_ccw,
)


class RotatedEndPositionSelector:
    @staticmethod
    def determine_rotated_end_pos(slice_size: str, start_pos: str) -> str:
        if slice_size == "quartered":
            return random.choice(
                [
                    quarter_position_map_cw[start_pos],
                    quarter_position_map_ccw[start_pos],
                ]
            )
        elif slice_size == "halved":
            return half_position_map[start_pos]
        raise ValueError("Invalid slice size")
