import logging
from data.constants import DASH, FLOAT, PRO, ANTI, STATIC
from objects.motion.motion import Motion
from .dash_directional_tuple_generator import DashDirectionalGenerator
from .shift_directional_tuple_generator import ShiftDirectionalGenerator
from .static_directional_tuple_generator import StaticDirectionalGenerator
from .base_directional_tuple_generator import BaseDirectionalGenerator


class DirectionalTupleManager:
    """

    DirectionalTupleManager generates directional tuples for a given motion. 
    Directional tuples are used to adjust the arrow's
    special placement in the pictograph.

    These generators ensure that we can use one tuple for each adjustment and
    apply it correctly in each quadrant by modifying the x and y values to match.

    """

    def __init__(self, motion: Motion) -> None:
        self.generator: BaseDirectionalGenerator = self._select_generator(motion)

    def _select_generator(self, motion: Motion) -> "BaseDirectionalGenerator":
        if motion.motion_type in [PRO, ANTI, FLOAT]:
            return ShiftDirectionalGenerator(motion)
        elif motion.motion_type == DASH:
            return DashDirectionalGenerator(motion)
        elif motion.motion_type == STATIC:
            return StaticDirectionalGenerator(motion)
        else:
            logging.error(
                f"Can't find a directional tuple generator for motion type: {motion.motion_type}"
            )

    def generate_directional_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        new_var = self.generator.generate_directional_tuples(x, y)
        return new_var
