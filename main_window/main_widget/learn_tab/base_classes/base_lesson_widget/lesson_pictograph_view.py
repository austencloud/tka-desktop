from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsRectItem
from PyQt6.QtGui import QBrush, QColor

from base_widgets.base_pictograph.bordered_pictograph_view import BorderedPictographView


if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class LessonPictographView(BorderedPictographView):
    def __init__(self, pictograph: "BasePictograph") -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph

    ### EVENTS ###

    def set_overlay_color(self, color: str) -> None:
        overlay = QGraphicsRectItem(self.sceneRect())
        overlay.setBrush(QBrush(QColor(color)))
        overlay.setOpacity(0.5)
        self.scene().addItem(overlay)
