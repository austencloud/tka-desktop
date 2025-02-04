from typing import TYPE_CHECKING
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor

if TYPE_CHECKING:
    from .visibility_button import VisibilityButton


class VisibilityButtonAnimation:
    def __init__(self, button: "VisibilityButton"):
        self.button = button

        # Background color animation
        self.background_animation = QPropertyAnimation(button, b"background_color")
        self.background_animation.setDuration(300)
        self.background_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # Text color animation
        self.text_animation = QPropertyAnimation(button, b"text_color")
        self.text_animation.setDuration(300)
        self.text_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def play_toggle_animation(self, is_toggled: bool):
        """Play the toggle animation for both background and text colors."""
        self.background_animation.stop()
        self.text_animation.stop()

        self.background_animation.setStartValue(self.button.background_color)
        self.background_animation.setEndValue(
            QColor("#4CAF50") if is_toggled else QColor("#F5F5F5")
        )

        self.text_animation.setStartValue(self.button.text_color)
        self.text_animation.setEndValue(
            QColor("#FFFFFF") if is_toggled else QColor("#000000")
        )

        self.background_animation.start()
        self.text_animation.start()
