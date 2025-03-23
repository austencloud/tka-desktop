from enum import Enum
from typing import TYPE_CHECKING, Union

from data.constants import *
from data.prop_class_mapping import PropType
from objects.prop.prop_state import PropState

if TYPE_CHECKING:
    from objects.prop.prop import Prop


class PropAttribute(Enum):
    COLOR = "color"
    PROP_TYPE = "prop_type"
    LOC = "loc"
    ORI = "ori"
    MOTION = "motion"
    LAYER = "layer"


class PropAttrManager:
    def __init__(self, prop: "Prop") -> None:
        self.prop = prop

    def update_attributes(
        self, prop_data: dict[str, Union[str, str, str, int]]
    ) -> None:
        self.prop.state.update_from_dict(prop_data)
        if PROP_TYPE in prop_data:
            value = prop_data[PROP_TYPE]
            self.prop.state.prop_type = (
                value.name if isinstance(value, PropType) else value
            )
        self.set_z_value_based_on_color()

    def clear_attributes(self) -> None:
        self.prop.state = PropState()  # Reset state to default

    def swap_ori(self) -> None:
        ori_map = {
            IN: OUT,
            OUT: IN,
            CLOCK: COUNTER,
            COUNTER: CLOCK,
        }
        if self.prop.state.ori in ori_map:
            self.prop.state.ori = ori_map[self.prop.state.ori]

    def get_attributes(self) -> dict[str, Union[str, str, str]]:
        return {
            attr: getattr(self.prop.state, attr, None)
            for attr in PropAttribute._member_names_
        }

    def set_z_value_based_on_color(self) -> None:
        if self.prop.state.color == RED:
            self.prop.setZValue(5)  # Higher Z value for red props
        elif self.prop.state.color == BLUE:
            self.prop.setZValue(4)  # Lower Z value for blue props
