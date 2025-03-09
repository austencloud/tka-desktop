

# === turns_box/ui/buttons/adjust_turns_button.py ===
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QRectF, QByteArray
from PyQt6.QtGui import QPainter, QColor, QCursor, QPen
from PyQt6.QtSvg import QSvgRenderer

from styles.styled_button import StyledButton
from data.constants import NO_ROT, RED, BLUE

if TYPE_CHECKING:
    from ..turns_widget import TurnsWidget


class AdjustTurnsButton(StyledButton):
    """Button for adjusting turns values (increment/decrement)"""

    def __init__(self, svg_path: str, turns_widget: "TurnsWidget") -> None:
        super().__init__(turns_widget)
        self.svg_path = svg_path
        self.turns_widget = turns_widget
        self.turns_box = self.turns_widget.turns_box
        self.svg_renderer = QSvgRenderer(svg_path)
        self.hovered = False
        self.pressed = False

        # Setup
        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

    def paintEvent(self, event) -> None:
        """Custom paint event for better visual feedback"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw hover effect
        if self.hovered and self.isEnabled():
            painter.fillRect(self.rect(), QColor(255, 255, 255, 80))

        # Get color based on turns box color
        turns_box_color = self.turns_widget.turns_box.color
        border_color = (
            "#ED1C24"
            if turns_box_color == RED
            else "#2E3192" if turns_box_color == BLUE else "black"
        )

        # Draw border based on button state
        if self.isEnabled():
            if self.hovered:
                painter.setPen(QPen(QColor("white"), 4))
            elif self.pressed:
                painter.setPen(QPen(QColor(border_color), 5))
            else:
                painter.setPen(QPen(QColor("black"), 2))

        # Draw SVG icon
        icon_size = int(min(self.width(), self.height()) * 0.9)
        x = (self.width() - icon_size) / 2
        y = (self.height() - icon_size) / 2
        icon_rect = QRectF(x, y, icon_size, icon_size)
        self.svg_renderer.render(painter, icon_rect)
        painter.end()

    def mousePressEvent(self, event) -> None:
        """Handle mouse press events"""
        self.pressed = True
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        """Handle mouse release events"""
        self.pressed = False
        self.update()
        super().mouseReleaseEvent(event)

    def enterEvent(self, event) -> None:
        """Handle mouse enter events"""
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.hovered = True
        self.update()

    def leaveEvent(self, event) -> None:
        """Handle mouse leave events"""
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.hovered = False
        self.update()

    def setEnabled(self, enabled: bool) -> None:
        """Override setEnabled to customize SVG color"""
        super().setEnabled(enabled)

        # Update SVG color based on enabled state
        svg_data = QByteArray()
        with open(self.svg_path, "r") as file:
            svg_data = QByteArray(file.read().encode("utf-8"))

        if not enabled:
            svg_data.replace(b"black", b"gray")

        self.svg_renderer.load(svg_data)
        self.update()

    def resizeEvent(self, event) -> None:
        """Handle resize events"""
        size = int(self.turns_box.graph_editor.height() * 0.3)
        self.setMaximumWidth(size)
        self.setMaximumHeight(size)
        super().resizeEvent(event)

