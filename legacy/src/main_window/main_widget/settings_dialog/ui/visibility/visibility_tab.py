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
    from legacy.src.main_window.main_widget.settings_dialog.legacy_settings_dialog import (
        LegacySettingsDialog,
    )


class VisibilityTab(QWidget):
    """Visibility tab with original layout structure and improved feedback."""

    def __init__(self, settings_dialog: "LegacySettingsDialog"):
        super().__init__()
        self.main_widget = settings_dialog.main_widget
        self.dialog = settings_dialog

        # Get settings_manager from dependency injection system
        try:
            settings_manager = self.main_widget.app_context.settings_manager
            self.settings = settings_manager.visibility
            # Create the visibility state manager
            self.state_manager = VisibilityStateManager(settings_manager)
        except AttributeError:
            # Fallback for cases where app_context is not available during initialization
            self.settings = None
            self.state_manager = None
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                "settings_manager not available during VisibilityTab initialization"
            )

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
            """
            QLabel {
                color: rgba(245, 158, 11, 1);
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(245, 158, 11, 0.15),
                    stop:1 rgba(217, 119, 6, 0.1));
                border: 1px solid rgba(245, 158, 11, 0.3);
                border-radius: 12px;
                padding: 12px 16px;
                font-size: 13px;
                font-weight: 500;
            }
            """
        )
        font = QFont()
        font.setPointSize(13)
        font.setWeight(500)
        self.help_label.setFont(font)

        # Initialize visibility
        all_motions_visible = self.state_manager.are_all_motions_visible()
        self.help_label.setVisible(not all_motions_visible)

    def _setup_layout(self):
        """Set up the tab layout with modern glassmorphism styling."""
        # Main layout with improved spacing
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # Motion buttons container with glassmorphism background
        motion_container = QWidget()
        motion_container.setObjectName("motion_container")
        motion_container.setStyleSheet(
            """
            QWidget#motion_container {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(31, 41, 59, 0.1),
                    stop:1 rgba(55, 65, 81, 0.08));
                border: 1px solid rgba(75, 85, 99, 0.3);
                border-radius: 12px;
                padding: 16px;
            }
            """
        )

        motion_buttons_layout = QHBoxLayout(motion_container)
        motion_buttons_layout.setSpacing(16)
        motion_buttons_layout.setContentsMargins(16, 16, 16, 16)
        motion_buttons_layout.addWidget(
            self.buttons_widget.glyph_buttons["Blue Motion"]
        )
        motion_buttons_layout.addWidget(self.buttons_widget.glyph_buttons["Red Motion"])

        # Add motion buttons container
        main_layout.addWidget(motion_container)

        # Add help text that appears when options are hidden
        main_layout.addWidget(self.help_label)

        # Pictograph in middle with container
        pictograph_container = QWidget()
        pictograph_container.setObjectName("pictograph_container")
        pictograph_container.setStyleSheet(
            """
            QWidget#pictograph_container {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(31, 41, 59, 0.05),
                    stop:1 rgba(55, 65, 81, 0.03));
                border: 1px solid rgba(75, 85, 99, 0.15);
                border-radius: 16px;
                padding: 20px;
            }
            """
        )

        pictograph_layout = QVBoxLayout(pictograph_container)
        pictograph_layout.setContentsMargins(20, 20, 20, 20)
        pictograph_layout.addWidget(
            self.pictograph_view, alignment=Qt.AlignmentFlag.AlignCenter
        )

        main_layout.addWidget(pictograph_container, stretch=4)

        # Glyph buttons at the bottom with container
        buttons_container = QWidget()
        buttons_container.setObjectName("buttons_container")
        buttons_container.setStyleSheet(
            """
            QWidget#buttons_container {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(31, 41, 59, 0.1),
                    stop:1 rgba(55, 65, 81, 0.08));
                border: 1px solid rgba(75, 85, 99, 0.3);
                border-radius: 12px;
                padding: 16px;
            }
            """
        )

        buttons_layout = QVBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(16, 16, 16, 16)
        buttons_layout.addWidget(self.buttons_widget)

        main_layout.addWidget(buttons_container)

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
