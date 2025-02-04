from enum import Enum, auto
from enum import Enum


class PropType(Enum):
    Hand = auto()
    Staff = auto()
    Bigstaff = auto()
    Club = auto()
    Buugeng = auto()
    Bigbuugeng = auto()
    Fractalgeng = auto()
    Eightrings = auto()
    BigEightRings = auto()
    Fan = auto()
    Triad = auto()
    Minihoop = auto()
    Bighoop = auto()
    Doublestar = auto()
    Bigdoublestar = auto()
    Quiad = auto()
    Sword = auto()
    Guitar = auto()
    Ukulele = auto()
    Chicken = auto()

    def get_prop_type(prop_type_value):
        for prop_type_enum in PropType:
            if str(prop_type_enum.name) == prop_type_value:
                return prop_type_enum


big_unilateral_prop_types = [
    PropType.Bighoop,
    PropType.Guitar,
    PropType.Sword,
    PropType.Chicken,
]
small_unilateral_prop_types = [
    PropType.Fan,
    PropType.Club,
    PropType.Minihoop,
    PropType.Triad,
    PropType.Ukulele,
]
big_bilateral_prop_types = [
    PropType.Bigstaff,
    PropType.Bigbuugeng,
    PropType.Bigdoublestar,
    PropType.BigEightRings,
]
small_bilateral_prop_types = [
    PropType.Staff,
    PropType.Buugeng,
    PropType.Doublestar,
    PropType.Quiad,
    PropType.Fractalgeng,
    PropType.Eightrings,
]
non_strictly_placed_props = [
    PropType.Staff,
    PropType.Fan,
    PropType.Club,
    PropType.Buugeng,
    PropType.Minihoop,
    PropType.Triad,
    PropType.Quiad,
    PropType.Ukulele,
    PropType.Chicken,
    PropType.Fractalgeng,
    PropType.Eightrings,
    PropType.BigEightRings,
]
strictly_placed_props = [
    PropType.Bighoop,
    PropType.Doublestar,
    PropType.Bigbuugeng,
    PropType.Bigdoublestar,
]

### LISTS FOR ITERATION ###

PropTypesList = [
    PropType.Staff,
    PropType.Bigstaff,
    PropType.Club,
    PropType.Buugeng,
    PropType.Bigbuugeng,
    PropType.Fractalgeng,
    PropType.Fan,
    PropType.Triad,
    PropType.Minihoop,
    PropType.Bighoop,
    PropType.Doublestar,
    PropType.Bigdoublestar,
    PropType.Quiad,
    PropType.Sword,
    PropType.Guitar,
    PropType.Ukulele,
    PropType.Chicken,
]
