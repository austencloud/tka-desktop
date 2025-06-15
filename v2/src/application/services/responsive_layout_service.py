"""
Responsive Layout Service - Focused Responsive Scaling Operations

Handles all responsive layout and scaling calculations including:
- Responsive scaling factor calculations
- Screen size adaptation
- Context-aware scaling
- Layout configuration for different screen sizes

This service provides a clean, focused interface for responsive layout operations
while maintaining the proven scaling algorithms.
"""

from typing import Tuple
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass


class IResponsiveLayoutService(ABC):
    """Interface for responsive layout operations."""

    @abstractmethod
    def calculate_responsive_scaling(
        self, content_size: Tuple[int, int], container_size: Tuple[int, int]
    ) -> float:
        """Calculate responsive scaling factor."""
        pass

    @abstractmethod
    def calculate_context_aware_scaling(
        self, context: str, base_size: Tuple[int, int], container_size: Tuple[int, int]
    ) -> float:
        """Calculate scaling based on context."""
        pass

    @abstractmethod
    def get_layout_for_screen_size(self, screen_size: Tuple[int, int]) -> "LayoutConfig":
        """Get appropriate layout configuration for screen size."""
        pass


class LayoutMode(Enum):
    """Layout modes for different contexts."""

    HORIZONTAL_SCROLL = "horizontal_scroll"
    VERTICAL_SCROLL = "vertical_scroll"
    GRID = "grid"
    FLOW = "flow"
    FIXED = "fixed"


class ScalingMode(Enum):
    """Scaling modes for responsive layouts."""

    FIT_WIDTH = "fit_width"
    FIT_HEIGHT = "fit_height"
    FIT_BOTH = "fit_both"
    MAINTAIN_ASPECT = "maintain_aspect"
    NO_SCALING = "no_scaling"


@dataclass
class LayoutConfig:
    """Configuration for layout calculations."""

    mode: LayoutMode = LayoutMode.HORIZONTAL_SCROLL
    scaling_mode: ScalingMode = ScalingMode.MAINTAIN_ASPECT
    padding: int = 10
    spacing: int = 5
    min_item_size: Tuple[int, int] = (100, 100)
    max_item_size: Tuple[int, int] = (300, 300)
    items_per_row: int = None
    maintain_aspect_ratio: bool = True


class ResponsiveLayoutService(IResponsiveLayoutService):
    """
    Focused responsive layout service.

    Provides comprehensive responsive layout including:
    - Responsive scaling factor calculations
    - Screen size adaptation and categorization
    - Context-aware scaling with constraints
    - Layout configuration for different screen sizes
    """

    def __init__(self):
        # Scaling factors for different screen densities
        self._density_scaling = {
            "low": 0.8,
            "normal": 1.0,
            "high": 1.2,
            "extra_high": 1.5,
        }

        # Context-specific scaling configurations
        self._context_configs = self._load_context_configs()

    def calculate_responsive_scaling(
        self, content_size: Tuple[int, int], container_size: Tuple[int, int]
    ) -> float:
        """Calculate responsive scaling factor."""
        content_width, content_height = content_size
        container_width, container_height = container_size

        if content_width == 0 or content_height == 0:
            return 1.0

        # Calculate scaling factors for both dimensions
        width_scale = container_width / content_width
        height_scale = container_height / content_height

        # Use the smaller scale to ensure content fits
        scale = min(width_scale, height_scale)

        # Clamp scaling factor to reasonable bounds
        return max(0.1, min(3.0, scale))

    def calculate_context_aware_scaling(
        self, context: str, base_size: Tuple[int, int], container_size: Tuple[int, int]
    ) -> float:
        """Calculate scaling based on context."""
        config = self._context_configs.get(
            context, {"min_scale": 0.5, "max_scale": 2.0, "preferred_scale": 1.0}
        )

        # Calculate base scaling
        base_scale = self.calculate_responsive_scaling(base_size, container_size)

        # Apply context constraints
        min_scale = config["min_scale"]
        max_scale = config["max_scale"]
        preferred_scale = config["preferred_scale"]

        # Bias towards preferred scale
        if abs(base_scale - preferred_scale) < 0.2:
            scale = preferred_scale
        else:
            scale = base_scale

        # Clamp to context bounds
        return max(min_scale, min(max_scale, scale))

    def get_layout_for_screen_size(self, screen_size: Tuple[int, int]) -> LayoutConfig:
        """Get appropriate layout configuration for screen size."""
        width, height = screen_size

        # Categorize screen size
        if width < 800:
            # Small screen (mobile/tablet)
            return LayoutConfig(
                mode=LayoutMode.VERTICAL_SCROLL,
                scaling_mode=ScalingMode.FIT_WIDTH,
                padding=5,
                spacing=3,
                min_item_size=(80, 80),
                max_item_size=(200, 200),
            )
        elif width < 1200:
            # Medium screen (laptop)
            return LayoutConfig(
                mode=LayoutMode.GRID,
                scaling_mode=ScalingMode.MAINTAIN_ASPECT,
                padding=8,
                spacing=4,
                min_item_size=(100, 100),
                max_item_size=(250, 250),
            )
        else:
            # Large screen (desktop)
            return LayoutConfig(
                mode=LayoutMode.HORIZONTAL_SCROLL,
                scaling_mode=ScalingMode.MAINTAIN_ASPECT,
                padding=10,
                spacing=5,
                min_item_size=(120, 120),
                max_item_size=(300, 300),
            )

    def get_density_scaling(self, density: str) -> float:
        """Get scaling factor for screen density."""
        return self._density_scaling.get(density, 1.0)

    def calculate_adaptive_scaling(
        self,
        content_size: Tuple[int, int],
        container_size: Tuple[int, int],
        min_scale: float = 0.1,
        max_scale: float = 3.0,
    ) -> float:
        """Calculate adaptive scaling with custom bounds."""
        base_scale = self.calculate_responsive_scaling(content_size, container_size)
        return max(min_scale, min(max_scale, base_scale))

    def is_mobile_layout(self, screen_size: Tuple[int, int]) -> bool:
        """Determine if mobile layout should be used."""
        width, height = screen_size
        return width < 800 or height < 600

    def is_tablet_layout(self, screen_size: Tuple[int, int]) -> bool:
        """Determine if tablet layout should be used."""
        width, height = screen_size
        return 800 <= width < 1200 and 600 <= height < 900

    def is_desktop_layout(self, screen_size: Tuple[int, int]) -> bool:
        """Determine if desktop layout should be used."""
        width, height = screen_size
        return width >= 1200 and height >= 900

    # Private helper methods

    def _load_context_configs(self) -> dict:
        """Load context-specific scaling configurations."""
        return {
            "sequence_editor": {
                "min_scale": 0.5,
                "max_scale": 2.0,
                "preferred_scale": 1.0,
            },
            "dictionary_browser": {
                "min_scale": 0.3,
                "max_scale": 1.5,
                "preferred_scale": 0.8,
            },
            "beat_frame": {"min_scale": 0.4, "max_scale": 1.8, "preferred_scale": 1.0},
            "pictograph_viewer": {
                "min_scale": 0.2,
                "max_scale": 3.0,
                "preferred_scale": 1.2,
            },
        }
