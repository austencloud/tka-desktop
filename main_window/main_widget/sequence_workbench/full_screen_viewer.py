from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMessageBox

from main_window.main_widget.full_screen_image_overlay import (
    FullScreenImageOverlay,
)
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


class FullScreenViewer:
    def __init__(self, sequence_workbench: "SequenceWorkbench"):
        self.sequence_workbench = sequence_workbench
        self.main_widget = sequence_workbench.main_widget
        self.beat_frame = sequence_workbench.beat_frame
        self.indicator_label = sequence_workbench.indicator_label
        self.json_loader = self.main_widget.json_manager.loader_saver

        self.full_screen_overlay = None

    def view_full_screen(self):
        """Display the current image in full screen mode."""
        mw = self.main_widget
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        last_beat = self.beat_frame.get.last_filled_beat()
        if last_beat.__class__.__name__ == "StartPositionBeatView":
            self.indicator_label.show_message("Please build a sequence first.")
            QApplication.restoreOverrideCursor()
            return
        else:
            current_thumbnail = self.create_thumbnail()
            if current_thumbnail:
                pixmap = QPixmap(current_thumbnail)
                mw.full_screen_overlay = FullScreenImageOverlay(mw)
                mw.full_screen_overlay.show(pixmap)
                QApplication.restoreOverrideCursor()
            else:
                QMessageBox.warning(None, "No Image", "Please select an image first.")
                QApplication.restoreOverrideCursor()

    def create_thumbnail(self):
        self.thumbnail_generator = (
            self.sequence_workbench.add_to_dictionary_manager.thumbnail_generator
        )
        current_sequence = self.json_loader.load_current_sequence_json()
        temp_path = get_images_and_data_path("temp")
        image_path = self.thumbnail_generator.generate_and_save_thumbnail(
            current_sequence, 0, temp_path
        )
        return image_path
