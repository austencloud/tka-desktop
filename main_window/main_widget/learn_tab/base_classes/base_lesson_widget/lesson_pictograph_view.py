from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsRectItem
from PyQt6.QtGui import QBrush, QColor

from base_widgets.pictograph.bordered_pictograph_view import BorderedPictographView


if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph_scene import PictographScene


class LessonPictographView(BorderedPictographView):
    def __init__(self, pictograph: "PictographScene") -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph

    ### EVENTS ###

    def set_overlay_color(self, color: str) -> None:
        # First, remove any existing overlay so we don't stack them.
        for item in self.scene().items():
            if item.data(0) == "overlay":
                self.scene().removeItem(item)
        # If color is None, don't add a new overlay.
        if color is None:
            return
        # Otherwise, create and tag the new overlay.
        self.overlay = QGraphicsRectItem(self.sceneRect())
        self.overlay.setBrush(QBrush(QColor(color)))
        self.overlay.setOpacity(0.5)
        self.overlay.setData(0, "overlay")  # Tag it so we can find and remove it later.
        self.scene().addItem(self.overlay)
