from data.constants import *
from .base_rot_angle_calculator import BaseRotAngleCalculator


class ProRotAngleCalculator(BaseRotAngleCalculator):
    def calculate_angle(self):
        direction_map = self._pro_direction_map()
        prop_rot_dir = self.arrow.motion.state.prop_rot_dir
        loc = self.arrow.state.loc
        return direction_map.get(prop_rot_dir, {}).get(loc, 0)

    def _pro_direction_map(self):
        return {
            CLOCKWISE: {
                NORTH: 315,
                EAST: 45,
                SOUTH: 135,
                WEST: 225,
                NORTHEAST: 0,
                SOUTHEAST: 90,
                SOUTHWEST: 180,
                NORTHWEST: 270,
            },
            COUNTER_CLOCKWISE: {
                NORTH: 315,
                EAST: 225,
                SOUTH: 135,
                WEST: 45,
                NORTHEAST: 270,
                SOUTHEAST: 180,
                SOUTHWEST: 90,
                NORTHWEST: 0,
            },
        }
