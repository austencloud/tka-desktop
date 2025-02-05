# orientation_label.py
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class OrientationTextLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__("Orientation", parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resize_orientation_label(self, parent_width):
        font_size = parent_width // 60
        font = QFont("Cambria", font_size, QFont.Weight.Bold)
        font.setUnderline(True)
        self.setFont(font)
