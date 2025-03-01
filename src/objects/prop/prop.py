from typing import TYPE_CHECKING, Optional

from objects.prop.prop_updater import PropUpdater
from ..graphical_object import GraphicalObject
from PyQt6.QtWidgets import QGraphicsPixmapItem
from .prop_attr_manager import PropAttrManager
from .prop_checker import PropChecker
from .prop_rot_angle_manager import PropRotAngleManager

if TYPE_CHECKING:
    from enums.prop_type import PropType
    from objects.arrow.arrow import Arrow
    from base_widgets.pictograph.pictograph import Pictograph
    from objects.motion.motion import Motion


class Prop(GraphicalObject):
    loc: str
    ori: str
    previous_location: str
    prop_type_str: str
    arrow: "Arrow"
    pixmap_item: Optional["QGraphicsPixmapItem"]
    color: str
    motion: "Motion"
    prop_data: dict
    attr_manager: PropAttrManager
    rot_angle_manager: PropRotAngleManager
    check: PropChecker
    updater: PropUpdater

    def __init__(
        self, pictograph, prop_data: dict, motion: "Motion", prop_type_str: str
    ):
        super().__init__(pictograph)
        self.motion = motion
        self.prop_data = prop_data
        self.prop_type_str = prop_type_str  # Store the prop type for reference

        self.pictograph: Pictograph = pictograph
        self.attr_manager = PropAttrManager(self)
        self.rot_angle_manager = PropRotAngleManager(self)
        self.check = PropChecker(self)
        self.updater = PropUpdater(self)
