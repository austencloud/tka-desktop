# sparkle_manager.py

import random
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt


class SparkleManager:
    def __init__(self, num_sparkles=50):
        self.sparkles = self.create_sparkles(num_sparkles)

    def create_sparkles(self, num_sparkles):
        """Create initial sparkles with random positions and properties."""
        return [
            {
                "x": random.uniform(0, 1),
                "y": random.uniform(0, 1),
                "size": random.uniform(2, 4),
                "opacity": random.uniform(0.5, 1.0),
                "pulse_speed": random.uniform(0.005, 0.015),
            }
            for _ in range(num_sparkles)
        ]

    def animate(self):
        """Animate sparkles by updating their opacity."""
        for sparkle in self.sparkles:
            sparkle["opacity"] += sparkle["pulse_speed"]
            if sparkle["opacity"] > 1.0 or sparkle["opacity"] < 0.5:
                sparkle["pulse_speed"] *= -1  # Reverse the pulse direction

    def draw(self, widget, painter: QPainter):
        """Draw sparkles on the widget using the painter."""
        for sparkle in self.sparkles:
            x = int(sparkle["x"] * widget.width())
            y = int(sparkle["y"] * widget.height())
            size = int(sparkle["size"])
            opacity = sparkle["opacity"]

            painter.setOpacity(opacity)
            painter.setBrush(QColor(255, 255, 255, int(opacity * 255)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(x, y, size, size)

        painter.setOpacity(1.0)  # Reset opacity
