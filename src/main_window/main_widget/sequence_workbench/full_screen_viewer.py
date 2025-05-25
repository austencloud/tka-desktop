from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMessageBox

from main_window.main_widget.full_screen_image_overlay import (
    FullScreenImageOverlay,
)
from src.settings_manager.global_settings.app_context import AppContext
from utils.path_helpers import get_data_path

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
        self.json_loader = AppContext.json_manager().loader_saver

        self.full_screen_overlay = None

    def view_full_screen(self):
        """Display the current image in full screen mode."""
        mw = self.main_widget
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        sequence_length = len(self.json_loader.load_current_sequence())

        if sequence_length <= 2:
            self.indicator_label.show_message("Please build a sequence first.")
            QApplication.restoreOverrideCursor()
            return
        else:
            current_thumbnail = self.create_thumbnail()
            if current_thumbnail:
                pixmap = QPixmap(current_thumbnail)
                full_screen_overlay = mw.get_widget("full_screen_overlay")
                if not full_screen_overlay:
                    # Create overlay if it doesn't exist
                    full_screen_overlay = FullScreenImageOverlay(mw)
                    # Store it for future use if the widget manager supports it
                    if hasattr(mw, "widget_manager") and hasattr(
                        mw.widget_manager, "_widgets"
                    ):
                        mw.widget_manager._widgets["full_screen_overlay"] = (
                            full_screen_overlay
                        )
                full_screen_overlay.show(pixmap)
                QApplication.restoreOverrideCursor()
            else:
                QMessageBox.warning(None, "No Image", "Please select an image first.")
                QApplication.restoreOverrideCursor()

    def create_thumbnail(self):
        self.thumbnail_generator = (
            self.sequence_workbench.dictionary_service.thumbnail_generator
        )
        current_sequence = self.json_loader.load_current_sequence()
        temp_path = get_data_path("temp")
        image_path = self.thumbnail_generator.generate_and_save_thumbnail(
            current_sequence, 0, temp_path, fullscreen_preview=True
        )
        return image_path
