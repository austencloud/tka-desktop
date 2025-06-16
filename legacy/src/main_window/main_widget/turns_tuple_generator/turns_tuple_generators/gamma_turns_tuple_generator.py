from typing import TYPE_CHECKING
from data.constants import *
from main_window.main_widget.turns_tuple_generator.turns_tuple_generators.base_turns_tuple_generator import (
    BaseTurnsTupleGenerator,
)


class GammaTurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        blue_static = self.pictograph.elements.blue_motion
        red_static = self.pictograph.elements.red_motion
        blue_static_map, red_static_map = self._get_direction_maps()

        if blue_static.state.turns == 0 and red_static.state.turns > 0:
            red_static_state = red_static_map.get(
                (
                    blue_static.state.end_loc,
                    red_static.state.end_loc,
                    red_static.state.prop_rot_dir,
                ),
                "",
            )
            return f"({self._normalize_turns(blue_static)}, {self._normalize_turns(red_static)}, {red_static_state})"
        elif red_static.state.turns == 0 and blue_static.state.turns > 0:
            blue_static_state = blue_static_map.get(
                (
                    blue_static.state.end_loc,
                    red_static.state.end_loc,
                    blue_static.state.prop_rot_dir,
                ),
                "",
            )
            return f"({self._normalize_turns(blue_static)}, {self._normalize_turns(red_static)}, {blue_static_state})"
        elif red_static.state.turns > 0 and blue_static.state.turns > 0:
            red_static_state = red_static_map.get(
                (
                    blue_static.state.end_loc,
                    red_static.state.end_loc,
                    red_static.state.prop_rot_dir,
                ),
                "",
            )
            blue_static_state = blue_static_map.get(
                (
                    blue_static.state.end_loc,
                    red_static.state.end_loc,
                    blue_static.state.prop_rot_dir,
                ),
                "",
            )
            vtg_dir = (
                "s"
                if red_static.state.prop_rot_dir == blue_static.state.prop_rot_dir
                else "o"
            )
            return f"({vtg_dir}, {self._normalize_turns(blue_static)}, {self._normalize_turns(red_static)}, {blue_static_state}, {red_static_state})"
        else:
            return f"({self._normalize_turns(blue_static)}, {self._normalize_turns(red_static)})"

    def _get_direction_maps(self):
        blue_static_direction_map = {
            (EAST, NORTH, CLOCKWISE): OPENING,
            (EAST, NORTH, COUNTER_CLOCKWISE): CLOSING,
            (EAST, SOUTH, CLOCKWISE): CLOSING,
            (EAST, SOUTH, COUNTER_CLOCKWISE): OPENING,
            (WEST, NORTH, CLOCKWISE): CLOSING,
            (WEST, NORTH, COUNTER_CLOCKWISE): OPENING,
            (WEST, SOUTH, CLOCKWISE): OPENING,
            (WEST, SOUTH, COUNTER_CLOCKWISE): CLOSING,
            (NORTH, EAST, CLOCKWISE): CLOSING,
            (NORTH, EAST, COUNTER_CLOCKWISE): OPENING,
            (NORTH, WEST, CLOCKWISE): OPENING,
            (NORTH, WEST, COUNTER_CLOCKWISE): CLOSING,
            (SOUTH, EAST, CLOCKWISE): OPENING,
            (SOUTH, EAST, COUNTER_CLOCKWISE): CLOSING,
            (SOUTH, WEST, CLOCKWISE): CLOSING,
            (SOUTH, WEST, COUNTER_CLOCKWISE): OPENING,
            (NORTHEAST, SOUTHEAST, CLOCKWISE): CLOSING,
            (NORTHEAST, SOUTHEAST, COUNTER_CLOCKWISE): OPENING,
            (NORTHEAST, NORTHWEST, CLOCKWISE): OPENING,
            (NORTHEAST, NORTHWEST, COUNTER_CLOCKWISE): CLOSING,
            (SOUTHEAST, NORTHEAST, CLOCKWISE): OPENING,
            (SOUTHEAST, NORTHEAST, COUNTER_CLOCKWISE): CLOSING,
            (SOUTHEAST, SOUTHWEST, CLOCKWISE): CLOSING,
            (SOUTHEAST, SOUTHWEST, COUNTER_CLOCKWISE): OPENING,
            (SOUTHWEST, NORTHWEST, CLOCKWISE): CLOSING,
            (SOUTHWEST, NORTHWEST, COUNTER_CLOCKWISE): OPENING,
            (SOUTHWEST, SOUTHEAST, CLOCKWISE): OPENING,
            (SOUTHWEST, SOUTHEAST, COUNTER_CLOCKWISE): CLOSING,
            (NORTHWEST, SOUTHWEST, CLOCKWISE): OPENING,
            (NORTHWEST, SOUTHWEST, COUNTER_CLOCKWISE): CLOSING,
            (NORTHWEST, NORTHEAST, CLOCKWISE): CLOSING,
            (NORTHWEST, NORTHEAST, COUNTER_CLOCKWISE): OPENING,
        }
        red_static_direction_map = {
            (EAST, NORTH, CLOCKWISE): CLOSING,
            (EAST, NORTH, COUNTER_CLOCKWISE): OPENING,
            (EAST, SOUTH, CLOCKWISE): OPENING,
            (EAST, SOUTH, COUNTER_CLOCKWISE): CLOSING,
            (WEST, NORTH, CLOCKWISE): OPENING,
            (WEST, NORTH, COUNTER_CLOCKWISE): CLOSING,
            (WEST, SOUTH, CLOCKWISE): CLOSING,
            (WEST, SOUTH, COUNTER_CLOCKWISE): OPENING,
            (NORTH, EAST, CLOCKWISE): OPENING,
            (NORTH, EAST, COUNTER_CLOCKWISE): CLOSING,
            (NORTH, WEST, CLOCKWISE): CLOSING,
            (NORTH, WEST, COUNTER_CLOCKWISE): OPENING,
            (SOUTH, EAST, CLOCKWISE): CLOSING,
            (SOUTH, EAST, COUNTER_CLOCKWISE): OPENING,
            (SOUTH, WEST, CLOCKWISE): OPENING,
            (SOUTH, WEST, COUNTER_CLOCKWISE): CLOSING,
            (NORTHEAST, SOUTHEAST, CLOCKWISE): OPENING,
            (NORTHEAST, SOUTHEAST, COUNTER_CLOCKWISE): CLOSING,
            (NORTHEAST, NORTHWEST, CLOCKWISE): CLOSING,
            (NORTHEAST, NORTHWEST, COUNTER_CLOCKWISE): OPENING,
            (SOUTHEAST, NORTHEAST, CLOCKWISE): CLOSING,
            (SOUTHEAST, NORTHEAST, COUNTER_CLOCKWISE): OPENING,
            (SOUTHEAST, SOUTHWEST, CLOCKWISE): OPENING,
            (SOUTHEAST, SOUTHWEST, COUNTER_CLOCKWISE): CLOSING,
            (SOUTHWEST, NORTHWEST, CLOCKWISE): OPENING,
            (SOUTHWEST, NORTHWEST, COUNTER_CLOCKWISE): CLOSING,
            (SOUTHWEST, SOUTHEAST, CLOCKWISE): CLOSING,
            (SOUTHWEST, SOUTHEAST, COUNTER_CLOCKWISE): OPENING,
            (NORTHWEST, SOUTHWEST, CLOCKWISE): CLOSING,
            (NORTHWEST, SOUTHWEST, COUNTER_CLOCKWISE): OPENING,
            (NORTHWEST, NORTHEAST, CLOCKWISE): OPENING,
            (NORTHWEST, NORTHEAST, COUNTER_CLOCKWISE): CLOSING,
        }
        return blue_static_direction_map, red_static_direction_map
