"""
Beat Layout Service - Focused Beat Frame Layout Operations

Handles all beat frame layout calculations including:
- Beat frame layout for sequences
- Horizontal beat layout calculations
- Grid beat layout calculations
- Beat positioning and sizing

This service provides a clean, focused interface for beat layout operations
while maintaining the proven layout algorithms.
"""

from typing import Dict, Any, Tuple
from abc import ABC, abstractmethod
import math

from domain.models.core_models import SequenceData


class IBeatLayoutService(ABC):
    """Interface for beat layout operations."""

    @abstractmethod
    def calculate_beat_frame_layout(
        self, sequence: SequenceData, container_size: Tuple[int, int]
    ) -> Dict[str, Any]:
        """Calculate layout for beat frames in a sequence."""
        pass

    @abstractmethod
    def get_optimal_grid_layout(
        self, item_count: int, container_size: Tuple[int, int]
    ) -> Tuple[int, int]:
        """Get optimal grid layout (rows, cols) for items."""
        pass


class BeatLayoutService(IBeatLayoutService):
    """
    Focused beat layout service.

    Provides comprehensive beat frame layout including:
    - Beat frame layout calculations for sequences
    - Horizontal and grid layout algorithms
    - Optimal grid layout calculations
    - Beat positioning and sizing
    """

    def __init__(self):
        # Default layout configurations
        self._default_configs = self._load_default_configs()

    def calculate_beat_frame_layout(
        self, sequence: SequenceData, container_size: Tuple[int, int]
    ) -> Dict[str, Any]:
        """Calculate layout for beat frames using enhanced algorithm."""
        from application.services.layout.enhanced_beat_layout_service import EnhancedBeatLayoutService
        
        # Use enhanced layout system
        enhanced_service = EnhancedBeatLayoutService()
        layout_config = enhanced_service.calculate_beat_frame_layout(sequence, container_size)
        
        return layout_config

    def get_optimal_grid_layout(
        self, item_count: int, container_size: Tuple[int, int]
    ) -> Tuple[int, int]:
        """Get optimal grid layout (rows, cols) for items."""
        if item_count <= 0:
            return (0, 0)

        container_width, container_height = container_size
        aspect_ratio = container_width / container_height if container_height > 0 else 1.0

        # Calculate optimal number of columns based on aspect ratio
        cols = max(1, int(math.sqrt(item_count * aspect_ratio)))
        rows = math.ceil(item_count / cols)

        # Adjust if the layout doesn't fit well
        while cols > 1 and rows * container_height / cols > container_width:
            cols -= 1
            rows = math.ceil(item_count / cols)

        return (rows, cols)

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
        start_x = padding + (available_width - (beat_count * beat_width + total_spacing)) // 2
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

    def _load_default_configs(self) -> Dict[str, Any]:
        """Load default configuration values."""
        return {
            "min_beat_size": (80, 80),
            "max_beat_size": (200, 200),
            "default_padding": 10,
            "default_spacing": 5,
            "aspect_ratio_tolerance": 0.1,
        }
