from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from main_window.main_widget.browse_tab.sequence_picker.control_panel.sort_widget.sequence_picker_sort_controller import (
    SequencePickerSortController,
)
from main_window.main_widget.browse_tab.sequence_picker.control_panel.sort_widget.sort_buttons_bar import (
    SortButtonsBar,
)
from main_window.main_widget.browse_tab.sequence_picker.control_panel.sort_widget.sort_option import (
    SortOption,
)
from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from ...sequence_picker import SequencePicker


class SequencePickerSortWidget(QWidget):
    """Main widget that manages sorting of dictionary entries."""

    def __init__(self, sequence_picker: "SequencePicker") -> None:
        super().__init__(sequence_picker)
        self.sequence_picker = sequence_picker
        self.settings_manager = AppContext.settings_manager()
        self.controller = SequencePickerSortController(sequence_picker)

        self.sort_options = [
            SortOption(
                "sequence_length",
                "Sequence Length",
                lambda: self.controller.on_sort("sequence_length"),
            ),
            SortOption(
                "alphabetical",
                "Alphabetical",
                lambda: self.controller.on_sort("alphabetical"),
            ),
            SortOption(
                "date_added",
                "Date Added",
                lambda: self.controller.on_sort("date_added"),
            ),
            SortOption(
                "level",
                "Level",
                lambda: self.controller.on_sort("level"),
            ),
        ]

        self.sort_buttons_bar = SortButtonsBar(self.sort_options, sort_widget=self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.sort_buttons_bar)
        self.setLayout(layout)
