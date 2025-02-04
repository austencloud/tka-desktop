from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.option_picker import (
        OptionPicker,
    )


class ChooseYourNextPictographLabel(QLabel):
    def __init__(self, option_picker: "OptionPicker") -> None:
        super().__init__(option_picker)
        self.option_picker = option_picker
        self.main_widget = option_picker.main_widget
        self.set_default_text()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.hide()

    def set_default_text(self) -> None:
        self.setText("Choose your next pictograph:")

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
