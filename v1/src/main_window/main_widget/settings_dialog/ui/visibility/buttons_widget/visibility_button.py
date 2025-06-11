from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from styles.button_state import ButtonState
from styles.styled_button import StyledButton

if TYPE_CHECKING:
    from .visibility_buttons_widget import VisibilityButtonsWidget


class VisibilityButton(StyledButton):
    """Button for toggling visibility with improved feedback for dependent glyphs."""

    def __init__(self, name: str, visibility_buttons_widget: "VisibilityButtonsWidget"):
        super().__init__(name)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.visibility_buttons_widget = visibility_buttons_widget
        self.name = name
        self.is_toggled = False
        self.is_dependent = name in ["TKA", "VTG", "Elemental", "Positions"]

        self.clicked.connect(self._toggle_state)
        self._initialize_state()

        # Set tooltips based on button type
        if self.is_dependent:
            self.setToolTip("Requires both red and blue motions to be visible")
        elif name in ["Red Motion", "Blue Motion"]:
            self.setToolTip(
                "Toggle motion visibility. At least one motion must remain visible."
            )
        elif name == "Non-radial_points":
            self.setToolTip("Toggle visibility of non-radial grid points")
        else:
            self.setToolTip(f"Toggle {name} visibility")

    def _initialize_state(self):
        """Initialize button state from settings."""
        self.update_is_toggled()
        self.repaint()

    def update_is_toggled(self):
        """Update the visual state based on current settings."""
        settings = self.visibility_buttons_widget.visibility_tab.settings

        if self.name in ["Red Motion", "Blue Motion"]:
            color = self.name.split(" ")[0].lower()
            is_toggled = settings.get_motion_visibility(color)
        elif self.name in self.visibility_buttons_widget.glyph_names:
            is_toggled = settings.get_glyph_visibility(self.name)
        else:
            # Non-radial points
            is_toggled = settings.get_non_radial_visibility()

        self.is_toggled = is_toggled
        self.state = ButtonState.ACTIVE if is_toggled else ButtonState.NORMAL

        # If this is a dependent button, check if it should be disabled
        if self.is_dependent:
            all_motions_visible = settings.are_all_motions_visible()
            self.setEnabled(all_motions_visible)
            if not all_motions_visible:
                self.state = ButtonState.DISABLED

        self.update_appearance()

    def _toggle_state(self):
        """Handle button click to toggle visibility state."""
        state_manager = self.visibility_buttons_widget.visibility_tab.state_manager
        toggler = self.visibility_buttons_widget.visibility_tab.toggler

        if self.name in ["Red Motion", "Blue Motion"]:
            color = self.name.split(" ")[0].lower()
            current_state = state_manager.get_motion_visibility(color)

            # Update state manager and toggler
            state_manager.set_motion_visibility(color, not current_state)
            toggler.toggle_prop_visibility(color, not current_state)

            # The state_manager will handle the case where both motions can't be off

        elif self.name in self.visibility_buttons_widget.glyph_names:
            # For glyph buttons
            current_state = state_manager.get_glyph_visibility(self.name)
            new_state = not current_state

            # Update state manager
            state_manager.set_glyph_visibility(self.name, new_state)

            # Update all other pictographs
            toggler.toggle_glyph_visibility(self.name, new_state)

        else:  # Non-radial points
            current_state = state_manager.get_non_radial_visibility()
            new_state = not current_state

            # Update state manager
            state_manager.set_non_radial_visibility(new_state)

            # Update all other pictographs
            toggler.toggle_non_radial_points(new_state)

        # Force update to visibility pictograph
        pictograph = self.visibility_buttons_widget.visibility_tab.pictograph
        pictograph._update_from_state_manager()

        # Update all button states
        self.visibility_buttons_widget.update_button_flags()

    def set_active(self, is_active: bool):
        """Set the active state of the button."""
        self.is_toggled = is_active
        self.state = ButtonState.ACTIVE if is_active else ButtonState.NORMAL

        # If this is a dependent button, check if it should be disabled
        if self.is_dependent:
            all_motions_visible = (
                self.visibility_buttons_widget.visibility_tab.settings.are_all_motions_visible()
            )
            self.setEnabled(all_motions_visible)
            if not all_motions_visible:
                self.state = ButtonState.DISABLED

        self.update_appearance()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        tab_width = self.visibility_buttons_widget.visibility_tab.width()
        font_size = int(tab_width / 40)
        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)
