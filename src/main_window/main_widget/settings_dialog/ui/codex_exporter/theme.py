"""
Centralized theme for the application UI.

This module provides a single source of truth for all styling constants and
style generation functions used throughout the application.
"""

from PyQt6.QtWidgets import QWidget


# Color Palette
class Colors:
    """Central color definitions for the entire application."""

    # Main colors
    DARK_BG = "#121212"
    CARD_BG = "#1E1E1E"
    SURFACE = "#252525"
    BORDER_LIGHT = "#333333"

    # Accent colors
    RED = "#FF4F6C"
    BLUE = "#4F9BFF"
    GREEN = "#4FFF8F"

    # Text colors
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#B0B0B0"
    DISABLED_BG = "#2A2A2A"
    DISABLED_TEXT = "#666666"

    # Gradients
    BACKGROUND_GRADIENT = (
        "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #121212, stop:1 #1A1A2E)"
    )
    CARD_GRADIENT = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1E1E2E, stop:1 #252536)"
    )
    BUTTON_GRADIENT = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4FFF8F, stop:1 #3AE07A)"
    )
    BUTTON_HOVER_GRADIENT = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #62FFAC, stop:1 #4AE88A)"
    )
    BUTTON_PRESSED_GRADIENT = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3AE07A, stop:1 #2ACC65)"
    )
    SEPARATOR_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(80, 80, 100, 0), stop:0.5 rgba(80, 80, 100, 0.5), stop:1 rgba(80, 80, 100, 0))"

    # Turn configuration specific colors
    TURN_RED = RED
    TURN_BLUE = BLUE
    TURN_ACCENT = GREEN


