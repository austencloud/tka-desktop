from typing import TYPE_CHECKING
from data.constants import (
    BLUE_ATTRIBUTES,
    DIRECTION,
    END_LOC,
    END_POS,
    LETTER,
    MOTION_TYPE,
    PROP_ROT_DIR,
    RED_ATTRIBUTES,
    START_LOC,
    START_POS,
    TIMING,
)

if TYPE_CHECKING:
    pass


class PictographKeyGenerator:
    def generate_pictograph_key(self, pictograph_data: dict) -> str:
        blue_attrs = pictograph_data[BLUE_ATTRIBUTES]
        red_attrs = pictograph_data[RED_ATTRIBUTES]

        return (
            f"{pictograph_data[LETTER]}_"
            f"{pictograph_data[START_POS]}→{pictograph_data[END_POS]}_"
            f"{pictograph_data[TIMING]}_"
            f"{pictograph_data[DIRECTION]}_"
            f"{blue_attrs[MOTION_TYPE]}_"
            f"{blue_attrs[PROP_ROT_DIR]}_"
            f"{blue_attrs[START_LOC]}→{blue_attrs[END_LOC]}_"
            f"{red_attrs[MOTION_TYPE]}_"
            f"{red_attrs[PROP_ROT_DIR]}_"
            f"{red_attrs[START_LOC]}→{red_attrs[END_LOC]}"
        )
