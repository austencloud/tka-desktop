from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from pytoggle import PyToggle
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from ..circular.circular_sequence_generator_frame import (
        CircularSequenceGeneratorFrame,
    )


class PermutationTypeToggle(QWidget):
    def __init__(self, circular_builder_frame: "CircularSequenceGeneratorFrame"):
        super().__init__()
        self.circular_builder_frame = circular_builder_frame
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.mirrored_label = QLabel("Mirrored")
        self.rotated_label = QLabel("Rotated")
        self.permutation_type_toggle = PyToggle()
        self.permutation_type_toggle.stateChanged.connect(self._toggle_changed)

        # Add labels and toggle to layout
        self.layout.addWidget(self.mirrored_label)
        self.layout.addWidget(self.permutation_type_toggle)
        self.layout.addWidget(self.rotated_label)

        # Initial style update
        # self.update_mode_label_styles()

    def _toggle_changed(self, state):
        permutation_type = "rotated" if state else "mirrored"
        self.circular_builder_frame._update_permutation_type(permutation_type)
        self.update_mode_label_styles()

    def update_mode_label_styles(self):
        """Update the styles of the labels to indicate the selected permutation type."""
        font_color_updater = (
            self.circular_builder_frame.tab.main_widget.font_color_updater
        )
        font_color = font_color_updater.get_font_color(
            self.circular_builder_frame.tab.main_widget.settings_manager.global_settings.get_background_type()
        )
        if self.permutation_type_toggle.isChecked():
            self.mirrored_label.setStyleSheet("font-weight: normal; color: gray;")
            self.rotated_label.setStyleSheet(f"font-weight: bold; color: {font_color};")
        else:
            self.mirrored_label.setStyleSheet(
                f"font-weight: bold; color: {font_color};"
            )
            self.rotated_label.setStyleSheet("font-weight: normal; color: gray;")

    def set_state(self, state):
        """Set the toggle state when loading settings."""
        self.permutation_type_toggle.setChecked(state)
        self.update_mode_label_styles()

    def resizeEvent(self, event):
        font_size = self.circular_builder_frame.tab.main_widget.width() // 75
        self.mirrored_label.setStyleSheet(f"font-size: {font_size}px;")
        self.rotated_label.setStyleSheet(f"font-size: {font_size}px;")
        self.mirrored_label.updateGeometry()
        self.rotated_label.updateGeometry()

        self.mirrored_label.repaint()
        self.rotated_label.repaint()
