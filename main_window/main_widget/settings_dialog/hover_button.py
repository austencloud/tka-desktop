from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QPushButton,
)
from PyQt6.QtCore import Qt



if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class HoverButton(QPushButton):
    def __init__(self, text, dialog: "SettingsDialog"):
        super().__init__(text, dialog)
        self.dialog = dialog
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def enterEvent(self, event):
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #99CCFF;
                color: white;
                border-radius: 10px;
                padding: 10px 15px;
            }
        """
        )
        super().enterEvent(event)

