from PyQt6.QtCore import QPointF
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowMouseEventHandler:
    def __init__(self, arrow: "Arrow") -> None:
        self.arrow = arrow

    def handle_mouse_press(self, event) -> None:
        # self.arrow.pictograph.mouse_event_handler.clear_selections()
        self.arrow.pictograph.selected_arrow = self.arrow
        self.arrow.setSelected(True)

    def handle_mouse_release(self, event) -> None:
        self.arrow.pictograph.arrows[self.arrow.state.color] = self.arrow

    def set_drag_pos(self, new_pos: QPointF) -> None:
        self.arrow.setPos(new_pos)
