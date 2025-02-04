from typing import TYPE_CHECKING, Union

from .managers.motion_checker import MotionChecker
from .managers.motion_attr_manager import MotionAttrManager
from .managers.motion_manipulator import MotionManipulator
from .managers.motion_ori_calculator import MotionOriCalculator
from .managers.motion_updater import MotionUpdater
from .managers.motion_turn_manager import MotionTurnsManager


if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph

    from objects.arrow.arrow import Arrow
    from objects.prop.prop import Prop


class Motion:
    def __init__(self, pictograph: "BasePictograph", motion_dict: dict) -> None:
        self.pictograph = pictograph
        self.motion_dict = motion_dict
        self.ori_calculator = MotionOriCalculator(self)
        self.manipulator = MotionManipulator(self)
        self.attr_manager = MotionAttrManager(self)
        self.turns_manager = MotionTurnsManager(self)
        self.updater = MotionUpdater(self)
        self.check = MotionChecker(self)

    pictograph: "BasePictograph"
    color: str
    turns: Union[int, str]
    arrow: "Arrow"
    prop: "Prop"
    motion_type: str
    start_loc: str
    start_ori: str
    end_loc: str
    end_ori: str
    prop_rot_dir: str
    lead_state: str
    prefloat_motion_type: str = None
    prefloat_prop_rot_dir: str
