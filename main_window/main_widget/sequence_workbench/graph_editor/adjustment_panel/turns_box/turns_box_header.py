from typing import TYPE_CHECKING
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, NO_ROT
from ..base_adjustment_box_header_widget import BaseAdjustmentBoxHeaderWidget

if TYPE_CHECKING:
    from .turns_box import TurnsBox


class TurnsBoxHeader(BaseAdjustmentBoxHeaderWidget):
    def __init__(self, turns_box: "TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self.graph_editor = self.turns_box.adjustment_panel.graph_editor
        self.main_widget = self.graph_editor.main_widget
        self._add_widgets()
        # self.update_turns_box_header()

    def update_turns_box_header(self) -> None:
        """Update the header to display correct buttons based on motion type."""
        pictograph = self.turns_box.graph_editor.pictograph_container.GE_view.pictograph
        motion = pictograph.get.motion_by_color(self.turns_box.color)
        prop_rot_dir_button_mngr = self.turns_box.prop_rot_dir_button_manager

        if motion.prop_rot_dir == NO_ROT:
            prop_rot_dir_button_mngr.hide_prop_rot_dir_buttons()
        else:
            prop_rot_dir_button_mngr.show_prop_rot_dir_buttons()
            if motion.prop_rot_dir == CLOCKWISE:
                prop_rot_dir_button_mngr.cw_button.press()
                prop_rot_dir_button_mngr.ccw_button.unpress()
                self.turns_box.prop_rot_dir_btn_state[CLOCKWISE] = True
                self.turns_box.prop_rot_dir_btn_state[COUNTER_CLOCKWISE] = False
            elif motion.prop_rot_dir == COUNTER_CLOCKWISE:
                prop_rot_dir_button_mngr.ccw_button.press()
                prop_rot_dir_button_mngr.cw_button.unpress()
                self.turns_box.prop_rot_dir_btn_state[CLOCKWISE] = False
                self.turns_box.prop_rot_dir_btn_state[COUNTER_CLOCKWISE] = True
        # QApplication.processEvents()

    def _add_widgets(self) -> None:
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.turns_box.prop_rot_dir_button_manager.ccw_button)
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.header_label)
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.turns_box.prop_rot_dir_button_manager.cw_button)
        self.top_hbox.addStretch(1)
        self.separator_hbox.addWidget(self.separator)
