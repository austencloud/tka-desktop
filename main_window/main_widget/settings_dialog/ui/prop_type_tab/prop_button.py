from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import Qt, QSize
from Enums.PropTypes import PropType
from styles.dark_theme_styler import DarkThemeStyler

if TYPE_CHECKING:
    from .prop_type_tab import PropTypeTab


class PropButton(QPushButton):
    """A button representing a prop type, styled with dark mode and hover animations."""

    def __init__(
        self, prop: str, icon_path: str, prop_type_tab: "PropTypeTab", callback
    ):
        super().__init__(prop_type_tab)
        self.prop_type_tab = prop_type_tab
        self.prop = prop
        self.setIcon(QIcon(icon_path))
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clicked.connect(lambda: callback(PropType.get_prop_type(prop)))

        self._is_active = False

    def set_active(self, is_active: bool):
        """Updates the button's active state and applies styling accordingly."""
        self._is_active = is_active
        self.set_button_style(is_active)

    def set_button_style(self, is_active=False):
        """Set the button style dynamically based on whether it's active."""
        if is_active:
            self.setStyleSheet(
                f"""
                QPushButton {{
                    {DarkThemeStyler.ACTIVE_BG_GRADIENT}
                    border: 2px solid {DarkThemeStyler.ACCENT_COLOR};
                    color: white;
                    padding: 8px 12px;
                    border-radius: 8px;
                }}
                QPushButton:hover {{
                    {DarkThemeStyler.ACTIVE_BG_GRADIENT} 
                }}
                QPushButton:pressed {{
                    background-color: {DarkThemeStyler.BORDER_COLOR};
                }}
            """
            )
        else:
            self.setStyleSheet(
                f"""
                QPushButton {{
                    {DarkThemeStyler.DEFAULT_BG_GRADIENT}
                    border: 2px solid {DarkThemeStyler.BORDER_COLOR};
                    color: {DarkThemeStyler.TEXT_COLOR};
                    padding: 8px 12px;
                    border-radius: 8px;
                }}
                QPushButton:hover {{
                    {DarkThemeStyler.DARK_HOVER_GRADIENT}
                }}
                QPushButton:pressed {{
                    background-color: {DarkThemeStyler.BORDER_COLOR};
                }}
            """
            )

        self.update()
        self.repaint()

    def resizeEvent(self, event):
        """Resize the button and its icon dynamically."""
        size = self.prop_type_tab.width() // 4
        icon_size = int(size * 0.75)
        self.setFixedSize(QSize(size, size))
        self.setIconSize(QSize(icon_size, icon_size))
        super().resizeEvent(event)
