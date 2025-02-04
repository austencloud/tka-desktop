from typing import TYPE_CHECKING
from objects.prop.prop import Prop
from Enums.PropTypes import (
    PropType,
    big_unilateral_prop_types,
    small_unilateral_prop_types,
    small_bilateral_prop_types,
    big_bilateral_prop_types,
)

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


string_to_enum_map = {
    "hand": PropType.Hand,
    "staff": PropType.Staff,
    "bigstaff": PropType.Bigstaff,
    "club": PropType.Club,
    "buugeng": PropType.Buugeng,
    "bigbuugeng": PropType.Bigbuugeng,
    "fractalgeng": PropType.Fractalgeng,
    "eightrings": PropType.Eightrings,
    "bigeightrings": PropType.BigEightRings,
    "fan": PropType.Fan,
    "triad": PropType.Triad,
    "minihoop": PropType.Minihoop,
    "bighoop": PropType.Bighoop,
    "doublestar": PropType.Doublestar,
    "bigdoublestar": PropType.Bigdoublestar,
    "quiad": PropType.Quiad,
    "sword": PropType.Sword,
    "guitar": PropType.Guitar,
    "ukulele": PropType.Ukulele,
    "chicken": PropType.Chicken,
}


class PropClassifier:
    def __init__(self, pictograph: "BasePictograph") -> None:
        self.pictograph = pictograph
        self.classify_props()

    def classify_props(self) -> None:
        self.big_uni: list[Prop] = []
        self.small_uni: list[Prop] = []
        self.small_bi: list[Prop] = []
        self.big_bi: list[Prop] = []
        self.hands: list[Prop] = []

        for prop in self.pictograph.props.values():

            if prop.prop_type in big_unilateral_prop_types:
                self.big_uni.append(prop)
            elif prop.prop_type in small_unilateral_prop_types:
                self.small_uni.append(prop)
            elif prop.prop_type in small_bilateral_prop_types:
                self.small_bi.append(prop)
            elif prop.prop_type in big_bilateral_prop_types:
                self.big_bi.append(prop)
            elif prop.prop_type == PropType.Hand:
                self.hands.append(prop)

        self.big_props = self.big_uni + self.big_bi
        self.small_props = self.small_uni + self.small_bi
