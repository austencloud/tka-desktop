from typing import TYPE_CHECKING, Literal
from data.constants import BOX, DIAMOND, END_POS, START_POS
from data.positions_maps import box_positions, diamond_positions


class GridModeChecker:
    """Checks what grid a given pictograph is in by looking at its start and end positions"""

    @staticmethod
    def get_grid_mode(
        pictograph_data: dict,
    ) -> None | Literal["box"] | Literal["diamond"] | Literal["skewed"]:
        start_pos = pictograph_data.get(START_POS) or pictograph_data.get(
            END_POS
        )  # Handles the start position
        end_pos = pictograph_data.get(END_POS)

        if start_pos in box_positions and end_pos in box_positions:
            return BOX
        if start_pos in diamond_positions and end_pos in diamond_positions:
            return DIAMOND
        if (start_pos in box_positions and end_pos in diamond_positions) or (
            start_pos in diamond_positions and end_pos in box_positions
        ):
            return "skewed"
        return None
