"""
Turn pair display component for the codex exporter.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from .turn_config_style_provider import TurnConfigStyleProvider


class TurnPairDisplay(QWidget):
    """Displays the current turn pair values."""

    def __init__(self, parent=None, style_provider=None, initial_values=(0.0, 0.0)):
        """Initialize the turn pair display.
        
        Args:
            parent: The parent widget
            style_provider: The style provider for consistent styling
            initial_values: The initial values to display (first_turn, second_turn)
        """
        super().__init__(parent)
        self.style_provider = style_provider or TurnConfigStyleProvider(self)
        self.initial_values = initial_values
        self._setup_ui()

    def _setup_ui(self):
        """Set up the turn pair display UI."""
        # Create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(self.style_provider.pair_display_spacing)

        # Create label
        self.pair_label = QLabel("Current Turn Pair:", self)
        self.pair_label.setStyleSheet(self.style_provider.get_pair_label_style())

        # Create value label
        first_value, second_value = self.initial_values
        self.pair_value = QLabel(f"({first_value:.1f}, {second_value:.1f})", self)
        self.pair_value.setStyleSheet(self.style_provider.get_pair_value_style())

        # Add to layout
        layout.addWidget(self.pair_label)
        layout.addWidget(self.pair_value)
        layout.addStretch(1)

    def update_values(self, first_value, second_value):
        """Update the displayed values.
        
        Args:
            first_value: The first turn value
            second_value: The second turn value
        """
        self.pair_value.setText(f"({first_value:.1f}, {second_value:.1f})")

    def set_enabled(self, enabled):
        """Enable or disable the display.
        
        Args:
            enabled: Whether the display should be enabled
        """
        self.pair_value.setEnabled(enabled)
        
        # Update styling based on enabled state
        self.pair_value.setStyleSheet(self.style_provider.get_pair_value_style(enabled))
