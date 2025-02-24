from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab


class TurnIntensityAdjuster(QWidget):
    def __init__(self, generate_tab: "GenerateTab"):
        super().__init__()
        self.generate_tab = generate_tab

        self.values = [0.5, 1, 1.5, 2, 2.5, 3]
        self.intensity = self.generate_tab.settings.get_setting("turn_intensity")
        self.intensity_label = QLabel("Turn Intensity:")
        self.intensity_buttons_layout = QHBoxLayout()
        self._create_turn_intensity_adjuster()

        layout = QHBoxLayout()
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.intensity_label)
        layout.addLayout(self.intensity_buttons_layout)
        self.setLayout(layout)

    def _create_turn_intensity_adjuster(self):
        self.minus_button = self._create_button("-", self._decrease_intensity)
        self.intensity_value_label = QLabel(str(self.intensity))
        self.intensity_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.plus_button = self._create_button("+", self._increase_intensity)
        self.intensity_buttons_layout.addWidget(self.minus_button)
        self.intensity_buttons_layout.addWidget(self.intensity_value_label)
        self.intensity_buttons_layout.addWidget(self.plus_button)

    def _create_button(self, text, callback):
        button = QPushButton(text)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(callback)
        return button

    def _adjust_intensity(self, change):
        try:
            current_index = self.values.index(float(self.intensity))
        except ValueError:
            current_index = self.values.index(int(self.intensity))
        new_index = current_index + change
        if 0 <= new_index < len(self.values):
            self.intensity = self.values[new_index]
            self.intensity_value_label.setText(str(self.intensity))
            self.generate_tab.settings.set_setting(
                "turn_intensity", str(self.intensity)
            )

    def _increase_intensity(self):
        self._adjust_intensity(1)

    def _decrease_intensity(self):
        self._adjust_intensity(-1)

    def set_intensity(self, intensity):
        try:
            self.intensity = (
                int(intensity) if intensity in [0, 1, 2, 3] else float(intensity)
            )
        except ValueError:
            self.intensity = float(intensity)
        self.intensity_value_label.setText(str(self.intensity))

    def adjust_values(self, level):
        self.values = [0, 1, 2, 3] if level == 2 else [0, 0.5, 1, 1.5, 2, 2.5, 3]
        if self.intensity not in self.values:
            self.intensity = min(self.values, key=lambda x: abs(x - self.intensity))
            self.intensity_value_label.setText(str(self.intensity))
            self.generate_tab.settings.set_setting(
                "turn_intensity", str(self.intensity)
            )

    def resizeEvent(self, event):
        font_size = self.generate_tab.main_widget.width() // 75
        font = self.intensity_label.font()
        font.setPointSize(font_size)
        widgets: list[QWidget] = [
            self.minus_button,
            self.plus_button,
            self.intensity_label,
            self.intensity_value_label,
        ]
        for widget in widgets:
            widget.setFont(font)
        btn_size = self.generate_tab.main_widget.width() // 40
        self.minus_button.setFixedSize(btn_size, btn_size)
        self.plus_button.setFixedSize(btn_size, btn_size)
