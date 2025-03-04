from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING

from main_window.main_widget.generate_tab.widgets.increment_adjuster_button import (
    IncrementAdjusterButton,
)

if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab


class GenerateTabLengthAdjuster(QWidget):
    def __init__(self, generate_tab: "GenerateTab"):
        super().__init__()
        self.generate_tab = generate_tab
        self.length = self.generate_tab.settings.get_setting("length")

        # Layout setup
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.adjustment_amount = 2

        # Create UI elements
        self.length_label = QLabel("Length:")
        self.length_buttons_layout = QHBoxLayout()
        self._create_length_adjuster()

        # Add elements to layout
        self.layout.addWidget(self.length_label)
        self.layout.addLayout(self.length_buttons_layout)

    def _create_length_adjuster(self):
        """Creates the plus/minus buttons and label for the length adjuster."""
        self.minus_button = IncrementAdjusterButton("-")
        self.minus_button.clicked.connect(self._decrement_length)

        self.length_value_label = QLabel(str(self.length))
        self.length_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.length_value_label.setFixedWidth(50)
        self.length_value_label.setFont(QFont("Georgia", 14, QFont.Weight.Bold))

        self.plus_button = IncrementAdjusterButton("+")
        self.plus_button.clicked.connect(self._increment_length)

        self.length_buttons_layout.addWidget(self.minus_button)
        self.length_buttons_layout.addWidget(self.length_value_label)
        self.length_buttons_layout.addWidget(self.plus_button)

    def limit_length(self, state):
        """Adjusts length constraints dynamically."""
        if state:
            self.length = (self.length // 4) * 4
            self.adjustment_amount = 4
        else:
            self.length = (self.length // 2) * 2
            self.adjustment_amount = 2

        self.length_value_label.setText(str(self.length))
        self.generate_tab.settings.set_setting("length", str(self.length))

    def _increment_length(self):
        """Increments the length, with upper limit of 64."""
        if self.length < 64:
            self.length += self.adjustment_amount
            self.length_value_label.setText(str(self.length))
            self.generate_tab.settings.set_setting("length", str(self.length))

    def _decrement_length(self):
        """Decrements the length, with lower limit of 4."""
        if self.length > 4:
            self.length -= self.adjustment_amount
            self.length_value_label.setText(str(self.length))
            self.generate_tab.settings.set_setting("length", str(self.length))

    def set_length(self, length):
        """Sets the length based on stored settings."""
        self.length = length
        self.length_value_label.setText(str(self.length))

    def resizeEvent(self, event):
        """Dynamically resizes UI elements based on the window size."""
        self.layout.setSpacing(self.generate_tab.width() // 50)

        font_size = self.generate_tab.main_widget.width() // 65
        font = self.length_label.font()
        font.setPointSize(font_size)

        self.length_label.setFont(font)
        self.length_value_label.setFont(font)

        btn_size = max(26, self.generate_tab.main_widget.width() // 40)
        self.minus_button.setFixedSize(QSize(btn_size, btn_size))
        self.plus_button.setFixedSize(QSize(btn_size, btn_size))
