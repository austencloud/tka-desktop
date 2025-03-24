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
        state_manager = self.visibility_buttons_widget.visibility_tab.state_manager
        
        if self.name in ["Red Motion", "Blue Motion"]:
            color = self.name.split(" ")[0].lower()
            current_state = state_manager.get_motion_visibility(color)
            
            # Use state manager, which will handle the button update through notification
            state_manager.set_motion_visibility(color, not current_state)
            
            # Also update all other pictographs
            toggler = self.visibility_buttons_widget.visibility_tab.toggler
            toggler.toggle_prop_visibility(color, not current_state)
        
        # Rest of the method remains the same...

    def _update_dependent_button_visibility(self):
        """Update visibility of dependent buttons based on motion states"""
        settings = self.visibility_buttons_widget.visibility_tab.settings
        all_motions_visible = settings.are_all_motions_visible()

        # Get all non-motion buttons
        dependent_buttons = [
            button
            for name, button in self.visibility_buttons_widget.glyph_buttons.items()
            if name not in ["Red Motion", "Blue Motion"]
        ]

        # Show/hide buttons based on motion visibility
        for button in dependent_buttons:
            if button.name in ["TKA", "VTG", "Elemental", "Positions"]:
                # These are motion dependent buttons - only show when both motions visible
                button.setVisible(all_motions_visible)

                # If visible, update active state based on user intent
                if all_motions_visible:
                    user_intent = settings.get_user_intent_visibility(button.name)
                    button.set_active(user_intent)

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
