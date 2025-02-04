from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from pytoggle import PyToggle
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from ..circular.circular_sequence_generator_frame import (
        CircularSequenceGeneratorFrame,
    )


class RotationTypeToggle(QWidget):
    def __init__(self, circular_builder_frame: "CircularSequenceGeneratorFrame"):
        super().__init__()
        self.circular_builder_frame = circular_builder_frame
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.halved_label = QLabel("Halved")
        self.quartered_label = QLabel("Quartered")
        self.rotation_type_toggle = PyToggle()
        self.rotation_type_toggle.stateChanged.connect(self._toggle_changed)

        # Add labels and toggle to layout
        self.layout.addWidget(self.halved_label)
        self.layout.addWidget(self.rotation_type_toggle)
        self.layout.addWidget(self.quartered_label)

        # Initial style update
        # self.update_mode_label_styles()

    def _toggle_changed(self, state):
        rotation_type = "quartered" if state else "halved"
        self.circular_builder_frame._update_rotation_type(rotation_type)
        self.circular_builder_frame.length_adjuster.limit_length(state)
        self.update_mode_label_styles()

    def update_mode_label_styles(self):
        """Update the styles of the labels to indicate the selected rotation type."""
        font_color_updater = (
            self.circular_builder_frame.tab.main_widget.font_color_updater
        )
        font_color = font_color_updater.get_font_color(
            self.circular_builder_frame.tab.main_widget.settings_manager.global_settings.get_background_type()
        )
        if self.rotation_type_toggle.isChecked():
            self.halved_label.setStyleSheet("font-weight: normal; color: gray;")
            self.quartered_label.setStyleSheet(
                f"font-weight: bold; color: {font_color};"
            )
        else:
            self.halved_label.setStyleSheet(f"font-weight: bold; color: {font_color};")
            self.quartered_label.setStyleSheet("font-weight: normal; color: gray;")
        self.halved_label.repaint()
        self.quartered_label.repaint()

    def set_state(self, state):
        """Set the toggle state when loading settings."""
        self.rotation_type_toggle.setChecked(state)
        self.update_mode_label_styles()

    def resizeEvent(self, event):
        font_size = self.circular_builder_frame.tab.main_widget.width() // 75
        font = self.halved_label.font()
        font.setPointSize(font_size)
        self.halved_label.setFont(font)
        self.quartered_label.setFont(font)

        self.halved_label.updateGeometry()
        self.quartered_label.updateGeometry()
        self.halved_label.repaint()
        self.quartered_label.repaint()
