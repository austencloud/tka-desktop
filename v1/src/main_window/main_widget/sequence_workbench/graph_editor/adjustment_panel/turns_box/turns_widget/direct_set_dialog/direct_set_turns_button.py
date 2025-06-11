from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication, QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from data.constants import BLUE, HEX_BLUE, HEX_RED

if TYPE_CHECKING:
    from .direct_set_turns_dialog import DirectSetTurnsDialog


class DirectSetTurnsButton(QPushButton):
    def __init__(self, value, direct_set_dialog: "DirectSetTurnsDialog") -> None:
        super().__init__(value)
        self.turns_widget = direct_set_dialog.turns_widget
        self.turns_box = self.turns_widget.turns_box
        self.clicked.connect(self.direct_set_adjustment)
        self.setMouseTracking(True)

    def enterEvent(self, event) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)

    def leaveEvent(self, event) -> None:
        QApplication.restoreOverrideCursor()

    def direct_set_adjustment(self):
        pass

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        button_size = self.turns_box.height() // 2
        turns_display_font_size = int(
            self.turns_box.adjustment_panel.graph_editor.height() / 6
        )
        self.setFixedSize(QSize(button_size, button_size))
        self.setFont(QFont("Arial", turns_display_font_size, QFont.Weight.Bold))
        self.setStyleSheet(
            f"""
            QPushButton {{
                border: 4px solid {HEX_BLUE if self.turns_box.color == BLUE else HEX_RED};
                border-radius: {button_size // 2}px;
                background-color: white;
            }}
            QPushButton:hover {{
                background-color: #f0f0f0;
            }}
        """
        )
