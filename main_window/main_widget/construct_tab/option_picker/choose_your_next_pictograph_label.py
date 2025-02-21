from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFontMetrics
from typing import Callable


class ChooseYourNextPictographLabel(QLabel):
    def __init__(self, size_provider: Callable[[], QSize]):
        super().__init__()
        self.size_provider = size_provider
        self.set_default_text()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_default_text(self) -> None:
        self.setText("Choose your next pictograph:")

    def resizeEvent(self, event) -> None:
        main_size = self.size_provider()
        height = main_size.height()  # Extract height from QSize

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
