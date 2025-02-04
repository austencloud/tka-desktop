from typing import TYPE_CHECKING
from data.constants import LOC, ORI

if TYPE_CHECKING:
    from objects.motion.motion import Motion


class MotionUpdater:
    def __init__(self, motion: "Motion") -> None:
        self.motion = motion

    def update_motion(self, motion_dict=None) -> None:
        if motion_dict:
            self.motion.attr_manager.update_attributes(motion_dict)
        if not self.motion.arrow.initialized:
            self.motion.arrow.setup_components()
        self.update_end_ori()
        prop_dict = {
            LOC: self.motion.end_loc,
            ORI: self.motion.end_ori,
        }
        self.motion.prop.updater.update_prop(prop_dict)

    def update_end_ori(self) -> None:
        self.motion.end_ori = self.motion.ori_calculator.get_end_ori()
        self.motion.pictograph.pictograph_dict[f"{self.motion.color}_attributes"][
            "end_ori"
        ] = self.motion.end_ori
