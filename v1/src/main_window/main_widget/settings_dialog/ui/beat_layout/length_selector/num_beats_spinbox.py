from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSpinBox
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .length_selector import LengthSelector


class NumBeatsSpinbox(QSpinBox):
    def __init__(self, length_selector: "LengthSelector"):
        super().__init__(length_selector)
        self.length_selector = length_selector
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setRange(2, 64)
        self.valueChanged.connect(
            lambda: self.length_selector.value_changed.emit(self.value())
        )
