"""
Component Layout Service - Focused Component Positioning Operations

Handles all component layout and positioning calculations including:
- Component positioning in different layout modes
- Flow layout calculations
- Grid layout calculations
- Component arrangement and spacing

This service provides a clean, focused interface for component layout operations
while maintaining the proven positioning algorithms.
"""

from typing import Dict, Any, Tuple
from abc import ABC, abstractmethod
from enum import Enum


class IComponentLayoutService(ABC):
    """Interface for component layout operations."""

    @abstractmethod
    def calculate_component_positions(
        self, layout_config: Dict[str, Any]
    ) -> Dict[str, Tuple[int, int]]:
        """Calculate positions for UI components."""
        pass

    @abstractmethod
    def calculate_flow_layout(
        self, components: Dict[str, Any], container_size: Tuple[int, int]
    ) -> Dict[str, Tuple[int, int]]:
        """Calculate flow layout for components."""
        pass

    @abstractmethod
    def calculate_grid_layout(
        self, components: Dict[str, Any], container_size: Tuple[int, int]
    ) -> Dict[str, Tuple[int, int]]:
        """Calculate grid layout for components."""
        pass


class LayoutMode(Enum):
    """Layout modes for different contexts."""

    HORIZONTAL_SCROLL = "horizontal_scroll"
    VERTICAL_SCROLL = "vertical_scroll"
    GRID = "grid"
    FLOW = "flow"
    FIXED = "fixed"


class ComponentLayoutService(IComponentLayoutService):
    """
    Focused component layout service.

    Provides comprehensive component positioning including:
    - Component positioning in different layout modes
    - Flow layout with automatic wrapping
    - Grid layout with optimal arrangement
    - Fixed positioning support
    """

    def __init__(self):
        # Default layout settings
        self._default_settings = self._load_default_settings()

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
            positions = self.calculate_flow_layout(components, container_size)

        elif layout_mode == LayoutMode.GRID:
            # Grid layout - arrange in grid pattern
            positions = self.calculate_grid_layout(components, container_size)

        else:
            # Default to flow layout
            positions = self.calculate_flow_layout(components, container_size)

        return positions

    def calculate_flow_layout(
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

    def calculate_grid_layout(
        self, components: Dict[str, Any], container_size: Tuple[int, int]
    ) -> Dict[str, Tuple[int, int]]:
        """Calculate grid layout for components."""
        component_count = len(components)
        if component_count == 0:
            return {}

        rows, cols = self._get_optimal_grid_dimensions(component_count, container_size)

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

    def calculate_vertical_layout(
        self, components: Dict[str, Any], container_size: Tuple[int, int]
    ) -> Dict[str, Tuple[int, int]]:
        """Calculate vertical layout for components."""
        positions = {}
        current_y = 10
        container_width = container_size[0]

        for name, config in components.items():
            width = config.get("width", 100)
            height = config.get("height", 100)

            # Center horizontally
            x = (container_width - width) // 2

            positions[name] = (x, current_y)
            current_y += height + 10

        return positions

    def calculate_horizontal_layout(
        self, components: Dict[str, Any], container_size: Tuple[int, int]
    ) -> Dict[str, Tuple[int, int]]:
        """Calculate horizontal layout for components."""
        positions = {}
        current_x = 10
        container_height = container_size[1]

        for name, config in components.items():
            width = config.get("width", 100)
            height = config.get("height", 100)

            # Center vertically
            y = (container_height - height) // 2

            positions[name] = (current_x, y)
            current_x += width + 10

        return positions

    def calculate_centered_layout(
        self, components: Dict[str, Any], container_size: Tuple[int, int]
    ) -> Dict[str, Tuple[int, int]]:
        """Calculate centered layout for components."""
        positions = {}
        container_width, container_height = container_size

        # Calculate total size of all components
        total_width = sum(config.get("width", 100) for config in components.values())
        total_height = max(config.get("height", 100) for config in components.values())

        # Add spacing between components
        spacing = 10
        total_width += (len(components) - 1) * spacing

        # Calculate starting position to center everything
        start_x = (container_width - total_width) // 2
        start_y = (container_height - total_height) // 2

        current_x = start_x

        for name, config in components.items():
            width = config.get("width", 100)
            height = config.get("height", 100)

            # Center vertically within the row
            y = start_y + (total_height - height) // 2

            positions[name] = (current_x, y)
            current_x += width + spacing

        return positions

    def get_layout_bounds(
        self, positions: Dict[str, Tuple[int, int]], components: Dict[str, Any]
    ) -> Tuple[int, int]:
        """Calculate the total bounds of a layout."""
        if not positions:
            return (0, 0)

        max_x = 0
        max_y = 0

        for name, (x, y) in positions.items():
            width = components.get(name, {}).get("width", 100)
            height = components.get(name, {}).get("height", 100)

            max_x = max(max_x, x + width)
            max_y = max(max_y, y + height)

        return (max_x, max_y)

    # Private helper methods

    def _get_optimal_grid_dimensions(
        self, item_count: int, container_size: Tuple[int, int]
    ) -> Tuple[int, int]:
        """Get optimal grid dimensions (rows, cols) for items."""
        if item_count <= 0:
            return (0, 0)

        container_width, container_height = container_size
        aspect_ratio = container_width / container_height if container_height > 0 else 1.0

        # Calculate optimal number of columns based on aspect ratio
        import math

        cols = max(1, int(math.sqrt(item_count * aspect_ratio)))
        rows = math.ceil(item_count / cols)

        # Adjust if the layout doesn't fit well
        while cols > 1 and rows * container_height / cols > container_width:
            cols -= 1
            rows = math.ceil(item_count / cols)

        return (rows, cols)

    def _load_default_settings(self) -> Dict[str, Any]:
        """Load default layout settings."""
        return {
            "default_padding": 10,
            "default_spacing": 5,
            "min_component_size": (50, 50),
            "max_component_size": (500, 500),
            "grid_cell_padding": 5,
        }
