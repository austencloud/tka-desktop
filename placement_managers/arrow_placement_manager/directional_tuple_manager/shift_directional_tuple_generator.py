from data.constants import (
    BOX,
    CCW_HANDPATH,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    CW_HANDPATH,
    DIAMOND,
    FLOAT,
    PRO,
    ANTI,
)
from .base_directional_tuple_generator import BaseDirectionalGenerator


class ShiftDirectionalGenerator(BaseDirectionalGenerator):
    def generate_directional_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        grid_mode = self._get_grid_mode()
        if grid_mode == DIAMOND:
            directional_tuples = {
                PRO: self._generate_diamond_pro_directional_tuples,
                ANTI: self._generate_diamond_anti_directional_tuples,
                FLOAT: self._generate_diamond_float_directional_tuples,
            }
        elif grid_mode == BOX:
            directional_tuples = {
                PRO: self._generate_box_pro_directional_tuples,
                ANTI: self._generate_box_anti_directional_tuples,
                FLOAT: self._generate_box_float_directional_tuples,
            }
        return directional_tuples.get(self.motion.motion_type, [])(x, y)


    def _generate_diamond_pro_directional_tuples(
        self, x: int, y: int
    ) -> list[tuple[int, int]]:
        directional_tuples = {
            CLOCKWISE: [(x, y), (-y, x), (-x, -y), (y, -x)],
            COUNTER_CLOCKWISE: [(-y, -x), (x, -y), (y, x), (-x, y)],
        }
        return directional_tuples.get(self.motion.prop_rot_dir, [])

    def _generate_diamond_anti_directional_tuples(
        self, x: int, y: int
    ) -> list[tuple[int, int]]:
        directional_tuples = {
            CLOCKWISE: [(-y, -x), (x, -y), (y, x), (-x, y)],
            COUNTER_CLOCKWISE: [(x, y), (-y, x), (-x, -y), (y, -x)],
        }
        return directional_tuples.get(self.motion.prop_rot_dir, [])

    def _generate_diamond_float_directional_tuples(
        self, x: int, y: int
    ) -> list[tuple[int, int]]:
        handpath_direction = self.hand_rot_dir_calculator.get_hand_rot_dir(
            self.motion.start_loc, self.motion.end_loc
        )
        directional_tuples = {
            CW_HANDPATH: [(x, y), (-y, x), (-x, -y), (y, -x)],
            CCW_HANDPATH: [(-y, -x), (x, -y), (y, x), (-x, y)],
        }
        return directional_tuples.get(handpath_direction, [])

    def _generate_box_pro_directional_tuples(
        self, x: int, y: int
    ) -> list[tuple[int, int]]:
        directional_tuples = {
            CLOCKWISE: [(-x, y), (-y, -x), (x, -y), (y, x)],
            COUNTER_CLOCKWISE: [(x, y), (-y, x), (-x, -y), (y, -x)],
        }
        return directional_tuples.get(self.motion.prop_rot_dir, [])

    def _generate_box_anti_directional_tuples(
        self, x: int, y: int
    ) -> list[tuple[int, int]]:
        directional_tuples = {
            CLOCKWISE: [(-x, y), (-y, -x), (x, -y), (y, x)],
            COUNTER_CLOCKWISE: [(x, y), (-y, x), (-x, -y), (y, -x)],
        }
        return directional_tuples.get(self.motion.prop_rot_dir, [])

    def _generate_box_float_directional_tuples(
        self, x: int, y: int
    ) -> list[tuple[int, int]]:
        handpath_direction = self.hand_rot_dir_calculator.get_hand_rot_dir(
            self.motion.start_loc, self.motion.end_loc
        )
        directional_tuples = {
            CW_HANDPATH: [(-y, -x), (x, -y), (y, x), (-x, y)],
            CCW_HANDPATH: [(-y, -x), (x, -y), (y, x), (-x, y)],
        }
        return directional_tuples.get(handpath_direction, [])
