from PyQt6.QtWidgets import QWidget, QGridLayout
from .visibility_button import VisibilityButton
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..visibility_tab import VisibilityTab


class VisibilityButtonsWidget(QWidget):
    """A widget for arranging and managing visibility buttons."""

    glyph_buttons: dict[str, VisibilityButton] = {}
    non_radial_button: VisibilityButton = None
    glyph_names = ["TKA", "Reversals", "VTG", "Elemental", "Positions"]
    grid_name = "Non-radial_points"

    def __init__(self, visibility_tab: "VisibilityTab"):
        super().__init__()
        self.visibility_tab = visibility_tab
        self._create_buttons()
        self._setup_layout()
        self.update_button_flags()

    def _create_buttons(self):
        """Creates all buttons for toggling visibility."""
        for name in self.glyph_names:
            button = VisibilityButton(name, self)
            self.glyph_buttons[name] = button

        self.non_radial_button = VisibilityButton(self.grid_name, self)

    def _setup_layout(self):
        """Organizes the buttons in a grid layout."""
        grid_layout = QGridLayout(self)
        grid_layout.setSpacing(10)

        button_list = list(self.glyph_buttons.values()) + [self.non_radial_button]

        for i, button in enumerate(button_list):
            row = i // 3  # 3 buttons per row
            col = i % 3
            grid_layout.addWidget(button, row, col)

        self.setLayout(grid_layout)

    def update_button_flags(self):
        """Ensure buttons correctly reflect saved settings."""
        settings = self.visibility_tab.main_widget.settings_manager.visibility

        for name, button in self.glyph_buttons.items():
            is_active = settings.get_glyph_visibility(name)
            button.set_active(is_active)

        if self.non_radial_button:
            is_active = settings.get_non_radial_visibility()
            self.non_radial_button.set_active(is_active)

    def update_visibility_buttons_from_settings(self):
        """Update all visibility buttons based on saved settings."""
        for button in self.glyph_buttons.values():
            button.update_is_toggled(button.name)

        if self.non_radial_button:
            self.non_radial_button.update_is_toggled(self.grid_name)