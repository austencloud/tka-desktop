from objects.prop.prop_classes import *
from Enums.PropTypes import PropType


class PropFactory:
    def __init__(self):
        self.prop_classes = {
            PropType.Hand.name.lower(): Hand,
            PropType.Staff.name.lower(): Staff,
            PropType.Bigstaff.name.lower(): BigStaff,
            PropType.Triad.name.lower(): Triad,
            PropType.Minihoop.name.lower(): MiniHoop,
            PropType.Fan.name.lower(): Fan,
            PropType.Club.name.lower(): Club,
            PropType.Buugeng.name.lower(): Buugeng,
            PropType.Bigbuugeng.name.lower(): BigBuugeng,
            PropType.Fractalgeng.name.lower(): Fractalgeng,
            PropType.Eightrings.name.lower(): EightRings,
            PropType.BigEightRings.name.lower(): BigEightRings,
            PropType.Doublestar.name.lower(): DoubleStar,
            PropType.Bighoop.name.lower(): BigHoop,
            PropType.Bigdoublestar.name.lower(): BigDoubleStar,
            PropType.Quiad.name.lower(): Quiad,
            PropType.Sword.name.lower(): Sword,
            PropType.Guitar.name.lower(): Guitar,
            PropType.Ukulele.name.lower(): Ukulele,
            PropType.Chicken.name.lower(): Chicken,
        }

    def create_prop_of_type(
        self, existing_prop: Prop, target_prop_type: PropType
    ) -> Prop:
        if isinstance(target_prop_type, str):
            target_prop_type = PropType[target_prop_type]
        elif isinstance(target_prop_type, PropType):
            target_prop_type = target_prop_type

        if target_prop_type.name.lower() in self.prop_classes:
            return self.prop_classes[target_prop_type.name.lower()](
                existing_prop.pictograph, existing_prop.prop_dict, existing_prop.motion
            )
        else:
            raise ValueError(f"Unknown prop type: {target_prop_type}")
