# src/main_window/main_widget/sequence_workbench/graph_editor/adjustment_panel/new_turns_adjustment_manager/turns_presenter.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMessageBox

from ..new_turns_adjustment_manager.turns_value import TurnsValue

if TYPE_CHECKING:
    from ..turns_box.turns_widget.turns_widget import TurnsWidget
    from ..turns_box.turns_widget.motion_type_label import MotionTypeLabel


class TurnsPresenter:
    def __init__(
        self, turns_widget: "TurnsWidget", motion_type_label: "MotionTypeLabel"
    ):
        self._motion_type_label = motion_type_label
        self.turns_widget = turns_widget

    def update_display(self, value: "TurnsValue"):
        self.turns_widget.display_frame.turns_label.setText(value.display_value)
        self._update_buttons(value)
        self._update_motion_type(value)

    def _update_buttons(self, value: "TurnsValue"):
        is_float = value.raw_value == "fl"
        self.turns_widget.display_frame.decrement_button.setEnabled(not is_float)
        self.turns_widget.display_frame.increment_button.setEnabled(
            value.raw_value != 3 if not is_float else False
        )

    def _update_motion_type(self, value: "TurnsValue"):
        motion_type = "float" if value.raw_value == "fl" else "standard"
        self._motion_type_label.update_display(motion_type.capitalize())

    def show_error(self, message):
        QMessageBox.critical(None, "Turns Error", message)
