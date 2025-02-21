from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsItem

if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph_scene import PictographScene


class GraphicalObject(QGraphicsSvgItem):
    color: str
    renderer: QSvgRenderer

    def __init__(self, pictograph: "PictographScene") -> None:
        super().__init__()
        self.pictograph = pictograph
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
