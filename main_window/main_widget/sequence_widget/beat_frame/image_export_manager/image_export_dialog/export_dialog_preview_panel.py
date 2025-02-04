from datetime import datetime
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QFrame, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


if TYPE_CHECKING:
    from .image_export_dialog import ImageExportDialog


class ExportDialogPreviewPanel(QFrame):
    def __init__(self, export_dialog: "ImageExportDialog", image=None):
        super().__init__(export_dialog)
        self.image = image
        self.export_dialog = export_dialog
        self.preview_image = None  # Store the QPixmap for sharing
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.preview_label = QLabel(self)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.preview_label)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_preview(
        self,
        include_start_pos: bool,
        add_info: bool,
        sequence: list[dict],
        add_word: bool,
        include_difficulty_level: bool,
        add_beat_numbers: bool,
        add_reversal_symbols: bool,
    ):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        current_date = datetime.now().strftime("%m-%d-%Y")
        current_date = "-".join([str(int(part)) for part in current_date.split("-")])
        options = {
            "include_start_pos": include_start_pos,
            "add_info": add_info,
            "user_name": self.export_dialog.control_panel.user_combo_box.currentText(),
            "export_date": current_date,
            "add_word": add_word,
            "notes": self.export_dialog.control_panel.notes_combo_box.currentText(),
            "add_difficulty_level": include_difficulty_level,
            "add_beat_numbers": add_beat_numbers,
            "add_reversal_symbols": add_reversal_symbols,
        }
        self.image = (
            self.export_dialog.export_manager.image_creator.create_sequence_image(
                sequence, include_start_pos, options
            )
        )
        self.preview_image = QPixmap.fromImage(self.image)

        self.resize_preview_image()
        QApplication.restoreOverrideCursor()

    def resize_preview_image(self):
        if self.preview_image:
            image_aspect_ratio = (
                self.preview_image.width() / self.preview_image.height()
            )
            image_width = int(self.width() * 0.95)
            image_height = int(image_width / image_aspect_ratio)

            if image_height > self.height():
                image_height = int(self.height() * 0.95)
                image_width = int(image_height * image_aspect_ratio)

            self.preview_label.setPixmap(
                self.preview_image.scaled(
                    image_width,
                    image_height,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
            self.preview_label.setFixedSize(image_width, image_height)
