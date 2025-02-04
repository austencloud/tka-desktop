from .managers.location_manager.arrow_location_manager import ArrowLocationManager
from .managers.arrow_mirror_handler import ArrowMirrorManager
from .managers.arrow_updater import ArrowUpdater
from .managers.arrow_attr_handler import ArrowAttrManager
from .managers.rot_angle_manager.arrow_rot_angle_manager import ArrowRotAngleManager

from ..graphical_object.graphical_object import GraphicalObject
from Enums.Enums import Turns
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..motion.motion import Motion
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class Arrow(GraphicalObject):
    """
    An arrow graphical object that can be added to a pictograph as part of a motion.

    Parameters
    ----------
    pictograph : Pictograph
        The pictograph to which the arrow belongs.
    arrow_dict : dict
        A dictionary containing the arrow's attributes.

    """

    svg_cache = {}
    turns: Turns
    motion: "Motion"
    color: str
    location: str
    is_svg_mirrored: bool
    loc: str = None
    initialized: bool = False

    def __init__(self, pictograph, arrow_dict) -> None:
        super().__init__(pictograph)
        self.arrow_dict = arrow_dict
        self.pictograph: BasePictograph = pictograph

    def setup_components(self):
        self.location_manager = ArrowLocationManager(self)
        self.rot_angle_manager = ArrowRotAngleManager(self)
        self.mirror_manager = ArrowMirrorManager(self)
        self.attr_manager = ArrowAttrManager(self)
        self.updater = ArrowUpdater(self)
        self.initialized = True
