from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from main_window.main_widget.browse_tab.sequence_picker.control_panel.sequence_picker_go_back_button import (
    SequencePickerGoBackButton,
)

from .currently_displaying_label import (
    CurrentlyDisplayingLabel,
)
from .sequence_picker_count_label import SequencePickerCountLabel
from .sort_widget.sequence_picker_sort_widget import SequencePickerSortWidget

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.sequence_picker.sequence_picker import (
        SequencePicker,
    )


class SequencePickerControlPanel(QWidget):
    def __init__(self, sequence_picker: "SequencePicker"):
        super().__init__(sequence_picker)
        self.sequence_picker = sequence_picker
        self._setup_ui()

    def _setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)

        self.go_back_button = SequencePickerGoBackButton(self.sequence_picker)
        self.currently_displaying_label = CurrentlyDisplayingLabel(self.sequence_picker)
        self.count_label = SequencePickerCountLabel(self.sequence_picker)
        self.sort_widget = SequencePickerSortWidget(self.sequence_picker)

        self.main_layout.addWidget(self.go_back_button)
        self.main_layout.addWidget(self.currently_displaying_label)
        self.main_layout.addWidget(self.count_label)
        self.main_layout.addWidget(self.sort_widget)

        self.setLayout(self.main_layout)
