from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from base_widgets.pictograph.elements.views.visibility_pictograph_view import (
    VisibilityPictographView,
)
from main_window.main_widget.settings_dialog.ui.visibility.visibility_state_manager import (
    VisibilityStateManager,
)

from .pictograph.visibility_pictograph import VisibilityPictograph
from .visibility_toggler import VisibilityToggler
from .buttons_widget.visibility_buttons_widget import VisibilityButtonsWidget

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class VisibilityTab(QWidget):
    """Visibility tab with original layout structure and improved feedback."""

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
        # Update help text visibility based on motion state
        all_motions_visible = self.state_manager.are_all_motions_visible()
        if hasattr(self, "help_label"):
            self.help_label.setVisible(not all_motions_visible)

    def _setup_components(self):
        """Create the tab components."""
        self.toggler = VisibilityToggler(self)
        self.pictograph = VisibilityPictograph(self)
        self.pictograph_view = VisibilityPictographView(self, self.pictograph)
        self.buttons_widget = VisibilityButtonsWidget(self)

        # Create help text that appears when dependent glyphs are hidden
        self.help_label = QLabel(
            "Some visibility options are hidden.\nActivate both motions to show them."
        )
        self.help_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.help_label.setWordWrap(True)
        self.help_label.setStyleSheet(
            "color: #FF9900; background-color: rgba(0, 0, 0, 0.1); border-radius: 5px; padding: 8px;"
        )
        font = QFont()
        self.help_label.setFont(font)

        # Initialize visibility
        all_motions_visible = self.state_manager.are_all_motions_visible()
        self.help_label.setVisible(not all_motions_visible)

    def _setup_layout(self):
        """Set up the tab layout preserving the original structure."""
        # Main layout
        main_layout = QVBoxLayout(self)

        # Motion buttons at the top
        motion_buttons_layout = QHBoxLayout()
        motion_buttons_layout.addWidget(
            self.buttons_widget.glyph_buttons["Blue Motion"]
        )
        motion_buttons_layout.addWidget(self.buttons_widget.glyph_buttons["Red Motion"])

        # Add motion buttons at top
        main_layout.addLayout(motion_buttons_layout, 1)

        # Add help text that appears when options are hidden
        main_layout.addWidget(self.help_label)

        # Pictograph in middle
        main_layout.addWidget(
            self.pictograph_view, stretch=4, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Glyph buttons at the bottom (handled by the VisibilityButtonsWidget)
        main_layout.addWidget(self.buttons_widget, 1)

        self.setLayout(main_layout)

    # make s resizeEvent that resizes the note
    def resizeEvent(self, event):
        """Resize the help text note based on the tab width."""
        super().resizeEvent(event)
        tab_width = self.width()
        font_size = int(tab_width / 60)
        font = QFont()
        font.setPointSize(font_size)
        self.help_label.setFont(font)
        self.help_label.setFixedWidth(tab_width - 20)
        self.help_label.adjustSize()
        self.update()
