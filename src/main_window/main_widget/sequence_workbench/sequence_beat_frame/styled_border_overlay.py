from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QRect
from typing import TYPE_CHECKING

from data.constants import GOLD
from enums.letter.letter_type import LetterType

if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.base_pictograph_view import (
        BasePictographView,
    )
import math


class StyledBorderOverlay(QWidget):
    def __init__(self, view: "BasePictographView") -> None:
        super().__init__(view)
        self.view = view
        self.is_set = False
        self.primary_color = None
        self.secondary_color = None
        self.saved_primary_color = None
        self.saved_secondary_color = None
        self.setFixedSize(view.size())
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.border_colors_map = self._get_border_colors_map()
        self.setContentsMargins(0, 0, 0, 0)

    def _get_border_colors_map(self) -> dict[LetterType, tuple[str, str]]:
        border_colors_map = {
            LetterType.Type1: ("#36c3ff", "#6F2DA8"),  # Cyan, Purple
            LetterType.Type2: ("#6F2DA8", "#6F2DA8"),  # Purple, Purple
            LetterType.Type3: ("#26e600", "#6F2DA8"),  # Green, Purple
            LetterType.Type4: ("#26e600", "#26e600"),  # Green, Green
            LetterType.Type5: ("#00b3ff", "#26e600"),  # Cyan, Green
            LetterType.Type6: ("#eb7d00", "#eb7d00"),  # Orange, Orange
        }
        return border_colors_map

    def get_border_colors(self) -> tuple[str, str]:
        letter_type = self.view.pictograph.state.letter_type
        return self.border_colors_map.get(letter_type, ("black", "black"))

    def update_border_widths(self) -> None:
        view_width = self.view.size().width()
        self.outer_border_width = max(1, math.ceil(view_width * 0.016))
        self.inner_border_width = max(1, math.ceil(view_width * 0.016))
        self.update()

    def update_border_color_and_width(self, primary_color, secondary_color) -> None:
        self.update_border_widths()
        self.primary_color = primary_color
        self.secondary_color = (
            secondary_color if primary_color != secondary_color else "transparent"
        )
        self.is_set = True
        self.update()

    def _draw_borders(self, painter: QPainter) -> None:
        pen = QPen()
        outer_border = self._draw_outer_border(painter, pen)
        self._draw_inner_border(painter, pen, outer_border)

    def _draw_inner_border(
        self, painter: QPainter, pen: QPen, outer_rect: QRect
    ) -> None:
        pen.setColor(QColor(self.secondary_color))
        pen.setWidth(self.inner_border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        # Adjust the rectangle by half the pen width
        half_pen_width = int(self.inner_border_width / 2)
        inner_rect = outer_rect.adjusted(
            half_pen_width,
            half_pen_width,
            -half_pen_width,
            -half_pen_width,
        )
        painter.drawRect(inner_rect)

    def _draw_outer_border(self, painter: QPainter, pen: QPen) -> QRect:
        pen.setColor(QColor(self.primary_color))
        pen.setWidth(self.outer_border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        # Adjust the rectangle by half the pen width
        half_pen_width = int(self.outer_border_width / 2)
        outer_rect = self.rect().adjusted(
            half_pen_width,
            half_pen_width,
            -half_pen_width,
            -half_pen_width,
        )
        painter.drawRect(outer_rect)
        return outer_rect

    def set_gold_border(self) -> None:
        # Add a condition to skip setting the gold border when in quiz mode
        if getattr(self.view.pictograph.state, "disable_gold_overlay", True):
            # If in quiz mode, don't apply the gold border
            return
        self.saved_primary_color = self.primary_color
        self.saved_secondary_color = self.secondary_color
        self.update_border_color_and_width(GOLD, GOLD)

    def reset_border(self) -> None:
        if self.saved_primary_color and self.saved_secondary_color:
            self.update_border_color_and_width(
                self.saved_primary_color, self.saved_secondary_color
            )

    def set_thick_gold_border(self) -> None:
        self.saved_primary_color = self.primary_color
        self.saved_secondary_color = self.secondary_color
        self.update_border_color_and_width(GOLD, GOLD)

    def remove_border(self) -> None:
        self.is_set = False
        self.update()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.setFixedSize(self.view.width(), self.view.height())
        self.update_border_widths()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        if self.primary_color and self.secondary_color:
            painter = QPainter(self)
            self._draw_borders(painter)
            painter.end()

    def update_borders(self) -> None:
        primary_color, secondary_color = self.get_border_colors()
        self.update_border_color_and_width(primary_color, secondary_color)
        self.update()
