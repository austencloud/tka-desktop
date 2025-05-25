from typing import TYPE_CHECKING
import random
from data.constants import (
    END_POS,
)


class PictographSelector:
    @staticmethod
    def select_pictograph(options: list, expected_end_pos: str):
        valid_options = [opt for opt in options if opt[END_POS] == expected_end_pos]
        if not valid_options:
            raise ValueError(f"No valid pictograph with end pos {expected_end_pos}")
        return random.choice(valid_options)
