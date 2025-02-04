from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .beat_adjustment_panel import BeatAdjustmentPanel


class AdjustmentPanelPlaceHolderText(QLabel):
    def __init__(self, adjustment_panel: "BeatAdjustmentPanel") -> None:
        super().__init__(adjustment_panel)
        self.adjustment_panel = adjustment_panel
        self.set_default_text()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hide()

    def set_default_text(self) -> None:
        self.setText(
            "This is where you'll modify each pictograph.\nSelect a pictograph to show the controls!"
        )

    def resize_adjustment_panel_placeholder_text(self) -> None:
        width = self.adjustment_panel.width()
        font_size = int(0.02 * width)
        self.setFont(QFont("Cambria", font_size))
        self.setStyleSheet("background-color: white;")

    def resizeEvent(self, event):
        self.resize_adjustment_panel_placeholder_text()
        super().resizeEvent(event)
