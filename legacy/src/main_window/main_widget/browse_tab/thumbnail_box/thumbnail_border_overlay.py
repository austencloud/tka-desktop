# thumbnail_border_overlay.py (example)

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt

class ThumbnailBorderOverlay(QWidget):
    """
    A transparent overlay that can draw a colored border on top of its parent widget.
    This avoids layout shifts because we never change the parent's style or padding;
    we just paint on top.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._border_color = QColor("transparent")
        self._border_width = 3
        # Make it ignore mouse events so clicks pass through to the thumbnail label
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.hide()  # start hidden

    def show_border(self, color: str):
        """Show the overlay with the given color, e.g. 'gold' or 'blue'."""
        self._border_color = QColor(color)
        self.show()
        # self.update()

    def hide_border(self):
        """Hide or set border color to transparent."""
        self._border_color = QColor("transparent")
        self.hide()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self._border_color.alpha() == 0:
            return  # no border to draw

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        pen = QPen(self._border_color, self._border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        half = self._border_width / 2
        draw_rect = self.rect().adjusted(half, half, -half, -half)
        painter.drawRect(draw_rect)
        painter.end()
