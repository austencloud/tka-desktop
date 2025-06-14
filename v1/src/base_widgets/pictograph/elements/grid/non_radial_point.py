from PyQt6.QtWidgets import QGraphicsEllipseItem
from PyQt6.QtGui import QBrush, QPen, QColor
from PyQt6.QtCore import QPointF, Qt



class NonRadialGridPoint(QGraphicsEllipseItem):
    def __init__(self, x, y, r, point_id):
        super().__init__(-r, -r, 2 * r, 2 * r)
        self.setBrush(QBrush(QColor("black")))
        self.setPen(QPen(Qt.PenStyle.NoPen))
        self.setPos(QPointF(x, y))
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)
        self.setToolTip(point_id)
        self.point_id = point_id
        self.setZValue(101)
