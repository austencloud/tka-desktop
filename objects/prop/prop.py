from typing import TYPE_CHECKING, Optional
from ..graphical_object import GraphicalObject
from PyQt6.QtWidgets import QGraphicsPixmapItem
from .prop_attr_manager import PropAttrManager
from .prop_checker import PropChecker
from .prop_rot_angle_manager import PropRotAngleManager
from .prop_updater import PropUpdater

if TYPE_CHECKING:
    from Enums.PropTypes import PropType
    from objects.arrow.arrow import Arrow
    from base_widgets.pictograph.pictograph import Pictograph
    from objects.motion.motion import Motion


class Prop(GraphicalObject):
    loc: str
    ori: str
    previous_location: str
    prop_type: str
    arrow: "Arrow"
    pixmap_item: Optional["QGraphicsPixmapItem"]

    def __init__(self, pictograph, prop_data: dict, motion: "Motion", prop_type: str):
        super().__init__(pictograph)
        self.motion = motion
        self.prop_data = prop_data
        self.prop_type = prop_type  # Store the prop type for reference

        self.pictograph: Pictograph = pictograph
        self.attr_manager = PropAttrManager(self)
        self.rot_angle_manager = PropRotAngleManager(self)
        self.check = PropChecker(self)
        self.updater = PropUpdater(self)
