from data.constants import PROP_TYPE
from enums.prop_type import PropType
from objects.prop.prop import Prop

# List of prop class names
prop_types = [
    "Hand",
    "Staff",
    "Simplestaff",  # Added Simplestaff
    "BigStaff",
    "Triad",
    "Minihoop",
    "Fan",
    "Club",
    "Buugeng",
    "BigBuugeng",
    "Fractalgeng",
    "EightRings",
    "BigEightRings",
    "DoubleStar",
    "BigHoop",
    "BigDoubleStar",
    "Quiad",
    "Sword",
    "Guitar",
    "Ukulele",
    "Chicken",
    "Triquetra",
    "Triquetra2",
]

# Dictionary to store dynamically created classes
prop_class_registry = {}

# Dynamically create and store prop classes
for prop_type in prop_types:

    def init(self, pictograph, attributes, motion, prop_type=prop_type):
        attributes[PROP_TYPE] = getattr(PropType, prop_type)
        super(type(self), self).__init__(pictograph, attributes, motion, prop_type)

    # Dynamically create a new prop class
    prop_class = type(prop_type, (Prop,), {"__init__": init})

    # Register in the global dictionary
    globals()[prop_type] = prop_class
    prop_class_registry[prop_type.lower()] = prop_class  # Store in a lookup dictionary
