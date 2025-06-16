import os
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import QImage

from utils.path_helpers import get_my_photos_path

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.legacy_beat_frame.image_export_manager.image_export_manager import (
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

        # Check if we're exporting only a start position
        include_start_pos = (
            self.export_manager.settings_manager.image_export.get_image_export_setting(
                "include_start_position"
            )
        )

        # If the word is empty but we're exporting a start position, use "start_position" as the filename
        if word == "":
            if include_start_pos:
                word = "start_position"
            else:
                self.indicator_label.show_message(
                    "You must build a sequence to save it as an image."
                )
                return

        # Determine the initial directory for the save dialog
        settings_manager = self.export_manager.settings_manager

        # Force sync the settings before reading
        settings_manager.settings.sync()

        use_last_directory = settings_manager.image_export.get_image_export_setting(
            "use_last_save_directory"
        )
        print(f"Use last directory setting: {use_last_directory}")

        if use_last_directory:
            # Use the last save directory if available and the setting is enabled
            last_directory = settings_manager.image_export.get_last_save_directory()
            print(f"Last save directory: {last_directory}")
            if last_directory and os.path.exists(last_directory):
                # Use the last directory with the current word and version
                version_number = 1
                file_path = os.path.join(
                    last_directory, f"{word}_v{version_number}.png"
                )

                # Increment version number if file exists
                while os.path.exists(file_path):
                    version_number += 1
                    file_path = os.path.join(
                        last_directory, f"{word}_v{version_number}.png"
                    )
            else:
                # Fall back to default if last directory doesn't exist
                version_number = 1
                base_word_folder = get_my_photos_path(f"{word}")
                file_path = os.path.join(
                    base_word_folder, f"{word}_v{version_number}.png"
                )
                os.makedirs(base_word_folder, exist_ok=True)

                # Increment version number if file exists
                while os.path.exists(file_path):
                    version_number += 1
                    file_path = os.path.join(
                        base_word_folder, f"{word}_v{version_number}.png"
                    )
        else:
            # Use the default directory (organized by word)
            version_number = 1
            base_word_folder = get_my_photos_path(f"{word}")
            file_path = os.path.join(base_word_folder, f"{word}_v{version_number}.png")
            os.makedirs(base_word_folder, exist_ok=True)

            # Increment version number if file exists
            while os.path.exists(file_path):
                version_number += 1
                file_path = os.path.join(
                    base_word_folder, f"{word}_v{version_number}.png"
                )

        # Show the save dialog with the appropriate initial directory
        file_name, _ = QFileDialog.getSaveFileName(
            self.beat_frame,
            "Save Image",
            file_path,
            "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)",
        )

        if not file_name:
            return None

        # Save the image with maximum quality
        if sequence_image.save(file_name, "PNG", 100):  # Quality 100 = maximum quality
            # Store the directory for future use
            save_directory = os.path.dirname(file_name)
            print(f"Saving directory: {save_directory}")
            settings_manager.image_export.set_last_save_directory(save_directory)
            print(
                f"After saving, last directory is: {settings_manager.image_export.get_last_save_directory()}"
            )

            self.indicator_label.show_message(
                f"Image saved as {os.path.basename(file_name)}"
            )
            os.startfile(file_name)
        else:
            self.indicator_label.show_message("Failed to save image.")
