import os
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import QImage

from utilities.path_helpers import get_my_photos_path

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_beat_frame.image_export_manager.image_export_manager import (
        ImageExportManager,
    )


class ImageSaver:
    def __init__(self, export_manager: "ImageExportManager"):
        self.export_manager = export_manager
        self.beat_frame = export_manager.beat_frame

    def save_image(self, sequence_image: QImage):
        self.indicator_label = (
            self.export_manager.main_widget.sequence_workbench.indicator_label
        )
        word = self.beat_frame.get.current_word()
        if word == "":
            self.indicator_label.show_message(
                "You must build a sequence to save it as an image."
            )
            return

        version_number = 1
        base_word_folder = get_my_photos_path(f"{word}")

        file_path = os.path.join(base_word_folder, f"{word}_v{version_number}.png")
        os.makedirs(base_word_folder, exist_ok=True)

        while os.path.exists(file_path):
            version_number += 1
            file_path = os.path.join(base_word_folder, f"{word}_v{version_number}.png")

        file_name, _ = QFileDialog.getSaveFileName(
            self.beat_frame,
            "Save Image",
            file_path,
            "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)",
        )

        if not file_name:
            return None

        if sequence_image.save(file_name, "PNG"):
            self.indicator_label.show_message(
                f"Image saved as {os.path.basename(file_name)}"
            )
            return file_name
        else:
            self.indicator_label.show_message("Failed to save image.")
            return None
