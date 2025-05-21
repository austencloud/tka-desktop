from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtWidgets import QFileDialog, QFrame, QMessageBox
from PyQt6.QtCore import Qt
import os
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from main_window.main_widget.sequence_card_tab.sequence_card_tab import (
        SequenceCardTab,
    )


class SequenceCardPageExporter:
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab

    def export_all_pages_as_images(self):
        """Export all sequence card pages as images."""
        # Check if there are any pages to export
        if not self.sequence_card_tab.pages:
            QMessageBox.warning(
                self.sequence_card_tab,
                "No Pages to Export",
                "There are no sequence card pages to export. Please select a sequence length first.",
            )
            return

        # Ask the user for the directory to save images
        directory = QFileDialog.getExistingDirectory(
            self.sequence_card_tab, "Select Directory to Save Images"
        )

        if not directory:
            return  # User canceled the dialog

        # Create a subdirectory with timestamp for this export
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        length = self.sequence_card_tab.currently_displayed_length
        export_dir = os.path.join(
            directory, f"sequence_cards_length_{length}_{timestamp}"
        )

        try:
            os.makedirs(export_dir, exist_ok=True)
        except Exception as e:
            QMessageBox.critical(
                self.sequence_card_tab,
                "Export Error",
                f"Failed to create export directory: {e}",
            )
            return

        # Iterate over each page in the current displayed length and save as image
        for i, page_widget in enumerate(self.sequence_card_tab.pages):
            page_image_path = os.path.join(export_dir, f"page_{i + 1}.png")
            try:
                self._save_page_as_image(page_widget, page_image_path)
                print(f"Page {i + 1} saved as image.")
            except Exception as e:
                print(f"Error saving page {i + 1}: {e}")

        # Show success message
        QMessageBox.information(
            self.sequence_card_tab,
            "Export Complete",
            f"Exported {len(self.sequence_card_tab.pages)} pages as images to:\n{export_dir}",
        )
        print(
            f"Exported {len(self.sequence_card_tab.pages)} pages as images at {export_dir}."
        )

    def _save_page_as_image(self, widget: QFrame, page_image_path):
        """Helper function to save a QWidget as an image."""
        pixmap = QPixmap(widget.size())
        pixmap.fill(Qt.GlobalColor.white)  # Fill with white background

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        widget.render(painter)
        painter.end()

        pixmap.save(page_image_path)
