from typing import TYPE_CHECKING
from enums.letter.letter import Letter

from data.constants import (
    BLUE,
    BOX,
    DIAMOND,
    DOWNLEFT,
    DOWNRIGHT,
    NONRADIAL,
    EAST,
    NORTH,
    NORTHEAST,
    NORTHWEST,
    RADIAL,
    RED,
    SOUTH,
    SOUTHEAST,
    SOUTHWEST,
    UPLEFT,
    UPRIGHT,
    WEST,
    LEFT,
    RIGHT,
    UP,
    DOWN,
)

from objects.motion.motion import Motion
from objects.prop.prop import Prop

if TYPE_CHECKING:
    from placement_managers.prop_placement_manager.prop_placement_manager import (
        PropPlacementManager,
    )


class BetaPropDirectionCalculator:

    def get_dir(self, motion: Motion) -> str:
        """Determine the translation direction based on the motion type, start location, end location, and end layer."""
        if (
            motion.pictograph.state.letter == Letter.I
            and motion.pictograph.managers.check.ends_with_radial_ori()
        ):
            return self.get_direction_for_radial_I(motion)
        elif (
            motion.pictograph.state.letter == Letter.I
            and motion.pictograph.managers.check.ends_with_nonradial_ori()
        ):
            return self.get_direction_for_nonradial_I(motion)
        if motion.check.is_shift():
            if motion.prop.check.is_radial():
                return self.get_dir_for_radial(motion)
            elif motion.prop.check.is_nonradial():
                return self.get_dir_for_nonradial(motion)
        elif motion.check.is_dash() or motion.check.is_static():
            return self.get_dir_for_non_shift(motion.prop)

    def get_direction_for_nonradial_I(self, motion: Motion) -> str:
        direction_map = {
            (NORTH, RED): UP,
            (NORTH, BLUE): DOWN,
            (EAST, RED): RIGHT,
            (EAST, BLUE): LEFT,
            (SOUTH, RED): DOWN,
            (SOUTH, BLUE): UP,
            (WEST, BLUE): LEFT,
            (WEST, RED): RIGHT,
            (NORTHEAST, RED): UPRIGHT,
            (NORTHEAST, BLUE): DOWNLEFT,
            (SOUTHEAST, RED): DOWNRIGHT,
            (SOUTHEAST, BLUE): UPLEFT,
            (SOUTHWEST, RED): UPRIGHT,
            (SOUTHWEST, BLUE): DOWNLEFT,
            (NORTHWEST, RED): DOWNRIGHT,
            (NORTHWEST, BLUE): UPLEFT,
        }
        return direction_map.get((motion.state.end_loc, motion.prop.state.color))

    def get_direction_for_radial_I(self, motion: Motion) -> str:
        direction_map = {
            (NORTH, RED): RIGHT,
            (NORTH, BLUE): LEFT,
            (EAST, RED): DOWN,
            (EAST, BLUE): UP,
            (SOUTH, RED): LEFT,
            (SOUTH, BLUE): RIGHT,
            (WEST, BLUE): UP,
            (WEST, RED): DOWN,
            (NORTHEAST, RED): DOWNRIGHT,
            (NORTHEAST, BLUE): UPLEFT,
            (SOUTHEAST, RED): UPRIGHT,
            (SOUTHEAST, BLUE): DOWNLEFT,
            (SOUTHWEST, RED): DOWNRIGHT,
            (SOUTHWEST, BLUE): UPLEFT,
            (NORTHWEST, RED): UPRIGHT,
            (NORTHWEST, BLUE): DOWNLEFT,
        }
        return direction_map.get((motion.state.end_loc, motion.prop.state.color))

    def get_dir_for_radial(self, motion: Motion) -> str:
        direction_map = {
            (EAST, NORTH): RIGHT,
            (WEST, NORTH): LEFT,
            (EAST, SOUTH): RIGHT,
            (WEST, SOUTH): LEFT,
            (NORTH, EAST): UP,
            (SOUTH, EAST): DOWN,
            (NORTH, WEST): UP,
            (SOUTH, WEST): DOWN,
            (NORTHEAST, NORTHWEST): UPRIGHT,
            (NORTHEAST, SOUTHEAST): UPRIGHT,
            (SOUTHEAST, NORTHEAST): DOWNRIGHT,
            (SOUTHEAST, SOUTHWEST): DOWNRIGHT,
            (SOUTHWEST, NORTHWEST): DOWNLEFT,
            (SOUTHWEST, SOUTHEAST): DOWNLEFT,
            (NORTHWEST, NORTHEAST): UPLEFT,
            (NORTHWEST, SOUTHWEST): UPLEFT,
        }
        return direction_map.get((motion.state.start_loc, motion.state.end_loc))

    def get_dir_for_nonradial(self, motion: Motion) -> str:
        direction_map = {
            (EAST, NORTH): UP,
            (WEST, NORTH): DOWN,
            (EAST, SOUTH): UP,
            (WEST, SOUTH): DOWN,
            (NORTH, EAST): RIGHT,
            (SOUTH, EAST): LEFT,
            (NORTH, WEST): RIGHT,
            (SOUTH, WEST): LEFT,
            (NORTHEAST, SOUTHEAST): UPLEFT,
            (NORTHEAST, NORTHWEST): DOWNRIGHT,
            (SOUTHEAST, NORTHEAST): UPRIGHT,
            (SOUTHEAST, SOUTHWEST): UPRIGHT,
            (SOUTHWEST, NORTHWEST): UPLEFT,
            (SOUTHWEST, SOUTHEAST): DOWNRIGHT,
            (NORTHWEST, NORTHEAST): DOWNLEFT,
            (NORTHWEST, SOUTHWEST): DOWNLEFT,
        }
        return direction_map.get((motion.state.start_loc, motion.state.end_loc))

    def get_dir_for_non_shift(self, prop: Prop) -> str:
        diamond_layer_reposition_map = {
            RADIAL: {
                (NORTH, RED): RIGHT,
                (NORTH, BLUE): LEFT,
                (EAST, RED): DOWN,
                (EAST, BLUE): UP,
                (SOUTH, RED): LEFT,
                (SOUTH, BLUE): RIGHT,
                (WEST, BLUE): DOWN,
                (WEST, RED): UP,
            },
            NONRADIAL: {
                (NORTH, RED): UP,
                (NORTH, BLUE): DOWN,
                (SOUTH, RED): UP,
                (SOUTH, BLUE): DOWN,
                (EAST, RED): RIGHT,
                (WEST, BLUE): LEFT,
                (WEST, RED): RIGHT,
                (EAST, BLUE): LEFT,
            },
        }
        box_layer_reposition_map = {
            RADIAL: {
                (NORTHEAST, RED): DOWNRIGHT,
                (NORTHEAST, BLUE): UPLEFT,
                (SOUTHEAST, RED): UPRIGHT,
                (SOUTHEAST, BLUE): DOWNLEFT,
                (SOUTHWEST, RED): DOWNRIGHT,
                (SOUTHWEST, BLUE): UPLEFT,
                (NORTHWEST, RED): UPRIGHT,
                (NORTHWEST, BLUE): DOWNLEFT,
            },
            NONRADIAL: {
                (NORTHEAST, RED): UPRIGHT,
                (NORTHEAST, BLUE): DOWNLEFT,
                (SOUTHEAST, RED): DOWNRIGHT,
                (SOUTHEAST, BLUE): UPLEFT,
                (SOUTHWEST, RED): UPRIGHT,
                (SOUTHWEST, BLUE): DOWNLEFT,
                (NORTHWEST, RED): DOWNRIGHT,
                (NORTHWEST, BLUE): UPLEFT,
            },
        }
        grid_mode = DIAMOND if prop.state.loc in [NORTH, SOUTH, EAST, WEST] else BOX
        if grid_mode == DIAMOND:
            if prop.check.is_radial():
                return diamond_layer_reposition_map[RADIAL][
                    (prop.state.loc, prop.state.color)
                ]
            elif prop.check.is_nonradial():
                return diamond_layer_reposition_map[NONRADIAL][
                    (prop.state.loc, prop.state.color)
                ]
        elif grid_mode == BOX:
            if prop.check.is_radial():
                return box_layer_reposition_map[RADIAL][
                    (prop.state.loc, prop.state.color)
                ]
            elif prop.check.is_nonradial():
                return box_layer_reposition_map[NONRADIAL][
                    (prop.state.loc, prop.state.color)
                ]

    def get_opposite_dir(self, movement: str) -> str:
        opposite_directions = {
            LEFT: RIGHT,
            RIGHT: LEFT,
            UP: DOWN,
            DOWN: UP,
            DOWNRIGHT: UPLEFT,
            UPLEFT: DOWNRIGHT,
            UPRIGHT: DOWNLEFT,
            DOWNLEFT: UPRIGHT,
        }
        return opposite_directions.get(movement)
