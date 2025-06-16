from typing import TYPE_CHECKING
from base_widgets.pictograph.elements.views.beat_view import (
    LegacyBeatView,
)
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .layout_beat_frame.layout_beat_frame import LayoutBeatFrame


class LayoutBeatView(LegacyBeatView):
    """A beat view designed for the layout preview frame."""

    def __init__(self, beat_frame: "LayoutBeatFrame", number: int) -> None:
        self.beat_frame = beat_frame
        super().__init__(beat_frame, number)
        self.setCursor(Qt.CursorShape.ArrowCursor)
