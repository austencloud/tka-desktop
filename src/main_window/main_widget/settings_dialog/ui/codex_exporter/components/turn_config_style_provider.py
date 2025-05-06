"""
Simplified style provider for turn configuration components.

This module provides a streamlined approach to styling turn configuration components
by leveraging the central theme module.
"""

from PyQt6.QtWidgets import QWidget
from ..theme import Colors, Sizing, StyleSheet


class TurnConfigStyleProvider:
    """Provides consistent styling for turn configuration components.

    This is a simplified version of the original TurnConfigStyleProvider that
    leverages the central theme module for styling constants and style generation.
    """

    def __init__(self, parent: QWidget):
        """Initialize the style provider.

        Args:
            parent: The parent widget to base DPI calculations on
        """
        self.parent = parent
        self.sizing = Sizing(parent)
        self.style_sheet = StyleSheet(self.sizing)

    # Layout properties
    @property
    def layout_spacing(self):
        """Get the layout spacing."""
        return self.sizing.spacing_md

    @property
    def layout_margin(self):
        """Get the layout margin."""
        return self.sizing.margin_md

    @property
    def grid_spacing(self):
        """Get the grid spacing."""
        return self.sizing.spacing_md

    @property
    def turn_selection_spacing(self):
        """Get the turn selection spacing."""
        return self.sizing.spacing_md

    @property
    def turn_pair_spacing(self):
        """Get the turn pair spacing."""
        return self.sizing.spacing_lg

    @property
    def slider_spacing(self):
        """Get the slider spacing."""
        return self.sizing.spacing_sm

    @property
    def pair_display_spacing(self):
        """Get the pair display spacing."""
        return self.sizing.spacing_sm

    @property
    def value_min_width(self):
        """Get the minimum width for value labels."""
        return self.sizing.turn_value_min_width

    # Style methods
    def get_card_style(self):
        """Get the style for the main card."""
        return self.style_sheet.card()

    def get_section_title_style(self):
        """Get the style for section titles."""
        return self.style_sheet.label(is_value=True)

    def get_explanation_style(self):
        """Get the style for explanation text."""
        return self.style_sheet.label(color=Colors.TEXT_SECONDARY)

    def get_radio_button_style(self):
        """Get the style for radio buttons."""
        return self.style_sheet.radio_button()

    def get_separator_style(self):
        """Get the style for separators."""
        return self.style_sheet.separator()

    def get_turn_label_style(self, color):
        """Get the style for turn labels."""
        return self.style_sheet.turn_label(color)

    def get_turn_value_label_style(self, color, enabled=True):
        """Get the style for turn value labels."""
        return self.style_sheet.turn_value_label(color, enabled)

    def get_slider_style(self, color, enabled=True):
        """Get the style for sliders."""
        return self.style_sheet.slider(color, enabled)

    def get_pair_label_style(self):
        """Get the style for the turn pair label."""
        return self.style_sheet.turn_pair_label()

    def get_pair_value_style(self, enabled=True):
        """Get the style for the turn pair value."""
        return self.style_sheet.turn_pair_value(enabled)

    def get_checkbox_style(self):
        """Get the style for the checkbox."""
        return self.style_sheet.checkbox()
