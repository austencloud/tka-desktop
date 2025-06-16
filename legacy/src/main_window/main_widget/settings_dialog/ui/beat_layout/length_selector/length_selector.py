from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal

from .layout_length_button import LayoutLengthButton
from .num_beats_spinbox import NumBeatsSpinbox
from .sequence_length_label import SequenceLengthLabel
from src.legacy_settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from ..layout_controls.layout_controls import LayoutControls


class LengthSelector(QFrame):
    value_changed = pyqtSignal(int)

    def __init__(self, controls_widget: "LayoutControls"):
        super().__init__(controls_widget)
        self.controls_widget = controls_widget
        self.layout_tab = controls_widget.layout_tab
        self.sequence_length_label = SequenceLengthLabel(self)
        self.minus_button = LayoutLengthButton("-", self, self._decrease_length)
        self.plus_button = LayoutLengthButton("+", self, self._increase_length)
        self.num_beats_spinbox = NumBeatsSpinbox(self)
        self.num_beats_spinbox.valueChanged.connect(self.value_changed.emit)
        self._setup_layout()

    def showEvent(self, event):
        beat_count = AppContext.settings_manager().sequence_layout.get_num_beats()
        self.num_beats_spinbox.setValue(int(beat_count))
        super().showEvent(event)

    def _setup_layout(self):
        spinbox_layout = QHBoxLayout(self)
        spinbox_layout.addStretch(3)
        spinbox_layout.addWidget(self.minus_button, 1)
        spinbox_layout.addWidget(self.num_beats_spinbox, 1)
        spinbox_layout.addWidget(self.plus_button, 1)
        spinbox_layout.addStretch(3)

    def _decrease_length(self):
        current_value = self.num_beats_spinbox.value()
        if current_value > 1:
            self.num_beats_spinbox.setValue(current_value - 1)

    def _increase_length(self):
        self.num_beats_spinbox.setValue(self.num_beats_spinbox.value() + 1)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        base_size = int(self.controls_widget.width() // 30)
        padding = int(base_size / 5)

        font = QFont()
        font.setPointSize(base_size)
        font.setBold(True)

        self.num_beats_spinbox.setFont(font)
        self.num_beats_spinbox.setStyleSheet(
            f"""
            QSpinBox {{
                padding: {padding}px;
                min-width: {base_size * 3}px;
            }}
        """
        )

        self.sequence_length_label.setFont(font)
        button_font = QFont(font)
        button_font.setPointSize(int(base_size * 1.2))
        self.minus_button.setFont(button_font)
        self.plus_button.setFont(button_font)
