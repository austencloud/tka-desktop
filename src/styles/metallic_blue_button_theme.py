from dataclasses import dataclass

from styles.button_state import ButtonState

# Define transparency value for easy modification
TRANSPARENCY = 0.5

# Define common gradients as constants for readability
# (Because nobody wants to stare at gradient gibberish at 2 AM)
# CSS-like gradient definitions - because even Qt deserves to look fabulous
METALLIC_BLUE_GRADIENT = f"""
    qlineargradient(
        spread: pad,
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #1e3c72,
        stop: 0.3 #6c9ce9,
        stop: 0.6 #4a77d4,
        stop: 1 #2a52be
    )
"""

GRAY_HOVER_GRADIENT = f"""
    qlineargradient(
        spread: pad,
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 rgba(80, 80, 80, {TRANSPARENCY}),
        stop: 0.3 rgba(160, 160, 160, {TRANSPARENCY}),
        stop: 0.6 rgba(120, 120, 120, {TRANSPARENCY}),
        stop: 1 rgba(40, 40, 40, {TRANSPARENCY})
    )
"""

DISABLED_HOVER_GRADIENT = f"""
    qlineargradient(
        spread: pad,
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 rgba(40, 40, 40, {TRANSPARENCY / 2}),
        stop: 1 rgba(60, 60, 60, {TRANSPARENCY / 2})
    )
"""

SHINY_NORMAL_GRADIENT = f"""
    qlineargradient(
        spread: pad,
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 rgba(58, 58, 58, {TRANSPARENCY}),
        stop: 0.5 rgba(74, 74, 74, {TRANSPARENCY}),
        stop: 1 rgba(90, 90, 90, {TRANSPARENCY})
    )
"""


@dataclass
class MetallicBlueButtonTheme:
    """Defines the visual styling for a button in different states."""

    # Button appearance properties
    background: str
    hover_background: str
    pressed_background: str
    font_color: str
    hover_font_color: str
    pressed_font_color: str
    border_color: str = "white"  # Default border color

    @classmethod
    def get_default_theme(
        cls, state: ButtonState, enabled: bool = True
    ) -> "MetallicBlueButtonTheme":
        """Factory method to get predefined themes based on state and enabled status.

        Args:
            state: The ButtonState (NORMAL or SELECTED)
            enabled: Whether the button is enabled

        Returns:
            A themed button style that won't make your eyes bleed
        """
        if state == ButtonState.SELECTED:
            # Selected state - Shiny blue like a peacock trying to impress
            return cls(
                background=METALLIC_BLUE_GRADIENT,
                hover_background=METALLIC_BLUE_GRADIENT,
                pressed_background="#1e3c72",
                font_color="black",
                hover_font_color="white",
                pressed_font_color="white",
            )
        elif enabled:
            # Normal enabled state - Professional, but not boring
            return cls(
                background=SHINY_NORMAL_GRADIENT,
                hover_background=GRAY_HOVER_GRADIENT,
                pressed_background="#505050",
                font_color="white",
                hover_font_color="white",
                pressed_font_color="white",
                border_color="white",
            )
        else:
            # Disabled state - Like the button had too much to drink
            return cls(
                background=f"rgba(30, 30, 30, {TRANSPARENCY})",
                hover_background=DISABLED_HOVER_GRADIENT,
                pressed_background="#707070",
                font_color="gray",
                hover_font_color="#aaa",
                pressed_font_color="white",
                border_color="#777",
            )
