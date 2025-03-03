from PyQt6.QtWidgets import QToolButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from typing import TYPE_CHECKING

from main_window.main_widget.metadata_extractor import MetaDataExtractor
from main_window.main_widget.sequence_workbench.labels.difficulty_level_icon import (
    DifficultyLevelIcon,
)

if TYPE_CHECKING:
    from .thumbnail_box import ThumbnailBox


class ThumbnailBoxDifficultyLabel(QToolButton):
    def __init__(self, thumbnail_box: "ThumbnailBox"):
        """Handles drawing difficulty level labels in the thumbnail box."""
        super().__init__(thumbnail_box)
        self.thumbnail_box = thumbnail_box
        self.main_widget = thumbnail_box.main_widget
        self.metadata_extractor = MetaDataExtractor()
        self.setToolTip("Difficulty Level")
        self.setCheckable(False)
        self.setStyleSheet("border: none; background: transparent;")  # Clean look

        self.difficulty_level = 1  # Default level
        self.update_difficulty_label()  # Fetch from metadata

    def update_difficulty_label(self):
        """Fetches the difficulty level from the **current** thumbnail's metadata."""
        current_thumbnail = self.thumbnail_box.state.get_current_thumbnail()
        if not current_thumbnail:
            self.hide()
            return

        metadata = self.metadata_extractor.get_full_metadata(current_thumbnail)
        sequence = metadata.get("sequence", [])
        if not sequence:
            self.hide()
            return

        difficulty_level = self.main_widget.sequence_level_evaluator.get_sequence_difficulty_level(
            sequence
        )

        if difficulty_level in ("", None):
            self.hide()
        else:
            self.show()
            self.set_difficulty_level(difficulty_level)

    def set_difficulty_level(self, level: int):
        """Sets the difficulty level and updates the display."""
        self.difficulty_level = level
        self.update_icon()

    def update_icon(self):
        """Updates the size of the icon dynamically based on thumbnail box size."""
        size = max(24, self.thumbnail_box.width() // 12)  # Ensure min size
        self.setIcon(QIcon(DifficultyLevelIcon.get_pixmap(self.difficulty_level, size)))
        self.setIconSize(QSize(size, size))
        self.setFixedSize(size, size)

    def resizeEvent(self, event):
        """Resizes the difficulty label when the thumbnail box resizes."""
        super().resizeEvent(event)
        self.update_icon()
