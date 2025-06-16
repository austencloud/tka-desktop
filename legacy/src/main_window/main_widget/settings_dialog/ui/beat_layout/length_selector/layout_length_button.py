from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .length_selector import LengthSelector


class LayoutLengthButton(QPushButton):
    def __init__(
        self, text: str, length_selector: "LengthSelector", callback: callable
    ):
        super().__init__(text, length_selector)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(callback)
        self.length_selector = length_selector
