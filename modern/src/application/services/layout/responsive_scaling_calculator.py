"""
Responsive Scaling Calculator

Handles responsive scaling and context-aware scaling calculations.
This class preserves all original scaling logic including density scaling,
context-aware scaling with specific configurations for different contexts,
and screen size-based layout selection.
"""

from typing import Tuple

from .layout_types import LayoutConfig, LayoutMode, ScalingMode

try:
    from src.core.decorators import handle_service_errors
    from src.core.monitoring import monitor_performance
except ImportError:

    def handle_service_errors(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    def monitor_performance(*args, **kwargs):
        def decorator(func):
            return func

        return decorator


class ResponsiveScalingCalculator:
    """
    Handles responsive scaling and context-aware scaling calculations.

    This class preserves all original scaling logic including density scaling,
    context-aware scaling with specific configurations for different contexts,
    and screen size-based layout selection.
    """

    def __init__(self):
        """Initialize the responsive scaling calculator."""
        # Scaling factors for different screen densities
        self._density_scaling = {
            "low": 0.8,
            "normal": 1.0,
            "high": 1.2,
            "extra_high": 1.5,
        }

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

    @handle_service_errors("calculate_context_aware_scaling")
    @monitor_performance("context_aware_scaling")
    def calculate_context_aware_scaling(
        self, context: str, base_size: Tuple[int, int], container_size: Tuple[int, int]
    ) -> float:
        """Calculate scaling based on context."""
        context_configs = {
            "sequence_editor": {
                "min_scale": 0.5,
                "max_scale": 2.0,
                "preferred_scale": 1.0,
            },
            "dictionary_browser": {
                "min_scale": 0.3,
                "max_scale": 1.5,
                "preferred_scale": 1.0,
            },
            "beat_frame": {"min_scale": 0.4, "max_scale": 1.8, "preferred_scale": 1.0},
            "pictograph_viewer": {
                "min_scale": 0.2,
                "max_scale": 3.0,
                "preferred_scale": 1.0,
            },
        }

        config = context_configs.get(
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
        width, _ = screen_size

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
