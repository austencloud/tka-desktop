# objects/arrow/arrow.py
from objects.arrow.managers.location_manager.arrow_location_manager import (
    ArrowLocationManager,
)
from objects.arrow.managers.rot_angle_manager.arrow_rot_angle_manager import (
    ArrowRotAngleManager,
)
from .arrow_state import ArrowState
from .arrow_mirror_handler import ArrowMirrorManager
from .arrow_updater import ArrowUpdater
from ..graphical_object import GraphicalObject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..motion.motion import Motion
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class Arrow(GraphicalObject):
    motion: "Motion"
    name = "arrow"

    def __init__(self, pictograph, arrow_data) -> None:
        super().__init__(pictograph)
        self.arrow_data = arrow_data
        self.pictograph: "LegacyPictograph" = pictograph
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
