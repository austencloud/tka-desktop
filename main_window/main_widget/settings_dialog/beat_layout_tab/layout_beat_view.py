from typing import TYPE_CHECKING
from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat_view import (
    BeatView,
)
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .layout_beat_frame import LayoutBeatFrame


class LayoutBeatView(BeatView):
    """A beat view designed for the layout preview frame."""

    def __init__(self, beat_frame: "LayoutBeatFrame", number: int) -> None:
        self.beat_frame = beat_frame
        super().__init__(beat_frame, number)
        self.setCursor(Qt.CursorShape.ArrowCursor)
