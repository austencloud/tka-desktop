from data.constants import *
from .base_rot_angle_calculator import BaseRotAngleCalculator


class StaticRotAngleCalculator(BaseRotAngleCalculator):
    def calculate_angle(self) -> int:
        rotation_override = self.has_rotation_angle_override()
        if rotation_override:
            return self._get_rot_angle_override_according_to_loc()
        if self.arrow.motion.state.start_ori in [IN, OUT]:
            direction_map = self._radial_static_direction_map()
        elif self.arrow.motion.state.start_ori in [CLOCK, COUNTER]:
            direction_map = self._nonradial_static_direction_map()

        prop_rot_dir = self.arrow.motion.state.prop_rot_dir
        loc = self.arrow.state.loc

        angle_dict = direction_map.get(prop_rot_dir)
        if angle_dict is None:
            angle = 0
        else:
            angle = angle_dict.get(loc, 0)
        return angle

    def _radial_static_direction_map(self) -> dict[str, dict[str, int]]:
        return {
            CLOCKWISE: {
                NORTH: 0,
                EAST: 90,
                SOUTH: 180,
                WEST: 270,
                NORTHEAST: 45,
                SOUTHEAST: 135,
                SOUTHWEST: 225,
                NORTHWEST: 315,
            },
            COUNTER_CLOCKWISE: {
                NORTH: 0,
                EAST: 270,
                SOUTH: 180,
                WEST: 90,
                NORTHEAST: 315,
                SOUTHEAST: 225,
                SOUTHWEST: 135,
                NORTHWEST: 45,
            },
        }

    def _nonradial_static_direction_map(self) -> dict[str, dict[str, int]]:
        return {
            CLOCKWISE: {
                NORTH: 180,
                EAST: 270,
                SOUTH: 0,
                WEST: 90,
                NORTHEAST: 225,
                SOUTHEAST: 315,
                SOUTHWEST: 45,
                NORTHWEST: 135,
            },
            COUNTER_CLOCKWISE: {
                NORTH: 180,
                EAST: 90,
                SOUTH: 0,
                WEST: 270,
                NORTHEAST: 135,
                SOUTHEAST: 45,
                SOUTHWEST: 315,
                NORTHWEST: 225,
            },
        }

    def _get_rot_angle_override_according_to_loc(self) -> int:
        static_from_radial_angle_override_map = {
            NORTH: 180,
            EAST: {CLOCKWISE: 270, COUNTER_CLOCKWISE: 90},
            SOUTH: 0,
            WEST: {CLOCKWISE: 90, COUNTER_CLOCKWISE: 270},
            NORTHEAST: {CLOCKWISE: 225, COUNTER_CLOCKWISE: 135},
            SOUTHEAST: {CLOCKWISE: 315, COUNTER_CLOCKWISE: 45},
            SOUTHWEST: {CLOCKWISE: 45, COUNTER_CLOCKWISE: 315},
            NORTHWEST: {CLOCKWISE: 135, COUNTER_CLOCKWISE: 225},
        }
        static_from_nonradial_angle_override_map = {
            NORTH: 0,
            EAST: {CLOCKWISE: 90, COUNTER_CLOCKWISE: 270},
            SOUTH: 180,
            WEST: {CLOCKWISE: 270, COUNTER_CLOCKWISE: 90},
            NORTHEAST: {CLOCKWISE: 45, COUNTER_CLOCKWISE: 315},
            SOUTHEAST: {CLOCKWISE: 135, COUNTER_CLOCKWISE: 225},
            SOUTHWEST: {CLOCKWISE: 225, COUNTER_CLOCKWISE: 135},
            NORTHWEST: {CLOCKWISE: 315, COUNTER_CLOCKWISE: 45},
        }
        if self.arrow.motion.state.start_ori in [IN, OUT]:
            loc_angle = static_from_radial_angle_override_map.get(self.arrow.state.loc)
            if isinstance(loc_angle, dict):
                return loc_angle.get(self.arrow.motion.state.prop_rot_dir, 0)
            return loc_angle
        elif self.arrow.motion.state.start_ori in [CLOCK, COUNTER]:
            loc_angle = static_from_nonradial_angle_override_map.get(
                self.arrow.state.loc
            )
            if isinstance(loc_angle, dict):
                return loc_angle.get(self.arrow.motion.state.prop_rot_dir, 0)
            return loc_angle
