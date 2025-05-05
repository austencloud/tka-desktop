"""
UI builder for the codex dialog.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel

from .components import LetterSelectionComponent, TurnConfigurationComponent
from .widgets import ModernButton

if TYPE_CHECKING:
    from .codex_dialog import CodexDialog


class CodexDialogUI:
    """UI builder for the codex dialog."""

    def __init__(self, dialog: "CodexDialog"):
        """Initialize the UI builder.

        Args:
            dialog: The parent dialog
        """
        self.dialog = dialog
        self.letter_selection = LetterSelectionComponent(dialog)
        self.turn_configuration = TurnConfigurationComponent(dialog)
        self.export_button = None
        self.cancel_button = None

    def setup_ui(self):
        """Set up the dialog UI components."""
        main_layout = QVBoxLayout(self.dialog)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title label
        title_label = QLabel("Export Pictographs with Turns")
        title_label.setObjectName("dialogTitle")
        title_label.setStyleSheet(
            """
            #dialogTitle {
                font-size: 24px;
                font-weight: bold;
                color: palette(windowtext);
                margin-bottom: 10px;
                background-color: transparent;
            }
        """
        )
        main_layout.addWidget(title_label)

        # Add components
        main_layout.addWidget(self.letter_selection)
        main_layout.addWidget(self.turn_configuration)

        # Buttons
        button_layout = QHBoxLayout()
        self.export_button = ModernButton("Export Pictographs", primary=True)
        self.export_button.clicked.connect(self.dialog._export_pictographs)
        self.cancel_button = ModernButton("Cancel", primary=False)
        self.cancel_button.clicked.connect(self.dialog.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.export_button)
        main_layout.addLayout(button_layout)
