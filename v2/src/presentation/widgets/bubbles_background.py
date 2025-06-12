from PyQt6.QtGui import QColor, QPainter, QLinearGradient
from PyQt6.QtWidgets import QWidget


class BubblesBackground:
    def __init__(self, widget: QWidget):
        self.widget = widget

    def paint_background(self, widget: QWidget, painter: QPainter):
        gradient = QLinearGradient(0, 0, 0, widget.height())
        gradient.setColorAt(0, QColor("#003d5b"))
        gradient.setColorAt(0.5, QColor("#30638e"))
        gradient.setColorAt(1, QColor("#ffc93c"))
        painter.fillRect(widget.rect(), gradient)

    def animate_background(self):
        pass

    def stop_animation(self):
        pass
