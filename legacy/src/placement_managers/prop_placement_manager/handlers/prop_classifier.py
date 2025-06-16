from typing import TYPE_CHECKING
from enums.prop_type import PropType
from objects.prop.prop import Prop
from enums.prop_type import (
    big_unilateral_prop_types,
    small_unilateral_prop_types,
    small_bilateral_prop_types,
    big_bilateral_prop_types,
)

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class PropClassifier:
    def __init__(self, pictograph: "LegacyPictograph") -> None:
        self.pictograph = pictograph
        self.big_uni: list[Prop] = []
        self.small_uni: list[Prop] = []
        self.small_bi: list[Prop] = []
        self.big_bi: list[Prop] = []
        self.hands: list[Prop] = []
        self.big_props: list[Prop] = []
        self.small_props: list[Prop] = []

    def classify_props(self) -> None:
        self.big_uni.clear()
        self.small_uni.clear()
        self.small_bi.clear()
        self.big_bi.clear()
        self.hands.clear()

        for prop in self.pictograph.elements.props.values():
            prop_type_enum = PropType.get_prop_type(prop.prop_type_str)
            if prop_type_enum in big_unilateral_prop_types:
                self.big_uni.append(prop)
            elif prop_type_enum in small_unilateral_prop_types:
                self.small_uni.append(prop)
            elif prop_type_enum in small_bilateral_prop_types:
                self.small_bi.append(prop)
            elif prop_type_enum in big_bilateral_prop_types:
                self.big_bi.append(prop)
            elif prop_type_enum == PropType.Hand:
                self.hands.append(prop)

        self.big_props = self.big_uni + self.big_bi
        self.small_props = self.small_uni + self.small_bi
