from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt


class NavButton(QPushButton):
    DEFAULT_BG_COLOR = "lightgray"
    ACTIVE_BG_GRADIENT = """
        background: qlineargradient(
            spread:pad, x1:0, y1:0, x2:1, y2:1,
            stop:0 #1e3c72,
            stop:0.3 #6c9ce9,
            stop:0.6 #4a77d4,
            stop:1 #2a52be
        );
    """
    HOVER_GRADIENT = """
        background: qlineargradient(
            spread:pad, x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(200, 200, 200, 1),
            stop:0.5 rgba(175, 175, 175, 1),
            stop:1 rgba(150, 150, 150, 1)
        );
    """
    DEFAULT_BG_GRADIENT = """
        background: qlineargradient(
            spread:pad, x1:0, y1:0, x2:1, y2:1,
            stop:0 #f0f0f0,
            stop:0.5 #d0d0d0,
            stop:1 #f0f0f0
        );
    """

    def __init__(self, label: str):
        super().__init__(label)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._radius = 0
        self._is_active = False

        self._update_style()

    def _update_style(self, custom_bg: str = None, force_active: bool = False):
        if self._is_active or force_active:
            bg_style = self.ACTIVE_BG_GRADIENT
            text_color = "white"
        else:
            bg_color = custom_bg or self.DEFAULT_BG_COLOR
            bg_style = self.DEFAULT_BG_GRADIENT
            text_color = "black"

        self.setStyleSheet(
            f"""
            QPushButton {{
                {bg_style}
                border: 2px solid black;
                color: {text_color};
                padding: 5px;
                border-radius: {self._radius}px;
            }}
            QPushButton:hover {{
                {"/* Disabled when active */" if self._is_active else self.HOVER_GRADIENT}
            }}
            QPushButton:pressed {{
                background-color: #d0d0d0;
            }}
            """
        )

    def enterEvent(self, event):
        if not self._is_active:
            self._update_style()

    def leaveEvent(self, event):
        if not self._is_active:
            self._update_style()

    def mousePressEvent(self, event):
        if not self._is_active:
            self._update_style(custom_bg="#aaaaaa")
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if not self._is_active:
            self._update_style()
        super().mouseReleaseEvent(event)

    def set_active(self, active: bool):
        self._is_active = active
        self._update_style()

    def set_rounded_button_style(self, radius: int):
        self._radius = radius
        self._update_style()
