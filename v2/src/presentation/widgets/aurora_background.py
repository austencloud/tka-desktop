from PyQt6.QtGui import QColor, QPainter, QLinearGradient
from PyQt6.QtWidgets import QWidget


class AuroraBackground:
    def __init__(self, widget: QWidget):
        self.widget = widget

    def paint_background(self, widget: QWidget, painter: QPainter):
        gradient = QLinearGradient(0, 0, 0, widget.height())
        gradient.setColorAt(0, QColor("#1a0f3d"))
        gradient.setColorAt(0.3, QColor("#2d1b69"))
        gradient.setColorAt(0.7, QColor("#40e0d0"))
        gradient.setColorAt(1, QColor("#ff6b9d"))
        painter.fillRect(widget.rect(), gradient)

    def animate_background(self):
        pass

    def stop_animation(self):
        pass
