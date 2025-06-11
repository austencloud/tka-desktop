from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING

from data.constants import BLUE, RED

if TYPE_CHECKING:
    from .turns_display_frame import TurnsDisplayFrame


class GE_TurnsLabel(QLabel):
    """This is the colored box that displays the turns number inside the turns box display frame of the graph editor."""

    clicked = pyqtSignal()

    def __init__(self, turns_display_frame: "TurnsDisplayFrame") -> None:
        super().__init__()
        self.turns_box = turns_display_frame.turns_box
        self.turns_display_font_size = 20
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.clicked.emit()

    def resizeEvent(self, event) -> None:
        self.turns_display_font_size = int(
            (self.turns_box.adjustment_panel.graph_editor.width() / 22)
        )
        self.setFont(QFont("Arial", self.turns_display_font_size, QFont.Weight.Bold))
        self.setMaximumWidth(
            int(self.turns_box.adjustment_panel.graph_editor.width() / 9)
        )
        self.setMaximumHeight(
            int(self.turns_box.adjustment_panel.graph_editor.height() / 4)
        )
        border_radius = self.width() // 4

        turn_display_border = int(self.width() / 20)

        turns_box_color = self.turns_box.color
        if turns_box_color == RED:
            border_color = "#ED1C24"
        elif turns_box_color == BLUE:
            border_color = "#2E3192"
        else:
            border_color = "black"

        self.setStyleSheet(
            f"""
            QLabel {{
                border: {turn_display_border}px solid {border_color};
                border-radius: {border_radius}px;
                background-color: white;
                padding-left: 2px; /* add some padding on the left for the text */
                padding-right: 2px; /* add some padding on the right for symmetry */
            }}
            """
        )
        super().resizeEvent(event)
