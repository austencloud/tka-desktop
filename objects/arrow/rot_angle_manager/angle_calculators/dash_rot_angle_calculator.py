from data.constants import *
from .base_rot_angle_calculator import BaseRotAngleCalculator


class DashRotAngleCalculator(BaseRotAngleCalculator):
    def calculate_angle(self) -> int:
        rotation_override = self.has_rotation_angle_override()
        if rotation_override:
            return self._get_rot_angle_override_according_to_loc()
        if self.arrow.motion.state.prop_rot_dir == NO_ROT:
            return self._handle_no_rotation()
        return self._handle_orientation_based_rotation()

    def _handle_no_rotation(self) -> int:
        no_rotation_map = self._no_rotation_map()
        return no_rotation_map.get(
            (self.arrow.motion.state.start_loc, self.arrow.motion.state.end_loc), 0
        )

    def _no_rotation_map(self):
        return {
            (NORTH, SOUTH): 90,
            (EAST, WEST): 180,
            (SOUTH, NORTH): 270,
            (WEST, EAST): 0,
            (SOUTHEAST, NORTHWEST): 225,
            (SOUTHWEST, NORTHEAST): 315,
            (NORTHWEST, SOUTHEAST): 45,
            (NORTHEAST, SOUTHWEST): 135,
        }

    def _handle_orientation_based_rotation(self) -> int:
        orientation_rotation_map = self._dash_orientation_rotation_map()
        start_ori_map = orientation_rotation_map.get(
            self.arrow.motion.state.start_ori, {}
        )
        rotation_map = start_ori_map.get(self.arrow.motion.state.prop_rot_dir, {})
        return rotation_map.get(self.arrow.state.loc, 0)

    def _dash_orientation_rotation_map(self):
        """Maps the start orientation to the prop rotation direction to the arrow loc"""

        return {
            IN: {
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
            },
            OUT: {
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
            },
            CLOCK: {
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
            },
            COUNTER: {
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
            },
        }

    def _get_rot_angle_override_according_to_loc(self) -> int:
        cw_dash_angle_override_map = {
            NORTH: 270,
            EAST: 0,
            SOUTH: 90,
            WEST: 180,
            NORTHEAST: 315,
            SOUTHEAST: 45,
            SOUTHWEST: 135,
            NORTHWEST: 225,
        }
        ccw_dash_angle_override_map = {
            NORTH: 270,
            EAST: 180,
            SOUTH: 90,
            WEST: 0,
            NORTHEAST: 225,
            SOUTHEAST: 135,
            SOUTHWEST: 45,
            NORTHWEST: 315,
        }

        if self.arrow.motion.state.prop_rot_dir == CLOCKWISE:
            loc_angle = cw_dash_angle_override_map.get(self.arrow.state.loc)
            if isinstance(loc_angle, dict):
                return loc_angle.get(self.arrow.motion.state.prop_rot_dir, 0)
            return loc_angle

        if self.arrow.motion.state.prop_rot_dir == COUNTER_CLOCKWISE:
            loc_angle = ccw_dash_angle_override_map.get(self.arrow.state.loc)
            if isinstance(loc_angle, dict):
                return loc_angle.get(self.arrow.motion.state.prop_rot_dir, 0)
            return loc_angle

        elif self.arrow.motion.state.prop_rot_dir == NO_ROT:
            return self._handle_no_rotation()

        return None
