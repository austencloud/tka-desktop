"""
Modern dialog for exporting codex pictographs with turns.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QDialog, QMessageBox

from .codex_exporter import CodexExporter
from .codex_dialog_ui import CodexDialogUI
from settings_manager.settings_manager import SettingsManager

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
        ImageExportTab,
    )


class CodexDialog(QDialog):
    """Modern dialog for exporting codex pictographs with turns."""

    def __init__(self, image_export_tab: "ImageExportTab"):
        """Initialize the dialog.

        Args:
            image_export_tab: The parent image export tab
        """
        super().__init__(image_export_tab)
        self.image_export_tab = image_export_tab
        self.main_widget = image_export_tab.main_widget
        self.codex_exporter = CodexExporter(image_export_tab)
        self.settings_manager = SettingsManager()

        # Initialize UI
        self.setWindowTitle("Export Pictographs with Turns")
        self.resize(700, 600)  # Larger size for modern UI
        self.setStyleSheet(
            """
            QDialog {
                background-color: palette(window);
                color: palette(windowtext);
            }
            QLabel {
                color: palette(windowtext);
            }
            QCheckBox {
                color: palette(windowtext);
            }
        """
        )

        # Create the UI builder
        self.ui = CodexDialogUI(self)
        self.ui.setup_ui()

    def _export_pictographs(self):
        """Export the selected pictographs with the configured turns."""
        # Get the selected pictograph types
        selected_types = self.ui.letter_selection.get_selected_types()

        if not selected_types:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select at least one pictograph type to export.",
            )
            return

        # Get the turn configuration
        turn_config = self.ui.turn_configuration.get_turn_values()
        red_turns = turn_config["red_turns"]
        blue_turns = turn_config["blue_turns"]
        generate_all = turn_config["generate_all"]
        grid_mode = turn_config["grid_mode"]

        # Save the settings for next time
        self.settings_manager.codex_exporter.set_last_red_turns(red_turns)
        self.settings_manager.codex_exporter.set_last_blue_turns(blue_turns)
        self.settings_manager.codex_exporter.set_grid_mode(grid_mode)

        # Export the pictographs
        exported_count = self.codex_exporter.export_pictographs(
            selected_types, red_turns, blue_turns, generate_all, grid_mode
        )

        if exported_count > 0:
            self.accept()
