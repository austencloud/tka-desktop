from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Union

from objects import motion
from objects.prop.prop_updater import PropUpdater
from ..graphical_object import GraphicalObject
from PyQt6.QtWidgets import QGraphicsPixmapItem
from .prop_attr_manager import PropAttrManager
from .prop_checker import PropChecker
from .prop_rot_angle_manager import PropRotAngleManager

if TYPE_CHECKING:
    from enums.prop_type import PropType
    from objects.arrow.arrow import Arrow
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
    from objects.motion.motion import Motion


@dataclass
class PropState:
    color: Optional[str] = None
    prop_type: Optional[str] = None
    loc: Optional[str] = None
    ori: Optional[str] = None

    def update_from_dict(
        self, prop_data: dict[str, Union[str, "Arrow", "QGraphicsPixmapItem"]]
    ) -> None:
        for key, value in prop_data.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Prop(GraphicalObject):
    arrow: "Arrow"
    motion: "Motion"
    prop_data: dict
    attr_manager: PropAttrManager
    rot_angle_manager: PropRotAngleManager
    check: PropChecker
    updater: PropUpdater
    state: PropState
    pixmap_item: QGraphicsPixmapItem
    name = "prop"

    def __init__(
        self, pictograph, prop_data: dict, motion: "Motion", prop_type_str: str
    ):
        super().__init__(pictograph)
        self.motion = motion
        self.prop_data = prop_data
        self.prop_type_str = prop_type_str
        self.pictograph: LegacyPictograph = pictograph
        self.attr_manager = PropAttrManager(self)
        self.rot_angle_manager = PropRotAngleManager(self)
        self.check = PropChecker(self)
        self.updater = PropUpdater(self)
        self.state = PropState()
