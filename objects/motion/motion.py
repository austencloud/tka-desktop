from typing import TYPE_CHECKING

from objects.motion.motion_turns_manager import MotionTurnsManager
from .motion_checker import MotionChecker
from .motion_attr_manager import MotionAttrManager
from .motion_ori_calculator import MotionOriCalculator
from .motion_updater import MotionUpdater

if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph_scene import PictographScene

    from objects.arrow.arrow import Arrow
    from objects.prop.prop import Prop


class Motion:
    pictograph: "PictographScene"
    color: str
    turns: int
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

    def __init__(self, pictograph: "PictographScene", motion_data: dict) -> None:
        self.pictograph = pictograph
        self.motion_data = motion_data
        self.ori_calculator = MotionOriCalculator(self)
        self.attr_manager = MotionAttrManager(self)
        self.updater = MotionUpdater(self)
        self.check = MotionChecker(self)
        self.turns_manager = MotionTurnsManager(self)
