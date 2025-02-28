from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap

from main_window.main_widget.sequence_workbench.sequence_beat_frame.image_export_manager.image_export_manager import (
    ImageExportManager,
)

if TYPE_CHECKING:
    from .image_export_tab import ImageExportTab


class ImageExportPreviewPanel(QFrame):
    def __init__(self, tab: "ImageExportTab"):
        super().__init__(tab)
        self.tab = tab
        self.image_export_manager: "ImageExportManager" = (
            tab.main_widget.sequence_workbench.sequence_beat_frame.image_export_manager
        )
        self._setup_ui()

    def _setup_ui(self):
        self.layout :QVBoxLayout= QVBoxLayout(self)
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.preview_label)

    def update_preview(
        self,
        include_start_pos: bool,
        add_info: bool,
        sequence: list,
        add_word: bool,
        include_difficulty_level: bool,
        add_beat_numbers: bool,
        add_reversal_symbols: bool,
    ):
        options = {
            "include_start_position": include_start_pos,
            "add_info": add_info,
            "add_word": add_word,
            "add_difficulty_level": include_difficulty_level,
            "add_beat_numbers": add_beat_numbers,
            "add_reversal_symbols": add_reversal_symbols,
        }
        image = self.image_export_manager.image_creator.create_sequence_image(
            sequence, include_start_pos, options
        )
        pixmap = QPixmap.fromImage(image)
        self.preview_label.setPixmap(
            pixmap.scaled(
                self.width(),
                self.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
