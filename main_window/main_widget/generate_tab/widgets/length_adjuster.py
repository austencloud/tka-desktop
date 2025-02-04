from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..base_classes.base_sequence_generator_frame import BaseSequenceGeneratorFrame


class LengthAdjuster(QWidget):
    def __init__(self, sequence_generator_frame: "BaseSequenceGeneratorFrame"):
        super().__init__()
        self.sequence_generator_frame = sequence_generator_frame
        self.length = 8
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.adjustment_amount = 2
        self.length_label = QLabel("Length:")
        # self.length_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.length_buttons_layout = QHBoxLayout()
        # self.length_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._create_length_adjuster()

        self.layout.addWidget(self.length_label)
        self.layout.addLayout(self.length_buttons_layout)

    def _create_length_adjuster(self):
        self.minus_button = QPushButton("-")
        self.minus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.minus_button.clicked.connect(self._decrement_length)

        self.length_value_label = QLabel(str(self.length))
        self.length_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.length_value_label.setFixedWidth(40)

        self.plus_button = QPushButton("+")
        self.plus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.plus_button.clicked.connect(self._increment_length)

        self.length_buttons_layout.addWidget(self.minus_button)
        self.length_buttons_layout.addWidget(self.length_value_label)
        self.length_buttons_layout.addWidget(self.plus_button)

    def limit_length(self, state):
        if state:
            self.length = (self.length // 4) * 4
            self.length_value_label.setText(str(self.length))
            self.sequence_generator_frame._update_sequence_length(self.length)
            self.adjustment_amount = 4
        else:
            self.length = (self.length // 2) * 2
            self.length_value_label.setText(str(self.length))
            self.sequence_generator_frame._update_sequence_length(self.length)
            self.adjustment_amount = 2

    def _increment_length(self):
        if self.length < 64:
            self.length += self.adjustment_amount
            self.length_value_label.setText(str(self.length))
            self.sequence_generator_frame._update_sequence_length(self.length)

    def _decrement_length(self):
        if self.length > 4:
            self.length -= self.adjustment_amount
            self.length_value_label.setText(str(self.length))
            self.sequence_generator_frame._update_sequence_length(self.length)

    def set_length(self, length):
        """Set the initial length when loading settings."""
        self.length = length
        self.length_value_label.setText(str(self.length))

    def resizeEvent(self, event):
        font_size = self.sequence_generator_frame.tab.main_widget.width() // 75
        font = self.length_label.font()
        font.setPointSize(font_size)

        self.minus_button.setFont(font)
        self.plus_button.setFont(font)
        self.length_label.setFont(font)
        self.length_value_label.setFont(font)

        btn_size = self.sequence_generator_frame.tab.main_widget.width() // 40
        self.minus_button.setFixedSize(btn_size, btn_size)
        self.plus_button.setFixedSize(btn_size, btn_size)
