from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout

from base_widgets.pictograph.elements.views.visibility_pictograph_view import (
    VisibilityPictographView,
)
from main_window.main_widget.settings_dialog.ui.visibility.visibility_state_manager import (
    VisibilityStateManager,
)

from .pictograph.visibility_pictograph import VisibilityPictograph
from .visibility_toggler import VisibilityToggler
from .buttons_widget.visibility_buttons_widget import VisibilityButtonsWidget
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class VisibilityTab(QWidget):
    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__()
        self.main_widget = settings_dialog.main_widget
        self.settings = self.main_widget.settings_manager.visibility
        self.dialog = settings_dialog
        # Create the visibility state manager
        self.state_manager = VisibilityStateManager(self.main_widget.settings_manager)

        # Setup components with the state manager
        self._setup_components()
        self._setup_layout()

        # Register tab for state updates
        self.state_manager.register_observer(self._on_state_changed)

    def _on_state_changed(self):
        """Handle any visibility state changes."""
        # Update button visibility based on motion states
        all_motions_visible = self.state_manager.are_all_motions_visible()
        for name, button in self.buttons_widget.glyph_buttons.items():
            if name in ["TKA", "VTG", "Elemental", "Positions"]:
                button.setVisible(all_motions_visible)

                if all_motions_visible:
                    user_intent = self.state_manager.get_user_intent_visibility(name)
                    button.set_active(user_intent)

    def _setup_components(self):
        self.toggler = VisibilityToggler(self)
        self.pictograph = VisibilityPictograph(self)
        self.pictograph_view = VisibilityPictographView(self, self.pictograph)
        self.buttons_widget = VisibilityButtonsWidget(self)

    def _setup_layout(self):
        # Main layout
        main_layout = QVBoxLayout(self)

        # Motion buttons container (top)
        motion_buttons_layout = QHBoxLayout()
        motion_buttons_layout.addWidget(
            self.buttons_widget.glyph_buttons["Blue Motion"]
        )
        motion_buttons_layout.addWidget(self.buttons_widget.glyph_buttons["Red Motion"])

        # Add motion buttons at top
        main_layout.addLayout(motion_buttons_layout)

        # Pictograph in middle
        main_layout.addWidget(
            self.pictograph_view, stretch=3, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Glyph buttons container (bottom)
        glyph_buttons_layout = QGridLayout()

        # Filter out the motion buttons that are now at the top
        glyph_button_list = [
            button
            for name, button in self.buttons_widget.glyph_buttons.items()
            if name not in ["Red Motion", "Blue Motion"]
        ] + [self.buttons_widget.non_radial_button]

        # Arrange in 2 rows of 3 buttons
        for i, button in enumerate(glyph_button_list):
            row = i // 3
            col = i % 3
            glyph_buttons_layout.addWidget(button, row, col)
        all_motions_visible = self.settings.are_all_motions_visible()
        for name, button in self.buttons_widget.glyph_buttons.items():
            if name in ["TKA", "VTG", "Elemental", "Positions"]:
                button.setVisible(all_motions_visible)

        main_layout.addLayout(glyph_buttons_layout)
        self.setLayout(main_layout)
