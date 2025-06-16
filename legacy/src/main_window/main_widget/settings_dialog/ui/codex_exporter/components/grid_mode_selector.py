"""
Grid mode selector component for the codex exporter.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QButtonGroup
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from legacy.src.legacy_settings_manager.legacy_settings_manager import LegacySettingsManager
from ..widgets import ModernRadioButton
from .turn_config_style_provider import TurnConfigStyleProvider


class GridModeSelector(QWidget):
    """Component for selecting grid mode (Diamond/Box)."""

    def __init__(self, parent=None, style_provider=None, settings_manager=None):
        """Initialize the grid mode selector.

        Args:
            parent: The parent widget
            style_provider: The style provider for consistent styling
            settings_manager: The settings manager for loading/saving settings
        """
        super().__init__(parent)
        self.style_provider = style_provider or TurnConfigStyleProvider(self)
        self.settings_manager = settings_manager or LegacySettingsManager()
        self._setup_ui()

    def _setup_ui(self):
        """Set up the grid mode selector UI."""
        # Create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(self.style_provider.grid_spacing)

        # Create radio buttons
        self.grid_mode_group = QButtonGroup(self)
        self.diamond_radio = ModernRadioButton("Diamond", self)
        self.diamond_radio.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.diamond_radio.setStyleSheet(self.style_provider.get_radio_button_style())

        self.box_radio = ModernRadioButton("Box", self)
        self.box_radio.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.box_radio.setStyleSheet(self.style_provider.get_radio_button_style())

        # Set initial state from settings
        grid_mode = self.settings_manager.codex_exporter.get_grid_mode()
        if grid_mode == "box":
            self.box_radio.setChecked(True)
        else:
            self.diamond_radio.setChecked(True)

        # Add to button group
        self.grid_mode_group.addButton(self.diamond_radio)
        self.grid_mode_group.addButton(self.box_radio)

        # Add to layout
        layout.addStretch(1)
        layout.addWidget(self.diamond_radio)
        layout.addWidget(self.box_radio)
        layout.addStretch(1)

    def get_grid_mode(self):
        """Get the selected grid mode.

        Returns:
            str: "box" if box is selected, "diamond" otherwise
        """
        return "box" if self.box_radio.isChecked() else "diamond"
