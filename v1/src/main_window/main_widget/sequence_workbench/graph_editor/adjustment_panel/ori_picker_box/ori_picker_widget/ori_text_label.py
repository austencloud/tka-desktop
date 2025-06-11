# orientation_text_label.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.ori_picker_box.ori_picker_widget.ori_picker_widget import (
        OriPickerWidget,
    )


class OrientationTextLabel(QLabel):
    def __init__(self, ori_picker_widget: "OriPickerWidget"):
        super().__init__("Orientation", ori_picker_widget)
        self.ori_picker_widget = ori_picker_widget
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resizeEvent(self, event):
        font_size = int(
            self.ori_picker_widget.ori_picker_box.graph_editor.width() // 60
        )
        font = QFont("Cambria", font_size, QFont.Weight.Bold)
        font.setUnderline(True)
        self.setFont(font)
        super().resizeEvent(event)
