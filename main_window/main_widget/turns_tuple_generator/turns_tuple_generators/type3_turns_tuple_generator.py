from typing import TYPE_CHECKING
from data.constants import *
from main_window.main_widget.turns_tuple_generator.turns_tuple_generators.base_turns_tuple_generator import (
    BaseTurnsTupleGenerator,
)

if TYPE_CHECKING:
    pass


class Type3TurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        shift = self.pictograph.managers.get.shift()
        dash = self.pictograph.managers.get.dash()
        if shift.motion_type in [PRO, ANTI]:
            direction = "s" if dash.prop_rot_dir == shift.prop_rot_dir else "o"
            if dash.turns > 0:
                if isinstance(shift.turns, int) or isinstance(shift.turns, float):
                    if shift.turns > 0:
                        return f"({direction}, {self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
                    elif dash.turns > 0:
                        return f"({direction}, {self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
                    else:
                        return f"({self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
                elif shift.turns == "fl":
                    if dash.turns > 0:
                        return f"({direction}, {self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
                    else:
                        return f"({self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
            elif dash.turns == 0:
                return (
                    f"({self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
                )
        elif shift.motion_type == FLOAT:
            direction = "s" if dash.prop_rot_dir == shift.prefloat_prop_rot_dir else "o"
            if dash.turns > 0:
                if isinstance(shift.turns, int) or isinstance(shift.turns, float):
                    if shift.turns > 0:
                        return f"({direction}, {self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
                    elif dash.turns > 0:
                        return f"({direction}, {self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
                    else:
                        return f"({self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
                elif shift.turns == "fl":
                    if dash.turns > 0:
                        return f"({direction}, {self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
                    else:
                        return f"({self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
            elif dash.turns == 0:
                return (
                    f"({self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
                )
