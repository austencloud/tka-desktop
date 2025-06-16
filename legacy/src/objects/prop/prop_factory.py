from typing import Union


import importlib

from data.prop_class_mapping import PropType
from objects.prop.prop import Prop


class PropFactory:
    def __init__(self):
        self.module_path = (
            "objects.prop.prop_classes"  # Module where the classes are defined
        )

        # Instead of directly referencing classes, store their names
        self.prop_classes = {
            PropType.Hand.name.lower(): "Hand",
            PropType.Staff.name.lower(): "Staff",
            PropType.Simplestaff.name.lower(): "Simplestaff",  # Added Simplestaff
            PropType.Bigstaff.name.lower(): "BigStaff",
            PropType.Triad.name.lower(): "Triad",
            PropType.Minihoop.name.lower(): "Minihoop",
            PropType.Fan.name.lower(): "Fan",
            PropType.Club.name.lower(): "Club",
            PropType.Buugeng.name.lower(): "Buugeng",
            PropType.Bigbuugeng.name.lower(): "BigBuugeng",
            PropType.Fractalgeng.name.lower(): "Fractalgeng",
            PropType.Eightrings.name.lower(): "EightRings",
            PropType.BigEightRings.name.lower(): "BigEightRings",
            PropType.Doublestar.name.lower(): "DoubleStar",
            PropType.Bighoop.name.lower(): "BigHoop",
            PropType.Bigdoublestar.name.lower(): "BigDoubleStar",
            PropType.Quiad.name.lower(): "Quiad",
            PropType.Sword.name.lower(): "Sword",
            PropType.Guitar.name.lower(): "Guitar",
            PropType.Ukulele.name.lower(): "Ukulele",
            PropType.Chicken.name.lower(): "Chicken",
            PropType.Triquetra.name.lower(): "Triquetra",
            PropType.Triquetra2.name.lower(): "Triquetra2",
        }

    def get_class(self, class_name):
        """Dynamically import a class from the module path."""
        try:
            module = importlib.import_module(self.module_path)
            return getattr(module, class_name)  # Fetch class dynamically
        except (ModuleNotFoundError, AttributeError):
            raise ImportError(
                f"Class '{class_name}' not found in '{self.module_path}'."
            )

    def create_prop_of_type(self, existing_prop: "Prop", target_prop_type: str):
        """Instantiate the correct prop class dynamically."""
        if isinstance(target_prop_type, str):
            target_prop_type = PropType[target_prop_type]
        elif not isinstance(target_prop_type, PropType):
            raise ValueError(f"Invalid prop type: {target_prop_type}")
        target_prop_type: PropType
        class_name = self.prop_classes.get(target_prop_type.name.lower())

        if class_name:
            prop_class = self.get_class(class_name)  # Dynamically get the class
            return prop_class(
                existing_prop.pictograph, existing_prop.prop_data, existing_prop.motion
            )
        else:
            raise ValueError(f"Unknown prop type: {target_prop_type}")
