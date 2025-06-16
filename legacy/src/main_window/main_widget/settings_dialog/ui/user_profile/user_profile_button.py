from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor

from styles.dark_theme_styler import DarkThemeStyler


class UserProfileButton(QWidget):
    """A widget containing a user button and a remove button."""

    def __init__(self, user_name: str, parent: QWidget, is_current: bool = False):
        super().__init__(parent)
        self.user_name = user_name
        self.button = QPushButton(user_name, self)
        self.remove_button = QPushButton("❌", self)
        self._is_current = is_current
        self._setup_ui()

    def _setup_ui(self):
        """Sets up the UI for the user profile button with dark mode styles."""
        self.button.setFont(self._get_scaled_font())
        self.button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.apply_style(self._is_current)

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

    def apply_style(self, is_current: bool):
        """Applies the button style."""
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
        self.button.update()
        self.button.repaint()
