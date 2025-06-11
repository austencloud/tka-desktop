from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QFont, QEnterEvent
from PyQt6.QtCore import Qt

from styles.styled_button import StyledButton


if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.start_pos_picker.start_pos_picker import (
        StartPosPicker,
    )


class StartPosVariationsButton(StyledButton):
    def __init__(self, start_pos_picker: "StartPosPicker") -> None:
        super().__init__(start_pos_picker)
        self.start_pos_picker = start_pos_picker
        self.setText("Variations")

    def resizeEvent(self, event):
        width = self.start_pos_picker.width() // 5
        height = self.start_pos_picker.height() // 10
        self.setFixedSize(width, height)
        font_size = int(width // 10)
        self.setFont(QFont("Calibri", font_size, italic=True))
        super().resizeEvent(event)

    def enterEvent(self, event: QEnterEvent) -> None:
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def leaveEvent(self, event: QEnterEvent) -> None:
        self.setCursor(Qt.CursorShape.ArrowCursor)
