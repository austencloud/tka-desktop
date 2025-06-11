#!/usr/bin/env python3
"""
Standalone Layout Calculator - Calculates image layout dimensions.

This module calculates the optimal layout (columns and rows) for sequence images
based on the number of beats and whether to include a start position.
"""

import math
from typing import Tuple


class StandaloneLayoutCalculator:
    """
    Calculator for determining optimal image layout dimensions.

    This class replicates the layout calculation logic from the main application
    but works independently without external dependencies.
    """

    def __init__(self):
        """Initialize the layout calculator."""
        pass

    def calculate_layout(
        self, num_beats: int, include_start_position: bool = False
    ) -> Tuple[int, int]:
        """
        Calculate the optimal layout (columns, rows) for the given number of beats.

        Args:
            num_beats: Number of beats to arrange
            include_start_position: Whether to include a start position

        Returns:
            Tuple of (columns, rows)
        """
        # Adjust beat count if including start position
        total_positions = num_beats
        if include_start_position:
            total_positions += 1

        # Handle edge cases
        if total_positions == 0:
            return (1, 1)  # Minimum layout
        elif total_positions == 1:
            return (1, 1)
        elif total_positions == 2:
            return (2, 1)
        elif total_positions == 3:
            return (3, 1)
        elif total_positions == 4:
            return (2, 2)
        elif total_positions <= 6:
            return (3, 2)
        elif total_positions <= 9:
            return (3, 3)
        elif total_positions <= 12:
            return (4, 3)
        elif total_positions <= 16:
            return (4, 4)
        elif total_positions <= 20:
            return (5, 4)
        elif total_positions <= 25:
            return (5, 5)
        else:
            # For larger sequences, calculate optimal rectangle
            return self._calculate_optimal_rectangle(total_positions)

    def _calculate_optimal_rectangle(self, total_positions: int) -> Tuple[int, int]:
        """
        Calculate optimal rectangle dimensions for large sequences.

        Args:
            total_positions: Total number of positions to arrange

        Returns:
            Tuple of (columns, rows) that minimizes aspect ratio difference
        """
        # Try to find dimensions that create a rectangle close to square
        sqrt_positions = math.sqrt(total_positions)

        # Start with square-ish dimensions
        cols = math.ceil(sqrt_positions)
        rows = math.ceil(total_positions / cols)

        # Ensure we have enough space
        while cols * rows < total_positions:
            if cols <= rows:
                cols += 1
            else:
                rows += 1

        return (cols, rows)

    def calculate_image_dimensions(
        self, columns: int, rows: int, beat_size: int = 950, additional_height: int = 0
    ) -> Tuple[int, int]:
        """
        Calculate the final image dimensions.

        Args:
            columns: Number of columns
            rows: Number of rows
            beat_size: Size of each beat in pixels
            additional_height: Additional height for overlays

        Returns:
            Tuple of (width, height) in pixels
        """
        width = columns * beat_size
        height = rows * beat_size + additional_height

        return (width, height)

    def get_beat_position(
        self,
        beat_index: int,
        columns: int,
        beat_size: int = 950,
        include_start_position: bool = False,
    ) -> Tuple[int, int]:
        """
        Get the pixel position for a specific beat.

        Args:
            beat_index: Index of the beat (0-based)
            columns: Number of columns in the layout
            beat_size: Size of each beat in pixels
            include_start_position: Whether start position is included

        Returns:
            Tuple of (x, y) pixel coordinates
        """
        # Adjust index if start position is included
        position_index = beat_index
        if include_start_position:
            position_index += 1

        # Calculate grid position
        col = position_index % columns
        row = position_index // columns

        # Convert to pixel coordinates
        x = col * beat_size
        y = row * beat_size

        return (x, y)

    def get_start_position_coordinates(self, beat_size: int = 950) -> Tuple[int, int]:
        """
        Get the pixel coordinates for the start position.

        Args:
            beat_size: Size of each beat in pixels

        Returns:
            Tuple of (x, y) pixel coordinates (always at 0, 0)
        """
        return (0, 0)

    def validate_layout(self, columns: int, rows: int, total_positions: int) -> bool:
        """
        Validate that the layout can accommodate all positions.

        Args:
            columns: Number of columns
            rows: Number of rows
            total_positions: Total positions to accommodate

        Returns:
            True if layout is valid, False otherwise
        """
        return columns * rows >= total_positions

    def get_layout_info(
        self, num_beats: int, include_start_position: bool = False
    ) -> dict:
        """
        Get comprehensive layout information.

        Args:
            num_beats: Number of beats
            include_start_position: Whether to include start position

        Returns:
            Dictionary with layout information
        """
        columns, rows = self.calculate_layout(num_beats, include_start_position)
        total_positions = num_beats + (1 if include_start_position else 0)

        return {
            "columns": columns,
            "rows": rows,
            "total_positions": total_positions,
            "num_beats": num_beats,
            "include_start_position": include_start_position,
            "aspect_ratio": columns / rows if rows > 0 else 1.0,
            "efficiency": (
                total_positions / (columns * rows) if columns * rows > 0 else 0.0
            ),
        }
