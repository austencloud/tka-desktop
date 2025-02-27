from typing import TYPE_CHECKING
from data.constants import COLOR, END_ORI, LOC, ORI

if TYPE_CHECKING:
    from objects.motion.motion import Motion


class MotionUpdater:
    def __init__(self, motion: "Motion") -> None:
        self.motion = motion

    def update_motion(self, motion_data: dict = None) -> None:
        if motion_data:
            self.motion.state.update_motion_state(motion_data)
        self.motion.arrow.setup_components()
        self.update_end_ori()
        prop_data = {
            COLOR: self.motion.state.color,
            LOC: self.motion.state.end_loc,
            ORI: self.motion.state.end_ori,
        }
        self.motion.prop.updater.update_prop(prop_data)

    def update_end_ori(self) -> None:
        self.motion.state.end_ori = self.motion.ori_calculator.get_end_ori()
        self.motion.pictograph.state.pictograph_data[
            f"{self.motion.state.color}_attributes"
        ][END_ORI] = self.motion.state.end_ori
