# src/main_window/main_widget/sequence_card_tab/export/export_ui_manager.py
import os
import logging
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from PyQt6.QtWidgets import (
    QFileDialog,
    QMessageBox,
    QProgressDialog,
    QApplication,
)
from PyQt6.QtCore import Qt

from utils.path_helpers import get_user_editable_resource_path, get_win32_photos_path

if TYPE_CHECKING:
    from ..tab import SequenceCardTab


class ExportUIManager:
    """
    Manages UI interactions for sequence card page exports.

    This class handles:
    1. File dialogs for selecting export directories
    2. Progress dialogs for showing export progress
    3. Message boxes for error and success notifications
    4. Cancellation handling
    """

    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab
        self.logger = logging.getLogger(__name__)
        self.progress_dialog: Optional[QProgressDialog] = None
        self.cancel_requested = False

    def get_export_directory(self) -> Optional[str]:
        """
        Show a file dialog to select an export directory.

        Returns:
            Optional[str]: Selected directory path or None if cancelled
        """
        self.logger.debug("Showing export directory dialog")

        # Try to get the last used export directory from settings
        try:
            import json
            settings_path = get_user_editable_resource_path("export_settings.json")
            default_dir = None

            if os.path.exists(settings_path):
                with open(settings_path, "r") as f:
                    settings = json.load(f)
                    default_dir = os.path.join(get_win32_photos_path(), "TKA Sequence Cards")

            # If no saved directory or it doesn't exist, use My Pictures/TKA Sequence Cards
            if not default_dir or not os.path.exists(default_dir):
                os.makedirs(default_dir, exist_ok=True)

        except Exception as e:
            self.logger.warning(f"Could not load export settings: {e}")
            # Fallback to a basic default
            default_dir = os.path.expanduser("~/Pictures")

        # Show the directory selection dialog
        export_dir = QFileDialog.getExistingDirectory(
            self.sequence_card_tab,
            "Select Export Directory",
            default_dir,
            QFileDialog.Option.ShowDirsOnly,
        )

        if not export_dir:
            self.logger.debug("Export directory selection cancelled")
            return None

        # Save the selected directory for next time
        try:
            settings = {"last_export_directory": export_dir}
            with open(settings_path, "w") as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            self.logger.warning(f"Could not save export settings: {e}")

        self.logger.info(f"Selected export directory: {export_dir}")
        return export_dir

    def create_export_subdirectory(self, export_dir: str, selected_length: int) -> str:
        """
        Create a timestamped subdirectory for this export.

        Args:
            export_dir: Base export directory
            selected_length: Selected sequence length

        Returns:
            str: Path to the created subdirectory
        """
        length_text = f"{selected_length}-step" if selected_length > 0 else "all"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_subdir = os.path.join(
            export_dir, f"sequence_cards_{length_text}_{timestamp}"
        )

        # Create the subdirectory
        os.makedirs(export_subdir, exist_ok=True)
        self.logger.info(f"Created export subdirectory: {export_subdir}")

        return export_subdir

    def create_progress_dialog(self, total_pages: int) -> QProgressDialog:
        """
        Create a progress dialog for the export process.

        Args:
            total_pages: Total number of pages to export

        Returns:
            QProgressDialog: The created progress dialog
        """
        self.logger.debug(f"Creating progress dialog for {total_pages} pages")

        # Reset cancellation flag
        self.cancel_requested = False

        # Create the progress dialog
        progress = QProgressDialog(
            "Preparing to export pages...",
            "Cancel",
            0,
            total_pages,
            self.sequence_card_tab,
        )
        progress.setWindowTitle("Exporting Sequence Card Pages")
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(0)  # Show immediately
        progress.setAutoClose(True)
        progress.setAutoReset(True)

        # Connect the cancel button
        progress.canceled.connect(self.handle_cancel_request)

        # Store the progress dialog
        self.progress_dialog = progress

        return progress

    def handle_cancel_request(self) -> None:
        """Handle a cancellation request from the progress dialog."""
        self.logger.info("Export cancelled by user")
        self.cancel_requested = True

    def update_progress(self, value: int, message: str) -> None:
        """
        Update the progress dialog.

        Args:
            value: Current progress value
            message: Progress message to display
        """
        if self.progress_dialog:
            self.progress_dialog.setValue(value)
            self.progress_dialog.setLabelText(message)
            QApplication.processEvents()

    def show_error_message(self, title: str, message: str) -> None:
        """
        Show an error message box.

        Args:
            title: Error title
            message: Error message
        """
        self.logger.error(f"Error: {message}")
        QMessageBox.critical(self.sequence_card_tab, title, message)

    def show_warning_message(self, title: str, message: str) -> None:
        """
        Show a warning message box.

        Args:
            title: Warning title
            message: Warning message
        """
        self.logger.warning(f"Warning: {message}")
        QMessageBox.warning(self.sequence_card_tab, title, message)

    def show_info_message(self, title: str, message: str) -> None:
        """
        Show an information message box.

        Args:
            title: Info title
            message: Info message
        """
        self.logger.info(f"Info: {message}")
        QMessageBox.information(self.sequence_card_tab, title, message)

    def show_export_complete_message(self, export_dir: str, page_count: int) -> None:
        """
        Show a message indicating that the export is complete.

        Args:
            export_dir: Directory where the pages were exported
            page_count: Number of pages exported
        """
        self.logger.info(
            f"Export complete: {page_count} pages exported to {export_dir}"
        )
        QMessageBox.information(
            self.sequence_card_tab,
            "Export Complete",
            f"Successfully exported {page_count} sequence card pages to:\n{export_dir}",
        )
