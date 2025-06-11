# src/main_window/main_widget/sequence_card_tab/components/navigation/sidebar.py
from PyQt6.QtWidgets import (
    QLabel,
    QFrame,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QFont, QColor


class LengthOptionFrame(QFrame):
    length_clicked = pyqtSignal(int)

    def __init__(self, length: int, custom_text: str = None):
        super().__init__()
        self.length = length
        self.setObjectName(f"lengthFrame_{length}")
        self.setMinimumHeight(45)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setup_ui(custom_text)
        self.add_shadow_effect()

    def setup_ui(self, custom_text: str = None):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        text = custom_text or str(self.length)
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("lengthLabel")

        font = QFont()
        font.setPointSize(14)
        font.setWeight(QFont.Weight.Medium)
        self.label.setFont(font)

        layout.addWidget(self.label)

    def add_shadow_effect(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

    def mousePressEvent(self, event):
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.2);")
        self.length_clicked.emit(self.length)

    def enterEvent(self, event):
        shadow = self.graphicsEffect()
        if shadow:
            shadow.setBlurRadius(15)
            shadow.setOffset(0, 3)

    def leaveEvent(self, event):
        shadow = self.graphicsEffect()
        if shadow:
            shadow.setBlurRadius(10)
            shadow.setOffset(0, 2)
        self.setStyleSheet("")

    def set_selected(self, selected: bool):
        if selected:
            self.setObjectName(f"lengthFrame_{self.length}_selected")
        else:
            self.setObjectName(f"lengthFrame_{self.length}")
