import random
import math
from PyQt6.QtGui import QColor, QPainter, QPainterPath
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt


# StarManager: Manages stars, including different shapes and twinkling behavior
class StarManager:
    def __init__(self):
        self.stars = [
            {
                "x": random.random(),
                "y": random.random(),
                "size": random.random() * 2 + 1,
                "color": random.choice([QColor(255, 255, 255), QColor(255, 255, 0)]),
                "spikiness": random.choice(
                    [0, 1, 2]
                ),  # 0: round, 1: star shape, 2: spiky
            }
            for _ in range(100)
        ]
        self.twinkle_state = [random.uniform(0.8, 1.0) for _ in range(100)]  # Twinkle

    def animate_stars(self):
        # Update twinkle state
        self.twinkle_state = [random.uniform(0.8, 1.0) for _ in range(len(self.stars))]

    def draw_stars(self, painter: QPainter, widget: QWidget):
        for i, star in enumerate(self.stars):
            x = int(star["x"] * widget.width())
            y = int(star["y"] * widget.height())
            size = int(star["size"] * (1 if self.twinkle_state[i] < 0.95 else 1.5))

            painter.setBrush(star["color"])
            painter.setPen(Qt.PenStyle.NoPen)
            if star["spikiness"] == 0:  # Round stars
                painter.drawEllipse(x, y, size, size)
            elif star["spikiness"] == 1:  # Star-shaped stars
                self.draw_star_shape(painter, x, y, size)
            else:  # Spiky stars
                self.draw_spiky_star(painter, x, y, size)

    def draw_star_shape(self, painter, x, y, size):
        path = QPainterPath()
        radius = size / 2
        angle_step = math.pi / 3  # 6 points

        for i in range(6):
            angle = i * angle_step
            x1 = x + radius * math.cos(angle)
            y1 = y + radius * math.sin(angle)
            path.moveTo(x, y)
            path.lineTo(x1, y1)

        painter.setPen(QColor(255, 255, 255))
        painter.drawPath(path)

    def draw_spiky_star(self, painter, x, y, size):
        path = QPainterPath()
        radius = size / 2
        small_radius = radius * 0.6
        angle_step = math.pi / 6  # 12 points

        for i in range(12):
            angle = i * angle_step
            r = radius if i % 2 == 0 else small_radius
            x1 = x + r * math.cos(angle)
            y1 = y + r * math.sin(angle)
            if i == 0:
                path.moveTo(x1, y1)
            else:
                path.lineTo(x1, y1)
        path.closeSubpath()

        painter.setPen(QColor(255, 255, 255))
        painter.drawPath(path)
