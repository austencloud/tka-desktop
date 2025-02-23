from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont, QCursor, QColor

from main_window.main_widget.settings_dialog.styles.dark_theme_styler import (
    DarkThemeStyler,
)

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class UserProfileButton(QWidget):
    """A widget containing a user button and a remove button, with smooth transitions."""

    def __init__(self, user_name: str, parent: QWidget, is_current: bool = False):
        super().__init__(parent)
        self.user_name = user_name
        self.button = QPushButton(user_name, self)
        self.remove_button = QPushButton("❌", self)
        self._is_current = is_current
        self._opacity = 1.0  # Track fade effect
        self._setup_ui()

        # Fade Animation
        self.animation = QPropertyAnimation(self, b"opacity")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def _setup_ui(self):
        """Sets up the UI for the user profile button with dark mode styles."""
        self.button.setFont(self._get_scaled_font())
        self.button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.set_button_style(self._is_current)

        # Remove Button (styled for better contrast)
        self.remove_button.setFixedSize(30, 30)
        self.remove_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.remove_button.setStyleSheet(
            """
            QPushButton {
                background: none;
                color: #FF4C4C;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                color: #FF9999;
            }
            QPushButton:pressed {
                color: #CC0000;
            }
        """
        )

        # Layout
        user_layout = QHBoxLayout()
        user_layout.addWidget(self.button)
        user_layout.addWidget(self.remove_button)
        user_layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(user_layout)

    def _get_scaled_font(self) -> QFont:
        """Returns a dynamically scaled font for user buttons."""
        font = QFont()
        font_size = max(
            10, self.parentWidget().width() // 30 if self.parentWidget() else 10
        )
        font.setPointSize(font_size)
        return font

    def set_button_style(self, is_current: bool, animate: bool = True):
        """Updates the button style with a smooth transition."""
        if self._is_current == is_current:
            return  # No need to change style if already selected

        self._is_current = is_current

        if animate:
            self.animation.stop()
            self.animation.setStartValue(1.0 if is_current else 0.0)
            self.animation.setEndValue(0.0 if is_current else 1.0)
            self.animation.start()
            self.animation.finished.connect(lambda: self._apply_style(is_current))
        else:
            self._apply_style(is_current)

    def _apply_style(self, is_current: bool):
        """Applies the button style after the fade effect."""
        if is_current:
            self.button.setStyleSheet(
                f"""
                QPushButton {{
                    {DarkThemeStyler.ACTIVE_BG_GRADIENT}
                    border: 2px solid {DarkThemeStyler.ACCENT_COLOR};
                    color: white;
                    padding: 8px 12px;
                    border-radius: 8px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    {DarkThemeStyler.ACTIVE_BG_GRADIENT} /* Keep selected effect even on hover */
                }}
                QPushButton:pressed {{
                    background-color: {DarkThemeStyler.BORDER_COLOR};
                }}
            """
            )
        else:
            self.button.setStyleSheet(
                f"""
                QPushButton {{
                    {DarkThemeStyler.DEFAULT_BG_GRADIENT}
                    border: 2px solid {DarkThemeStyler.BORDER_COLOR};
                    color: {DarkThemeStyler.TEXT_COLOR};
                    padding: 8px 12px;
                    border-radius: 8px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    {DarkThemeStyler.DARK_HOVER_GRADIENT}
                }}
                QPushButton:pressed {{
                    background-color: {DarkThemeStyler.BORDER_COLOR};
                }}
            """
            )

    # Fade effect property
    def get_opacity(self):
        return self._opacity

    def set_opacity(self, value):
        self._opacity = value
        self.setWindowOpacity(value)

    opacity = pyqtProperty(float, get_opacity, set_opacity)
