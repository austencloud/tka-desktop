import math
from typing import TYPE_CHECKING
from PyQt6.QtGui import (
    QPainter,
    QPen,
    QFont,
    QFontMetrics,
    QColor,
    QImage,
    QPolygon,
    QLinearGradient,
)
from PyQt6.QtCore import QRect, Qt, QPoint
from numpy import diff
from PyQt6.QtCore import QPointF

from main_window.main_widget.sequence_workbench.sequence_beat_frame.image_export_manager.image_creator.difficult_level_gradients import DifficultyLevelGradients

if TYPE_CHECKING:
    from ..image_creator.image_creator import ImageCreator



class DifficultyLevelDrawer:
    def __init__(self):
        # Use the gradients I painstakingly crafted.
        self.gradients = DifficultyLevelGradients()

    def draw_difficulty_level(
        self, image: QImage, difficulty_level: int, additional_height_top: int
    ):
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        shape_size = int(additional_height_top * 0.75)
        inset_left = additional_height_top // 8
        inset_top = additional_height_top // 8
        rect = QRect(inset_left, inset_top, shape_size, shape_size)

        pen = QPen(Qt.GlobalColor.black, max(1, additional_height_top // 50))
        painter.setPen(pen)

        gradient = self.gradients.get_gradient(rect, difficulty_level)
        painter.setBrush(gradient)

        self._draw_shape(painter, rect, difficulty_level)
        self._draw_text(painter, rect, difficulty_level)

        painter.end()

    def _draw_shape(self, painter: QPainter, rect: QRect, difficulty_level: int):
        self._draw_circle(painter, rect)

    def _draw_circle(self, painter: QPainter, rect: QRect):
        painter.drawEllipse(rect)

    def _draw_triangle(self, painter: QPainter, rect: QRect):
        top = QPoint(rect.center().x(), rect.top())
        bottom_left = QPoint(rect.left(), rect.bottom())
        bottom_right = QPoint(rect.right(), rect.bottom())
        triangle = QPolygon([top, bottom_left, bottom_right])
        painter.drawPolygon(triangle)

    def _draw_star(self, painter: QPainter, rect: QRect):
        center_x, center_y = rect.center().x(), rect.center().y()

        scale_factor = 1.3
        radius_outer = int((rect.width() // 2) * scale_factor)
        radius_inner = int(radius_outer / 2.5)

        points = []
        for i in range(10):
            angle = (i * 36 - 90) * (math.pi / 180.0)
            radius = radius_outer if i % 2 == 0 else radius_inner
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))
            points.append(QPoint(x, y))

        star = QPolygon(points)
        painter.drawPolygon(star)

    def _draw_text(self, painter: QPainter, rect: QRect, difficulty_level: int):
        font_size = int(rect.height() // 2)
        font = QFont("Georgia", font_size, QFont.Weight.Bold)
        painter.setFont(font)
        metrics = QFontMetrics(font)

        text = str(difficulty_level)

        bounding_rect = metrics.boundingRect(text)

        text_x = rect.center().x() - bounding_rect.width() // 2
        text_y = rect.center().y() - bounding_rect.height() // 2

        x_offset = 0
        y_offset = 0

        y_offset -= 15

        bounding_rect.moveTopLeft(QPoint(text_x + x_offset, text_y + y_offset))

        painter.setPen(Qt.GlobalColor.black)

        painter.drawText(bounding_rect, Qt.AlignmentFlag.AlignLeft, text)
