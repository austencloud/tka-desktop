from typing import TYPE_CHECKING
from main_window.main_widget.turns_tuple_generator.turns_tuple_generators.base_turns_tuple_generator import (
    BaseTurnsTupleGenerator,
)


class ColorTurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        key = f"({self._normalize_turns(self.blue_motion)}, {self._normalize_turns(self.red_motion)})"
        return key
