from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QFontMetrics
from data.constants import BLUE, HEX_BLUE, HEX_RED

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.ori_picker_box.ori_picker_widget.ori_selection_dialog import (
        OriSelectionDialog,
    )


class OriButton(QPushButton):
    def __init__(self, orientation: str, ori_selection_dialog: "OriSelectionDialog"):
        super().__init__(orientation)
        self.orientation = orientation
        self.ori_selection_dialog = ori_selection_dialog
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ori_picker_widget = ori_selection_dialog.ori_picker_widget

    def resize_buttons(self):
        """Resize buttons according to the orientation label's size."""
        ori_label_width = self.ori_picker_widget.clickable_ori_label.width()
        button_height = int(self.ori_picker_widget.ori_picker_box.height() // 3)
        font_size = int(button_height * 0.5)  # Font size based on button height

        font = QFont("Arial", font_size, QFont.Weight.Bold)
        font_metrics = QFontMetrics(font)

        self.setFont(font)

        # Calculate button width based on text length
        text_width = font_metrics.horizontalAdvance(self.orientation)
        button_width = max(text_width + 40, ori_label_width // 2)  # Add padding
        border_width = button_height // 20
        self.setFixedSize(QSize(button_width, button_height))
        self.setStyleSheet(
            f"""
            QPushButton {{
                border: {border_width}px solid {HEX_BLUE if self.ori_picker_widget.color == BLUE else HEX_RED};
                border-radius: {button_height // 2}px;
                background-color: #ffffff;
            }}
            QPushButton:hover {{
                background-color: #f0f0f0;
            }}
            """
        )

    def resizeEvent(self, event):
        self.resize_buttons()
        super().resizeEvent(event)
