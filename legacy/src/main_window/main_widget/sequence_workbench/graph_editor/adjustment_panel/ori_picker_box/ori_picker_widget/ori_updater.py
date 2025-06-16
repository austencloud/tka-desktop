from typing import TYPE_CHECKING
from data.constants import *

if TYPE_CHECKING:
    from .ori_picker_widget import OriPickerWidget
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph

    from objects.motion.motion import Motion


class OriUpdater:
    def __init__(self, ori_picker_widget: "OriPickerWidget") -> None:
        self.ori_picker_box = ori_picker_widget.ori_picker_box
        self.turns_widget = ori_picker_widget

    def set_motion_turns(self, motion: "Motion", new_turns: int) -> None:
        pictograph_data = {f"{motion.state.color}_turns": new_turns}
        motion.pictograph.managers.updater.update_pictograph(pictograph_data)

    def _adjust_turns_for_pictograph(
        self, pictograph: "LegacyPictograph", adjustment: int
    ) -> None:
        """Adjust turns for each relevant motion in the pictograph."""
        for motion in pictograph.elements.motion_set.values():
            if motion.state.color == self.ori_picker_box.color:
                new_turns = self._calculate_new_turns(motion.state.turns, adjustment)
                self.set_motion_turns(motion, new_turns)

    def _calculate_new_turns(self, current_turns: int, adjustment: int) -> int:
        """Calculate new turns value based on adjustment."""
        new_turns = max(0, min(3, current_turns + adjustment))
        return int(new_turns) if new_turns.is_integer() else new_turns

    def _set_vtg_dir_state_default(self) -> None:
        """set the vtg direction state to default."""
        self.ori_picker_box.vtg_dir_btn_state[SAME] = True
        self.ori_picker_box.vtg_dir_btn_state[OPP] = False

    def _set_prop_rot_dir_state_default(self) -> None:
        """set the vtg direction state to default."""
        self.ori_picker_box.prop_rot_dir_btn_state[SAME] = True
        self.ori_picker_box.prop_rot_dir_btn_state[OPP] = False

    def _clamp_turns(self, turns: int) -> int:
        """Clamp the turns value to be within allowable range."""
        return max(0, min(3, turns))
