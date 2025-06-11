from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .turns_widget import TurnsWidget


class TurnsTextLabel(QLabel):
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        super().__init__("Turns", turns_widget)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turns_widget = turns_widget

    def resizeEvent(self, event) -> None:
        font_size = self.turns_widget.turns_box.graph_editor.width() // 50
        font = QFont("Cambria", font_size, QFont.Weight.Bold)
        font.setUnderline(True)
        self.setFont(font)
        super().resizeEvent(event)
