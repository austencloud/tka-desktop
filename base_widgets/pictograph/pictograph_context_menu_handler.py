from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph_scene import PictographScene

from PyQt6.QtWidgets import QGraphicsSceneMouseEvent


class PictographContextMenuHandler:
    def __init__(self, pictograph: "PictographScene") -> None:
        self.pictograph = pictograph

    def handle_context_menu(self, event: "QGraphicsSceneMouseEvent") -> None:
        scene_pos = self.pictograph.view.mapToScene(event.pos().toPoint())
        items_at_pos = self.pictograph.items(scene_pos)

        clicked_item = None
        for item in items_at_pos:
            if isinstance(item, Arrow) or isinstance(item, Prop):
                clicked_item = item
                break

        if not clicked_item and items_at_pos:
            clicked_item = items_at_pos[0]

        event_pos = event.screenPos()
