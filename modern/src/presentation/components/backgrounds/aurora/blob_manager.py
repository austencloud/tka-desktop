import random
from PyQt6.QtGui import QPainter, QColor, QPainterPath
from PyQt6.QtCore import Qt


class BlobManager:
    def __init__(self, num_blobs=3):
        self.blobs = self.create_blobs(num_blobs)

    def create_blobs(self, num_blobs):
        """Create initial blobs with random positions and properties."""
        return [
            {
                "x": random.uniform(0.1, 0.9),
                "y": random.uniform(0.1, 0.9),
                "size": random.uniform(100, 200),
                "opacity": random.uniform(0.2, 0.5),
                "dx": random.uniform(-0.0005, 0.0005),
                "dy": random.uniform(-0.0005, 0.0005),
                "dsize": random.uniform(-0.1, 0.1),
                "dopacity": random.uniform(-0.001, 0.001),
            }
            for _ in range(num_blobs)
        ]

    def animate(self):
        """Animate blobs by updating their position, size, and opacity."""
        for blob in self.blobs:
            blob["x"] += blob["dx"]
            blob["y"] += blob["dy"]
            blob["size"] += blob["dsize"]
            blob["opacity"] += blob["dopacity"]

            # Keep within bounds and reverse direction if necessary
            if blob["x"] < 0 or blob["x"] > 1:
                blob["dx"] *= -1
            if blob["y"] < 0 or blob["y"] > 1:
                blob["dy"] *= -1
            if blob["size"] < 50 or blob["size"] > 250:
                blob["dsize"] *= -1
            if blob["opacity"] < 0.1 or blob["opacity"] > 0.5:
                blob["dopacity"] *= -1

    def draw(self, widget, painter: QPainter):
        """Draw blobs on the widget using the painter."""
        for blob in self.blobs:
            blob_path = QPainterPath()
            blob_x = blob["x"] * widget.width()
            blob_y = blob["y"] * widget.height()
            blob_size = blob["size"]
            opacity = blob["opacity"]

            blob_path.addEllipse(blob_x, blob_y, blob_size, blob_size)

            painter.setOpacity(opacity)
            painter.setBrush(QColor(255, 255, 255, int(opacity * 255)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPath(blob_path)

        painter.setOpacity(1.0)  # Reset opacity
