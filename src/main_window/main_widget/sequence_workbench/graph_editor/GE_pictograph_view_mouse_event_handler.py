from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING
from PyQt6.QtGui import QMouseEvent

if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.GE_pictograph_view import (
        GE_PictographView,
    )


class GE_PictographViewMouseEventHandler:
    def __init__(self, pictograph_view: "GE_PictographView") -> None:
        self.pictograph_view = pictograph_view
        self.pictograph = pictograph_view.pictograph
        self.selection_manager = self.pictograph_view.graph_editor.selection_manager

    def handle_mouse_press(self, event: QMouseEvent) -> None:
        widget_pos = event.pos()
        scene_pos = self.pictograph_view.mapToScene(widget_pos)
        items_at_pos = self.pictograph_view.scene().items(scene_pos)
        arrow = next((item for item in items_at_pos if isinstance(item, Arrow)), None)

        if arrow:
            self.selection_manager.set_selected_arrow(arrow)
        else:
            self.selection_manager.clear_selection()

        self.pictograph_view.repaint()

    def is_arrow_under_cursor(self, event: "QMouseEvent") -> bool:
        widget_pos = event.pos()
        scene_pos = self.pictograph_view.mapToScene(widget_pos)
        items_at_pos = self.pictograph_view.scene().items(scene_pos)
        return any(isinstance(item, Arrow) for item in items_at_pos)

    def clear_selections(self) -> None:
        for arrow in self.pictograph.elements.arrows.values():
            arrow.setSelected(False)
        for prop in self.pictograph.elements.props.values():
            prop.setSelected(False)
        self.dragged_prop = None
        self.dragged_arrow = None
