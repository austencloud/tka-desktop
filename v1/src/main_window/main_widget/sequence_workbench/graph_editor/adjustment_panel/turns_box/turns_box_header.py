from typing import TYPE_CHECKING
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, NO_ROT
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.prop_rot_dir_button_manager.prop_rot_dir_button import PropRotDirButton
from ..base_adjustment_box_header_widget import BaseAdjustmentBoxHeaderWidget
from utils.path_helpers import get_image_path
from data.constants import ICON_DIR

if TYPE_CHECKING:
    from .turns_box import TurnsBox


class TurnsBoxHeader(BaseAdjustmentBoxHeaderWidget):
    def __init__(self, turns_box: "TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self.graph_editor = self.turns_box.adjustment_panel.graph_editor
        self.main_widget = self.graph_editor.main_widget

        # ✅ Create buttons HERE, not in PropRotDirButtonManager
        self.cw_button = PropRotDirButton(
            self.turns_box, CLOCKWISE, get_image_path(f"{ICON_DIR}clock/clockwise.png")
        )
        self.ccw_button = PropRotDirButton(
            self.turns_box, COUNTER_CLOCKWISE, get_image_path(f"{ICON_DIR}clock/counter_clockwise.png")
        )

        self._add_widgets()

    def update_turns_box_header(self) -> None:
        """Update the header to display correct buttons based on motion type."""
        pictograph = self.turns_box.graph_editor.pictograph_container.GE_view.pictograph
        motion = pictograph.managers.get.motion_by_color(self.turns_box.color)

        if motion.state.prop_rot_dir == NO_ROT:
            self.hide_prop_rot_dir_buttons()
        else:
            self.show_prop_rot_dir_buttons()
            if motion.state.prop_rot_dir == CLOCKWISE:
                self.cw_button.set_selected(True)
                self.ccw_button.set_selected(False)
            elif motion.state.prop_rot_dir == COUNTER_CLOCKWISE:
                self.ccw_button.set_selected(True)
                self.cw_button.set_selected(False)

    def _add_widgets(self) -> None:
        """Add buttons to the header layout."""
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.ccw_button)
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.header_label)
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.cw_button)
        self.top_hbox.addStretch(1)
        self.separator_hbox.addWidget(self.separator)

    def show_prop_rot_dir_buttons(self) -> None:
        self.cw_button.show()
        self.ccw_button.show()

    def hide_prop_rot_dir_buttons(self) -> None:
        self.cw_button.hide()
        self.ccw_button.hide()

    def resizeEvent(self, event):
        self.cw_button.resizeEvent(event)
        self.ccw_button.resizeEvent(event)
        super().resizeEvent(event)

    def unpress_prop_rot_dir_buttons(self) -> None:
        self.cw_button.set_selected(True)
        self.ccw_button.set_selected(True)