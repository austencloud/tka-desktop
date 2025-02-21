from typing import TYPE_CHECKING
from main_window.main_widget.turns_tuple_generator.turns_tuple_generators.base_turns_tuple_generator import (
    BaseTurnsTupleGenerator,
)

if TYPE_CHECKING:
    pass


class Type4TurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        dash = self.pictograph.managers.get.dash()
        static = self.pictograph.managers.get.static()
        if dash.turns == 0 and static.turns == 0:
            return f"({self._normalize_turns(dash)}, {self._normalize_turns(static)})"
        elif dash.turns == 0 or static.turns == 0:
            turning_motion = dash if dash.turns != 0 else static
            return f"({turning_motion.prop_rot_dir}, {self._normalize_turns(dash)}, {self._normalize_turns(static)})"
        else:
            direction = "s" if dash.prop_rot_dir == static.prop_rot_dir else "o"
            return f"({direction}, {self._normalize_turns(dash)}, {self._normalize_turns(static)})"
