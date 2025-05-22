# src/main_window/main_widget/sequence_card_tab/export/page_exporter.py
import os
import time
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QApplication, QWidget, QLabel
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt, QSize, QRect, QPoint

from utils.path_helpers import get_app_data_path
from ..loading.progress_dialog import SequenceCardProgressDialog

if TYPE_CHECKING:
    from ..tab import SequenceCardTab


class SequenceCardPageExporter:
    """
    Exports sequence card pages as high-quality images.

    This class handles exporting the sequence card pages that are currently
    displayed in the sequence card tab as high-quality PNG images.
    """

    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab
        self.progress_dialog = None
        self.cancel_requested = False

        # Export settings
        self.export_settings = {
            "format": "PNG",
            "quality": 100,
            "dpi": 300,
            "background_color": Qt.GlobalColor.white,
            "margin": 20,
        }

    def export_all_pages_as_images(self):
        """
        Export all currently displayed sequence card pages as images.

        This method:
        1. Prompts the user for a directory to save the images
        2. Renders each page at high resolution
        3. Saves the images with appropriate naming
        4. Shows progress during export
        """
        # Get the pages to export
        pages = self.sequence_card_tab.pages
        if not pages:
            QMessageBox.warning(
                self.sequence_card_tab,
                "No Pages to Export",
                "There are no sequence card pages to export. Please select a sequence length first.",
            )
            return

        # Get the export directory
        export_dir = self._get_export_directory()
        if not export_dir:
            return  # User cancelled

        # Create progress dialog
        self.progress_dialog = SequenceCardProgressDialog(self.sequence_card_tab)
        self.progress_dialog.canceled.connect(self._on_cancel_requested)
        self.cancel_requested = False

        # Show the progress dialog
        self.progress_dialog.set_progress(0, len(pages))
        self.progress_dialog.set_operation("Preparing to export pages...")
        self.progress_dialog.show()

        # Export the pages
        try:
            self._export_pages(pages, export_dir)
        finally:
            # Close the progress dialog
            if self.progress_dialog:
                self.progress_dialog.close()
                self.progress_dialog = None

    def _get_export_directory(self) -> Optional[str]:
        """
        Prompt the user for a directory to save the exported images.

        Returns:
            str: The selected directory path, or None if cancelled
        """
        # Get the default export directory
        # Create a base path in the app data directory
        base_app_data_path = get_app_data_path("exports")
        default_dir = os.path.join(
            base_app_data_path,
            "sequence_cards",
            datetime.now().strftime("%Y-%m-%d"),
        )

        # Create the default directory if it doesn't exist
        os.makedirs(default_dir, exist_ok=True)

        # Show the directory selection dialog
        export_dir = QFileDialog.getExistingDirectory(
            self.sequence_card_tab,
            "Select Export Directory",
            default_dir,
            QFileDialog.Option.ShowDirsOnly,
        )

        return export_dir if export_dir else None

    def _on_cancel_requested(self):
        """Handle cancel button click in the progress dialog."""
        self.cancel_requested = True

    def _export_pages(self, pages: List[QWidget], export_dir: str):
        """
        Export the sequence card pages as high-quality images.

        Args:
            pages: List of page widgets to export
            export_dir: Directory to save the exported images
        """
        # Get the selected length
        selected_length = getattr(
            self.sequence_card_tab.nav_sidebar, "selected_length", 0
        )
        length_text = f"{selected_length}-step" if selected_length > 0 else "all"

        # Create a subdirectory for this export
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_subdir = os.path.join(
            export_dir, f"sequence_cards_{length_text}_{timestamp}"
        )
        os.makedirs(export_subdir, exist_ok=True)

        # Export each page
        for i, page in enumerate(pages):
            if self.cancel_requested:
                break

            # Update progress
            self.progress_dialog.set_progress(i, len(pages))
            self.progress_dialog.set_operation(
                f"Exporting page {i+1} of {len(pages)}..."
            )
            QApplication.processEvents()

            try:
                # Export the page
                filename = f"sequence_card_page_{i+1:03d}.png"
                filepath = os.path.join(export_subdir, filename)

                # Render the page at high resolution
                self._render_page_to_image(page, filepath)

                # Add a small delay to keep UI responsive
                time.sleep(0.1)
                QApplication.processEvents()

            except Exception as e:
                print(f"Error exporting page {i+1}: {e}")
                import traceback

                traceback.print_exc()

        # Show completion message
        if not self.cancel_requested:
            self.progress_dialog.set_progress(len(pages), len(pages))
            self.progress_dialog.set_operation(
                f"Export complete! Saved to {export_subdir}"
            )
            QApplication.processEvents()

            # Show success message
            QMessageBox.information(
                self.sequence_card_tab,
                "Export Complete",
                f"Successfully exported {len(pages)} sequence card pages to:\n{export_subdir}",
            )

            # Open the export directory
            os.startfile(export_subdir)

    def _render_page_to_image(self, page: QWidget, filepath: str):
        """
        Render a page widget to a high-quality image file.

        Args:
            page: The page widget to render
            filepath: Path to save the rendered image
        """
        # Get the page size
        page_size = page.size()

        # Calculate the target size (higher resolution for print quality)
        scale_factor = self.export_settings["dpi"] / 96  # Standard screen DPI is 96
        target_width = int(page_size.width() * scale_factor)
        target_height = int(page_size.height() * scale_factor)

        # Create a pixmap with the target size
        pixmap = QPixmap(target_width, target_height)
        pixmap.fill(self.export_settings["background_color"])

        # Create a painter
        painter = QPainter(pixmap)

        # Enable high-quality rendering
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

        # Scale the painter
        painter.scale(scale_factor, scale_factor)

        # Render the page
        page.render(
            painter, QPoint(0, 0), QRect(0, 0, page_size.width(), page_size.height())
        )

        # Check if this is a printable page and hide the page number label during export
        page_number_label = page.findChild(QLabel, "pageNumberLabel")
        if page_number_label:
            # Temporarily hide the page number label
            was_visible = page_number_label.isVisible()
            page_number_label.setVisible(False)

            # Re-render the page without the page number label
            page.render(
                painter,
                QPoint(0, 0),
                QRect(0, 0, page_size.width(), page_size.height()),
            )

            # Restore visibility
            page_number_label.setVisible(was_visible)

        # End painting
        painter.end()

        # Save the pixmap
        pixmap.save(
            filepath, self.export_settings["format"], self.export_settings["quality"]
        )
