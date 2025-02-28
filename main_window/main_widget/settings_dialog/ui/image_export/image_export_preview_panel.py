from datetime import datetime
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QFrame, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
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
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.preview_label, stretch=1)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

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
        current_date = datetime.now().strftime("%m-%d-%Y")
        options = {
            "include_start_position": include_start_pos,
            "add_user_info": add_info,
            "user_name": self.tab.control_panel.user_combo_box.currentText(),
            "open_directory": self.tab.main_widget.settings_manager.image_export.get_image_export_setting(
                "open_directory_on_export"
            ),
            "notes": self.tab.control_panel.notes_combo_box.currentText(),
            "export_date": current_date,
            "add_word": add_word,
            "add_difficulty_level": include_difficulty_level,
            "add_beat_numbers": add_beat_numbers,
            "add_reversal_symbols": add_reversal_symbols,
        }
        
        image = self.image_export_manager.image_creator.create_sequence_image(
            sequence, include_start_pos, options
        )
        pixmap = QPixmap.fromImage(image)

        # 🔥 Set a fixed height for the preview image
        max_image_height = int(self.height() * 0.98)  # Adjust as needed
        scaled_pixmap = pixmap.scaledToHeight(max_image_height, Qt.TransformationMode.SmoothTransformation)

        self.preview_label.setPixmap(scaled_pixmap)
