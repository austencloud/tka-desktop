from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, QFrame, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from typing import TYPE_CHECKING, Union

from data.constants import BLUE, RED

if TYPE_CHECKING:
    from .ori_picker_box.ori_picker_box import OriPickerBox
    from .turns_box.turns_box import TurnsBox


class BaseAdjustmentBoxHeaderWidget(QWidget):
    def __init__(self, adjustment_box: Union["OriPickerBox", "TurnsBox"]) -> None:
        super().__init__(adjustment_box)
        self.adjustment_box = adjustment_box
        self.graph_editor = self.adjustment_box.graph_editor
        self.separator: QFrame = self.create_separator()
        self.header_label: QLabel = self._setup_header_label()
        self.layout: QVBoxLayout = self._setup_layout()

    def _setup_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout(self)
        self.top_hbox = QHBoxLayout()
        self.separator_hbox = QHBoxLayout()
        layout.addLayout(self.top_hbox)
        layout.addLayout(self.separator_hbox)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        return layout

    def create_separator(self) -> QFrame:
        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Raised)
        separator.setStyleSheet("color: #000000;")
        return separator

    def _setup_header_label(self) -> QLabel:
        header_label = QLabel(self)
        color = self.adjustment_box.color
        text, font_color = self._get_label_text_and_color(color)

        self.header_label_font = QFont("Georgia")
        self.header_label_font.setBold(True)
        header_label.setFont(self.header_label_font)
        header_label.setText(text)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet(f"color: {font_color.name()};")
        return header_label

    def _get_label_text_and_color(self, color: str) -> tuple[str, QColor]:
        if color == RED:
            return "Right", QColor("#ED1C24")
        elif color == BLUE:
            return "Left", QColor("#2E3192")
        else:
            return "", QColor("#000000")

    def resizeEvent(self, event) -> None:
        self.setFixedHeight(self.adjustment_box.graph_editor.height() // 4)

        font_size = self.graph_editor.sequence_workbench.main_widget.width() // 80
        self.header_label_font.setPointSize(font_size)
        self.header_label.setFont(self.header_label_font)
        self.header_label.repaint()

        super().resizeEvent(event)
