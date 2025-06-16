"""
Border Manager for Modern Pictographs.

This manager handles border width calculations and visual border rendering
to match Legacy's border behavior exactly.
"""

import math
from typing import Optional, Tuple
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import QWidget

from domain.models.core_models import LetterType


class PictographBorderManager:
    """
    Manages border calculations and rendering for Modern pictographs to match Legacy behavior.

    Legacy border patterns:
    - Border width = max(1, int(size * 0.015)) (1.5% of size)
    - Size adjustment = size - (2 * border_width)
    - Different letter types have different border colors
    """

    def __init__(self):
        self.border_width_percentage = 0.015  # 1.5% as used in Legacy
        self.minimum_border_width = 1
        self.show_borders = True
        self.primary_color = "#000000"  # Default black
        self.secondary_color = "#000000"
        self.original_primary_color = "#000000"
        self.original_secondary_color = "#000000"

    def calculate_border_width(self, size: int) -> int:
        """
        Calculate border width based on size, matching Legacy's formula.

        Legacy formula: border_width = max(1, int(size * 0.015))
        """
        calculated_width = int(size * self.border_width_percentage)
        return max(self.minimum_border_width, calculated_width)

    def get_border_adjusted_size(self, target_size: int) -> int:
        """
        Get size adjusted for border width, matching Legacy calculations.

        Legacy formula: size -= 2 * border_width
        """
        border_width = self.calculate_border_width(target_size)
        adjusted_size = target_size - (2 * border_width)
        return max(50, adjusted_size)  # Minimum viable size

    def update_border_colors_for_letter_type(self, letter_type: LetterType) -> None:
        """Update border colors based on letter type, matching Legacy behavior."""
        border_colors_map = {
            LetterType.TYPE1: ("#36c3ff", "#6F2DA8"),  # Cyan, Purple
            LetterType.TYPE2: ("#6F2DA8", "#6F2DA8"),  # Purple, Purple
            LetterType.TYPE3: ("#26e600", "#6F2DA8"),  # Green, Purple
            LetterType.TYPE4: ("#26e600", "#26e600"),  # Green, Green
            LetterType.TYPE5: ("#00b3ff", "#26e600"),  # Blue, Green
            LetterType.TYPE6: ("#eb7d00", "#eb7d00"),  # Orange, Orange
        }

        self.primary_color, self.secondary_color = border_colors_map.get(
            letter_type, ("#000000", "#000000")
        )
        self.original_primary_color = self.primary_color
        self.original_secondary_color = self.secondary_color

    def set_gold_border(self) -> None:
        """Set border colors to gold, typically used on hover."""
        gold_color = "#FFD700"
        self.primary_color = gold_color
        self.secondary_color = gold_color

    def reset_border_colors(self) -> None:
        """Reset border colors to their original values."""
        self.primary_color = self.original_primary_color
        self.secondary_color = self.original_secondary_color

    def set_custom_border_colors(self, primary: str, secondary: str) -> None:
        """Set custom border colors."""
        self.primary_color = primary
        self.secondary_color = secondary

    def get_border_dimensions(self, view_width: int) -> Tuple[float, float]:
        """
        Get border dimensions for drawing, matching Legacy's floating-point calculations.

        Legacy uses: max(1.0, view_width * 0.016) for both outer and inner borders
        """
        outer_border_width = max(1.0, view_width * 0.016)
        inner_border_width = max(1.0, view_width * 0.016)
        return outer_border_width, inner_border_width

    def draw_borders(self, painter: QPainter, viewport_rect, view_width: int) -> None:
        """
        Draw borders on the viewport, exactly matching Legacy's border drawing logic.

        CRITICAL: Legacy borders are drawn as overlays that don't affect content positioning.
        The borders are positioned to be visible within the viewport without reducing
        the available content area.

        Args:
            painter: QPainter instance for drawing
            viewport_rect: The viewport rectangle to draw borders on
            view_width: Width of the view for border width calculations
        """
        if not self.show_borders:
            return

        # Get border dimensions - exactly matching Legacy's calculation
        view_width = viewport_rect.width()  # Use actual viewport width
        outer_border_width = max(1.0, view_width * 0.016)
        inner_border_width = max(1.0, view_width * 0.016)

        # Calculate half pen widths for proper positioning
        half_outer_pen = outer_border_width / 2.0
        half_inner_pen = inner_border_width / 2.0

        # Draw outer border - exactly matching Legacy's logic
        pen = QPen()
        pen.setColor(QColor(self.primary_color))
        pen.setWidthF(outer_border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        # Convert viewport rect to QRectF - exactly as Legacy does
        outer_rect = QRectF(viewport_rect)
        outer_rect = outer_rect.adjusted(
            +half_outer_pen,
            +half_outer_pen,
            -half_outer_pen,
            -half_outer_pen,
        )
        painter.drawRect(outer_rect)

        # Draw inner border - exactly matching Legacy's logic
        pen.setColor(QColor(self.secondary_color))
        pen.setWidthF(inner_border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        inner_rect = outer_rect.adjusted(
            +half_inner_pen,
            +half_inner_pen,
            -half_inner_pen,
            -half_inner_pen,
        )
        painter.drawRect(inner_rect)

    def enable_borders(self) -> None:
        """Enable border rendering."""
        self.show_borders = True

    def disable_borders(self) -> None:
        """Disable border rendering."""
        self.show_borders = False

    def set_border_width_percentage(self, percentage: float) -> None:
        """Set the border width percentage (default 0.015 = 1.5%)."""
        self.border_width_percentage = max(0.0, percentage)

    def set_minimum_border_width(self, width: int) -> None:
        """Set the minimum border width (default 1)."""
        self.minimum_border_width = max(0, width)


class BorderedPictographMixin:
    """
    Mixin class to add border functionality to Modern pictograph components.

    This mixin provides the same border functionality as Legacy's BorderedPictographView
    but designed for Modern's component architecture.
    """

    def __init__(self):
        self.border_manager = PictographBorderManager()

    def update_border_colors_for_letter_type(self, letter_type: LetterType) -> None:
        """Update border colors based on letter type."""
        self.border_manager.update_border_colors_for_letter_type(letter_type)
        if hasattr(self, "update"):
            self.update()  # Trigger repaint if this is a widget

    def set_gold_border(self) -> None:
        """Set border to gold color, typically on hover."""
        self.border_manager.set_gold_border()
        if hasattr(self, "update"):
            self.update()

    def reset_border_colors(self) -> None:
        """Reset border colors to original values."""
        self.border_manager.reset_border_colors()
        if hasattr(self, "update"):
            self.update()

    def enable_borders(self) -> None:
        """Enable border rendering."""
        self.border_manager.enable_borders()
        if hasattr(self, "update"):
            self.update()

    def disable_borders(self) -> None:
        """Disable border rendering."""
        self.border_manager.disable_borders()
        if hasattr(self, "update"):
            self.update()

    def get_border_adjusted_size(self, target_size: int) -> int:
        """Get size adjusted for border width."""
        return self.border_manager.get_border_adjusted_size(target_size)

    def calculate_border_width(self, size: int) -> int:
        """Calculate border width for given size."""
        return self.border_manager.calculate_border_width(size)

    def draw_pictograph_borders(
        self, painter: QPainter, viewport_rect, view_width: int
    ) -> None:
        """Draw borders on the pictograph viewport."""
        self.border_manager.draw_borders(painter, viewport_rect, view_width)
