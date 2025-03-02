from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont


class IncrementAdjusterButton(QPushButton):
    """A custom perfectly round button with hover effects and dynamic styling."""

    def __init__(self, symbol: str, parent=None):
        super().__init__(symbol, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(
            self.sizePolicy().Policy.Fixed, self.sizePolicy().Policy.Fixed
        )
        # Made the button slightly smaller:
        self.setFixedSize(35, 35)
        # Made font inside bigger:
        self.setFont(QFont("Georgia", 18, QFont.Weight.Bold))
        self._update_style()

    def enterEvent(self, event):
        self.setStyleSheet(self._get_hover_style())

    def leaveEvent(self, event):
        self._update_style()

    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        self.setFixedSize(QSize(size, size))
        self._update_style()

    def _update_style(self):
        radius = self.width() // 2
        self.setStyleSheet(self._get_style(radius))

    def _get_style(self, radius):
        return f"""
            QPushButton {{
                background-color: #2E2E2E;
                border: 2px solid #AAAAAA;
                color: white;
                font-weight: bold;
                border-radius: {radius}px;
            }}
            QPushButton:pressed {{
                background-color: #555555;
                border: 2px solid #DDDDDD;
            }}
        """

    def _get_hover_style(self):
        radius = self.width() // 2
        return f"""
            QPushButton {{
                background-color: #444444;
                border: 2px solid #FFFFFF;
                color: white;
                font-weight: bold;
                border-radius: {radius}px;
            }}
        """
