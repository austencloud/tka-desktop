"""
Base exporter class for the codex pictograph exporter.
"""
from typing import TYPE_CHECKING, Dict, Any, Optional
import os
from PyQt6.QtWidgets import QFileDialog, QProgressDialog
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import ImageExportTab
    from base_widgets.pictograph.pictograph import Pictograph


class BaseExporter:
    """Base exporter class for the codex pictograph exporter."""

    def __init__(self, image_export_tab: "ImageExportTab"):
        """Initialize the exporter.
        
        Args:
            image_export_tab: The parent image export tab
        """
        self.image_export_tab = image_export_tab
        self.main_widget = image_export_tab.main_widget
        
    def _get_export_directory(self) -> Optional[str]:
        """Ask the user for a directory to save the exported images.
        
        Returns:
            The selected directory, or None if the user canceled
        """
        directory = QFileDialog.getExistingDirectory(
            self.image_export_tab,
            "Select Directory to Save Pictographs",
            "",
            QFileDialog.Option.ShowDirsOnly,
        )
        return directory if directory else None
        
    def _create_progress_dialog(self, total_count: int) -> QProgressDialog:
        """Create a progress dialog for the export process.
        
        Args:
            total_count: The total number of pictographs to export
            
        Returns:
            The progress dialog
        """
        progress = QProgressDialog(
            "Exporting pictographs with turns...", "Cancel", 0, total_count, self.image_export_tab
        )
        progress.setWindowTitle("Exporting Pictographs")
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.show()
        return progress
        
    def _show_completion_message(self, exported_count: int, directory: str, turn_combinations=None):
        """Show a completion message after the export process.
        
        Args:
            exported_count: The number of exported pictographs
            directory: The directory where the pictographs were exported
            turn_combinations: The turn combinations that were exported
        """
        if exported_count > 0:
            # Get the first turn combination directory to show in the message
            if turn_combinations:
                first_turn = turn_combinations[0]
                from ..turn_configuration import TurnConfiguration
                first_dir_name = TurnConfiguration.get_turn_directory_name(first_turn[0], first_turn[1])
                first_dir_path = os.path.join(directory, first_dir_name)
                
                # If there are multiple turn combinations, indicate that in the message
                if len(turn_combinations) > 1:
                    message = f"Successfully exported {exported_count} codex pictographs with turns to {directory} (in {len(turn_combinations)} turn folders)"
                else:
                    message = f"Successfully exported {exported_count} codex pictographs with turns to {first_dir_path}"
                
                self.main_widget.sequence_workbench.indicator_label.show_message(message)
                
                # Open the directory - if multiple turn combinations, open the main directory
                # otherwise open the specific turn directory
                if len(turn_combinations) > 1:
                    os.startfile(directory)
                else:
                    os.startfile(first_dir_path)
            else:
                # Fallback if no turn combinations (shouldn't happen)
                self.main_widget.sequence_workbench.indicator_label.show_message(
                    f"Successfully exported {exported_count} codex pictographs with turns to {directory}"
                )
                os.startfile(directory)
        else:
            self.main_widget.sequence_workbench.indicator_label.show_message(
                "No codex pictographs were exported."
            )
