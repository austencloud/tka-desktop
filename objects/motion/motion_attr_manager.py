from typing import TYPE_CHECKING
from data.constants import *


if TYPE_CHECKING:
    from objects.motion.motion import Motion


class MotionAttrManager:
    def __init__(self, motion: "Motion") -> None:
        self.motion = motion
        self.motion.state.color = self.motion.motion_data.get(COLOR)
        self.motion.state.turns = self.motion.motion_data.get(TURNS)
        self.motion.state.start_loc = None
        self.motion.state.end_loc = None
        self.motion.state.motion_type = None

    def update_attributes(self, motion_data: dict[str, str]) -> None:
        if TURNS in motion_data:
            self.motion.state.turns = motion_data[TURNS]
        for attribute, value in motion_data.items():
            if value is not None:
                setattr(self.motion.state, attribute, value)
                self.motion.motion_data[attribute] = value
        if self.motion.check.is_shift():
            if "prefloat_motion_type" not in motion_data:
                if self.motion.state.motion_type != FLOAT:
                    self.motion.state.prefloat_motion_type = (
                        self.motion.state.motion_type
                    )
            if "prefloat_motion_type" in motion_data:
                if motion_data["prefloat_motion_type"] == FLOAT:
                    return
                else:
                    prefloat_motion_type = motion_data["prefloat_motion_type"]
                    self.motion.state.prefloat_motion_type = prefloat_motion_type
            if "prefloat_prop_rot_dir" in motion_data:
                if motion_data["prefloat_prop_rot_dir"] == NO_ROT:
                    return
                else:
                    self.motion.state.prefloat_prop_rot_dir = motion_data[
                        "prefloat_prop_rot_dir"
                    ]

    def update_prop_ori(self) -> None:
        if hasattr(self.motion, PROP) and self.motion.prop:
            if not self.motion.state.end_ori:
                self.motion.state.end_ori = self.motion.ori_calculator.get_end_ori()
            self.motion.prop.ori = self.motion.state.end_ori
            self.motion.prop.loc = self.motion.state.end_loc

    def get_attributes(self) -> dict[str, str]:
        return {
            COLOR: self.motion.state.color,
            MOTION_TYPE: self.motion.state.motion_type,
            TURNS: self.motion.state.turns,
            PROP_ROT_DIR: self.motion.state.prop_rot_dir,
            START_LOC: self.motion.state.start_loc,
            END_LOC: self.motion.state.end_loc,
            START_ORI: self.motion.state.start_ori,
            END_ORI: self.motion.state.end_ori,
        }

    def assign_lead_states(self) -> None:
        leading_motion = self.motion.pictograph.managers.get.leading_motion()
        trailing_motion = self.motion.pictograph.managers.get.trailing_motion()
        if self.motion.pictograph.managers.get.leading_motion():
            leading_motion.arrow.motion.state.lead_state = LEADING
            trailing_motion.arrow.motion.state.lead_state = TRAILING
