from dataclasses import dataclass

from styles.button_state import ButtonState

# Define transparency value for easy modification
OPACITY = 0.7

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
        stop: 0 rgba(80, 80, 80, {OPACITY}),
        stop: 0.3 rgba(160, 160, 160, {OPACITY}),
        stop: 0.6 rgba(120, 120, 120, {OPACITY}),
        stop: 1 rgba(40, 40, 40, {OPACITY})
    )
"""

DISABLED_HOVER_GRADIENT = f"""
    qlineargradient(
        spread: pad,
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 rgba(40, 40, 40, {OPACITY / 2}),
        stop: 1 rgba(60, 60, 60, {OPACITY / 2})
    )
"""

SHINY_NORMAL_GRADIENT = f"""
    qlineargradient(
        spread: pad,
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 rgba(30, 30, 30, {OPACITY}),
        stop: 0.5 rgba(45, 45, 45, {OPACITY}),
        stop: 1 rgba(60, 60, 60, {OPACITY})
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
                background=f"rgba(30, 30, 30, {OPACITY})",
                hover_background=DISABLED_HOVER_GRADIENT,
                pressed_background="#707070",
                font_color="gray",
                hover_font_color="#aaa",
                pressed_font_color="white",
                border_color="#777",
            )
