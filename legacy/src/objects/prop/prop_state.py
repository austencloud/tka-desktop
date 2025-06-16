from typing import TYPE_CHECKING, Optional

from objects.prop.prop_updater import PropUpdater
from ..graphical_object import GraphicalObject
from PyQt6.QtWidgets import QGraphicsPixmapItem
from .prop_checker import PropChecker
from .prop_rot_angle_manager import PropRotAngleManager

if TYPE_CHECKING:
    from enums.prop_type import PropType
    from objects.arrow.arrow import Arrow
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
    from objects.motion.motion import Motion


class PropState:
    def __init__(
        self,
        color: str,
        loc: str,
        ori: str,
        previous_location: str,
        arrow: "Arrow",
        pixmap_item: Optional["QGraphicsPixmapItem"],
    ):
        self.color = color
        self.loc = loc
        self.ori = ori
        self.previous_location = previous_location
        self.arrow = arrow
        self.pixmap_item = pixmap_item
