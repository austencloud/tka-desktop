from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .turns_widget import TurnsWidget


class MotionTypeLabel(QLabel):
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        super().__init__("", turns_widget)
        self.turns_widget = turns_widget
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_display(self, motion_type: str) -> None:
        """Update the display based on the motion type."""
        self.setText(motion_type.capitalize())

    def resizeEvent(self, event) -> None:
        """Resize the label based on the parent widget size."""
        font_size = self.turns_widget.turns_box.graph_editor.width() // 40
        font = QFont("Cambria", font_size, QFont.Weight.Bold)
        self.setFont(font)
