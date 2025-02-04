from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ...advanced_start_pos_picker.advanced_start_pos_picker import (
        AdvancedStartPosPicker,
    )
    from ...components.start_pos_picker.start_pos_picker import StartPosPicker


class ChooseYourStartPosLabel(QLabel):
    def __init__(
        self, start_pos_picker: Union["StartPosPicker", "AdvancedStartPosPicker"]
    ) -> None:
        super().__init__(start_pos_picker)
        self.start_pos_picker = start_pos_picker
        self.main_widget = start_pos_picker.main_widget
        self.setText("Choose your start position!")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resizeEvent(self, event) -> None:
        height = self.main_widget.height()
        font_size = int(0.03 * height)

        font = self.font()
        font.setPointSize(font_size)
        font.setFamily("Monotype Corsiva")
        self.setFont(font)

        font_metrics = QFontMetrics(font)
        text_width = font_metrics.horizontalAdvance(self.text())
        text_height = font_metrics.height()
        margin = 20
        width = text_width + margin
        height = text_height + margin

        self.setFixedSize(width, height)

        border_radius = height // 2

        self.setStyleSheet(
            f"QLabel {{"
            f"  background-color: rgba(255, 255, 255, 200);"
            f"  border-radius: {border_radius}px;"
            f"}}"
        )
