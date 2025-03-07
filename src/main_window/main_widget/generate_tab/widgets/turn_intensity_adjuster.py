from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING

from main_window.main_widget.generate_tab.widgets.increment_adjuster_button import (
    IncrementAdjusterButton,
)

if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab


class TurnIntensityAdjuster(QWidget):
    def __init__(self, generate_tab: "GenerateTab"):
        super().__init__()
        self.generate_tab = generate_tab

        self.values = [0.5, 1, 1.5, 2, 2.5, 3]
        self.intensity = (
            float(self.generate_tab.settings.get_setting("turn_intensity"))
            if self.generate_tab.settings.get_setting("turn_intensity")
            in [
                "0.5",
                "1.5",
                "2.5",
            ]
            else int(self.generate_tab.settings.get_setting("turn_intensity"))
        )

        # Layout setup
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.intensity_label = QLabel("Turn Intensity:")
        self.intensity_buttons_layout = QHBoxLayout()
        self._create_turn_intensity_adjuster()

        # Add elements to layout
        self.layout.addWidget(self.intensity_label)
        self.layout.addLayout(self.intensity_buttons_layout)

    def _create_turn_intensity_adjuster(self):
        """Creates the plus/minus buttons and label for the turn intensity adjuster."""
        self.minus_button = IncrementAdjusterButton("-")
        self.minus_button.clicked.connect(self._decrease_intensity)

        self.intensity_value_label = QLabel(str(self.intensity))
        self.intensity_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.intensity_value_label.setFont(QFont("Georgia", 14, QFont.Weight.Bold))
        self.intensity_value_label.setSizePolicy(
            self.intensity_value_label.sizePolicy().Policy.Minimum,
            self.intensity_value_label.sizePolicy().Policy.Fixed,
        )

        self.plus_button = IncrementAdjusterButton("+")
        self.plus_button.clicked.connect(self._increase_intensity)

        self.intensity_buttons_layout.addWidget(self.minus_button)
        self.intensity_buttons_layout.addWidget(self.intensity_value_label)
        self.intensity_buttons_layout.addWidget(self.plus_button)

    def _adjust_intensity(self, change):
        """Handles increasing or decreasing the intensity based on the preset values."""
        try:
            current_index = self.values.index(float(self.intensity))
        except ValueError:
            current_index = self.values.index(int(self.intensity))

        new_index = current_index + change
        if 0 <= new_index < len(self.values):
            self.intensity = self.values[new_index]
            self.intensity_value_label.setText(str(self.intensity))
            self.intensity_value_label.adjustSize()  # ✅ Dynamically adjust size
            self.generate_tab.settings.set_setting(
                "turn_intensity", str(self.intensity)
            )

    def _increase_intensity(self):
        """Increases the turn intensity within allowed values."""
        self._adjust_intensity(1)

    def _decrease_intensity(self):
        """Decreases the turn intensity within allowed values."""
        self._adjust_intensity(-1)

    def set_intensity(self, intensity):
        """Sets the turn intensity based on stored settings."""
        try:
            self.intensity = (
                int(intensity)
                if intensity in ["0", "1", "2", "3"]
                else float(intensity)
            )
        except ValueError:
            self.intensity = float(intensity)

        self.intensity_value_label.setText(str(self.intensity))
        self.intensity_value_label.adjustSize()  # ✅ Ensure it resizes properly

    def adjust_values(self, level):
        """Adjusts available turn intensity values based on the difficulty level."""
        self.values = [1, 2, 3] if level == 2 else [0, 0.5, 1, 1.5, 2, 2.5, 3]
        if self.intensity not in self.values:
            self.intensity = min(self.values, key=lambda x: abs(x - self.intensity))
            self.intensity_value_label.setText(str(self.intensity))
            self.intensity_value_label.adjustSize()
            self.generate_tab.settings.set_setting(
                "turn_intensity", str(self.intensity)
            )

    def resizeEvent(self, event):
        """Dynamically resizes UI elements based on the window size."""
        self.layout.setSpacing(self.generate_tab.width() // 50)

        font_size = self.generate_tab.main_widget.width() // 65
        font = self.intensity_label.font()
        font.setPointSize(font_size)

        self.intensity_label.setFont(font)
        self.intensity_value_label.setFont(font)

        btn_size = max(26, self.generate_tab.main_widget.width() // 40)
        self.minus_button.setFixedSize(QSize(btn_size, btn_size))
        self.plus_button.setFixedSize(QSize(btn_size, btn_size))
