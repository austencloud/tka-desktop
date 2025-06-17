"""
Layout Management Service - Unified Layout Operations

Consolidates all layout-related services into a single cohesive service:
- Simple layout calculations (simple_layout_service)
- Beat frame layout management (beat_frame_layout_service)
- Context-aware scaling (context_aware_scaling_service)

This service provides a clean, unified interface for all layout operations
while maintaining the proven algorithms from the individual services.
"""

from typing import Dict, Any, Optional, Tuple, List
from enum import Enum
from dataclasses import dataclass
import math

from PyQt6.QtCore import QSize
from domain.models.core_models import SequenceData
from core.interfaces.core_services import ILayoutService


# ILayoutManagementService has been consolidated into ILayoutService in core_services.py
# This removes the duplicate interface definition


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
    items_per_row: Optional[int] = None
    maintain_aspect_ratio: bool = True


@dataclass
class LayoutResult:
    """Result of layout calculations."""

    item_positions: Dict[str, Tuple[int, int]]
    item_sizes: Dict[str, Tuple[int, int]]
    total_size: Tuple[int, int]
    scaling_factor: float
    overflow: bool = False


class LayoutManagementService(ILayoutService):
    """
    Unified layout management service consolidating all layout operations.

    Provides comprehensive layout management including:
    - Beat frame layout calculations
    - Responsive scaling algorithms
    - Grid layout optimization
    - Component positioning
    - Context-aware layout adaptation
    - Basic UI layout information (ILayoutService)
    """

    def __init__(self):
        # Layout presets for different contexts
        self._layout_presets = self._load_layout_presets()

        # Scaling factors for different screen densities
        self._density_scaling = {
            "low": 0.8,
            "normal": 1.0,
            "high": 1.2,
            "extra_high": 1.5,
        }

        # Default layout configurations
        self._default_configs = self._load_default_configs()

        # Basic UI layout configuration (ILayoutService)
        self._main_window_size = QSize(1400, 900)
        self._layout_ratio = (10, 10)  # 50/50 split between workbench and picker

    def calculate_beat_frame_layout(
        self, sequence: SequenceData, container_size: Tuple[int, int]
    ) -> Dict[str, Any]:
        """Calculate layout for beat frames using enhanced algorithm."""
        from application.services.layout.beat_layout_service import BeatLayoutService

        # Use enhanced layout system
        enhanced_service = BeatLayoutService()
        layout_config = enhanced_service.calculate_beat_frame_layout(
            sequence, container_size
        )

        return layout_config

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

    def get_optimal_grid_layout(
        self, item_count: int, container_size: Tuple[int, int]
    ) -> Tuple[int, int]:
        """Get optimal grid layout (rows, cols) for items."""
        if item_count <= 0:
            return (0, 0)

        container_width, container_height = container_size
        aspect_ratio = (
            container_width / container_height if container_height > 0 else 1.0
        )

        # Calculate optimal number of columns based on aspect ratio
        cols = max(1, int(math.sqrt(item_count * aspect_ratio)))
        rows = math.ceil(item_count / cols)

        # Adjust if the layout doesn't fit well
        while cols > 1 and rows * container_height / cols > container_width:
            cols -= 1
            rows = math.ceil(item_count / cols)

        return (rows, cols)

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
                "preferred_scale": 0.8,
            },
            "beat_frame": {"min_scale": 0.4, "max_scale": 1.8, "preferred_scale": 1.0},
            "pictograph_viewer": {
                "min_scale": 0.2,
                "max_scale": 3.0,
                "preferred_scale": 1.2,
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

    # Private helper methods

    def _calculate_horizontal_beat_layout(
        self,
        beat_count: int,
        container_size: Tuple[int, int],
        base_size: Tuple[int, int],
        padding: int,
        spacing: int,
    ) -> Dict[str, Any]:
        """Calculate horizontal layout for beat frames."""
        container_width, container_height = container_size
        base_width, base_height = base_size

        # Calculate available space
        available_width = container_width - 2 * padding
        available_height = container_height - 2 * padding

        # Calculate beat size with spacing
        total_spacing = (beat_count - 1) * spacing
        available_beat_width = available_width - total_spacing
        beat_width = min(base_width, available_beat_width // beat_count)
        beat_height = min(base_height, available_height)

        # Maintain aspect ratio
        if beat_width / beat_height > base_width / base_height:
            beat_width = int(beat_height * base_width / base_height)
        else:
            beat_height = int(beat_width * base_height / base_width)

        # Calculate positions
        positions = {}
        sizes = {}
        start_x = (
            padding + (available_width - (beat_count * beat_width + total_spacing)) // 2
        )
        y = padding + (available_height - beat_height) // 2

        for i in range(beat_count):
            x = start_x + i * (beat_width + spacing)
            positions[f"beat_{i}"] = (x, y)
            sizes[f"beat_{i}"] = (beat_width, beat_height)

        total_width = beat_count * beat_width + total_spacing + 2 * padding
        total_height = beat_height + 2 * padding

        return {
            "positions": positions,
            "sizes": sizes,
            "total_size": (total_width, total_height),
            "scaling_factor": beat_width / base_width,
        }

    def _calculate_grid_beat_layout(
        self,
        beat_count: int,
        container_size: Tuple[int, int],
        base_size: Tuple[int, int],
        padding: int,
        spacing: int,
    ) -> Dict[str, Any]:
        """Calculate grid layout for beat frames."""
        rows, cols = self.get_optimal_grid_layout(beat_count, container_size)

        container_width, container_height = container_size
        base_width, base_height = base_size

        # Calculate available space
        available_width = container_width - 2 * padding
        available_height = container_height - 2 * padding

        # Calculate beat size
        col_spacing = (cols - 1) * spacing
        row_spacing = (rows - 1) * spacing

        beat_width = min(base_width, (available_width - col_spacing) // cols)
        beat_height = min(base_height, (available_height - row_spacing) // rows)

        # Maintain aspect ratio
        if beat_width / beat_height > base_width / base_height:
            beat_width = int(beat_height * base_width / base_height)
        else:
            beat_height = int(beat_width * base_height / base_width)

        # Calculate positions
        positions = {}
        sizes = {}

        grid_width = cols * beat_width + col_spacing
        grid_height = rows * beat_height + row_spacing
        start_x = padding + (available_width - grid_width) // 2
        start_y = padding + (available_height - grid_height) // 2

        for i in range(beat_count):
            row = i // cols
            col = i % cols

            x = start_x + col * (beat_width + spacing)
            y = start_y + row * (beat_height + spacing)

            positions[f"beat_{i}"] = (x, y)
            sizes[f"beat_{i}"] = (beat_width, beat_height)

        return {
            "positions": positions,
            "sizes": sizes,
            "total_size": (grid_width + 2 * padding, grid_height + 2 * padding),
            "scaling_factor": beat_width / base_width,
        }

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

        rows, cols = self.get_optimal_grid_layout(component_count, container_size)

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

    def _load_layout_presets(self) -> Dict[str, LayoutConfig]:
        """Load layout presets for different contexts."""
        return {
            "sequence_editor": LayoutConfig(
                mode=LayoutMode.HORIZONTAL_SCROLL,
                scaling_mode=ScalingMode.MAINTAIN_ASPECT,
                padding=10,
                spacing=5,
            ),
            "dictionary_browser": LayoutConfig(
                mode=LayoutMode.GRID,
                scaling_mode=ScalingMode.FIT_BOTH,
                padding=8,
                spacing=4,
                items_per_row=4,
            ),
            "mobile_view": LayoutConfig(
                mode=LayoutMode.VERTICAL_SCROLL,
                scaling_mode=ScalingMode.FIT_WIDTH,
                padding=5,
                spacing=3,
            ),
        }

    def _load_default_configs(self) -> Dict[str, Any]:
        """Load default configuration values."""
        return {
            "min_beat_size": (80, 80),
            "max_beat_size": (200, 200),
            "default_padding": 10,
            "default_spacing": 5,
            "aspect_ratio_tolerance": 0.1,
        }

    # ILayoutService implementation methods
    def get_main_window_size(self) -> QSize:
        """Get the main window size."""
        return self._main_window_size

    def get_workbench_size(self) -> QSize:
        """Get the workbench area size."""
        # Calculate workbench size based on main window and ratio
        total_width = self._main_window_size.width()
        total_height = self._main_window_size.height()

        # Account for margins and spacing
        usable_width = total_width - 60  # 60px for margins and spacing
        usable_height = total_height - 100  # 100px for header and margins

        # Calculate workbench width based on ratio
        ratio_total = self._layout_ratio[0] + self._layout_ratio[1]
        workbench_width = int(usable_width * self._layout_ratio[0] / ratio_total)

        return QSize(workbench_width, usable_height)

    def get_picker_size(self) -> QSize:
        """Get the option picker size."""
        # Calculate picker size based on main window and ratio
        total_width = self._main_window_size.width()
        total_height = self._main_window_size.height()

        # Account for margins and spacing
        usable_width = total_width - 60  # 60px for margins and spacing
        usable_height = total_height - 100  # 100px for header and margins

        # Calculate picker width based on ratio
        ratio_total = self._layout_ratio[0] + self._layout_ratio[1]
        picker_width = int(usable_width * self._layout_ratio[1] / ratio_total)

        return QSize(picker_width, usable_height)

    def get_layout_ratio(self) -> Tuple[int, int]:
        """Get the layout ratio (workbench:picker)."""
        return self._layout_ratio

    def set_layout_ratio(self, ratio: Tuple[int, int]) -> None:
        """Set the layout ratio."""
        self._layout_ratio = ratio

    def calculate_component_size(
        self, component_type: str, parent_size: QSize
    ) -> QSize:
        """Calculate component size based on parent and type."""
        parent_width = parent_size.width()
        parent_height = parent_size.height()

        if component_type == "beat_frame":
            # Beat frame takes most of the workbench area
            return QSize(int(parent_width * 0.85), int(parent_height * 0.9))

        elif component_type == "button_panel":
            # Button panel is narrow vertical strip
            return QSize(int(parent_width * 0.15), int(parent_height * 0.9))

        elif component_type == "option_picker":
            # Option picker takes full picker area
            return QSize(parent_width, parent_height)

        elif component_type == "start_position_picker":
            # Start position picker takes full picker area
            return QSize(parent_width, parent_height)

        elif component_type == "pictograph":
            # Individual pictograph size
            return QSize(120, 120)

        else:
            # Default size for unknown components
            return QSize(int(parent_width * 0.8), int(parent_height * 0.8))

    def set_main_window_size(self, size: QSize) -> None:
        """Set the main window size (for dynamic updates)."""
        self._main_window_size = size
