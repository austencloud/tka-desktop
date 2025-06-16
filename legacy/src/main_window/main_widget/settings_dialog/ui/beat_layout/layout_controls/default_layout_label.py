from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.beat_layout_tab.layout_controls.layout_controls import (
        LayoutControls,
    )


class DefaultLayoutLabel(QLabel):
    def __init__(self, control_widget: "LayoutControls"):
        super().__init__(control_widget)

        current_layout = control_widget.layout_tab.beat_frame.current_layout
        self.setText(
            f"Default: {current_layout[0]} x {current_layout[1]}",
        )
        self.control_widget = control_widget
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.font()
        font.setBold(True)
        self.setFont(font)

    def resizeEvent(self, event):
        font = self.font()
        font.setPointSize(self.control_widget.layout_tab.width() // 50)
        self.setFont(font)

    def update_text(self, layout_text: str):
        """Update label text programmatically"""
        self.setText(f"Default: {layout_text}")
        self.setFont(self.font())  # Trigger font update
