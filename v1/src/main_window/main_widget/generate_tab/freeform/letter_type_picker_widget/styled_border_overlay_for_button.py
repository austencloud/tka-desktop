from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen


if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.legacy_beat_frame.button_styled_border_overlay import (
        LetterTypeButton,
    )


class StyledBorderOverlayForButton(QWidget):
    def __init__(self, button: "LetterTypeButton"):
        super().__init__(button)
        self.parent_button = button
        self.is_set = False
        self.primary_color = None
        self.secondary_color = None
        self.outer_border_width = 4
        self.inner_border_width = 4
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def update_border_colors(self, primary_color: str, secondary_color: str):
        self.primary_color = primary_color
        self.secondary_color = (
            secondary_color if primary_color != secondary_color else "transparent"
        )
        self.is_set = True
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.is_set or not self.primary_color or not self.secondary_color:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        # Outer border
        outer_rect = self.rect().adjusted(
            self.outer_border_width // 2,
            self.outer_border_width // 2,
            -self.outer_border_width // 2,
            -self.outer_border_width // 2,
        )
        pen = QPen()
        pen.setColor(QColor(self.primary_color))
        pen.setWidth(self.outer_border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)
        painter.drawRect(outer_rect)

        # Inner border
        inner_rect = outer_rect.adjusted(
            self.inner_border_width,
            self.inner_border_width,
            -self.inner_border_width,
            -self.inner_border_width,
        )
        pen.setColor(QColor(self.secondary_color))
        pen.setWidth(self.inner_border_width)
        painter.setPen(pen)
        painter.drawRect(inner_rect)
        painter.end()
