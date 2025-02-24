from typing import TYPE_CHECKING

from objects.motion.motion_state import MotionState
from objects.motion.motion_turns_manager import MotionTurnsManager
from .motion_checker import MotionChecker
from .motion_ori_calculator import MotionOriCalculator
from .motion_updater import MotionUpdater

if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph import Pictograph

    from objects.arrow.arrow import Arrow
    from objects.prop.prop import Prop


class Motion:
    pictograph: "Pictograph"
    arrow: "Arrow"
    prop: "Prop"

    def __init__(self, pictograph: "Pictograph", motion_data: dict) -> None:
        self.pictograph = pictograph
        self.motion_data = motion_data
        self.state = MotionState()
        self.ori_calculator = MotionOriCalculator(self)
        self.updater = MotionUpdater(self)
        self.check = MotionChecker(self)
        self.turns_manager = MotionTurnsManager(self)
