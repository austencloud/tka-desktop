from typing import TYPE_CHECKING
from data.constants import *
from main_window.main_widget.turns_tuple_generator.turns_tuple_generators.base_turns_tuple_generator import (
    BaseTurnsTupleGenerator,
)


class Type3TurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        shift = self.pictograph.managers.get.shift()
        dash = self.pictograph.managers.get.dash()
        if shift.state.motion_type in [PRO, ANTI]:
            direction = (
                "s" if dash.state.prop_rot_dir == shift.state.prop_rot_dir else "o"
            )
            if dash.state.turns > 0:
                if isinstance(shift.state.turns, int) or isinstance(
                    shift.state.turns, float
                ):
                    if shift.state.turns > 0:
                        return f"({direction}, {self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
                    elif dash.state.turns > 0:
                        return f"({direction}, {self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
                    else:
                        return f"({self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
                elif shift.state.turns == "fl":
                    if dash.state.turns > 0:
                        return f"({direction}, {self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
                    else:
                        return f"({self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
            elif dash.state.turns == 0:
                return (
                    f"({self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
                )
        elif shift.state.motion_type == FLOAT:
            if dash.state.turns != 0 and dash.state.prop_rot_dir != NO_ROT:
                direction = (
                    "s"
                    if dash.state.prop_rot_dir == shift.state.prefloat_prop_rot_dir
                    else "o"
                )
                return f"({direction}, {self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
            else:
                return (
                    f"({self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
                )
