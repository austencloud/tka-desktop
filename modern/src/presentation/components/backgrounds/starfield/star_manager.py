import random
import math
from PyQt6.QtGui import QColor, QPainter, QPainterPath
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

# A+ Enhancement: Import Qt resource pooling - Temporarily disabled
# try:
#     from core.qt_integration import qt_resources, pooled_pen, pooled_brush
#     QT_RESOURCES_AVAILABLE = True
# except ImportError:
#     QT_RESOURCES_AVAILABLE = False

# Temporary fallback
QT_RESOURCES_AVAILABLE = False


class StarManager:
    """
    Manages stars with different shapes and twinkling behavior.

    Creates a variety of star types including round stars, star-shaped stars,
    and spiky stars with realistic twinkling effects.
    """

    def __init__(self):
        # Create diverse star population
        self.stars = [
            {
                "x": random.random(),
                "y": random.random(),
                "size": random.random() * 2 + 1,
                "color": random.choice(
                    [
                        QColor(255, 255, 255),  # White stars
                        QColor(255, 255, 0),  # Yellow stars
                        QColor(255, 200, 200),  # Reddish stars
                        QColor(200, 200, 255),  # Bluish stars
                    ]
                ),
                "spikiness": random.choice(
                    [0, 1, 2]
                ),  # 0: round, 1: star shape, 2: spiky
                "twinkle_speed": random.uniform(0.5, 2.0),
                "twinkle_phase": random.uniform(0, 2 * math.pi),
            }
            for _ in range(150)  # More stars for richer sky
        ]

        # Initialize twinkle states
        self.twinkle_state = [random.uniform(0.8, 1.0) for _ in range(len(self.stars))]

    def animate_stars(self):
        """Update star twinkling animation."""
        for i, star in enumerate(self.stars):
            # Smooth twinkling using sine waves
            star["twinkle_phase"] += star["twinkle_speed"] * 0.1
            twinkle_intensity = (math.sin(star["twinkle_phase"]) + 1) / 2
            self.twinkle_state[i] = 0.6 + (twinkle_intensity * 0.4)  # Range: 0.6 to 1.0

    def draw_stars(self, painter: QPainter, widget: QWidget):
        """Draw all stars with their current twinkle states."""
        for i, star in enumerate(self.stars):
            x = int(star["x"] * widget.width())
            y = int(star["y"] * widget.height())

            # Apply twinkling to size and opacity
            twinkle = self.twinkle_state[i]
            size = int(star["size"] * (1 + twinkle * 0.5))

            # Set color with twinkling opacity
            color = QColor(star["color"])
            color.setAlphaF(twinkle)

            # A+ Enhancement: Use resource pooling - Temporarily disabled
            # if QT_RESOURCES_AVAILABLE:
            #     with pooled_brush(color) as brush:
            #         painter.setBrush(brush)
            #         painter.setPen(Qt.PenStyle.NoPen)
            # else:
            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)

            # Draw star based on its type
            if star["spikiness"] == 0:  # Round stars
                painter.drawEllipse(x - size // 2, y - size // 2, size, size)
            elif star["spikiness"] == 1:  # Star-shaped stars
                self._draw_star_shape(painter, x, y, size, color)
            else:  # Spiky stars
                self._draw_spiky_star(painter, x, y, size, color)

    def _draw_star_shape(
        self, painter: QPainter, x: int, y: int, size: int, color: QColor
    ):
        """Draw a classic 6-pointed star shape."""
        path = QPainterPath()
        radius = size / 2
        angle_step = math.pi / 3  # 6 points

        # Create star rays
        for i in range(6):
            angle = i * angle_step
            x1 = x + radius * math.cos(angle)
            y1 = y + radius * math.sin(angle)
            path.moveTo(x, y)
            path.lineTo(x1, y1)

        # A+ Enhancement: Use resource pooling - Temporarily disabled
        # if QT_RESOURCES_AVAILABLE:
        #     with pooled_pen(color, 1) as pen:
        #         painter.setPen(pen)
        #         painter.drawPath(path)
        # else:
        painter.setPen(color)
        painter.drawPath(path)

    def _draw_spiky_star(
        self, painter: QPainter, x: int, y: int, size: int, color: QColor
    ):
        """Draw a spiky multi-pointed star."""
        path = QPainterPath()
        radius = size / 2
        small_radius = radius * 0.6
        angle_step = math.pi / 6  # 12 points

        # Create alternating long and short points
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

        # A+ Enhancement: Use resource pooling - Temporarily disabled
        # if QT_RESOURCES_AVAILABLE:
        #     with pooled_brush(color) as brush:
        #         painter.setBrush(brush)
        #         painter.setPen(Qt.PenStyle.NoPen)
        #         painter.drawPath(path)
        # else:
        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)
