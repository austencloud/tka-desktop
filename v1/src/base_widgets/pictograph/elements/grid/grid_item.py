import logging
from typing import TYPE_CHECKING
from PyQt6.QtSvgWidgets import QGraphicsSvgItem


logger = logging.getLogger(__name__)


GRID_DIR = "images/grid/"


class GridItem(QGraphicsSvgItem):
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setZValue(100)

    def wheelEvent(self, event) -> None:
        event.ignore()

    def mousePressEvent(self, event) -> None:
        event.ignore()

    def mouseMoveEvent(self, event) -> None:
        event.ignore()

    def mouseReleaseEvent(self, event) -> None:
        event.ignore()
