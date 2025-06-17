"""
Option Picker Dimension Analyzer

Provides utilities for analyzing and calculating optimal dimensions
for the option picker layout system.
"""

from typing import Tuple
from PyQt6.QtWidgets import QWidget


class OptionPickerDimensionAnalyzer:
    """Analyzes and calculates optimal dimensions for option picker components"""

    def __init__(self, widget, sections_container, sections_layout, sections):
        self.widget = widget
        self.sections_container = sections_container
        self.sections_layout = sections_layout
        self.sections = sections

        self.default_pictograph_size = 160
        self.min_pictograph_size = 60
        self.max_pictograph_size = 200
        self.grid_spacing = 8
        self.container_margins = 10

    def calculate_optimal_pictograph_size(
        self, available_width: int, column_count: int = 8
    ) -> int:
        """Calculate optimal pictograph size based on available width"""
        total_spacing = self.grid_spacing * (column_count - 1)
        available_for_pictographs = (
            available_width - (2 * self.container_margins) - total_spacing
        )

        optimal_size = available_for_pictographs // column_count

        # Clamp to reasonable bounds
        return max(
            self.min_pictograph_size, min(self.max_pictograph_size, optimal_size)
        )

    def calculate_container_dimensions(
        self, pictograph_count: int, pictograph_size: int, column_count: int = 8
    ) -> Tuple[int, int]:
        """Calculate container dimensions for given pictograph count and size"""
        rows_needed = (pictograph_count - 1) // column_count + 1

        width = (
            (column_count * pictograph_size)
            + (self.grid_spacing * (column_count - 1))
            + (2 * self.container_margins)
        )
        height = (
            (rows_needed * pictograph_size)
            + (self.grid_spacing * (rows_needed - 1))
            + (2 * self.container_margins)
        )

        return width, height

    def analyze_layout_efficiency(
        self, available_width: int, pictograph_count: int
    ) -> dict:
        """Analyze layout efficiency for different configurations"""
        results = {}

        for columns in [6, 7, 8, 9, 10]:
            pictograph_size = self.calculate_optimal_pictograph_size(
                available_width, columns
            )
            container_width, container_height = self.calculate_container_dimensions(
                pictograph_count, pictograph_size, columns
            )

            # Calculate efficiency metrics
            used_width = container_width
            width_efficiency = (
                used_width / available_width if available_width > 0 else 0
            )

            results[columns] = {
                "pictograph_size": pictograph_size,
                "container_width": container_width,
                "container_height": container_height,
                "width_efficiency": width_efficiency,
                "rows_needed": (pictograph_count - 1) // columns + 1,
            }

        return results

    def log_all_container_dimensions(self, phase: str) -> None:
        """Log comprehensive dimension analysis for debugging"""
        print(f"\n=== {phase} - Dimension Analysis ===")

        if self.widget:
            print(f"Main widget: {self.widget.width()}x{self.widget.height()}")

        if self.sections_container:
            print(
                f"Sections container: {self.sections_container.width()}x{self.sections_container.height()}"
            )

        if self.sections:
            for name, section in self.sections.items():
                if hasattr(section, "width") and hasattr(section, "height"):
                    print(f"{name} section: {section.width()}x{section.height()}")

        print("=" * 50)
