import math
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QEvent, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QCursor

from data.constants import GOLD
from enums.letter.letter_type import LetterType
from base_widgets.pictograph.elements.views.base_pictograph_view import (
    BasePictographView,
)

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class BorderedPictographView(BasePictographView):
    def __init__(self, pictograph: "LegacyPictograph") -> None:
        super().__init__(pictograph)
        self.primary_color = None
        self.secondary_color = None
        self.original_primary_color = None
        self.original_secondary_color = None
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.update_borders()

    ### BORDER METHODS ###

    def update_borders(self):
        """Initialize or update the border colors based on the pictograph's letter type."""
        letter_type = self.pictograph.state.letter_type
        border_colors_map = {
            LetterType.Type1: ("#36c3ff", "#6F2DA8"),  # Cyan, Purple
            LetterType.Type2: ("#6F2DA8", "#6F2DA8"),  # Purple, Purple
            LetterType.Type3: ("#26e600", "#6F2DA8"),  # Green, Purple
            LetterType.Type4: ("#26e600", "#26e600"),  # Green, Green
            LetterType.Type5: ("#00b3ff", "#26e600"),  # Cyan, Green
            LetterType.Type6: ("#eb7d00", "#eb7d00"),  # Orange, Orange
        }
        self.primary_color, self.secondary_color = border_colors_map.get(
            letter_type, ("black", "black")
        )
        self.original_primary_color = self.primary_color
        self.original_secondary_color = self.secondary_color

    def set_gold_border(self):
        """Set the border colors to gold, typically on hover."""
        if getattr(self.pictograph.state, "disable_gold_overlay", False):
            return
        self.primary_color = GOLD
        self.secondary_color = GOLD
        self.update()

    def reset_border(self):
        """Reset the border colors to their original values."""
        self.primary_color = self.original_primary_color
        self.secondary_color = self.original_secondary_color
        self.update()

    def update_border_widths(self) -> None:
        view_width = self.size().width()
        self.outer_border_width = max(1, math.ceil(view_width * 0.016))
        self.inner_border_width = max(1, math.ceil(view_width * 0.016))
        self.update()

    ### EVENTS ###

    def paintEvent(self, event):
        """Draw the pictograph and borders."""
        super().paintEvent(event)
        painter = QPainter(self.viewport())

        # Check if borders should be disabled
        if (
            hasattr(self.pictograph.state, "disable_borders")
            and self.pictograph.state.disable_borders
        ):
            # Skip drawing borders
            pass
        elif self.primary_color and self.secondary_color:
            self._draw_borders(painter)

        painter.end()

    def _draw_borders(self, painter: QPainter):
        """Draw the outer and inner borders."""
        pen = QPen()

        # Use floating-point calculations
        view_width = self.viewport().size().width()
        outer_border_width = max(1.0, view_width * 0.016)
        inner_border_width = max(1.0, view_width * 0.016)

        # Calculate half pen widths
        half_outer_pen = outer_border_width / 2.0
        half_inner_pen = inner_border_width / 2.0

        # Draw outer border
        pen.setColor(QColor(self.primary_color))
        pen.setWidthF(outer_border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        # Convert viewport rect to QRectF
        outer_rect = QRectF(self.viewport().rect())
        outer_rect = outer_rect.adjusted(
            +half_outer_pen,
            +half_outer_pen,
            -half_outer_pen,
            -half_outer_pen,
        )
        painter.drawRect(outer_rect)

        # Draw inner border
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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setSceneRect(self.scene().itemsBoundingRect())
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.update_border_widths()

    def enterEvent(self, event: QEvent) -> None:
        self.set_gold_border()

    def leaveEvent(self, event: QEvent) -> None:
        self.reset_border()
