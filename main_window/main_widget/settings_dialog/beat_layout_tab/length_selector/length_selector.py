from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from main_window.main_widget.settings_dialog.beat_layout_tab.length_selector.layout_length_button import (
    LayoutLengthButton,
)
from main_window.main_widget.settings_dialog.beat_layout_tab.length_selector.num_beats_spinbox import (
    NumBeatsSpinbox,
)
from main_window.main_widget.settings_dialog.beat_layout_tab.length_selector.sequence_length_label import (
    SequenceLengthLabel,
)
from main_window.settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from ..layout_controls.layout_controls import LayoutControls


class LengthSelector(QFrame):
    value_changed = pyqtSignal(int)  # Add signal

    def __init__(self, controls_widget: "LayoutControls"):
        super().__init__(controls_widget)
        self.controls_widget = controls_widget
        self.layout_tab = controls_widget.layout_tab
        self.sequence_length_label = SequenceLengthLabel(self)
        self.minus_button = LayoutLengthButton("-", self, self._decrease_length)
        self.plus_button = LayoutLengthButton("+", self, self._increase_length)
        self.num_beats_spinbox = NumBeatsSpinbox(self)

        # Connect spinbox changes to signal
        self.num_beats_spinbox.valueChanged.connect(self.value_changed.emit)
        beat_count = AppContext.settings_manager().sequence_layout.get_num_beats()
        self.num_beats_spinbox.setValue(int(beat_count))
        self._setup_layout()


    def _setup_layout(self):
        spinbox_layout = QHBoxLayout()
        spinbox_layout.addWidget(self.minus_button)
        spinbox_layout.addWidget(self.num_beats_spinbox)
        spinbox_layout.addWidget(self.plus_button)

        main_layout = QVBoxLayout(self)
        # main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.sequence_length_label)
        main_layout.addLayout(spinbox_layout)

    def _decrease_length(self):
        """Decrease the sequence length and emit the change."""
        current_value = self.num_beats_spinbox.value()
        if current_value > 1:
            self.num_beats_spinbox.setValue(current_value - 1)

    def _increase_length(self):
        """Increase the sequence length and emit the change."""
        self.num_beats_spinbox.setValue(self.num_beats_spinbox.value() + 1)

