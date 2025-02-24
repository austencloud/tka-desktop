# objects/arrow/arrow.py
from .arrow_state import ArrowState
from .location_manager.arrow_loc_manager import ArrowLocationManager
from .arrow_mirror_handler import ArrowMirrorManager
from .arrow_updater import ArrowUpdater
from .rot_angle_manager.arrow_rot_angle_manager import ArrowRotAngleManager
from ..graphical_object import GraphicalObject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..motion.motion import Motion
    from base_widgets.pictograph.pictograph import Pictograph


class Arrow(GraphicalObject):
    motion: "Motion"

    def __init__(self, pictograph, arrow_data) -> None:
        super().__init__(pictograph)
        self.arrow_data = arrow_data
        self.pictograph: "Pictograph" = pictograph
        self.state = ArrowState()
        self.state.initialized = False
        self.state.update_from_dict(arrow_data)

    def setup_components(self):
        """Lazily initializes components when accessed from the MotionUpdater."""
        if self.state.initialized:
            return

        self.location_manager = ArrowLocationManager(self)
        self.rot_angle_manager = ArrowRotAngleManager(self)
        self.mirror_manager = ArrowMirrorManager(self)
        self.updater = ArrowUpdater(self)

        self.state.initialized = True
