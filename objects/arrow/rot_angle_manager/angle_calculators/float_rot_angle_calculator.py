from data.constants import *
from .base_rot_angle_calculator import BaseRotAngleCalculator


class FloatRotAngleCalculator(BaseRotAngleCalculator):
    def calculate_angle(self):
        direction_map = self._float_direction_map()
        loc = self.arrow.state.loc
        handpath_direction = self.handpath_calculator.get_hand_rot_dir(
            self.arrow.motion.state.start_loc, self.arrow.motion.state.end_loc
        )
        return direction_map.get(handpath_direction, {}).get(loc, 0)

    def _float_direction_map(self):
        return {
            CW_HANDPATH: self._clockwise_map(),
            CCW_HANDPATH: self._counter_clockwise_map(),
        }

    def _clockwise_map(self):
        return {
            NORTH: 315,
            EAST: 45,
            SOUTH: 135,
            WEST: 225,
            NORTHEAST: 0,
            SOUTHEAST: 90,
            SOUTHWEST: 180,
            NORTHWEST: 270,
        }

    def _counter_clockwise_map(self):
        return {
            NORTH: 135,
            EAST: 225,
            SOUTH: 315,
            WEST: 45,
            NORTHEAST: 180,
            SOUTHEAST: 270,
            SOUTHWEST: 0,
            NORTHWEST: 90,
        }
