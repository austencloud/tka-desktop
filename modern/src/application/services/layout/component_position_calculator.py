"""
Component Position Calculator

Handles component positioning and grid layout calculations.
This class preserves all original component positioning logic including
flow layout, grid layout, and fixed positioning calculations.
"""

from typing import Dict, Any, Tuple

from .beat_layout_calculator import BeatLayoutCalculator
from .layout_types import LayoutMode

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


class ComponentPositionCalculator:
    """
    Handles component positioning and grid layout calculations.

    This class preserves all original component positioning logic including
    flow layout, grid layout, and fixed positioning calculations.
    """

    def __init__(self, beat_layout_calculator: BeatLayoutCalculator):
        """Initialize with reference to beat layout calculator for grid operations."""
        self._beat_layout_calculator = beat_layout_calculator

    @handle_service_errors("calculate_component_positions")
    @monitor_performance("component_positioning")
    def calculate_component_positions(
        self, layout_config: Dict[str, Any]
    ) -> Dict[str, Tuple[int, int]]:
        """Calculate positions for UI components."""
        components = layout_config.get("components", {})
        container_size = layout_config.get("container_size", (800, 600))
        layout_mode = LayoutMode(layout_config.get("mode", "flow"))

        positions = {}

        if layout_mode == LayoutMode.FIXED:
            # Fixed positioning - use absolute coordinates
            for name, config in components.items():
                x = config.get("x", 0)
                y = config.get("y", 0)
                positions[name] = (x, y)

        elif layout_mode == LayoutMode.FLOW:
            # Flow layout - arrange components in sequence
            positions = self._calculate_flow_layout(components, container_size)

        elif layout_mode == LayoutMode.GRID:
            # Grid layout - arrange in grid pattern
            positions = self._calculate_grid_layout(components, container_size)

        else:
            # Default to flow layout
            positions = self._calculate_flow_layout(components, container_size)

        return positions

    def _calculate_flow_layout(
        self, components: Dict[str, Any], container_size: Tuple[int, int]
    ) -> Dict[str, Tuple[int, int]]:
        """Calculate flow layout for components."""
        positions = {}
        current_x = 10
        current_y = 10
        row_height = 0
        container_width = container_size[0]

        for name, config in components.items():
            width = config.get("width", 100)
            height = config.get("height", 100)

            # Check if component fits in current row
            if current_x + width > container_width - 10:
                # Move to next row
                current_x = 10
                current_y += row_height + 10
                row_height = 0

            positions[name] = (current_x, current_y)
            current_x += width + 10
            row_height = max(row_height, height)

        return positions

    def _calculate_grid_layout(
        self, components: Dict[str, Any], container_size: Tuple[int, int]
    ) -> Dict[str, Tuple[int, int]]:
        """Calculate grid layout for components."""
        component_count = len(components)
        if component_count == 0:
            return {}

        rows, cols = self._beat_layout_calculator.get_optimal_grid_layout(
            component_count, container_size
        )

        positions = {}
        container_width, container_height = container_size

        cell_width = container_width // cols
        cell_height = container_height // rows

        for i, name in enumerate(components.keys()):
            row = i // cols
            col = i % cols

            x = col * cell_width + 10
            y = row * cell_height + 10

            positions[name] = (x, y)

        return positions
