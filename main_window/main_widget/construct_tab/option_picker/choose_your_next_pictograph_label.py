from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFontMetrics
from typing import Callable


class ChooseYourNextPictographLabel(QLabel):
    def __init__(self, size_provider: Callable[[], QSize]):
        super().__init__()
        self.size_provider = size_provider
        self.setText("Choose your next pictograph:")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resizeEvent(self, event):
        size = self.size_provider()
        font_size = int(0.03 * size.height())
        font = self.font()
        font.setPointSize(font_size)
        font.setFamily("Monotype Corsiva")
        self.setFont(font)
        fm = QFontMetrics(font)
        w = fm.horizontalAdvance(self.text()) + 20
        h = fm.height() + 20
        self.setFixedSize(w, h)
        self.setStyleSheet(
            f"background-color: rgba(255,255,255,200); border-radius: {h//2}px;"
        )
