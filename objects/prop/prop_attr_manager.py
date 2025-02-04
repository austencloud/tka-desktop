from typing import TYPE_CHECKING, Union

from data.constants import *

from Enums.Enums import Axes, PropAttribute, Turns


if TYPE_CHECKING:
    from objects.prop.prop import Prop


class PropAttrManager:
    def __init__(self, prop: "Prop") -> None:
        self.prop = prop
        self.update_attributes(self.prop.prop_dict)

    def update_attributes(
        self, prop_dict: dict[str, Union[str, str, str, Turns]]
    ) -> None:
        prop_attributes = [COLOR, LOC, LAYER, ORI, MOTION, PROP_TYPE]
        for attr in prop_attributes:
            value = prop_dict.get(attr)
            if value is not None:
                setattr(self.prop, attr, value)
        self.set_z_value_based_on_color()

    def clear_attributes(self) -> None:
        prop_attributes = [COLOR, LOC, LAYER, ORI, MOTION, PROP_TYPE]
        for attr in prop_attributes:
            setattr(self.prop, attr, None)

    def get_axis_from_ori(self) -> None:
        if self.prop.check.is_radial():
            axis: Axes = VERTICAL if self.prop.loc in [NORTH, SOUTH] else HORIZONTAL
        elif self.prop.check.is_nonradial():
            axis: Axes = HORIZONTAL if self.prop.loc in [NORTH, SOUTH] else VERTICAL
        else:
            axis: Axes = None
        return axis

    def swap_ori(self) -> None:
        ori_map = {
            IN: OUT,
            OUT: IN,
            CLOCK: COUNTER,
            COUNTER: CLOCK,
        }
        self.ori = ori_map[self.ori]

    def get_attributes(self) -> dict[str, Union[str, str, str]]:
        prop_attributes = [attr.value for attr in PropAttribute]
        return {attr: getattr(self.prop, attr) for attr in prop_attributes}

    def set_z_value_based_on_color(self) -> None:
        if self.prop.color == RED:
            self.prop.setZValue(5)  # Higher Z value for red props
        elif self.prop.color == BLUE:
            self.prop.setZValue(4)  # Lower Z value for blue props
