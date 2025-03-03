from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QLabel,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from functools import partial

from .filter_section_base import FilterSectionBase
from settings_manager.global_settings.app_context import AppContext  # to get data_manager

if TYPE_CHECKING:
    from .sequence_picker_filter_stack import SequencePickerFilterStack


class FilterByLevelSection(FilterSectionBase):
    MAX_COLUMNS = 3
    LEVEL_DESCRIPTIONS = {
        1: "Base letters with no turns.",
        2: "Turns added with only radial orientations.",
        3: "Non-radial orientations.",
    }

    def __init__(self, initial_selection_widget: "SequencePickerFilterStack"):
        super().__init__(initial_selection_widget, "Select by Difficulty Level:")
        self.main_widget = initial_selection_widget.browse_tab.main_widget
        self.buttons: dict[int, QPushButton] = {}
        self.description_labels: dict[int, QLabel] = {}
        self.tally_labels: dict[int, QLabel] = {}
        self.add_buttons()

    def add_buttons(self):
        """Initialize the UI components for the level selection."""
        self.go_back_button.show()
        self.header_label.show()
        layout: QVBoxLayout = self.layout()

        # Using the new data manager:
        data_manager = AppContext.dictionary_data_manager()
        all_levels = self.LEVEL_DESCRIPTIONS.keys()

        # Build a level -> count map
        self.sequence_counts = {
            level: len(data_manager.get_records_by_level(level))
            for level in all_levels
        }

        grid_layout = QGridLayout()
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.setHorizontalSpacing(50)
        grid_layout.setVerticalSpacing(30)

        row, col = 0, 0
        for level in sorted(self.sequence_counts.keys()):
            level_vbox = self.create_level_vbox(level)
            grid_layout.addLayout(level_vbox, row, col)

            col += 1
            if col >= self.MAX_COLUMNS:
                col = 0
                row += 1

        layout.addLayout(grid_layout)
        layout.addStretch(1)

    def create_level_vbox(self, level: int) -> QVBoxLayout:
        """Create a vertical box layout containing all components for a level."""
        level_vbox = QVBoxLayout()
        level_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button = self.create_level_button(level)
        description_label = self.create_description_label(level)
        sequence_count_label = self.create_sequence_count_label(level)

        level_vbox.addWidget(button)
        level_vbox.addWidget(description_label)
        level_vbox.addItem(
            QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        )
        level_vbox.addWidget(sequence_count_label)

        return level_vbox

    def create_level_button(self, level: int) -> QPushButton:
        """Create and configure the level selection button."""
        button = QPushButton(f"Level {level}")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(partial(self.handle_level_click, level))
        self.buttons[level] = button
        return button

    def create_description_label(self, level: int) -> QLabel:
        """Create a label for the level description."""
        description_label = QLabel(self.LEVEL_DESCRIPTIONS.get(level, ""))
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_labels[level] = description_label
        return description_label

    def create_sequence_count_label(self, level: int) -> QLabel:
        """Create a label displaying the sequence count for a level."""
        count = self.sequence_counts.get(level, 0)
        sequence_text = "sequence" if count == 1 else "sequences"
        sequence_count_label = QLabel(f"{count} {sequence_text}")
        sequence_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tally_labels[level] = sequence_count_label
        return sequence_count_label

    def handle_level_click(self, level: int):
        """Handle clicks on level buttons."""
        self.browse_tab.filter_controller.apply_filter({"level": level})
