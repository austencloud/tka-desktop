from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .length_selector import LengthSelector


class SequenceLengthLabel(QLabel):
    def __init__(self, length_selector: "LengthSelector"):
        super().__init__("Length:", length_selector)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.length_selector = length_selector
