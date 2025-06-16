from typing import Union, TYPE_CHECKING
from data.constants import COLOR, LOC, MOTION_TYPE, TURNS

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowAttrManager:
    def __init__(self, arrow: "Arrow") -> None:
        self.arrow = arrow
        self.arrow.state.color = self.arrow.arrow_data[COLOR]

    def update_attributes(
        self, arrow_data: dict[str, Union[str, str, str, int]]
    ) -> None:
        arrow_attributes = [COLOR, LOC, MOTION_TYPE, TURNS]
        for attr in arrow_attributes:
            value = arrow_data.get(attr)
            if value is not None:
                setattr(self.arrow.state, attr, value)
                self.arrow.arrow_data[attr] = value
