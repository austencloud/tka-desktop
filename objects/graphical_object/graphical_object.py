from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QGraphicsItem


if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph

    from objects.arrow.arrow import Arrow
    from objects.prop.prop import Prop


class GraphicalObject(QGraphicsSvgItem):
    svg_file: str = None
    self: Union["Arrow", "Prop"]
    color: str
    renderer: QSvgRenderer

    def __init__(self, pictograph: "BasePictograph") -> None:
        super().__init__()
        self.pictograph = pictograph
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)


