# rotate_buttons_widget.py
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from typing import TYPE_CHECKING
from utils.path_helpers import get_image_path
from .rotate_button import RotateButton

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.ori_picker_box.ori_picker_widget.ori_picker_widget import (
        OriPickerWidget,
    )


class RotateButtonsWidget(QWidget):
    def __init__(
        self,
        ori_picker_widget: "OriPickerWidget",
    ):
        super().__init__(ori_picker_widget)
        self.ori_picker_widget = ori_picker_widget
        path = get_image_path("icons")
        self.ccw_button = RotateButton(
            self, f"{path}/rotate_ccw_white.png", self.rotate_ccw
        )
        self.cw_button = RotateButton(
            self, f"{path}/rotate_cw_white.png", self.rotate_cw
        )

        layout = QHBoxLayout(self)
        layout.addWidget(self.ccw_button)
        layout.addWidget(self.cw_button)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

    def resize_rotate_buttons_widget(self):
        self.ccw_button.resize_button()
        self.cw_button.resize_button()

    def rotate_cw(self) -> None:
        self.ori_picker_widget.current_orientation_index = (
            self.ori_picker_widget.current_orientation_index + 1
        ) % len(self.ori_picker_widget.orientations)
        new_ori = self.ori_picker_widget.orientations[
            self.ori_picker_widget.current_orientation_index
        ]
        self.ori_picker_widget.ori_setter.set_orientation(new_ori)

    def rotate_ccw(self) -> None:
        self.ori_picker_widget.current_orientation_index = (
            self.ori_picker_widget.current_orientation_index - 1
        ) % len(self.ori_picker_widget.orientations)
        new_ori = self.ori_picker_widget.orientations[
            self.ori_picker_widget.current_orientation_index
        ]
        self.ori_picker_widget.ori_setter.set_orientation(new_ori)

    def resizeEvent(self, event):
        self.resize_rotate_buttons_widget()
        event.accept()
