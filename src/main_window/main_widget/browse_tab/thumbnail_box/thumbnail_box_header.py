from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QLabel, QPushButton, QWidget, QHBoxLayout
from PyQt6.QtGui import QFont, QIcon
from typing import TYPE_CHECKING, Literal
import os

from main_window.main_widget.browse_tab.thumbnail_box.favorite_sequence_button import FavoriteSequenceButton
from settings_manager.global_settings.app_context import AppContext
from utils.path_helpers import get_image_path
from .thumbnail_box_difficulty_label import ThumbnailBoxDifficultyLabel

if TYPE_CHECKING:
    from .thumbnail_box import ThumbnailBox



class ThumbnailBoxHeader(QWidget):
    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__(thumbnail_box)
        self.thumbnail_box = thumbnail_box
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(60)
        self.settings_manager = AppContext.settings_manager()

        self.difficulty_label = ThumbnailBoxDifficultyLabel(thumbnail_box)
        self.word_label = QLabel(thumbnail_box.word)
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.favorite_button = FavoriteSequenceButton(thumbnail_box)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.addWidget(self.difficulty_label, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addStretch(1)
        layout.addWidget(self.word_label)
        layout.addStretch(1)
        layout.addWidget(self.favorite_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

    def resizeEvent(self, event):
        font_size = self.thumbnail_box.width() // 18
        font = QFont("Georgia", font_size, QFont.Weight.DemiBold)
        self.word_label.setFont(font)

        self.difficulty_label.setFixedSize(self.favorite_button.size())

        color = self.settings_manager.global_settings.get_current_font_color()
        self.word_label.setStyleSheet(f"color: {color};")

        available_width = self.thumbnail_box.width() - (self.favorite_button.width() * 3)
        fm = self.word_label.fontMetrics()
        while (
            fm.horizontalAdvance(self.word_label.text()) > available_width
            and font_size > 1
        ):
            font_size -= 1
            font.setPointSize(font_size)
            self.word_label.setFont(font)
            fm = self.word_label.fontMetrics()
        super().resizeEvent(event)
