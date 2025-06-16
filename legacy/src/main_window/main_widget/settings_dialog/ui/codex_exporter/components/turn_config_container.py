"""
Container component that combines all turn configuration components.
"""

from typing import Dict, Any
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy
from legacy.src.legacy_settings_manager.legacy_settings_manager import LegacySettingsManager
from ..widgets import ModernCard
from ..theme import Colors
from .turn_config_style_provider import TurnConfigStyleProvider
from .grid_mode_selector import GridModeSelector
from .turn_slider import TurnSlider
from .turn_pair_display import TurnPairDisplay
from .generate_all_checkbox import GenerateAllCheckbox


class TurnConfigContainer(QWidget):
    """Container that combines all turn configuration components."""

    def __init__(self, parent=None):
        """Initialize the turn configuration container.

        Args:
            parent: The parent widget
        """
        super().__init__(parent)
        self.settings_manager = LegacySettingsManager()
        self.style_provider = TurnConfigStyleProvider(self)
        self._setup_ui()

    def _setup_ui(self):
        """Set up the container UI."""
        # Set a proportional font size based on DPI
        font = self.font()
        font.setPointSize(self.style_provider.sizing.font_large)
        self.setFont(font)

        # Create main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create the card
        self.card = ModernCard(self, "Turn Configuration")
        self.card.setStyleSheet(self.style_provider.get_card_style())

        # Make the card expand to fill available space
        self.card.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # Create the main layout for the card content
        card_layout = QVBoxLayout()
        card_layout.setSpacing(self.style_provider.layout_spacing)
        card_layout.setContentsMargins(
            self.style_provider.layout_margin,
            self.style_provider.layout_margin,
            self.style_provider.layout_margin,
            self.style_provider.layout_margin,
        )

        # Get last saved turn values
        last_red_turns = self.settings_manager.codex_exporter.get_last_red_turns()
        last_blue_turns = self.settings_manager.codex_exporter.get_last_blue_turns()

        # Create grid mode selector
        self.grid_mode_selector = GridModeSelector(
            self, self.style_provider, self.settings_manager
        )

        # Add separator
        separator1 = QFrame(self)
        separator1.setFrameShape(QFrame.Shape.HLine)
        separator1.setFrameShadow(QFrame.Shadow.Sunken)
        separator1.setStyleSheet(self.style_provider.get_separator_style())

        # Create turn sliders
        self.first_turn_slider = TurnSlider(
            "First Turn Value",
            Colors.TURN_RED,
            self,
            self.style_provider,
            last_red_turns,
        )
        self.second_turn_slider = TurnSlider(
            "Second Turn Value",
            Colors.TURN_BLUE,
            self,
            self.style_provider,
            last_blue_turns,
        )

        # Create turn pair layout
        turn_pair_layout = QHBoxLayout()
        turn_pair_layout.setSpacing(self.style_provider.turn_pair_spacing)
        turn_pair_layout.addWidget(self.first_turn_slider)
        turn_pair_layout.addWidget(self.second_turn_slider)

        # Create turn pair display
        self.turn_pair_display = TurnPairDisplay(
            self, self.style_provider, (last_red_turns, last_blue_turns)
        )

        # Connect signals
        self.first_turn_slider.value_changed.connect(self._update_turn_pair_display)
        self.second_turn_slider.value_changed.connect(self._update_turn_pair_display)

        # Add separator
        separator2 = QFrame(self)
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setFrameShadow(QFrame.Shadow.Sunken)
        separator2.setStyleSheet(self.style_provider.get_separator_style())

        # Create generate all checkbox
        self.generate_all_checkbox = GenerateAllCheckbox(self, self.style_provider)
        self.generate_all_checkbox.state_changed.connect(self._update_sliders_state)

        # Add components to layout with better vertical spacing
        card_layout.addWidget(self.grid_mode_selector)
        card_layout.addWidget(separator1)

        # Add turn pair layout with a stretch factor
        card_layout.addLayout(turn_pair_layout, 2)  # Give it more space

        # Add spacing between components
        card_layout.addSpacing(self.style_provider.layout_spacing)

        card_layout.addWidget(self.turn_pair_display)

        # Add spacing between components
        card_layout.addSpacing(self.style_provider.layout_spacing)

        card_layout.addWidget(separator2)
        card_layout.addWidget(self.generate_all_checkbox)

        # Add a stretch at the end to push everything up
        card_layout.addStretch(1)

        # Add the layout to the card
        self.card.layout.addLayout(card_layout)

        # Add the card to the main layout
        layout.addWidget(self.card)

    def _update_turn_pair_display(self, _=None):
        """Update the turn pair display."""
        first_value = self.first_turn_slider.get_value()
        second_value = self.second_turn_slider.get_value()
        self.turn_pair_display.update_values(first_value, second_value)

    def _update_sliders_state(self, state):
        """Update the state of sliders based on the checkbox."""
        enabled = not bool(state)
        self.first_turn_slider.set_enabled(enabled)
        self.second_turn_slider.set_enabled(enabled)
        self.turn_pair_display.set_enabled(enabled)

    def get_turn_values(self) -> Dict[str, Any]:
        """Get the selected turn values and configuration.

        Returns:
            Dict containing red_turns, blue_turns, generate_all, and grid_mode
        """
        return {
            "red_turns": self.first_turn_slider.get_value(),
            "blue_turns": self.second_turn_slider.get_value(),
            "generate_all": self.generate_all_checkbox.is_checked(),
            "grid_mode": self.grid_mode_selector.get_grid_mode(),
        }
