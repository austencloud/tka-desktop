import random
import math
from PyQt6.QtGui import QColor, QPainter, QPainterPath
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt


class SnowflakeManager:
    def __init__(self):
        self.snowflakes = [
            {
                "x": random.uniform(0, 1),
                "y": random.uniform(0, 1),
                "speed": random.uniform(0.001, 0.005),
                "size": random.uniform(2, 5) * (2 if random.random() < 0.2 else 1),
                "sway": random.uniform(-0.001, 0.001),
                "opacity": random.uniform(0.6, 1.0),
                "twinkle_factor": random.uniform(0.98, 1.02),
                "is_special": random.random() < 0.7,
                "snowflake_type": random.choice([1, 2, 3]),
            }
            for _ in range(200)
        ]
        self.wind = 0.0002
        self.wind_direction_change = 0.00001

    def animate_snowflakes(self):
        for flake in self.snowflakes:
            flake["y"] += flake["speed"]
            flake["x"] += flake["sway"] + self.wind

            flake["opacity"] *= flake["twinkle_factor"]
            flake["opacity"] = max(0.6, min(flake["opacity"], 1.0))

            if flake["y"] > 1:
                flake.update(
                    {
                        "y": 0,
                        "x": random.uniform(0, 1),
                        "speed": random.uniform(0.001, 0.005),
                        "size": random.uniform(2, 5)
                        * (2 if random.random() < 0.2 else 1),
                        "sway": random.uniform(-0.001, 0.001),
                        "opacity": random.uniform(0.6, 1.0),
                        "is_special": random.random() < 0.5,
                        "snowflake_type": random.choice([1, 2, 3]),
                    }
                )

            flake["x"] = flake["x"] % 1.0

        self.wind += random.uniform(
            -self.wind_direction_change, self.wind_direction_change
        )
        self.wind = max(-0.002, min(self.wind, 0.002))

    def draw_snowflakes(self, painter: QPainter, widget: QWidget):
        painter.save()
        try:
            for flake in self.snowflakes:
                x = int(flake["x"] * widget.width())
                y = int(flake["y"] * widget.height())
                size = int(flake["size"])

                painter.setOpacity(flake["opacity"])
                painter.setBrush(QColor(255, 255, 255, int(flake["opacity"] * 255)))
                painter.setPen(Qt.PenStyle.NoPen)

                if flake["is_special"]:
                    if flake["snowflake_type"] == 1:
                        self.draw_star_snowflake(painter, x, y, size)
                    elif flake["snowflake_type"] == 2:
                        self.draw_spiky_snowflake(painter, x, y, size)
                    elif flake["snowflake_type"] == 3:
                        self.draw_spiky_snowflake_variant(painter, x, y, size)
                else:
                    painter.drawEllipse(x, y, size, size)
        finally:
            painter.restore()

    def draw_star_snowflake(self, painter: QPainter, x, y, size):
        path = QPainterPath()
        radius = size / 2
        angle_step = math.pi / 8
        for i in range(16):
            angle = i * angle_step
            x1 = x + radius * math.cos(angle)
            y1 = y + radius * math.sin(angle)
            path.moveTo(x, y)
            path.lineTo(x1, y1)
        painter.setPen(QColor(255, 255, 255))
        painter.drawPath(path)

    def draw_spiky_snowflake(self, painter: QPainter, x, y, size):
        path = QPainterPath()
        radius = size / 2
        small_radius = radius * 0.3
        angle_step = math.pi / 10
        for i in range(20):
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

    def draw_spiky_snowflake_variant(self, painter: QPainter, x, y, size):
        path = QPainterPath()
        radius = size / 2
        small_radius = radius * 0.2
        angle_step = 2 * math.pi / 18
        for i in range(18):
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
