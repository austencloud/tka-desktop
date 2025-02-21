from typing import Callable

from data.constants import *
from data.start_end_loc_map import get_start_end_locs
from Enums.Enums import Handpaths

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.motion.motion import Motion


class MotionManipulator:
    def __init__(self, motion: "Motion"):
        self.motion = motion

    def move_wasd(self, direction: str) -> None:
        wasd_location_map = {
            UP: {SOUTHEAST: NORTHEAST, SOUTHWEST: NORTHWEST},
            LEFT: {NORTHEAST: NORTHWEST, SOUTHEAST: SOUTHWEST},
            DOWN: {NORTHEAST: SOUTHEAST, NORTHWEST: SOUTHWEST},
            RIGHT: {NORTHWEST: NORTHEAST, SOUTHWEST: SOUTHEAST},
        }
        current_location = self.motion.arrow.loc
        new_location = wasd_location_map.get(direction, {}).get(
            current_location, current_location
        )
        (new_start_loc, new_end_loc) = get_start_end_locs(
            self.motion.arrow.motion.motion_type, self.motion.prop_rot_dir, new_location
        )
        pictograph_data = {
            f"{self.motion.color}_start_location": new_start_loc,
            f"{self.motion.color}_end_location": new_end_loc,
        }
        self.motion.pictograph.managers.updater.update_pictograph(pictograph_data)

    ### MIRRORING ###

    def swap_rot_dir(self) -> None:
        self.motion.arrow.mirror_manager.update_mirror()

        rotation_direction_map = {
            COUNTER_CLOCKWISE: CLOCKWISE,
            CLOCKWISE: COUNTER_CLOCKWISE,
            NO_ROT: NO_ROT,
        }
        new_rot_dir = rotation_direction_map.get(self.motion.prop_rot_dir)

        new_start_loc = self.motion.end_loc
        new_end_loc = self.motion.start_loc

        pictograph_data = {
            f"{self.motion.color}_start_location": new_start_loc,
            f"{self.motion.color}_end_location": new_end_loc,
            f"{self.motion.color}_prop_rot_dir": new_rot_dir,
        }
        self.motion.pictograph.managers.updater.update_pictograph(pictograph_data)

    ### MOTION TYPE ###

    def swap_motion_type(self) -> None:
        swap_motion_type_map = {
            ANTI: PRO,
            PRO: ANTI,
            STATIC: DASH,
            DASH: STATIC,
        }

        rotation_direction_map = {
            COUNTER_CLOCKWISE: CLOCKWISE,
            CLOCKWISE: COUNTER_CLOCKWISE,
            NO_ROT: NO_ROT,
        }
        new_motion_type = swap_motion_type_map.get(self.motion.arrow.motion.motion_type)
        new_rot_dir = rotation_direction_map.get(self.motion.prop_rot_dir)

        self.motion.prop.attr_manager.swap_ori(self.motion.prop.ori)
        pictograph_data = {
            f"{self.motion.color}_motion_type": new_motion_type,
            f"{self.motion.color}_prop_rot_dir": new_rot_dir,
            f"{self.motion.color}_end_ori": self.motion.prop.ori,
        }
        self.motion.pictograph.managers.updater.update_pictograph(pictograph_data)

    ### ROTATION ###

    def rotate_motion(self, rotation_direction: Handpaths) -> None:
        mode_mappings = self._get_mode_mappings()
        rotate_func, locations = mode_mappings.get(
            (
                self.motion.motion_type,
                self.motion.arrow.pictograph.elements.grid.grid_mode,
            ),
            (None, None),
        )

        if rotate_func:
            rotate_func(rotation_direction, locations)

    def _get_mode_mappings(self) -> dict[tuple[str, str], tuple[Callable, list]]:
        """Returns mappings for different modes and motion types."""
        return {
            (STATIC, DIAMOND): (self._rotate_arrow, [NORTH, EAST, SOUTH, WEST]),
            (PRO, DIAMOND): (
                self._rotate_arrow,
                [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST],
            ),
            (ANTI, DIAMOND): (
                self._rotate_arrow,
                [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST],
            ),
            (FLOAT, DIAMOND): (
                self._rotate_arrow,
                [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST],
            ),
            (DASH, DIAMOND): (self._rotate_arrow, [NORTH, EAST, SOUTH, WEST]),
            (STATIC, BOX): (
                self._rotate_arrow,
                [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST],
            ),
            (PRO, BOX): (self._rotate_arrow, [NORTH, EAST, SOUTH, WEST]),
            (ANTI, BOX): (self._rotate_arrow, [NORTH, EAST, SOUTH, WEST]),
            (FLOAT, BOX): (self._rotate_arrow, [NORTH, EAST, SOUTH, WEST]),
            (DASH, BOX): (
                self._rotate_arrow,
                [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST],
            ),
        }

    def _rotate_arrow(self, handpath, locations: list[str]) -> None:
        """
        Generic method to rotate arrows based on the handpath and locations.
        """
        current_index = locations.index(self.motion.arrow.loc)
        new_index = (
            (current_index + 1) % len(locations)
            if handpath == CW_HANDPATH
            else (current_index - 1) % len(locations)
        )
        new_location = locations[new_index]

        new_start_loc, new_end_loc = get_start_end_locs(
            self.motion.arrow.motion.motion_type, self.motion.prop_rot_dir, new_location
        )

        self._update_motion_attributes(new_location, new_start_loc, new_end_loc)

    def _update_motion_attributes(self, new_location, new_start_loc, new_end_loc):
        """
        Update motion attributes and reflect changes in the pictograph.
        """
        self.motion.arrow.loc = new_location
        self.motion.start_loc = new_start_loc
        self.motion.end_loc = new_end_loc
        self.motion.prop.loc = new_end_loc

        self._refresh_pictograph()

    def _refresh_pictograph(self):
        """
        Refresh the arrow and prop, and update the pictograph.
        """
        self.motion.arrow.pictograph.managers.updater.update_pictograph()

    def set_prop_rot_dir(self, prop_rot_dir: str) -> None:
        self.motion.prop_rot_dir = prop_rot_dir
