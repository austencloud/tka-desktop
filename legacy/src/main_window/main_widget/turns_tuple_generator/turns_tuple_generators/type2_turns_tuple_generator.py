from typing import TYPE_CHECKING
from data.constants import *
from main_window.main_widget.turns_tuple_generator.turns_tuple_generators.base_turns_tuple_generator import (
    BaseTurnsTupleGenerator,
)

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class Type2TurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph: "LegacyPictograph") -> str:
        super().set_pictograph(pictograph)

        shift = (
            self.red_motion if self.red_motion.check.is_shift() else self.blue_motion
        )
        static = (
            self.red_motion if self.red_motion.check.is_static() else self.blue_motion
        )
        if shift.state.motion_type in [PRO, ANTI]:
            if static.state.turns != 0 and static.state.prop_rot_dir != NO_ROT:
                direction = (
                    "s"
                    if static.state.prop_rot_dir == shift.state.prop_rot_dir
                    else "o"
                )
                return f"({direction}, {self._normalize_turns(shift)}, {self._normalize_turns(static)})"
            else:
                return (
                    f"({self._normalize_turns(shift)}, {self._normalize_turns(static)})"
                )
        elif shift.state.motion_type == FLOAT:
            if static.state.turns != 0 and static.state.prop_rot_dir != NO_ROT:
                direction = (
                    "s"
                    if static.state.prop_rot_dir == shift.state.prefloat_prop_rot_dir
                    else "o"
                )
                return f"({direction}, {self._normalize_turns(shift)}, {self._normalize_turns(static)})"
            else:
                return (
                    f"({self._normalize_turns(shift)}, {self._normalize_turns(static)})"
                )
