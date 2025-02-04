from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING

from main_window.main_widget.generate_tab.widgets.level_button import LevelButton


if TYPE_CHECKING:
    from ..base_classes.base_sequence_generator_frame import BaseSequenceGeneratorFrame


class LevelSelector(QWidget):
    def __init__(self, sequence_generator_frame: "BaseSequenceGeneratorFrame"):
        super().__init__()
        self.sequence_generator_frame = sequence_generator_frame

        # Main layout: Central alignment for the entire widget
        self.main_layout: QVBoxLayout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setSpacing(0)

        self.group_layout: QHBoxLayout = QHBoxLayout()  #
        self.group_layout.addStretch(1)
        self.group_layout.setSpacing(10)

        self.level_label = QLabel("Level:")
        self.level_label.setFont(QFont("Arial", 16))
        self.group_layout.addWidget(self.level_label)

        self.level_buttons_layout = QHBoxLayout()
        self.level_buttons_layout.setSpacing(10)

        self.level_buttons: dict[str, LevelButton] = {}
        self._create_level_buttons()

        self.group_layout.addLayout(self.level_buttons_layout)
        self.group_layout.addStretch(1)
        self.main_layout.addLayout(self.group_layout)

    def _create_level_buttons(self):
        levels = [
            {"level": 1, "icon": "images/icons/level_1.png"},
            {"level": 2, "icon": "images/icons/level_2.png"},
            {"level": 3, "icon": "images/icons/level_3.png"},
        ]
        for level_info in levels:
            level = level_info["level"]
            icon_path = level_info["icon"]

            # Create a custom LevelButton
            button = LevelButton(level, icon_path)
            button.clicked.connect(self._on_level_change)
            self.level_buttons_layout.addWidget(button)
            self.level_buttons[f"level_{level}"] = button

    def _on_level_change(self, selected_level: int):
        # Trigger sequence generator update
        self.sequence_generator_frame._update_sequence_level(selected_level)

        if selected_level == 1:
            self.sequence_generator_frame.turn_intensity_adjuster.hide()
        else:
            self.sequence_generator_frame.turn_intensity_adjuster.show()
            self.sequence_generator_frame.turn_intensity_adjuster.adjust_values(
                selected_level
            )

    def set_level(self, level: int):
        """Set the initial level when loading settings."""
        self._on_level_change(level)

    def resizeEvent(self, event):
        """Resize the level label font dynamically based on the parent height."""
        self.level_label.setFont(
            QFont("Arial", self.sequence_generator_frame.height() // 30, 0)
        )
