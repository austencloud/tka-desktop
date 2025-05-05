"""
Dialog for exporting codex pictographs with turns.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QCheckBox,
    QLabel,
    QComboBox,
    QPushButton,
    QMessageBox,
    QGridLayout,
)
from PyQt6.QtCore import Qt

from .codex_exporter import CodexExporter

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
        ImageExportTab,
    )


class CodexDialog(QDialog):
    """Dialog for exporting codex pictographs with turns."""

    def __init__(self, image_export_tab: "ImageExportTab"):
        """Initialize the dialog.

        Args:
            image_export_tab: The parent image export tab
        """
        super().__init__(image_export_tab)
        self.image_export_tab = image_export_tab
        self.main_widget = image_export_tab.main_widget
        self.codex_exporter = CodexExporter(image_export_tab)

        # Track which pictograph types to export
        # All Type 1 letters: A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V
        self.pictograph_types_to_export = {
            letter: True for letter in "ABCDEFGHIJKLMNOPQRSTUV"
        }

        # Initialize UI
        self.setWindowTitle("Export Pictographs with Turns")
        self.resize(600, 500)  # Larger size to fit all letters
        self._setup_ui()

    def _setup_ui(self):
        """Set up the dialog UI components."""
        main_layout = QVBoxLayout(self)

        # Pictograph selection group
        pictograph_group = QGroupBox("Select Pictograph Types to Export")
        pictograph_layout = QGridLayout()

        # Create checkboxes for each pictograph type
        self.pictograph_checkboxes = {}
        row, col = 0, 0
        # All Type 1 letters: A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V
        for letter in "ABCDEFGHIJKLMNOPQRSTUV":
            checkbox = QCheckBox(letter)
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(
                lambda state, letter=letter: self._on_pictograph_checkbox_changed(
                    state, letter
                )
            )
            self.pictograph_checkboxes[letter] = checkbox
            pictograph_layout.addWidget(checkbox, row, col)
            col += 1
            if col > 3:  # 4 columns to fit all letters
                col = 0
                row += 1

        pictograph_group.setLayout(pictograph_layout)
        main_layout.addWidget(pictograph_group)

        # Turn configuration group
        turn_group = QGroupBox("Turn Configuration")
        turn_layout = QVBoxLayout()

        # Description label
        turn_description = QLabel(
            "Configure how turns are applied to different pictograph types:\n"
            "- Non-hybrid types (A, B, D, E, G, H, J, K, M, N, P, Q, S, T): Turns will be applied according to your selection\n"
            "- Hybrid types (C, F, I, L, O, R, U, V): Two versions will be generated when red and blue turns are different"
        )
        turn_description.setWordWrap(True)
        turn_layout.addWidget(turn_description)

        # Turn selection for right hand (red)
        right_hand_layout = QHBoxLayout()
        right_hand_layout.addWidget(QLabel("Right Hand (Red) Turns:"))
        self.right_hand_combo = QComboBox()
        self.right_hand_combo.addItems(["0", "1", "2", "3"])
        self.right_hand_combo.setCurrentIndex(1)  # Default to 1 turn
        right_hand_layout.addWidget(self.right_hand_combo)
        turn_layout.addLayout(right_hand_layout)

        # Turn selection for left hand (blue)
        left_hand_layout = QHBoxLayout()
        left_hand_layout.addWidget(QLabel("Left Hand (Blue) Turns:"))
        self.left_hand_combo = QComboBox()
        self.left_hand_combo.addItems(["0", "1", "2", "3"])
        self.left_hand_combo.setCurrentIndex(0)  # Default to 0 turns
        left_hand_layout.addWidget(self.left_hand_combo)
        turn_layout.addLayout(left_hand_layout)

        # Generate all combinations checkbox
        self.generate_all_checkbox = QCheckBox(
            "Generate all turn combinations (0-3 for each hand)"
        )
        self.generate_all_checkbox.setChecked(False)
        self.generate_all_checkbox.stateChanged.connect(self._on_generate_all_changed)
        turn_layout.addWidget(self.generate_all_checkbox)

        turn_group.setLayout(turn_layout)
        main_layout.addWidget(turn_group)

        # Buttons
        button_layout = QHBoxLayout()
        self.export_button = QPushButton("Export Pictographs")
        self.export_button.clicked.connect(self._export_pictographs)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

    def _on_pictograph_checkbox_changed(self, state, letter):
        """Handle pictograph checkbox state changes."""
        self.pictograph_types_to_export[letter] = state == Qt.CheckState.Checked.value

    def _on_generate_all_changed(self, state):
        """Handle generate all combinations checkbox state changes."""
        generate_all = state == Qt.CheckState.Checked.value

        # Enable/disable the individual turn selection combos based on the checkbox
        self.right_hand_combo.setEnabled(not generate_all)
        self.left_hand_combo.setEnabled(not generate_all)

    def _export_pictographs(self):
        """Export the selected pictographs with the configured turns."""
        # Get the selected pictograph types
        selected_types = [
            letter
            for letter, selected in self.pictograph_types_to_export.items()
            if selected
        ]

        if not selected_types:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select at least one pictograph type to export.",
            )
            return

        # Get the selected turn values
        red_turns = int(self.right_hand_combo.currentText())
        blue_turns = int(self.left_hand_combo.currentText())
        generate_all = self.generate_all_checkbox.isChecked()

        # Export the pictographs
        exported_count = self.codex_exporter.export_pictographs(
            selected_types, red_turns, blue_turns, generate_all
        )

        if exported_count > 0:
            self.accept()
