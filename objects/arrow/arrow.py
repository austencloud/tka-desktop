from .location_manager.arrow_loc_manager import ArrowLocationManager
from .arrow_mirror_handler import ArrowMirrorManager
from .arrow_updater import ArrowUpdater
from .arrow_attr_handler import ArrowAttrManager
from .rot_angle_manager.arrow_rot_angle_manager import ArrowRotAngleManager

from ..graphical_object.graphical_object import GraphicalObject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..motion.motion import Motion
    from base_widgets.pictograph.pictograph import Pictograph


class Arrow(GraphicalObject):
    motion: "Motion"
    color: str
    is_svg_mirrored: bool
    loc: str = None
    initialized: bool = False

    def __init__(self, pictograph, arrow_data) -> None:
        super().__init__(pictograph)
        self.arrow_data = arrow_data
        self.pictograph: Pictograph = pictograph
        self._initialized = False

    def setup_components(self):
        """Lazily initializes components when accessed from the MotionUpdater."""
        if self._initialized:
            return

        self.location_manager = ArrowLocationManager(self)
        self.rot_angle_manager = ArrowRotAngleManager(self)
        self.mirror_manager = ArrowMirrorManager(self)
        self.attr_manager = ArrowAttrManager(self)
        self.updater = ArrowUpdater(self)

        self._initialized = True
