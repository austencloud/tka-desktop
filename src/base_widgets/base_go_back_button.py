from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton, QSizePolicy
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class BaseGoBackButton(QPushButton):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__("Back")
        self.main_widget = main_widget
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def resizeEvent(self, event):
        self.setFixedHeight(self.main_widget.height() // 20)
        self.setFixedWidth(self.main_widget.width() // 20)
        font = self.font()
        font.setPointSize(self.main_widget.width() // 100)
        self.setFont(font)
        super().resizeEvent(event)
