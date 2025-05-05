"""
Letter selection component for the codex exporter dialog.
"""
from typing import Dict, Callable
from PyQt6.QtWidgets import QWidget, QGridLayout, QHBoxLayout
from ..widgets import ModernCard, LetterButton, ModernButton


class LetterSelectionComponent(QWidget):
    """Component for selecting pictograph letters."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pictograph_types_to_export = {
            letter: True for letter in "ABCDEFGHIJKLMNOPQRSTUV"
        }
        self.letter_buttons: Dict[str, LetterButton] = {}
        self._setup_ui()

    def _setup_ui(self):
        """Set up the letter selection UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create the card
        letter_card = ModernCard(self, "Select Pictograph Types")

        # Create a grid of letter buttons
        letter_grid = QGridLayout()
        letter_grid.setSpacing(10)

        # Create buttons for each pictograph type
        row, col = 0, 0
        for letter in "ABCDEFGHIJKLMNOPQRSTUV":
            button = LetterButton(letter, self)
            button.clicked.connect(
                lambda checked, letter=letter: self._on_letter_button_clicked(
                    checked, letter
                )
            )
            self.letter_buttons[letter] = button
            letter_grid.addWidget(button, row, col)
            col += 1
            if col > 5:  # 6 columns for better layout
                col = 0
                row += 1

        # Add quick selection buttons
        quick_select_layout = QHBoxLayout()
        select_all_btn = ModernButton("Select All", primary=False)
        select_all_btn.clicked.connect(self._select_all_letters)

        deselect_all_btn = ModernButton("Deselect All", primary=False)
        deselect_all_btn.clicked.connect(self._deselect_all_letters)

        select_hybrid_btn = ModernButton("Hybrid Only", primary=False)
        select_hybrid_btn.clicked.connect(self._select_hybrid_letters)

        select_non_hybrid_btn = ModernButton("Non-Hybrid Only", primary=False)
        select_non_hybrid_btn.clicked.connect(self._select_non_hybrid_letters)

        quick_select_layout.addWidget(select_all_btn)
        quick_select_layout.addWidget(deselect_all_btn)
        quick_select_layout.addWidget(select_hybrid_btn)
        quick_select_layout.addWidget(select_non_hybrid_btn)

        # Add layouts to letter card
        letter_card.layout.addLayout(letter_grid)
        letter_card.layout.addLayout(quick_select_layout)
        layout.addWidget(letter_card)

    def _on_letter_button_clicked(self, checked, letter):
        """Handle letter button clicks."""
        self.pictograph_types_to_export[letter] = checked

    def _select_all_letters(self):
        """Select all letter buttons."""
        for letter, button in self.letter_buttons.items():
            button.setChecked(True)
            self.pictograph_types_to_export[letter] = True

    def _deselect_all_letters(self):
        """Deselect all letter buttons."""
        for letter, button in self.letter_buttons.items():
            button.setChecked(False)
            self.pictograph_types_to_export[letter] = False

    def _select_hybrid_letters(self):
        """Select only hybrid letter buttons."""
        hybrid_letters = ["C", "F", "I", "L", "O", "R", "S", "T", "U", "V"]
        for letter, button in self.letter_buttons.items():
            is_hybrid = letter in hybrid_letters
            button.setChecked(is_hybrid)
            self.pictograph_types_to_export[letter] = is_hybrid

    def _select_non_hybrid_letters(self):
        """Select only non-hybrid letter buttons."""
        hybrid_letters = ["C", "F", "I", "L", "O", "R", "S", "T", "U", "V"]
        for letter, button in self.letter_buttons.items():
            is_non_hybrid = letter not in hybrid_letters
            button.setChecked(is_non_hybrid)
            self.pictograph_types_to_export[letter] = is_non_hybrid

    def get_selected_types(self):
        """Get the selected pictograph types."""
        return [
            letter
            for letter, is_selected in self.pictograph_types_to_export.items()
            if is_selected
        ]
