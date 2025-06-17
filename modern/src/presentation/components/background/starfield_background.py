from PyQt6.QtGui import QColor, QPainter, QLinearGradient
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, pyqtSignal
import random
import math


class StarfieldBackground:
    def __init__(self, widget: QWidget):
        self.widget = widget
        self.stars = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_background)
        self._generate_stars()

    def _generate_stars(self):
        self.stars = []
        for _ in range(150):
            star = {
                "x": random.randint(0, self.widget.width()),
                "y": random.randint(0, self.widget.height()),
                "brightness": random.uniform(0.3, 1.0),
                "twinkle_speed": random.uniform(0.02, 0.08),
            }
            self.stars.append(star)

    def paint_background(self, widget: QWidget, painter: QPainter):
        # Draw deep space gradient
        gradient = QLinearGradient(0, 0, 0, widget.height())
        gradient.setColorAt(0, QColor("#000814"))
        gradient.setColorAt(0.5, QColor("#001d3d"))
        gradient.setColorAt(1, QColor("#003566"))
        painter.fillRect(widget.rect(), gradient)

        # Draw stars
        for star in self.stars:
            alpha = int(star["brightness"] * 255)
            color = QColor(255, 255, 255, alpha)
            painter.setPen(color)
            painter.drawPoint(int(star["x"]), int(star["y"]))

    def animate_background(self):
        for star in self.stars:
            star["brightness"] += star["twinkle_speed"]
            if star["brightness"] > 1.0 or star["brightness"] < 0.3:
                star["twinkle_speed"] *= -1
        self.widget.update()

    def stop_animation(self):
        self.timer.stop()
