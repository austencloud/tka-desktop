from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from utils.path_helpers import get_images_and_data_path
from PyQt6.QtGui import QPixmap


class MoonManager:
    def __init__(self):
        moon_image_path = get_images_and_data_path("images/backgrounds/moon.png")
        self.moon_image = QPixmap(moon_image_path)

    def draw_moon(self, painter: QPainter, widget: QWidget):
        moon_size = int(min(widget.width(), widget.height()) * 0.15)
        x = int(widget.width() * 0.9)
        y = int(widget.height() * 0.03)

        moon_scaled = self.moon_image.scaled(
            moon_size,
            moon_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        painter.drawPixmap(x, y, moon_scaled)
