from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
)
from PyQt6.QtCore import Qt

from data.constants import LETTER
from settings_manager.global_settings.app_context import AppContext
from styles.styled_button import StyledButton  # to get data_manager

from .filter_section_base import FilterSectionBase

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.sequence_picker.filter_stack.sequence_picker_filter_stack import (
        SequencePickerFilterStack,
    )


class ContainsLettersSection(FilterSectionBase):
    SECTIONS = [
        [
            ["A", "B", "C", "D", "E", "F"],
            ["G", "H", "I", "J", "K", "L"],
            ["M", "N", "O", "P", "Q", "R"],
            ["S", "T", "U", "V"],
        ],
        [["W", "X", "Y", "Z"], ["Σ", "Δ", "θ", "Ω"]],
        [["W-", "X-", "Y-", "Z-"], ["Σ-", "Δ-", "θ-", "Ω-"]],
        [["Φ", "Ψ", "Λ"]],
        [["Φ-", "Ψ-", "Λ-"]],
        [["α", "β", "Γ"]],
    ]

    LETTER_ORDER = [letter for section in SECTIONS for row in section for letter in row]

    FONT_SIZE_FACTOR = 100
    BUTTON_SIZE_FACTOR = 20
    APPLY_BUTTON_WIDTH_FACTOR = 6

    SELECTED_STYLE = "background-color: blue; color: white; border: 2px solid black; border-radius: 5px;"
    UNSELECTED_STYLE = "background-color: lightgray; color: black; border: 1px solid darkgray; border-radius: 5px;"

    def __init__(self, initial_selection_widget: "SequencePickerFilterStack"):
        super().__init__(initial_selection_widget, "Select letters to be contained:")
        self.main_widget = initial_selection_widget.browse_tab.main_widget
        self.selected_letters: set[str] = set()
        self.buttons: dict[str, StyledButton] = {}
        self.add_buttons()

    def add_buttons(self):
        self.initialized = True
        self.go_back_button.show()
        self.header_label.show()

        layout: QVBoxLayout = self.layout()

        # Create letter buttons
        self.create_letter_buttons(layout)

        # Sequence tally label
        layout.addStretch(1)
        self.sequence_tally_label = QLabel("0 sequences")
        self.sequence_tally_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.sequence_tally_label)
        layout.addStretch(1)

        # Apply button
        apply_button_layout = QHBoxLayout()
        apply_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.apply_button = StyledButton("Apply")
        self.apply_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_button.clicked.connect(self.apply_filter)
        apply_button_layout.addWidget(self.apply_button)
        layout.addLayout(apply_button_layout)

        layout.addStretch(1)

    def create_letter_buttons(self, layout: QVBoxLayout):
        for section in self.SECTIONS:
            for row_data in section:
                button_row_layout = QHBoxLayout()
                button_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                for letter in row_data:
                    button = StyledButton(letter)
                    button.setCursor(Qt.CursorShape.PointingHandCursor)
                    button.setCheckable(True)
                    button.setProperty(LETTER, letter)
                    button.clicked.connect(self.update_letter_selection)
                    # self.update_button_style(button)  # Initialize style
                    self.buttons[letter] = button
                    button_row_layout.addWidget(button)
                layout.addLayout(button_row_layout)

        # def update_button_style(self, button: BaseStyledButton):
        """Update the button style based on its state."""
        if button.isChecked():
            button.setEnabled(True)
        else:
            button.setEnabled(False)

    def update_letter_selection(self):
        """Update the selected letters and the sequence tally."""
        for button in self.buttons.values():
            button.update_appearance()
            button.set_selected(button.isChecked())

        self.selected_letters = {
            button.property(LETTER)
            for button in self.buttons.values()
            if button.isChecked()
        }

        matching_sequences = self._count_sequences_matching_selected_letters()
        sequence_text = "sequence" if matching_sequences == 1 else "sequences"
        self.sequence_tally_label.setText(f"{matching_sequences} {sequence_text}")

    def _count_sequences_matching_selected_letters(self) -> int:
        """Count the number of sequences that match the currently selected letters."""
        if not self.selected_letters:
            return 0

        data_manager = AppContext.dictionary_data_manager()
        base_words = data_manager.get_all_words()

        return sum(
            any(letter in word for letter in self.selected_letters)
            for word in base_words
        )

    def apply_filter(self):
        """Apply the filter based on the selected letters."""
        self.browse_tab.filter_controller.apply_filter(
            {"contains_letters": list(self.selected_letters)}
        )

    def resize_widget_font(self, widget: QWidget):
        font = widget.font()
        font.setPointSize(self.main_widget.width() // self.FONT_SIZE_FACTOR)
        widget.setFont(font)

    def resize_buttons(self):
        width = self.main_widget.width() // self.BUTTON_SIZE_FACTOR
        height = self.main_widget.height() // self.BUTTON_SIZE_FACTOR
        font_size = self.main_widget.width() // self.FONT_SIZE_FACTOR
        for button in self.buttons.values():
            font = button.font()
            font.setPointSize(font_size)
            button.setFont(font)
            button.setFixedSize(width, height)

    def resize_apply_button(self):
        width = self.main_widget.width() // self.APPLY_BUTTON_WIDTH_FACTOR
        self.apply_button.setFixedWidth(width)
        self.resize_widget_font(self.apply_button)

    def resizeEvent(self, event):
        self.resize_widget_font(self.header_label)
        self.resize_widget_font(self.sequence_tally_label)
        self.resize_buttons()
        self.resize_apply_button()
