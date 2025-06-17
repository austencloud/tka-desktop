from PyQt6.QtGui import QLinearGradient, QColor, QPainter
from PyQt6.QtWidgets import QWidget
import math

from .aurora.blob_manager import BlobManager
from .aurora.sparkle_manager import SparkleManager
from .base_background import BaseBackground


class AuroraBackground(BaseBackground):
    def __init__(self, parent=None) -> None:
        super().__init__(parent or QWidget())
        self.gradient_shift = 0
        self.color_shift = 0
        self.wave_phase = 0  # Phase of sine wave for wavy gradient effect

        # Initialize the SparkleManager and BlobManager
        self.sparkle_manager = SparkleManager()
        self.blob_manager = BlobManager()

    def animate_background(self) -> None:
        self.gradient_shift += 0.01
        self.color_shift = (self.color_shift + 2) % 360
        self.wave_phase += 0.02  # Gradually move the wave phase

        # Animate sparkles and blobs
        self.sparkle_manager.animate()
        self.blob_manager.animate()

        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw a wavy gradient background
        gradient = QLinearGradient(0, widget.height(), widget.width(), 0)

        # Add a sine wave effect to the gradient position
        colors = [(255, 0, 255, 100), (0, 255, 255, 100), (255, 255, 0, 100)]
        for i, (r, g, b, a) in enumerate(colors):
            hue = int((self.color_shift + i * 120) % 360)
            color = QColor.fromHsv(hue, 255, 255, a)

            # Apply sine wave to adjust gradient positioning
            wave_shift = 0.1 * math.sin(self.wave_phase + i * 2 * math.pi / len(colors))
            position = min(max(i / len(colors) + wave_shift, 0), 1)
            gradient.setColorAt(position, color)

        painter.fillRect(widget.rect(), gradient)

        # Draw blobs and sparkles
        self.blob_manager.draw(widget, painter)
        self.sparkle_manager.draw(widget, painter)
