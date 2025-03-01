from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QRectF, QByteArray
from PyQt6.QtGui import (
    QPainter,
    QColor,
    QCursor,
    QBrush,
    QLinearGradient,
    QPen,
)
from PyQt6.QtWidgets import QAbstractButton
from PyQt6.QtSvg import QSvgRenderer

from data.constants import BLUE, RED

if TYPE_CHECKING:
    from ..turns_widget import TurnsWidget


class AdjustTurnsButton(QAbstractButton):
    def __init__(self, svg_path, turns_widget: "TurnsWidget") -> None:
        super().__init__(turns_widget)
        self.svg_path = svg_path
        self.turns_widget = turns_widget
        self.turns_box = self.turns_widget.turns_box
        self.svg_renderer = QSvgRenderer(svg_path)
        self.hovered = False
        self.pressed = False
        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())
        if self.pressed:
            gradient.setColorAt(0.0, QColor("#d3d3d3"))
            gradient.setColorAt(1.0, QColor("#a9a9a9"))
        else:
            gradient.setColorAt(0.0, QColor("white"))
            gradient.setColorAt(1.0, QColor("#f0f0f0"))

        painter.fillRect(self.rect(), QBrush(gradient))
        turns_box_color = self.turns_widget.turns_box.color
        if turns_box_color == RED:
            border_color = "#ED1C24"
        elif turns_box_color == BLUE:
            border_color = "#2E3192"
        else:
            border_color = "black"

        if self.isEnabled():
            if self.hovered or self.pressed:
                painter.setPen(QPen(QColor(f"{border_color}"), 5))
            else:
                painter.setPen(QPen(QColor("black"), 2))
            painter.drawRect(self.rect().adjusted(1, 1, -1, -1))

        icon_size = int(min(self.width(), self.height()) * 0.9)
        x = (self.width() - icon_size) / 2
        y = (self.height() - icon_size) / 2
        icon_rect = QRectF(x, y, icon_size, icon_size)
        self.svg_renderer.render(painter, icon_rect)
        painter.end()
        
    def mousePressEvent(self, event):
        self.pressed = True
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.update()
        super().mouseReleaseEvent(event)

    def enterEvent(self, event) -> None:
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.hovered = True
        self.update()

    def leaveEvent(self, event) -> None:
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.hovered = False
        self.update()

    def setEnabled(self, enabled) -> None:
        super().setEnabled(enabled)
        svgData = QByteArray()
        with open(self.svg_path, "r") as file:
            svgData = QByteArray(file.read().encode("utf-8"))

        if not enabled:
            svgData.replace(b"black", b"#b5b5b5")

        self.svg_renderer.load(svgData)
        self.update()

    def resizeEvent(self, event) -> None:
        size = int(self.turns_box.graph_editor.height() * 0.25)
        self.setMaximumWidth(size)
        self.setMaximumHeight(size)
        super().resizeEvent(event)