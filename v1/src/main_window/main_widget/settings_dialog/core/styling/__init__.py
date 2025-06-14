"""
Styling components for glassmorphism design system using coordinator pattern.

This package contains the refactored components that were extracted from
the monolithic GlassmorphismStyler class to follow the Single Responsibility Principle.
"""

from .glassmorphism_coordinator import GlassmorphismCoordinator
from .color_manager import ColorManager
from .typography_manager import TypographyManager
from .component_styler import ComponentStyler
from .effect_manager import EffectManager
from .layout_styler import LayoutStyler

__all__ = [
    "GlassmorphismCoordinator",
    "ColorManager",
    "TypographyManager", 
    "ComponentStyler",
    "EffectManager",
    "LayoutStyler",
]
