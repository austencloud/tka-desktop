from typing import TYPE_CHECKING
import random
from data.constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
)


class RotationDeterminer:
    @staticmethod
    def get_rotation_dirs(prop_continuity: str):
        if prop_continuity == "continuous":
            return random.choice([CLOCKWISE, COUNTER_CLOCKWISE]), random.choice(
                [CLOCKWISE, COUNTER_CLOCKWISE]
            )
        return None, None
