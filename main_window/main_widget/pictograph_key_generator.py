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

    def generate_pictograph_key(self, pictograph_dict: dict) -> str:
        blue_attrs = pictograph_dict["blue_attributes"]
        red_attrs = pictograph_dict["red_attributes"]
        
        return (
            f"{pictograph_dict[LETTER]}_"
            f"{pictograph_dict[START_POS]}→{pictograph_dict[END_POS]}_"
            f"{pictograph_dict[TIMING]}_"
            f"{pictograph_dict[DIRECTION]}_"
            f"{blue_attrs[MOTION_TYPE]}_"
            f"{blue_attrs[PROP_ROT_DIR]}_"
            f"{blue_attrs[START_LOC]}→{blue_attrs[END_LOC]}_"
            f"{red_attrs[MOTION_TYPE]}_"
            f"{red_attrs[PROP_ROT_DIR]}_"
            f"{red_attrs[START_LOC]}→{red_attrs[END_LOC]}"
        )
