from typing import TYPE_CHECKING
from main_window.main_widget.turns_tuple_generator.turns_tuple_generators.base_turns_tuple_generator import (
    BaseTurnsTupleGenerator,
)


class Type4TurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        dash = self.pictograph.managers.get.dash()
        static = self.pictograph.managers.get.static()
        if dash.state.turns == 0 and static.state.turns == 0:
            return f"({self._normalize_turns(dash)}, {self._normalize_turns(static)})"
        elif dash.state.turns == 0 or static.state.turns == 0:
            turning_motion = dash if dash.state.turns != 0 else static
            return f"({turning_motion.state.prop_rot_dir}, {self._normalize_turns(dash)}, {self._normalize_turns(static)})"
        else:
            direction = (
                "s" if dash.state.prop_rot_dir == static.state.prop_rot_dir else "o"
            )
            return f"({direction}, {self._normalize_turns(dash)}, {self._normalize_turns(static)})"
