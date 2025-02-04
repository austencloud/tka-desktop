from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..base_classes.base_sequence_generator_frame import BaseSequenceGeneratorFrame


class TurnIntensityAdjuster(QWidget):
    def __init__(self, sequence_generator_frame: "BaseSequenceGeneratorFrame"):
        super().__init__()
        self.sequence_generator_frame = sequence_generator_frame
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.values = [0.5, 1, 1.5, 2, 2.5, 3]
        self.intensity = 1
        self.intensity_label = QLabel("Turn Intensity:")
        # self.intensity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.intensity_buttons_layout = QHBoxLayout()
        # self.intensity_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._create_turn_intensity_adjuster()

        self.layout.addWidget(self.intensity_label)
        self.layout.addLayout(self.intensity_buttons_layout)

    def _create_turn_intensity_adjuster(self):
        self.minus_button = QPushButton("-")
        self.minus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.minus_button.clicked.connect(self._decrease_intensity)

        self.intensity_value_label = QLabel(str(self.intensity))
        self.intensity_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.plus_button = QPushButton("+")
        self.plus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.plus_button.clicked.connect(self._increase_intensity)

        self.intensity_buttons_layout.addWidget(self.minus_button)
        self.intensity_buttons_layout.addWidget(self.intensity_value_label)
        self.intensity_buttons_layout.addWidget(self.plus_button)

    def _increase_intensity(self):
        # Check the current index and make sure we do not exceed the max valid value
        try:
            current_index = self.values.index(float(self.intensity))
        except ValueError:
            current_index = self.values.index(int(self.intensity))
        if current_index < len(self.values) - 1:
            self.intensity = self.values[current_index + 1]
            self.intensity_value_label.setText(str(self.intensity))
            self.sequence_generator_frame._update_max_turn_intensity(self.intensity)

    def _decrease_intensity(self):
        # Check the current index and make sure we do not go below the min valid value
        current_index = self.values.index(self.intensity)
        if current_index > 0:
            self.intensity = self.values[current_index - 1]
            self.intensity_value_label.setText(str(self.intensity))
            self.sequence_generator_frame._update_max_turn_intensity(self.intensity)

    def set_intensity(self, intensity):
        """Set the initial intensity when loading settings."""
        try:
            self.intensity = (
                int(intensity)
                if intensity in ["0", "1", "2", "3"]
                else float(intensity)
            )
        except ValueError:
            self.intensity = float(intensity)
        self.intensity_value_label.setText(str(self.intensity))

    def adjust_values(self, level):
        if level == 2:
            self.values = [0, 1, 2, 3]
        elif level == 3:
            self.values = [0, 0.5, 1, 1.5, 2, 2.5, 3]

        if self.intensity not in self.values:
            self.intensity = min(self.values, key=lambda x: abs(x - self.intensity))
            self.intensity_value_label.setText(str(self.intensity))
            self.sequence_generator_frame._update_max_turn_intensity(self.intensity)

    def resizeEvent(self, event):
        font_size = self.sequence_generator_frame.tab.main_widget.width() // 75
        font = self.intensity_label.font()
        font.setPointSize(font_size)

        self.minus_button.setFont(font)
        self.plus_button.setFont(font)
        self.intensity_label.setFont(font)
        self.intensity_value_label.setFont(font)
        btn_size = self.sequence_generator_frame.tab.main_widget.width() // 40
        self.minus_button.setFixedSize(btn_size, btn_size)
        self.plus_button.setFixedSize(btn_size, btn_size)
