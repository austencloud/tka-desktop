from main_window.main_widget.turns_tuple_generator.turns_tuple_generators.base_turns_tuple_generator import (
    BaseTurnsTupleGenerator,
)


class Type56TurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        if self.blue_motion.state.turns == 0 and self.red_motion.state.turns == 0:
            return f"({self._normalize_turns(self.blue_motion)}, {self._normalize_turns(self.red_motion)})"
        elif self.blue_motion.state.turns == 0 or self.red_motion.state.turns == 0:
            turning_motion = (
                self.blue_motion
                if self.blue_motion.state.turns != 0
                else self.red_motion
            )
            return f"({turning_motion.state.prop_rot_dir}, {self._normalize_turns(self.blue_motion)}, {self._normalize_turns(self.red_motion)})"
        else:
            direction = (
                "s"
                if self.blue_motion.state.prop_rot_dir
                == self.red_motion.state.prop_rot_dir
                else "o"
            )
            return f"({direction}, {self._normalize_turns(self.blue_motion)}, {self._normalize_turns(self.red_motion)})"
