from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

from utils.path_helpers import get_image_path


class WorkbenchButton(QPushButton):
    def __init__(self, icon_path: str, tooltip: str, callback, button_size: int):
        super().__init__()
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(tooltip)
        self.clicked.connect(callback)

        self._base_background_color = "white"
        self._icon_path = icon_path
        self._button_size = button_size

        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(int(button_size * 0.8), int(button_size * 0.8)))

        self._update_style()

    def _update_style(self, background_color: str = None):
        background_color = background_color or self._base_background_color

        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {background_color};
                border: 2px solid black;
                border-radius: {self._button_size // 2}px;
                padding: 5px;
            }}
            QPushButton:hover {{
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(240, 240, 240, 1),
                    stop:1 rgba(200, 200, 200, 1)
                );
            }}
            QPushButton:pressed {{
                background-color: #d0d0d0;
            }}
        """
        )

    def enterEvent(self, event):
        self._update_style()

    def leaveEvent(self, event):
        self._update_style()

    def mousePressEvent(self, event):
        self._update_style(background_color="#bbbbbb")
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._update_style()
        super().mouseReleaseEvent(event)

    def update_size(self, button_size: int):
        self._button_size = button_size
        self.setFixedSize(button_size, button_size)
        self.setIconSize(QSize(int(button_size * 0.75), int(button_size * 0.75)))
        self._update_style()
