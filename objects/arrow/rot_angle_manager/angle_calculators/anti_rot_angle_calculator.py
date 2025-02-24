from data.constants import *
from .base_rot_angle_calculator import BaseRotAngleCalculator


class AntiRotAngleCalculator(BaseRotAngleCalculator):
    def calculate_angle(self):
        if self.arrow.motion.state.start_ori in [IN, OUT]:
            direction_map = {
                CLOCKWISE: {
                    NORTH: 315,
                    EAST: 225,
                    SOUTH: 135,
                    WEST: 45,
                    NORTHEAST: 270,
                    SOUTHEAST: 180,
                    SOUTHWEST: 90,
                    NORTHWEST: 0,
                },
                COUNTER_CLOCKWISE: {
                    NORTH: 315,
                    EAST: 45,
                    SOUTH: 135,
                    WEST: 225,
                    NORTHEAST: 0,
                    SOUTHEAST: 90,
                    SOUTHWEST: 180,
                    NORTHWEST: 270,
                },
            }
        elif self.arrow.motion.state.start_ori in [CLOCK, COUNTER]:

            if self.arrow.motion.state.turns in [0.5, 1.5, 2.5]:
                direction_map = {
                    CLOCKWISE: {
                        NORTH: 315,
                        EAST: 225,
                        SOUTH: 135,
                        WEST: 45,
                        NORTHEAST: 270,
                        SOUTHEAST: 180,
                        SOUTHWEST: 90,
                        NORTHWEST: 360,
                    },
                    COUNTER_CLOCKWISE: {
                        NORTH: 315,
                        EAST: 45,
                        SOUTH: 135,
                        WEST: 225,
                        NORTHEAST: 360,
                        SOUTHEAST: 90,
                        SOUTHWEST: 180,
                        NORTHWEST: 270,
                    },
                }
            else:
                direction_map = {
                    CLOCKWISE: {
                        NORTH: 315,
                        EAST: 225,
                        SOUTH: 135,
                        WEST: 45,
                        NORTHEAST: 270,
                        SOUTHEAST: 180,
                        SOUTHWEST: 90,
                        NORTHWEST: 0,
                    },
                    COUNTER_CLOCKWISE: {
                        NORTH: 315,
                        EAST: 45,
                        SOUTH: 135,
                        WEST: 225,
                        NORTHEAST: 0,
                        SOUTHEAST: 90,
                        SOUTHWEST: 180,
                        NORTHWEST: 270,
                    },
                }

        prop_rot_dir = self.arrow.motion.state.prop_rot_dir
        loc = self.arrow.state.loc
        return direction_map.get(prop_rot_dir, {}).get(loc, 0)
