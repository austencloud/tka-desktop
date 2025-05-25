from PyQt6.QtWidgets import QWidget, QGridLayout
from .visibility_button import VisibilityButton
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..visibility_tab import VisibilityTab


class VisibilityButtonsWidget(QWidget):
    """A widget for arranging and managing visibility buttons."""

    glyph_buttons: dict[str, VisibilityButton] = {}
    non_radial_button: VisibilityButton = None
    glyph_names = [
        "TKA",
        "Reversals",
        "VTG",
        "Elemental",
        "Positions",
        "Red Motion",
        "Blue Motion",
    ]
    dependent_glyphs = ["TKA", "VTG", "Elemental", "Positions"]
    grid_name = "Non-radial_points"

    def __init__(self, visibility_tab: "VisibilityTab"):
        super().__init__()
        self.visibility_tab = visibility_tab
        self._create_buttons()
        self._setup_layout()
        self.update_button_flags()

        # Register for state updates
        self.visibility_tab.state_manager.register_observer(
            self.update_button_flags, ["buttons", "motion", "glyph"]
        )
        self.visibility_tab.state_manager.register_observer(
            self._update_button_visibility, ["motion"]
        )

    def _create_buttons(self):
        """Creates all buttons for toggling visibility."""
        for name in self.glyph_names:
            button = VisibilityButton(name, self)
            self.glyph_buttons[name] = button

        self.non_radial_button = VisibilityButton(self.grid_name, self)

    def _setup_layout(self):
        """Sets up the initial grid layout for the buttons."""
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(10)

        # Initial setup of the grid - will be updated by _update_button_visibility
        self._update_button_visibility()

        self.setLayout(self.grid_layout)

    def _update_button_visibility(self):
        """
        Updates button visibility based on motion state and
        arranges visible buttons in an appealing layout.
        """
        # Check if all motions are visible
        try:
            settings_manager = (
                self.visibility_tab.main_widget.app_context.settings_manager
            )
            settings = settings_manager.visibility
            all_motions_visible = settings.are_all_motions_visible()
        except AttributeError:
            # Fallback when settings not available
            all_motions_visible = True

        # Set visibility for each button type
        # 1. Dependent glyphs: only visible when all motions are visible
        for name in self.dependent_glyphs:
            if name in self.glyph_buttons:
                self.glyph_buttons[name].setVisible(all_motions_visible)

        # 2. Always-visible buttons: Reversals and Non-radial points
        if "Reversals" in self.glyph_buttons:
            self.glyph_buttons["Reversals"].setVisible(True)

        if self.non_radial_button:
            self.non_radial_button.setVisible(True)

        # Clear the current grid layout without deleting widgets
        while self.grid_layout.count():
            self.grid_layout.takeAt(0)

        # Get the list of all visible buttons (excluding motion buttons)
        visible_buttons = []
        for name, button in self.glyph_buttons.items():
            if name not in ["Red Motion", "Blue Motion"] and button.isVisible():
                visible_buttons.append(button)

        # Add the non-radial button
        if self.non_radial_button:
            visible_buttons.append(self.non_radial_button)

        # Arrange visible buttons in the grid
        # If we have exactly 2 buttons (Reversals and Non-radial), place them side by side
        if len(visible_buttons) == 2:
            for i, button in enumerate(visible_buttons):
                self.grid_layout.addWidget(button, 0, i)
        # Otherwise use a grid with 3 buttons per row (default layout)
        else:
            for i, button in enumerate(visible_buttons):
                row = i // 3
                col = i % 3
                self.grid_layout.addWidget(button, row, col)

        # Update the widget
        self.update()

    def update_button_flags(self):
        """Ensure buttons correctly reflect saved settings."""
        try:
            settings_manager = (
                self.visibility_tab.main_widget.app_context.settings_manager
            )
            settings = settings_manager.visibility
        except AttributeError:
            # Fallback when settings not available
            return

        for name, button in self.glyph_buttons.items():
            if name in ["Red Motion", "Blue Motion"]:
                color = name.split(" ")[0].lower()
                is_active = settings.get_motion_visibility(color)
            else:
                is_active = settings.get_glyph_visibility(name)
            button.set_active(is_active)

        if self.non_radial_button:
            is_active = settings.get_non_radial_visibility()
            self.non_radial_button.set_active(is_active)

    def update_visibility_buttons_from_settings(self):
        """Update all visibility buttons based on saved settings."""
        try:
            settings_manager = (
                self.visibility_tab.main_widget.app_context.settings_manager
            )
            visibility_settings = settings_manager.visibility
        except AttributeError:
            # Fallback when settings not available
            return

        for button in self.glyph_buttons.values():
            if button.name in ["Red Motion", "Blue Motion"]:
                color = button.name.split(" ")[0].lower()
                button.is_toggled = visibility_settings.get_motion_visibility(color)
            else:
                button.update_is_toggled()

        if self.non_radial_button:
            self.non_radial_button.update_is_toggled()
