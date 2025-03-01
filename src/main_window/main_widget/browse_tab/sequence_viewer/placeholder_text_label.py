from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QFont

if TYPE_CHECKING:
    from .sequence_viewer import SequenceViewer


class PlaceholderTextLabel(QLabel):
    def __init__(self, sequence_viewer: "SequenceViewer"):
        super().__init__("Select a sequence to display it here.", sequence_viewer)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sequence_viewer = sequence_viewer

    def resizeEvent(self, event: QEvent):
        placeholder_text_font_size = self.sequence_viewer.main_widget.width() // 85
        font = QFont("Georgia", placeholder_text_font_size, QFont.Weight.Bold)
        self.setFont(font)
        min_height = self.sequence_viewer.main_widget.height() // 5
        self.setFixedHeight(min_height)
        super().resizeEvent(event)
