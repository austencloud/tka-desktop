from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .splash_screen import SplashScreen


class SplashProperties:
    """Handles window properties like flags, transparency, and size."""

    def __init__(self, splash_screen: "SplashScreen"):
        self.splash_screen = splash_screen
        self.target_screen = splash_screen.target_screen
        self._setup_window_properties()

    def _setup_window_properties(self):
        screen_geometry = self.target_screen.geometry()
        width = int(screen_geometry.width() // 2.5)
        height = int(screen_geometry.height() // 2.5)

        self.splash_screen.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint
        )
        self.splash_screen.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground, False
        )
        self.splash_screen.setFixedSize(width, height)
