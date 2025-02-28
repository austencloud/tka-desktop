import math
from typing import TYPE_CHECKING
from PyQt6.QtGui import QPainter, QPen, QFont, QFontMetrics, QColor, QImage, QPolygon
from PyQt6.QtCore import QRect, Qt, QPoint

if TYPE_CHECKING:
    from ..image_creator.image_creator import ImageCreator


class DifficultyLevelDrawer:
    def __init__(self, image_creator: "ImageCreator"):
        self.image_creator = image_creator

    def draw_difficulty_level(
        self, image: QImage, difficulty_level: int, additional_height_top: int
    ):
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        shape_size = int(additional_height_top * 0.75)
        inset_left = additional_height_top // 4
        inset_top = additional_height_top // 8
        rect = QRect(inset_left, inset_top, shape_size, shape_size)

        pen = QPen(Qt.GlobalColor.black, max(1, additional_height_top // 50))
        painter.setPen(pen)

        # Define colors for different difficulty levels (like a traffic light).
        if difficulty_level == 1:
            brush_color = QColor(0, 255, 0)  # Green for easy
        elif difficulty_level == 2:
            brush_color = QColor(255, 255, 0)  # Yellow for medium
        elif difficulty_level == 3:
            brush_color = QColor(255, 0, 0)  # Red for hard
        else:
            brush_color = (
                Qt.GlobalColor.white
            )  # Default to white if the level is invalid

        painter.setBrush(brush_color)

        # Draw different shapes based on the difficulty level
        if difficulty_level == 1:
            self._draw_circle(painter, rect)
        elif difficulty_level == 2:
            self._draw_triangle(painter, rect)
        elif difficulty_level == 3:
            self._draw_star(painter, rect)

        # Draw difficulty level number inside the shape
        self._draw_text(painter, rect, difficulty_level)

        painter.end()

    def _draw_circle(self, painter: QPainter, rect: QRect):
        """Draws a circle inside the given rectangle."""
        painter.drawEllipse(rect)

    def _draw_triangle(self, painter: QPainter, rect: QRect):
        """Draws an equilateral triangle inside the given rectangle."""
        top = QPoint(rect.center().x(), rect.top())  # Top vertex
        bottom_left = QPoint(rect.left(), rect.bottom())  # Bottom-left vertex
        bottom_right = QPoint(rect.right(), rect.bottom())  # Bottom-right vertex
        triangle = QPolygon([top, bottom_left, bottom_right])
        painter.drawPolygon(triangle)

    def _draw_star(self, painter: QPainter, rect: QRect):
        """Draws a 5-pointed star inside the given rectangle."""
        center_x, center_y = rect.center().x(), rect.center().y()

        # Increase the size of the star by scaling both radii
        scale_factor = 1.3  # Adjust this value to make the star bigger
        radius_outer = int((rect.width() // 2) * scale_factor)
        radius_inner = int(radius_outer / 2.5)  # Maintain the ratio

        points = []
        for i in range(10):
            angle = (i * 36 - 90) * (
                math.pi / 180.0
            )  # -90° ensures the top point is facing North
            radius = radius_outer if i % 2 == 0 else radius_inner
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))
            points.append(QPoint(x, y))

        star = QPolygon(points)
        painter.drawPolygon(star)

    def _draw_text(self, painter: QPainter, rect: QRect, difficulty_level: int, move_up=False):
        """Draws the difficulty level number inside the shape with an option to move it slightly up."""
        font_size = int(rect.height() // 2)
        font = QFont("Georgia", font_size, QFont.Weight.Bold)
        painter.setFont(font)
        metrics = QFontMetrics(font)

        text = str(difficulty_level)
        bounding_rect = metrics.boundingRect(rect, Qt.AlignmentFlag.AlignCenter, text)
        
        # Move text slightly up if requested
        if move_up:
            bounding_rect.translate(0, -rect.height() // 10)  # Adjust this value for fine-tuning

        bounding_rect.moveCenter(rect.center())

        painter.setPen(Qt.GlobalColor.black)  # Ensure text is always visible
        painter.drawText(bounding_rect, Qt.AlignmentFlag.AlignCenter, text)
