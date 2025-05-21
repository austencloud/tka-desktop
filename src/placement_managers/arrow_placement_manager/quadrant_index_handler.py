from typing import TYPE_CHECKING, Literal
from objects.arrow.arrow import Arrow
from data.constants import (
    BOX,
    DIAMOND,
    FLOAT,
    NORTHEAST,
    SOUTHEAST,
    SOUTHWEST,
    NORTHWEST,
    NORTH,
    EAST,
    SOUTH,
    WEST,
    PRO,
    ANTI,
    STATIC,
    DASH,
)

if TYPE_CHECKING:
    from placement_managers.arrow_placement_manager.arrow_placement_manager import (
        ArrowPlacementManager,
    )


class QuadrantIndexHandler:
    def __init__(self, placement_manager: "ArrowPlacementManager") -> None:
        self.placement_manager = placement_manager

    def get_quadrant_index(self, arrow: Arrow) -> Literal[0, 1, 2, 3]:
        grid_mode = self._get_grid_mode(arrow)
        if grid_mode == DIAMOND:
            if arrow.motion.state.motion_type in [PRO, ANTI, FLOAT]:
                return self._diamond_shift_quadrant_index(arrow.state.loc)
            elif arrow.motion.state.motion_type in [STATIC, DASH]:
                return self._diamond_static_dash_quadrant_index(arrow.state.loc)
        elif grid_mode == BOX:
            if arrow.motion.state.motion_type in [PRO, ANTI, FLOAT]:
                return self._box_shift_quadrant_index(arrow.state.loc)
            elif arrow.motion.state.motion_type in [STATIC, DASH]:
                return self._box_static_dash_quadrant_index(arrow.state.loc)

        return 0

    def _get_grid_mode(self, arrow: "Arrow") -> Literal["box"] | Literal["diamond"]:
        # Default to DIAMOND grid mode if loc is None
        grid_mode = DIAMOND

        # Check if prop state and loc exist
        if (
            hasattr(arrow, "motion")
            and hasattr(arrow.motion, "prop")
            and hasattr(arrow.motion.prop, "state")
        ):
            loc = arrow.motion.prop.state.loc

            # Determine grid mode based on location
            if loc in ["ne", "nw", "se", "sw"]:
                grid_mode = BOX
            elif loc in ["n", "s", "e", "w"]:
                grid_mode = DIAMOND

        return grid_mode

    def _diamond_shift_quadrant_index(self, location: str) -> Literal[0, 1, 2, 3]:
        location_to_index = {
            NORTHEAST: 0,
            SOUTHEAST: 1,
            SOUTHWEST: 2,
            NORTHWEST: 3,
        }
        return location_to_index.get(location, 0)

    def _diamond_static_dash_quadrant_index(self, location: str) -> Literal[0, 1, 2, 3]:
        location_to_index = {
            NORTH: 0,
            EAST: 1,
            SOUTH: 2,
            WEST: 3,
        }
        return location_to_index.get(location, 0)

    def _box_shift_quadrant_index(self, location: str) -> Literal[0, 1, 2, 3]:
        location_to_index = {
            NORTH: 0,
            EAST: 1,
            SOUTH: 2,
            WEST: 3,
        }
        return location_to_index.get(location, 0)

    def _box_static_dash_quadrant_index(self, location: str) -> Literal[0, 1, 2, 3]:
        location_to_index = {
            NORTHEAST: 0,
            SOUTHEAST: 1,
            SOUTHWEST: 2,
            NORTHWEST: 3,
        }
        return location_to_index.get(location, 0)
