from PyQt6.QtWidgets import QWidget, QGridLayout, QSizePolicy
from typing import TYPE_CHECKING

from main_window.main_widget.settings_dialog.visibility_tab.buttons_widget.visibility_button import VisibilityButton

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.visibility_tab.visibility_tab import VisibilityTab


class VisibilityButtonsWidget(QWidget):
    glyph_buttons: dict[str, VisibilityButton] = {}
    non_radial_button: VisibilityButton = None
    glyph_names = ["TKA", "Reversals", "VTG", "Elemental", "Positions"]
    grid_name = "Non-radial points"

    def __init__(self, visibility_tab: "VisibilityTab"):
        super().__init__()
        self.visibility_tab = visibility_tab
        self.toggler = visibility_tab.toggler

        # 🛠 Ensure this widget EXPANDS inside `VisibilityTab`
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self._create_buttons()
        self._setup_layout()
        self.update_button_flags()

    def _setup_layout(self):
        """Organizes buttons into a 3x2 grid layout."""
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)

        button_list = list(self.glyph_buttons.values()) + [self.non_radial_button]

        # Dynamically place buttons in a 3x2 grid
        for i, button in enumerate(button_list):
            row = i // 3  # 3 buttons per row
            col = i % 3  # Max 2 rows
            self.layout.addWidget(button, row, col)

            # 🛠 Ensure the buttons expand properly
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setLayout(self.layout)

    def _create_buttons(self):
        """Creates all buttons for toggling visibility."""
        for name in self.glyph_names:
            button = VisibilityButton(name, self)
            self.glyph_buttons[name] = button

        self.non_radial_button = VisibilityButton(self.grid_name, self)

    def update_button_flags(self):
        """Synchronize button states with visibility settings."""
        settings = self.visibility_tab.main_widget.settings_manager.visibility
        for name, button in self.glyph_buttons.items():
            button.is_toggled = settings.get_glyph_visibility(name)
            button.animations.play_toggle_animation(button.is_toggled)

        if self.non_radial_button:
            self.non_radial_button.is_toggled = settings.get_non_radial_visibility()
            self.non_radial_button.animations.play_toggle_animation(
                self.non_radial_button.is_toggled
            )
