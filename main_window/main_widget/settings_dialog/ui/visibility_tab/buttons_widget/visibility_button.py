from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from styles.dark_theme_styler import DarkThemeStyler
if TYPE_CHECKING:
    from .visibility_buttons_widget import VisibilityButtonsWidget


class VisibilityButton(QPushButton):
    """A visibility toggle button styled with modern effects."""

    def __init__(self, name: str, visibility_buttons_widget: "VisibilityButtonsWidget"):
        super().__init__(name)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.visibility_buttons_widget = visibility_buttons_widget
        self.name = name
        self.is_toggled = False  # Track active state

        self.clicked.connect(self._toggle_state)

        # 🔥 Ensure the button starts with the correct style

    def _initialize_state(self):
        """Retrieve toggle state and apply styles on initialization."""
        self.update_is_toggled(self.name)
        self.repaint()  # Ensure UI updates immediately

    def update_is_toggled(self, name: str):
        """Updates the button state based on saved settings."""
        is_toggled = (
            self.visibility_buttons_widget.visibility_tab.settings.get_glyph_visibility(
                name
            )
        )
        self.is_toggled = is_toggled
        self._apply_style(self.is_toggled)  # Apply correct styles on init

    def _toggle_state(self):
        """Handle button toggle state with parallel fading."""
        self.is_toggled = not self.is_toggled
        view = self.visibility_buttons_widget.visibility_tab.pictograph_view

        if self.name in self.visibility_buttons_widget.glyph_names:
            element = view.pictograph.managers.get.glyph(self.name)
        else:
            element = view.pictograph.managers.get.non_radial_points()

        # Create a parallel fade animation
        view.interaction_manager.fade_and_toggle_visibility(element, self.is_toggled)
        self._apply_style(self.is_toggled)  # Update button style

    def set_active(self, is_active: bool):
        """Updates the button style when toggled."""
        self.is_toggled = is_active
        self._apply_style(is_active)

    def _apply_style(self, is_active=False):
        """Applies styling dynamically based on active state."""
        if is_active:
            self.setStyleSheet(
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
        self.update()  # Ensure the UI updates
        self.repaint()  # Force an immediate refresh

    def resizeEvent(self, event):
        """Dynamically adjust button size without affecting layout."""
        super().resizeEvent(event)
        # Calculate font size based on the visibility_tab's width
        tab_width = self.visibility_buttons_widget.visibility_tab.width()
        font_size = int(tab_width / 40)  # Adjust divisor as needed
        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)
