from typing import TYPE_CHECKING
from data.constants import (
    DIRECTION,
    END_LOC,
    END_POS,
    LETTER,
    MOTION_TYPE,
    PROP_ROT_DIR,
    START_LOC,
    START_POS,
    TIMING,
)

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class PictographKeyGenerator:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget

    def generate_pictograph_key(self, pictograph_data: dict) -> str:
        blue_attrs = pictograph_data["blue_attributes"]
        red_attrs = pictograph_data["red_attributes"]

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
