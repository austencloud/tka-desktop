from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from styles.button_state import ButtonState
from styles.dark_theme_styler import DarkThemeStyler
from styles.styled_button import StyledButton

if TYPE_CHECKING:
    from .visibility_buttons_widget import VisibilityButtonsWidget


class VisibilityButton(StyledButton):

    def __init__(self, name: str, visibility_buttons_widget: "VisibilityButtonsWidget"):
        super().__init__(name)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.visibility_buttons_widget = visibility_buttons_widget
        self.name = name
        self.is_toggled = False

        self.clicked.connect(self._toggle_state)
        self._initialize_state()

    def _initialize_state(self):
        self.update_is_toggled(self.name)
        self.repaint()

    def update_is_toggled(self, name: str):
        settings = self.visibility_buttons_widget.visibility_tab.settings
        
        if name in ["Red Motion", "Blue Motion"]:
            color = name.split(" ")[0].lower()
            is_toggled = settings.get_motion_visibility(color)
        elif name in self.visibility_buttons_widget.glyph_names:
            # Use real state for glyph buttons to show user's intent
            is_toggled = settings.get_real_glyph_visibility(name)
        else:
            # Non-radial points
            is_toggled = settings.get_non_radial_visibility()
        
        self.is_toggled = is_toggled
        self.state = ButtonState.ACTIVE if is_toggled else ButtonState.NORMAL
        self.update_appearance()

    def _toggle_state(self):
        self.is_toggled = not self.is_toggled
        view = self.visibility_buttons_widget.visibility_tab.pictograph_view
        settings = self.visibility_buttons_widget.visibility_tab.settings
        toggler = self.visibility_buttons_widget.visibility_tab.toggler

        if self.name in ["Red Motion", "Blue Motion"]:
            color = self.name.split(" ")[0].lower()
            # Toggle motion visibility and update dependent elements
            toggler.toggle_prop_visibility(color, self.is_toggled)
            # No need to call fade_and_toggle_visibility here as it's done in toggle_prop_visibility
        
        elif self.name in ["TKA", "VTG", "Elemental"]:
            # For elements that depend on motion visibility:
            # 1. Update the real state (user's intent)
            settings.set_real_glyph_visibility(self.name, self.is_toggled)
            
            # 2. Calculate the actual visible state based on motion visibility
            actual_visibility = self.is_toggled and settings.are_all_motions_visible()
            
            # 3. Update the actual visibility
            toggler.toggle_glyph_visibility(self.name, self.is_toggled)
            
            # 4. Update button appearance based on actual visibility
            self.set_active(actual_visibility)
        
        elif self.name in self.visibility_buttons_widget.glyph_names:
            # For non-dependent glyphs
            toggler.toggle_glyph_visibility(self.name, self.is_toggled)
            self.set_active(self.is_toggled)
        
        else:
            # For non-radial points
            toggler.toggle_non_radial_points(self.is_toggled)
            self.set_active(self.is_toggled)

    def set_active(self, is_active: bool):
        self.is_toggled = is_active
        self.state = ButtonState.ACTIVE if is_active else ButtonState.NORMAL
        self.update_appearance()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        tab_width = self.visibility_buttons_widget.visibility_tab.width()
        font_size = int(tab_width / 40)
        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)
