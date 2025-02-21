from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from base_widgets.pictograph.pictograph_view import PictographView
from .beat import Beat

if TYPE_CHECKING:
    from .sequence_beat_frame import SequenceBeatFrame


class BeatView(PictographView):
    is_start_pos = False
    is_filled = False
    is_selected = False
    beat: "Beat" = None

    def __init__(self, beat_frame: "SequenceBeatFrame", number: int = None):
        super().__init__(beat_frame)
        self.beat_frame = beat_frame
        self.number = number
        self.setStyleSheet("border: none; border: 1px solid black;")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._setup_blank_beat()

    def _setup_blank_beat(self):
        self.blank_beat = Beat(self.beat_frame)
        self.beat = self.blank_beat
        self.setScene(self.blank_beat)
        self.blank_beat.grid.hide()
        self.blank_beat.beat_number_item.update_beat_number()

    def set_beat(self, beat: "Beat", number: int) -> None:
        self.beat = beat
        self.beat.view = self
        self.is_filled = True
        self.beat.beat_number = number
        self.setScene(self.beat)
        self.beat.beat_number_item.update_beat_number(number)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.is_filled:
            self.beat_frame.selection_overlay.select_beat(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        beat_scene_size = (950, 950)
        view_size = self.size()

        self.view_scale = min(
            view_size.width() / beat_scene_size[0],
            view_size.height() / beat_scene_size[1],
        )
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
