from typing import TYPE_CHECKING, Callable
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
)
from PyQt6.QtCore import Qt
from functools import partial
from datetime import datetime, timedelta

from main_window.main_widget.browse_tab.sequence_picker.filter_selector.filter_button_group import (
    FilterButtonGroup,
)
from main_window.main_widget.browse_tab.sequence_picker.filter_selector.choose_filter_label import (
    ChooseFilterLabel,
)

if TYPE_CHECKING:
    from .sequence_picker_filter_stack import SequencePickerFilterStack


class InitialFilterChoiceWidget(QWidget):
    """Widget to display filter options for the dictionary browser."""

    def __init__(self, filter_selector: "SequencePickerFilterStack"):
        super().__init__(filter_selector)
        self.filter_selector = filter_selector
        self.main_widget = filter_selector.browse_tab.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self.browse_tab = filter_selector.browse_tab
        self.button_groups: dict[str, QWidget] = {}
        self.buttons: dict[str, QPushButton] = {}
        self.description_labels: dict[str, QLabel] = {}
        self.filter_options = self._get_filter_options()

        self._setup_ui()

    def _setup_ui(self):
        """Set up the main UI layout."""
        self.header_label = ChooseFilterLabel(self)

        self._setup_button_groups()
        self._setup_grid_layout()
        self._setup_main_layout()

    def _setup_main_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addStretch(2)
        self.main_layout.addWidget(self.header_label)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.button_groups["Show All"])
        self.main_layout.addStretch(2)
        self.setLayout(self.main_layout)

    def _setup_grid_layout(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        horizontal_spacing = self.main_widget.width() // 20
        vertical_spacing = self.main_widget.height() // 20
        self.grid_layout.setHorizontalSpacing(horizontal_spacing)
        self.grid_layout.setVerticalSpacing(vertical_spacing)
        for index, label in enumerate(self.filter_options.keys()):
            if label != "Show All":
                button_group = self.button_groups[label]
                row = index // 3
                col = index % 3
                self.grid_layout.addWidget(button_group, row, col)

    def _setup_button_groups(self):
        """Create button groups for all filter options."""
        for label, (description, handler) in self.filter_options.items():
            self.button_groups[label] = FilterButtonGroup(
                label, description, handler, self
            )

    def _get_filter_options(self) -> dict[str, tuple[str, Callable]]:
        """Return a dictionary of filter options as {label: (description, handler)}."""
        return {
            "Starting Letter": (
                "Display sequences that start with a specific letter.",
                partial(self.filter_selector.show_section, "starting_letter"),
            ),
            "Contains Letter": (
                "Display sequences that contain specific letters.",
                partial(self.filter_selector.show_section, "contains_letters"),
            ),
            "Sequence Length": (
                "Display sequences by length.",
                partial(self.filter_selector.show_section, "sequence_length"),
            ),
            "Level": (
                "Display sequences by difficulty level.",
                partial(self.filter_selector.show_section, "level"),
            ),
            "Starting Position": (
                "Display sequences by starting position.",
                partial(self.filter_selector.show_section, "starting_position"),
            ),
            "Author": (
                "Display sequences by author.",
                partial(self.filter_selector.show_section, "author"),
            ),
            "Favorites": (
                "Display your favorite sequences.",
                partial(
                    self.browse_tab.filter_controller.apply_filter, {"favorites": True}
                ),
            ),
            "Most Recent": (
                "Display sequences created in the last week.",
                partial(
                    self.browse_tab.filter_controller.apply_filter,
                    {"most_recent": datetime.now() - timedelta(weeks=1)},
                ),
            ),
            "Grid Mode": (
                "Display sequences by grid mode (Box or Diamond).",
                partial(self.filter_selector.show_section, "grid_mode"),
            ),
            "Show All": (
                "Display every sequence in the dictionary.",
                partial(
                    self.browse_tab.filter_controller.apply_filter, {"show_all": True}
                ),
            ),
        }
