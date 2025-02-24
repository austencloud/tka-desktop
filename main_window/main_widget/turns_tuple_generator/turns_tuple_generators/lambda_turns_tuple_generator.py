from data.constants import (
    EAST,
    NORTH,
    CLOCKWISE,
    OPENING,
    CLOSING,
    WEST,
    SOUTH,
    NORTHEAST,
    SOUTHEAST,
    NORTHWEST,
    SOUTHWEST,
    COUNTER_CLOCKWISE,
)
from .base_turns_tuple_generator import BaseTurnsTupleGenerator


class LambdaTurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        dash = self.pictograph.managers.get.dash()
        static = self.pictograph.managers.get.static()
        dash_direction_map, static_direction_map = self._get_direction_maps()

        if dash.state.turns == 0 and static.state.turns > 0:
            open_close_state = static_direction_map.get(
                (dash.state.end_loc, static.state.end_loc, static.state.prop_rot_dir), ""
            )
            return f"({self._normalize_turns(dash)}, {self._normalize_turns(static)}, {open_close_state})"
        elif static.state.turns == 0 and dash.state.turns > 0:
            open_close_state = dash_direction_map.get(
                (dash.state.end_loc, static.state.end_loc, dash.state.prop_rot_dir), ""
            )
            return f"({self._normalize_turns(dash)}, {self._normalize_turns(static)}, {open_close_state})"
        elif static.state.turns > 0 and dash.state.turns > 0:
            static_open_close_state = static_direction_map.get(
                (dash.state.end_loc, static.state.end_loc, static.state.prop_rot_dir), ""
            )
            dash_open_close_state = dash_direction_map.get(
                (dash.state.end_loc, static.state.end_loc, dash.state.prop_rot_dir), ""
            )
            vtg_dir = "s" if static.state.prop_rot_dir == dash.state.prop_rot_dir else "o"
            return f"({vtg_dir}, {self._normalize_turns(dash)}, {self._normalize_turns(static)}, {dash_open_close_state}, {static_open_close_state})"
        else:
            return f"({self._normalize_turns(dash)}, {self._normalize_turns(static)})"

    def _get_direction_maps(self):
        dash_direction_map = {
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
        static_direction_map = {
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
        return dash_direction_map, static_direction_map
