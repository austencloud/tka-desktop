from PyQt6.QtGui import QColor, QPainter, QLinearGradient
from PyQt6.QtWidgets import QWidget


class SnowfallBackground:
    def __init__(self, widget: QWidget):
        self.widget = widget

    def paint_background(self, widget: QWidget, painter: QPainter):
        gradient = QLinearGradient(0, 0, 0, widget.height())
        gradient.setColorAt(0, QColor("#0b1d2a"))
        gradient.setColorAt(0.3, QColor("#142030"))
        gradient.setColorAt(0.7, QColor("#325078"))
        gradient.setColorAt(1, QColor("#49708a"))
        painter.fillRect(widget.rect(), gradient)

    def animate_background(self):
        pass

    def stop_animation(self):
        pass
