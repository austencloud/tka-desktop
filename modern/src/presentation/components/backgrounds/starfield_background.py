from .base_background import BaseBackground
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget
import random


class StarfieldBackground(BaseBackground):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stars = []
        self._initialize_stars()

    def _initialize_stars(self):
        """Initialize stars with random positions and properties."""
        self.stars = [
            {
                "x": random.uniform(0, 1),
                "y": random.uniform(0, 1),
                "size": random.uniform(1, 3),
                "opacity": random.uniform(0.3, 1.0),
                "twinkle_speed": random.uniform(0.01, 0.03),
            }
            for _ in range(200)
        ]

    def animate_background(self):
        # Animate star twinkling
        for star in self.stars:
            star["opacity"] += star["twinkle_speed"]
            if star["opacity"] > 1.0 or star["opacity"] < 0.3:
                star["twinkle_speed"] *= -1  # Reverse the twinkle direction

        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Paint black background
        painter.fillRect(widget.rect(), QColor(0, 0, 0))

        # Paint stars
        for star in self.stars:
            x = int(star["x"] * widget.width())
            y = int(star["y"] * widget.height())
            size = int(star["size"])
            opacity = star["opacity"]

            painter.setOpacity(opacity)
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(QColor(255, 255, 255))
            painter.drawEllipse(x, y, size, size)

        painter.setOpacity(1.0)  # Reset opacity
