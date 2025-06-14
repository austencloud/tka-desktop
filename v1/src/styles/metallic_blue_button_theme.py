from dataclasses import dataclass

from styles.button_state import ButtonState

# Modern 2025 Design Constants
GLASS_OPACITY = 0.15
NEOMORPHIC_OPACITY = 0.8
SHADOW_BLUR = 20
GLOW_INTENSITY = 0.6

# 2025 Glass-morphism Gradients with Realistic Depth
GLASS_MORPHISM_NORMAL = f"""
    qlineargradient(
        spread: pad,
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 rgba(255, 255, 255, {GLASS_OPACITY}),
        stop: 0.2 rgba(255, 255, 255, {GLASS_OPACITY * 0.8}),
        stop: 0.8 rgba(255, 255, 255, {GLASS_OPACITY * 0.4}),
        stop: 1 rgba(255, 255, 255, {GLASS_OPACITY * 0.2})
    )
"""

GLASS_MORPHISM_HOVER = f"""
    qlineargradient(
        spread: pad,
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 rgba(100, 200, 255, {GLASS_OPACITY * 2}),
        stop: 0.3 rgba(150, 220, 255, {GLASS_OPACITY * 1.5}),
        stop: 0.7 rgba(200, 240, 255, {GLASS_OPACITY}),
        stop: 1 rgba(255, 255, 255, {GLASS_OPACITY * 0.5})
    )
"""

NEOMORPHIC_ACTIVE = f"""
    qlineargradient(
        spread: pad,
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 rgba(64, 150, 255, {NEOMORPHIC_OPACITY}),
        stop: 0.2 rgba(100, 180, 255, {NEOMORPHIC_OPACITY}),
        stop: 0.5 rgba(120, 200, 255, {NEOMORPHIC_OPACITY}),
        stop: 0.8 rgba(80, 160, 255, {NEOMORPHIC_OPACITY}),
        stop: 1 rgba(40, 120, 255, {NEOMORPHIC_OPACITY})
    )
"""

NEOMORPHIC_PRESSED = f"""
    qlineargradient(
        spread: pad,
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 rgba(20, 80, 180, {NEOMORPHIC_OPACITY}),
        stop: 0.5 rgba(40, 100, 200, {NEOMORPHIC_OPACITY}),
        stop: 1 rgba(60, 120, 220, {NEOMORPHIC_OPACITY})
    )
"""

DISABLED_GLASS = f"""
    qlineargradient(
        spread: pad,
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 rgba(128, 128, 128, {GLASS_OPACITY * 0.5}),
        stop: 1 rgba(96, 96, 96, {GLASS_OPACITY * 0.3})
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
        """Factory method to get modern 2025 themes with glass-morphism and neomorphic effects.

        Args:
            state: The ButtonState (NORMAL or ACTIVE)
            enabled: Whether the button is enabled

        Returns:
            A modern 2025 themed button style with glass-morphism and depth
        """
        if state == ButtonState.ACTIVE:
            # Active state - Modern neomorphic design with depth and glow
            return cls(
                background=NEOMORPHIC_ACTIVE,
                hover_background=NEOMORPHIC_ACTIVE,
                pressed_background=NEOMORPHIC_PRESSED,
                font_color="white",
                hover_font_color="white",
                pressed_font_color="white",
                border_color="rgba(255, 255, 255, 0.3)",
            )
        elif enabled:
            # Normal enabled state - Glass-morphism with subtle transparency
            return cls(
                background=GLASS_MORPHISM_NORMAL,
                hover_background=GLASS_MORPHISM_HOVER,
                pressed_background=NEOMORPHIC_PRESSED,
                font_color="white",
                hover_font_color="white",
                pressed_font_color="white",
                border_color="rgba(255, 255, 255, 0.2)",
            )
        else:
            # Disabled state - Muted glass effect
            return cls(
                background=DISABLED_GLASS,
                hover_background=DISABLED_GLASS,
                pressed_background=DISABLED_GLASS,
                font_color="rgba(255, 255, 255, 0.4)",
                hover_font_color="rgba(255, 255, 255, 0.5)",
                pressed_font_color="rgba(255, 255, 255, 0.4)",
                border_color="rgba(128, 128, 128, 0.3)",
            )
