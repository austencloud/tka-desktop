from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .layout_controls import LayoutControls


class UpdateDefaultLayoutButton(QPushButton):
    def __init__(self, control_widget: "LayoutControls"):
        self.control_widget = control_widget

        super().__init__("Update Default Layout", control_widget)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(
            lambda: self.set_default_layout(
                control_widget.layout_selector.layout_dropdown.currentText()
            )
        )

    def resizeEvent(self, event):
        font = self.font()
        font.setPointSize(max(10, self.control_widget.layout_tab.width() // 50))
        self.setFont(font)

    def set_default_layout(self, layout_text: str):
        self.control_widget.layout_tab.num_beats = (
            self.control_widget.length_selector.num_beats_spinbox.value()
        )
        self.update_default_layout_label(layout_text)
        layout_tuple = tuple(map(int, layout_text.split(" x ")))
        self.control_widget.layout_settings.set_layout_setting(
            str(self.control_widget.layout_tab.num_beats), list(layout_tuple)
        )
        beat_frame = (
            self.control_widget.layout_tab.main_widget.sequence_workbench.beat_frame
        )
        beat_frame.layout_manager.configure_beat_frame(beat_frame.get.beat_count())

    def update_default_layout_label(self, layout_text):
        """Update the default layout label."""
        self.control_widget.default_layout_label.setText(f"Default: {layout_text}")
