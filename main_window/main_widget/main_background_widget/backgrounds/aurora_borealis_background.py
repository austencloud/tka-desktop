import math
import random

from PyQt6.QtGui import QLinearGradient, QColor, QPainter

from PyQt6.QtWidgets import QWidget

from .base_background import BaseBackground


class AuroraBorealisBackground(BaseBackground):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.light_waves = [random.random() * 2 * math.pi for _ in range(10)]

    def animate_background(self):
        # Update light waves positions
        self.light_waves = [x + 0.01 for x in self.light_waves]
        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        gradient = QLinearGradient(0, 0, widget.width(), widget.height())
        colors = [(0, 25, 50, 100), (0, 50, 100, 50), (0, 100, 150, 25)]
        for i, wave in enumerate(self.light_waves):
            pos = (math.sin(wave) + 1) / 2
            color = QColor(*colors[i % len(colors)])
            gradient.setColorAt(pos, color)
        painter.fillRect(widget.rect(), gradient)
