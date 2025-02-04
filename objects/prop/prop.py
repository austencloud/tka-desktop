from typing import TYPE_CHECKING
from ..graphical_object.graphical_object import GraphicalObject
from .prop_attr_manager import PropAttrManager
from .prop_checker import PropChecker
from .prop_rot_angle_manager import PropRotAngleManager
from .prop_updater import PropUpdater
from Enums.Enums import Axes
from Enums.PropTypes import PropType


if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow
    from base_widgets.base_pictograph.base_pictograph import BasePictograph

    from objects.motion.motion import Motion


class Prop(GraphicalObject):
    """
    A prop object that can be added to a pictograph.

    Parameters
    ----------
    pictograph : Pictograph
        The pictograph to which the prop belongs.
    prop_dict : dict
        A dictionary containing the prop's attributes.
    motion : Motion
        The motion to which the prop belongs.
    """

    loc: str = None
    ori: str = None
    axis: Axes
    prop_type: PropType

    def __init__(self, pictograph, prop_dict: dict, motion: "Motion") -> None:
        super().__init__(pictograph)
        self.motion = motion
        self.scene: BasePictograph = pictograph
        self.arrow: Arrow
        self.previous_location: str
        self.prop_dict = prop_dict
        self.attr_manager = PropAttrManager(self)
        self.rot_angle_manager = PropRotAngleManager(self)
        self.check = PropChecker(self)
        self.updater = PropUpdater(self)