class Sizing:
    """Responsive UI sizing based on DPI."""

    def __init__(self, widget: QWidget):
        """Initialize with a reference widget for DPI calculations."""
        self.dpi = widget.logicalDpiX() if widget.logicalDpiX() > 0 else 96
        self._calculate_sizes()

    def _calculate_sizes(self):
        """Calculate base sizes proportionally."""
        # Base unit calculated from DPI
        self.unit = max(4, self.dpi // 24)

        # Font sizes
        self.font_small = max(12, self.dpi // 8)
        self.font_medium = max(14, self.dpi // 7)
        self.font_large = max(16, self.dpi // 6)
        self.font_xlarge = max(18, self.dpi // 5)

        # Spacing
        self.spacing_xs = self.unit
        self.spacing_sm = self.unit * 2
        self.spacing_md = self.unit * 3
        self.spacing_lg = self.unit * 4
        self.spacing_xl = self.unit * 6

        # Component sizes
        self.border_radius_sm = self.unit
        self.border_radius_md = self.unit * 2
        self.border_radius_lg = self.unit * 3
        self.border_radius_xl = self.unit * 4

        # Slider specific sizes
        self.slider_groove_height = max(4, self.unit)
        self.slider_handle_size = max(16, self.unit * 4)
        self.slider_handle_margin = -self.slider_handle_size // 3

        # Control sizes (checkbox, radio button)
        self.control_indicator_size = max(18, self.unit * 4)
        self.control_border = max(1, self.unit // 4)

        # Component heights
        self.button_height = max(44, self.unit * 10)

        # Margins
        self.margin_sm = self.unit * 2
        self.margin_md = self.unit * 3
        self.margin_lg = self.unit * 4
        self.margin_xl = self.unit * 6

        # Turn configuration specific sizes
        self.turn_value_min_width = max(40, self.dpi // 5)
        self.turn_pair_value_radius = self.border_radius_sm
        self.turn_pair_padding_v = self.spacing_xs
        self.turn_pair_padding_h = self.spacing_md


class StyleSheet:
    """Generates style sheets for UI components."""

    def __init__(self, sizing: Sizing):
        self.sizing = sizing

    def card(self):
        """Style for cards."""
        return f"""
            QFrame[cssClass="card"] {{
                background: {Colors.CARD_GRADIENT};
                border-radius: {self.sizing.border_radius_lg}px;
                border: 1px solid rgba(255, 255, 255, 0.08);
            }}
            QLabel#cardTitle {{
                color: {Colors.TEXT_PRIMARY};
                font-size: {self.sizing.font_xlarge}px;
                font-weight: bold;
                margin-bottom: {self.sizing.margin_sm}px;
            }}
        """

    def button(self, primary=True):
        """Style for buttons."""
        if primary:
            return f"""
                QPushButton {{
                    background: {Colors.BUTTON_GRADIENT};
                    color: #121212;
                    border: none;
                    border-radius: {self.sizing.border_radius_md}px;
                    padding: {self.sizing.spacing_sm}px {self.sizing.spacing_lg}px;
                    font-weight: bold;
                    font-size: {self.sizing.font_medium}px;
                }}
                QPushButton:hover {{
                    background: {Colors.BUTTON_HOVER_GRADIENT};
                }}
                QPushButton:pressed {{
                    background: {Colors.BUTTON_PRESSED_GRADIENT};
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background-color: transparent;
                    color: {Colors.TEXT_PRIMARY};
                    border: 1px solid {Colors.BORDER_LIGHT};
                    border-radius: {self.sizing.border_radius_md}px;
                    padding: {self.sizing.spacing_sm}px {self.sizing.spacing_lg}px;
                    font-size: {self.sizing.font_medium}px;
                }}
                QPushButton:hover {{
                    background-color: rgba(255, 255, 255, 0.05);
                }}
                QPushButton:pressed {{
                    background-color: rgba(255, 255, 255, 0.1);
                }}
            """

    def radio_button(self):
        """Style for radio buttons."""
        return f"""
            QRadioButton {{
                color: {Colors.TEXT_PRIMARY};
                background-color: transparent;
                spacing: {self.sizing.spacing_sm}px;
                font-size: {self.sizing.font_medium}px;
                padding: {self.sizing.spacing_xs}px;
            }}
            QRadioButton::indicator {{
                width: {self.sizing.control_indicator_size}px;
                height: {self.sizing.control_indicator_size}px;
                border-radius: {self.sizing.control_indicator_size // 2}px;
                border: {self.sizing.control_border}px solid {Colors.BORDER_LIGHT};
            }}
            QRadioButton::indicator:checked {{
                border: {self.sizing.control_border}px solid {Colors.GREEN};
                background-color: qradialgradient(cx:0.5, cy:0.5, radius:0.4, fx:0.5, fy:0.5,
                                               stop:0 {Colors.GREEN}, stop:1 transparent);
            }}
        """

    def checkbox(self):
        """Style for checkboxes."""
        return f"""
            QCheckBox {{
                color: {Colors.TEXT_PRIMARY};
                font-size: {self.sizing.font_medium}px;
                padding: {self.sizing.spacing_sm}px 0;
                spacing: {self.sizing.spacing_sm}px;
            }}
            QCheckBox::indicator {{
                width: {self.sizing.control_indicator_size}px;
                height: {self.sizing.control_indicator_size}px;
                border-radius: {self.sizing.border_radius_sm}px;
                border: {self.sizing.control_border}px solid {Colors.BORDER_LIGHT};
            }}
            QCheckBox::indicator:checked {{
                background-color: {Colors.GREEN};
                border: {self.sizing.control_border}px solid {Colors.GREEN};
            }}
            QCheckBox::indicator:disabled {{
                background-color: {Colors.DISABLED_BG};
                border: {self.sizing.control_border}px solid {Colors.DISABLED_TEXT};
            }}
            QCheckBox:disabled {{
                color: {Colors.DISABLED_TEXT};
            }}
        """

    def slider(self, color, enabled=True):
        """Style for sliders."""
        active_color = color if enabled else Colors.DISABLED_BG
        return f"""
            QSlider::groove:horizontal {{
                border: none;
                height: {self.sizing.slider_groove_height}px;
                background-color: {Colors.BORDER_LIGHT};
                border-radius: {self.sizing.slider_groove_height // 2}px;
            }}
            QSlider::handle:horizontal {{
                background-color: {active_color};
                border: none;
                width: {self.sizing.slider_handle_size}px;
                height: {self.sizing.slider_handle_size}px;
                margin: {self.sizing.slider_handle_margin}px 0;
                border-radius: {self.sizing.slider_handle_size // 2}px;
            }}
            QSlider::sub-page:horizontal {{
                background-color: {active_color};
                border-radius: {self.sizing.slider_groove_height // 2}px;
            }}
        """

    def label(self, color=Colors.TEXT_PRIMARY, is_value=False, enabled=True):
        """Style for labels."""
        text_color = color if enabled else Colors.DISABLED_TEXT
        font_size = self.sizing.font_large if is_value else self.sizing.font_medium
        font_weight = "bold" if is_value else "normal"

        return f"""
            color: {text_color};
            font-size: {font_size}px;
            font-weight: {font_weight};
            background-color: transparent;
        """

    def value_display(self, enabled=True):
        """Style for value displays."""
        bg_color = Colors.SURFACE if enabled else Colors.DISABLED_BG
        text_color = Colors.TEXT_PRIMARY if enabled else Colors.DISABLED_TEXT

        return f"""
            color: {text_color};
            font-weight: bold;
            font-size: {self.sizing.font_medium}px;
            background-color: {bg_color};
            border-radius: {self.sizing.border_radius_sm}px;
            padding: {self.sizing.spacing_xs}px {self.sizing.spacing_md}px;
        """

    def separator(self):
        """Style for separators."""
        return f"background-color: {Colors.BORDER_LIGHT}; max-height: 1px;"

    def turn_label(self, color, enabled=True):
        """Style for turn labels."""
        text_color = color if enabled else Colors.DISABLED_TEXT
        return f"""
            color: {text_color};
            font-weight: bold;
            font-size: {self.sizing.font_medium}px;
            background-color: transparent;
        """

    def turn_value_label(self, color, enabled=True):
        """Style for turn value labels."""
        text_color = color if enabled else Colors.DISABLED_TEXT
        return f"""
            color: {text_color};
            font-weight: bold;
            font-size: {self.sizing.font_large}px;
            background-color: transparent;
        """

    def turn_pair_label(self):
        """Style for the turn pair label."""
        return f"""
            color: {Colors.TEXT_PRIMARY};
            font-size: {self.sizing.font_medium}px;
            background-color: transparent;
        """

    def turn_pair_value(self, enabled=True):
        """Style for the turn pair value display."""
        bg_color = Colors.SURFACE if enabled else Colors.DISABLED_BG
        text_color = Colors.TEXT_PRIMARY if enabled else Colors.DISABLED_TEXT
        return f"""
            color: {text_color};
            font-weight: bold;
            font-size: {self.sizing.font_large}px;
            background-color: {bg_color};
            border-radius: {self.sizing.turn_pair_value_radius}px;
            padding: {self.sizing.turn_pair_padding_v}px {self.sizing.turn_pair_padding_h}px;
        """
