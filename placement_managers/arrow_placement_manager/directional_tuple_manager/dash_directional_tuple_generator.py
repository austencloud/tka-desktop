from Enums.Enums import LetterType
from data.constants import (
    BLUE,
    BOX,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    DIAMOND,
    EAST,
    FLOAT,
    NO_ROT,
    NORTH,
    NORTHEAST,
    NORTHWEST,
    PRO,
    ANTI,
    RED,
    SOUTH,
    SOUTHEAST,
    SOUTHWEST,
    STATIC,
    WEST,
)
from objects.motion import motion
from .base_directional_tuple_generator import BaseDirectionalGenerator


class DashDirectionalGenerator(BaseDirectionalGenerator):
    def generate_directional_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        grid_mode = self._get_grid_mode()

        if grid_mode == DIAMOND:
            if (
                self.motion.pictograph.letter_type == LetterType.Type5
                and self.motion.turns == 0
            ):
                return self._handle_type5_zero_turns(x, y)

            elif self.motion.prop_rot_dir == NO_ROT:
                return self._handle_type5_zero_turns(x, y)
            elif self.motion.prop_rot_dir == CLOCKWISE:
                return [(x, -y), (y, x), (-x, y), (-y, -x)]
            elif self.motion.prop_rot_dir == COUNTER_CLOCKWISE:
                return [(-x, -y), (y, -x), (x, y), (-y, x)]

        elif grid_mode == BOX:
            if (
                self.motion.pictograph.letter_type == LetterType.Type5
                and self.motion.turns == 0
            ):
                return self._handle_type5_zero_turns(x, y)
            elif self.motion.prop_rot_dir == NO_ROT:
                return self._handle_type5_zero_turns(x, y)

            elif self.motion.prop_rot_dir == CLOCKWISE:
                return [(-y, x), (-x, -y), (y, -x), (x, y)]
            elif self.motion.prop_rot_dir == COUNTER_CLOCKWISE:
                return [(-x, y), (-y, -x), (x, -y), (y, x)]

    def _handle_no_rotation_dash(self, x: int, y: int) -> list[tuple[int, int]]:
        if self.other_motion.motion_type == PRO:
            return (
                [(x, y), (-y, x), (-x, -y), (y, -x)]
                if self.other_motion.prop_rot_dir == CLOCKWISE
                else [(-x, y), (-y, -x), (x, -y), (y, x)]
            )
        elif self.other_motion.motion_type == ANTI:
            return (
                [(-x, y), (-y, -x), (x, -y), (y, x)]
                if self.other_motion.prop_rot_dir == CLOCKWISE
                else [(x, y), (-y, x), (-x, -y), (y, -x)]
            )
        elif self.other_motion.motion_type == FLOAT:
            return [(x, -y), (y, x), (-x, y), (-y, -x)]

        elif self.other_motion.motion_type == DASH:
            if self.other_motion.prop_rot_dir == CLOCKWISE:
                return [(x, -y), (y, x), (-x, y), (-y, -x)]
            elif self.other_motion.prop_rot_dir == COUNTER_CLOCKWISE:
                return [(-x, -y), (y, -x), (x, y), (-y, x)]
            else:
                return [(x, -y), (y, x), (-x, y), (-y, -x)]
        elif self.other_motion.motion_type == STATIC:
            if self.other_motion.prop_rot_dir == CLOCKWISE:
                return [(x, -y), (y, x), (-x, y), (-y, -x)]
            elif self.other_motion.prop_rot_dir == COUNTER_CLOCKWISE:
                return [(-x, -y), (y, -x), (x, y), (-y, x)]
            else:
                return [(x, -y), (y, x), (-x, y), (-y, -x)]

    def _handle_type5_zero_turns(self, x: int, y: int) -> list[tuple[int, int]]:
        diamond_Type5_zero_turns_directional_tuples = {
            (BLUE, (NORTH, SOUTH)): [(x, y), (-y, x), (-x, -y), (y, -x)],
            (BLUE, (EAST, WEST)): [(x, y), (-y, -x), (x, -y), (y, x)],
            (BLUE, (SOUTH, NORTH)): [(x, y), (-y, x), (-x, -y), (y, x)],
            (BLUE, (WEST, EAST)): [(x, y), (-y, -x), (-x, -y), (-y, x)],
            (RED, (NORTH, SOUTH)): [(x, y), (-y, -x), (-x, -y), (y, -x)],
            (RED, (EAST, WEST)): [(x, y), (-y, -x), (-x, -y), (y, -x)],
            (RED, (SOUTH, NORTH)): [(x, y), (-y, x), (-x, -y), (y, -x)],
            (RED, (WEST, EAST)): [(-x, y), (-y, -x), (-x, -y), (y, x)],
        }
        box_Type5_zero_turns_directional_tuples = {
            (BLUE, (NORTHEAST, SOUTHWEST)): [(x, y), (y, x), (-x, -y), (y, x)],
            (BLUE, (NORTHWEST, SOUTHEAST)): [(x, -y), (-y, -x), (x, -y), (y, x)],
            (BLUE, (SOUTHWEST, NORTHEAST)): [(x, y), (-y, -x), (-x, -y), (-y, -x)],
            (BLUE, (SOUTHEAST, NORTHWEST)): [(-x, y), (-y, -x), (-x, y), (-y, x)],
            (RED, (NORTHEAST, SOUTHWEST)): [(x, y), (y, x), (-x, -y), (y, x)],
            (RED, (NORTHWEST, SOUTHEAST)): [(x, -y), (-y, -x), (x, -y), (y, -x)],
            (RED, (SOUTHWEST, NORTHEAST)): [(x, y), (-y, -x), (-x, -y), (-y, -x)],
            (RED, (SOUTHEAST, NORTHWEST)): [(-x, y), (-y, -x), (-x, y), (y, x)],
        }
        grid_mode = self.motion.pictograph.grid_mode
        if grid_mode == DIAMOND:
            return diamond_Type5_zero_turns_directional_tuples.get(
                (self.motion.color, (self.motion.start_loc, self.motion.end_loc)), []
            )
        elif grid_mode == BOX:
            return box_Type5_zero_turns_directional_tuples.get(
                (self.motion.color, (self.motion.start_loc, self.motion.end_loc)), []
            )
