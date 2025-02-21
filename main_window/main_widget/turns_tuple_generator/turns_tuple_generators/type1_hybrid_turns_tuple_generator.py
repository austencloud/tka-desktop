from typing import TYPE_CHECKING
from data.constants import *
from main_window.main_widget.turns_tuple_generator.turns_tuple_generators.base_turns_tuple_generator import (
    BaseTurnsTupleGenerator,
)

if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph_scene import PictographScene


class Type1HybridTurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph: "PictographScene") -> str:
        super().set_pictograph(pictograph)
        # if one of the motions is not a float, proceed with the written logic
        if not pictograph.check.has_one_float():
            pro_motion = (
                self.blue_motion
                if self.blue_motion.motion_type == PRO
                else self.red_motion
            )
            anti_motion = (
                self.blue_motion
                if self.blue_motion.motion_type == ANTI
                else self.red_motion
            )
            return f"({pro_motion.turns}, {anti_motion.turns})"
        elif pictograph.check.has_one_float():
            # return blue, then red tuple
            return f"({self._normalize_turns(self.blue_motion)}, {self._normalize_turns(self.red_motion)})"
