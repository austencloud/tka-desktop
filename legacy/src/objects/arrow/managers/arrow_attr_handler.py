from typing import Union, TYPE_CHECKING

from enums.glyph_enum import Turns
from data.constants import *

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowAttrManager:
    def __init__(self, arrow: "Arrow") -> None:
        self.arrow = arrow
        self.arrow.state.color = self.arrow.arrow_data[COLOR]
        self.arrow.turns = self.arrow.arrow_data[TURNS]

    def update_attributes(
        self, arrow_data: dict[str, Union[str, str, str, Turns]]
    ) -> None:
        arrow_attributes = [COLOR, LOC, MOTION_TYPE, TURNS]
        for attr in arrow_attributes:
            value = arrow_data.get(attr)
            if value is not None:
                setattr(self.arrow, attr, value)
                self.arrow.arrow_data[attr] = value

    def clear_attributes(self) -> None:
        arrow_attributes = [COLOR, LOC, MOTION_TYPE, TURNS]
        for attr in arrow_attributes:
            setattr(self.arrow, attr, None)

    def get_arrow_attributes(self) -> dict[str, Union[str, str, str]]:
        arrow_attributes = [COLOR, LOC]
        return {attr: getattr(self.arrow, attr) for attr in arrow_attributes}
