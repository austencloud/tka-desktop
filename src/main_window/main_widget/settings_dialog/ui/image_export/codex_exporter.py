"""
Dialog for exporting pictographs with turns.
"""
from typing import TYPE_CHECKING, List, Dict, Any
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QCheckBox,
    QComboBox,
    QGroupBox,
    QGridLayout,
    QDialogButtonBox,
    QMessageBox,
)
from PyQt6.QtCore import Qt

from .codex_exporter.codex_exporter import CodexExporter

if TYPE_CHECKING:
    from .image_export_tab import ImageExportTab


class CodexDialog(QDialog):
    """Dialog for exporting pictographs with turns."""

    def __init__(self, image_export_tab: "ImageExportTab"):
        """Initialize the dialog.
        
        Args:
            image_export_tab: The parent image export tab
        """
        super().__init__(image_export_tab)
        self.image_export_tab = image_export_tab
        self.main_widget = image_export_tab.main_widget
        
        # Create the exporter
        self.exporter = CodexExporter(image_export_tab)
        
        # Set up the UI
        self.setWindowTitle("Export Pictographs with Turns")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        
        # Create the layout
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the UI."""
        main_layout = QVBoxLayout(self)
        
        # Create the pictograph type selection group
        type_group = QGroupBox("Pictograph Types")
        type_layout = QGridLayout(type_group)
        
        # Create checkboxes for each pictograph type
        self.type_checkboxes = {}
        pictograph_types = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", 
                           "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V"]
        
        # Create a grid of checkboxes
        for i, type_name in enumerate(pictograph_types):
            checkbox = QCheckBox(type_name)
            checkbox.setChecked(True)  # Default to checked
            self.type_checkboxes[type_name] = checkbox
            
            # Calculate row and column (4 columns)
            row, col = divmod(i, 4)
            type_layout.addWidget(checkbox, row, col)
            
        # Add select/deselect all buttons
        select_all_button = QPushButton("Select All")
        select_all_button.clicked.connect(self._select_all_types)
        
        deselect_all_button = QPushButton("Deselect All")
        deselect_all_button.clicked.connect(self._deselect_all_types)
        
        # Add buttons to a horizontal layout
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(select_all_button)
        buttons_layout.addWidget(deselect_all_button)
        
        # Add the buttons layout to the type layout
        type_layout.addLayout(buttons_layout, len(pictograph_types) // 4 + 1, 0, 1, 4)
        
        # Create the turn selection group
        turn_group = QGroupBox("Turn Configuration")
        turn_layout = QVBoxLayout(turn_group)
        
        # Create the turn selection controls
        turn_selection_layout = QHBoxLayout()
        
        # Red turns
        red_layout = QHBoxLayout()
        red_layout.addWidget(QLabel("Red Turns:"))
        self.red_turns_combo = QComboBox()
        self.red_turns_combo.addItems(["0", "1", "2", "3"])
        red_layout.addWidget(self.red_turns_combo)
        
        # Blue turns
        blue_layout = QHBoxLayout()
        blue_layout.addWidget(QLabel("Blue Turns:"))
        self.blue_turns_combo = QComboBox()
        self.blue_turns_combo.addItems(["0", "1", "2", "3"])
        blue_layout.addWidget(self.blue_turns_combo)
        
        # Add the red and blue layouts to the turn selection layout
        turn_selection_layout.addLayout(red_layout)
        turn_selection_layout.addLayout(blue_layout)
        
        # Create the "Generate All Combinations" checkbox
        self.generate_all_checkbox = QCheckBox("Generate All Turn Combinations (0-3 turns)")
        self.generate_all_checkbox.setChecked(False)
        self.generate_all_checkbox.stateChanged.connect(self._update_turn_combos_state)
        
        # Add the controls to the turn layout
        turn_layout.addLayout(turn_selection_layout)
        turn_layout.addWidget(self.generate_all_checkbox)
        
        # Add the groups to the main layout
        main_layout.addWidget(type_group)
        main_layout.addWidget(turn_group)
        
        # Add the dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._export_pictographs)
        button_box.rejected.connect(self.reject)
        
        main_layout.addWidget(button_box)
        
    def _select_all_types(self):
        """Select all pictograph types."""
        for checkbox in self.type_checkboxes.values():
            checkbox.setChecked(True)
            
    def _deselect_all_types(self):
        """Deselect all pictograph types."""
        for checkbox in self.type_checkboxes.values():
            checkbox.setChecked(False)
            
    def _update_turn_combos_state(self, state):
        """Update the state of the turn combo boxes based on the "Generate All" checkbox."""
        enabled = not bool(state)
        self.red_turns_combo.setEnabled(enabled)
        self.blue_turns_combo.setEnabled(enabled)
        
    def _export_pictographs(self):
        """Export the pictographs with the selected turns."""
        # Get the selected pictograph types
        selected_types = [
            type_name for type_name, checkbox in self.type_checkboxes.items() 
            if checkbox.isChecked()
        ]
        
        # Check if any types are selected
        if not selected_types:
            QMessageBox.warning(
                self,
                "No Types Selected",
                "Please select at least one pictograph type to export.",
            )
            return
            
        # Get the turn configuration
        red_turns = int(self.red_turns_combo.currentText())
        blue_turns = int(self.blue_turns_combo.currentText())
        generate_all = self.generate_all_checkbox.isChecked()
        
        # Export the pictographs
        exported_count = self.exporter.export_pictographs(
            selected_types, red_turns, blue_turns, generate_all
        )
        
        # Close the dialog if export was successful
        if exported_count > 0:
            self.accept()
        else:
            # Don't close the dialog if the export was canceled or failed
            pass
