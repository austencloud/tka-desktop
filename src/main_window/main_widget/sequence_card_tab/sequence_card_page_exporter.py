from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtWidgets import QFileDialog, QFrame
import os
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.sequence_card_tab.sequence_card_tab import SequenceCardTab


class SequenceCardPageExporter:
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab

    def export_all_pages_as_images(self):
        # Ask the user for the directory to save images
        directory = QFileDialog.getExistingDirectory(
            self.sequence_card_tab, "Select Directory to Save Images"
        )

        if not directory:
            return  # User canceled the dialog

        # Iterate over each page in the current displayed length and save as image
        for i, page_widget in enumerate(self.sequence_card_tab.pages):
            page_image_path = os.path.join(directory, f"page_{i + 1}.png")
            self._save_page_as_image(page_widget, page_image_path)
            print(f"Page {i + 1} saved as image.")
        print(
            f"Exported {len(self.sequence_card_tab.pages)} pages as images at {directory}."
        )

    def _save_page_as_image(self, widget: QFrame, page_image_path):
        """Helper function to save a QWidget as an image."""
        pixmap = QPixmap(widget.size())
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        widget.render(painter)
        painter.end()

        pixmap.save(page_image_path)
