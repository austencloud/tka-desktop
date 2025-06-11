from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMessageBox
from data.constants import ANTI, FLOAT, PRO

from ..turns_adjustment_manager.turns_value import TurnsValue

if TYPE_CHECKING:
    from ..turns_box.turns_widget.turns_widget import TurnsWidget
    from ..turns_box.turns_widget.motion_type_label import MotionTypeLabel


class TurnsPresenter:
    def __init__(
        self, turns_widget: "TurnsWidget", motion_type_label: "MotionTypeLabel"
    ):
        self._motion_type_label = motion_type_label
        self.turns_widget = turns_widget

    def update_display(self, value: "TurnsValue", motion_type: str = None):
        self.turns_widget.display_frame.turns_label.setText(value.display_value)
        self._update_buttons(value, motion_type)
        if motion_type:
            self._update_motion_type(motion_type)
        elif value.raw_value == "fl":
            self._update_motion_type(FLOAT)

    def _update_buttons(self, value: "TurnsValue", motion_type: str):
        is_float = value.raw_value == "fl"
        if value.raw_value == 0 and motion_type in [PRO, ANTI]:
            self.turns_widget.display_frame.decrement_button.setEnabled(True)
            self.turns_widget.display_frame.increment_button.setEnabled(True)
        elif is_float:
            self.turns_widget.display_frame.decrement_button.setEnabled(False)
            self.turns_widget.display_frame.increment_button.setEnabled(True)
        else:
            self.turns_widget.display_frame.decrement_button.setEnabled(
                value.raw_value != 0
            )
            self.turns_widget.display_frame.increment_button.setEnabled(
                value.raw_value != 3
            )

        header = self.turns_widget.turns_box.header
        if is_float:
            header.hide_prop_rot_dir_buttons()
            header.unpress_prop_rot_dir_buttons()
        else:
            if value.raw_value > 0 or motion_type in [PRO, ANTI]:
                header.show_prop_rot_dir_buttons()
            else:
                header.hide_prop_rot_dir_buttons()

    def _update_motion_type(self, motion_type: str):
        if not motion_type:
            return
        display_text = motion_type.capitalize()
        self._motion_type_label.update_display(display_text)

    def show_error(self, message):
        QMessageBox.critical(None, "Turns Error", message)
