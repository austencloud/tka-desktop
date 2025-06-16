from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsItem

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class GraphicalObject(QGraphicsSvgItem):
    renderer: QSvgRenderer

    def __init__(self, pictograph: "LegacyPictograph") -> None:
        super().__init__()
        self.pictograph = pictograph
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
