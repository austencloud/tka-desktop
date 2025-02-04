# rotate_button.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.graph_editor.adjustment_panel.ori_picker_box.ori_picker_widget.rotate_buttons_widget import (
        RotateButtonsWidget,
    )


class RotateButton(QPushButton):
    def __init__(
        self,
        rotate_buttons_widget: "RotateButtonsWidget",
        icon_path: str,
        click_function: callable,
    ):
        super().__init__(rotate_buttons_widget)
        self.rotate_buttons_widget = rotate_buttons_widget
        self.setIcon(QIcon(icon_path))
        self.clicked.connect(click_function)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def resize_button(self):
        button_size = int(
            self.rotate_buttons_widget.ori_picker_widget.ori_picker_box.graph_editor.height()
            // 6
        )
        icon_size = int(button_size * 0.6)
        self.setFixedSize(QSize(button_size, button_size))
        self.setIconSize(QSize(icon_size, icon_size))
