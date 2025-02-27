from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from functools import partial


if TYPE_CHECKING:
    from .learn_tab import LearnTab


class LessonSelectorButton(QPushButton):
    def __init__(self, label: str):
        super().__init__(label)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._radius = 0
        self._default_stylesheet = """
            QPushButton {
                border: 2px solid black;
            }
            QPushButton:hover {
                background-color: lightgray; 
            }
        """
        self.setStyleSheet(self._default_stylesheet)
        self._base_background_color = "lightgray"

    def _update_style(self, background_color: str = None, shadow: bool = False):
        background_color = background_color or self._base_background_color

        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {background_color};
                border: 2px solid black;
                color: black;
                padding: 5px;
                border-radius: {self._radius}px;
            }}
            QPushButton:hover {{
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(200, 200, 200, 1),
                    stop:1 rgba(150, 150, 150, 1)
                );
            }}
            QPushButton:pressed {{
                background-color: #d0d0d0;
            }}
        """
        )

    def enterEvent(self, event):
        self._update_style(shadow=True)

    def leaveEvent(self, event):
        self._update_style(shadow=False)

    def set_rounded_button_style(self, radius: int):
        self._radius = radius
        self._update_style()

    def mousePressEvent(self, event):
        self._update_style(background_color="#aaaaaa")
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._update_style()
        super().mouseReleaseEvent(event)
