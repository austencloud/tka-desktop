from typing import TYPE_CHECKING, Union

from data.constants import LETTER
from utilities.word_simplifier import WordSimplifier
from PyQt6.QtWidgets import QGraphicsView

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat_view import (
        BeatView,
    )
    from main_window.main_widget.sequence_workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )


class BeatFrameGetter:
    def __init__(self, beat_frame: "SequenceBeatFrame"):
        self.beat_frame = beat_frame

    def next_available_beat(self) -> int:
        current_beat = 0
        for beat_view in self.beat_frame.beat_views:
            if beat_view.is_filled:
                current_beat += 1
            else:
                return current_beat
        return current_beat

    def last_filled_beat(self) -> "BeatView":
        for beat_view in reversed(self.beat_frame.beat_views):
            if beat_view.is_filled:
                return beat_view
        return self.beat_frame.start_pos_view

    def current_word(self) -> str:
        word = ""
        for beat_view in self.beat_frame.beat_views:
            if beat_view.is_filled:
                if beat_view.beat.state.pictograph_data.get("is_placeholder", False):
                    continue
                word += beat_view.beat.state.pictograph_data.get(LETTER, "")
        return WordSimplifier.simplify_repeated_word(word)

    def index_of_currently_selected_beat(self) -> int:
        for i, beat in enumerate(self.beat_frame.beat_views):
            if beat.is_selected:
                return i
        return 0

    def currently_selected_beat_view(self) -> Union["BeatView", None]:
        for beat_view in self.beat_frame.beat_views:
            if beat_view.is_selected:
                return beat_view
        return (
            self.beat_frame.start_pos_view
            if self.beat_frame.start_pos_view.is_selected
            else None
        )

    def beat_number_of_currently_selected_beat(self) -> int:
        return self.currently_selected_beat_view().number

    def duration_of_currently_selected_beat(self) -> int:
        return self.currently_selected_beat_view().beat.duration

    def beat_view_by_number(self, beat_number: int) -> "BeatView":
        for beat_view in self.beat_frame.beat_views:
            if beat_view.number == beat_number:
                return beat_view
        return None

    def beat_number(self, beat_view: QGraphicsView) -> int:
        """Get the beat number for a given beat view."""
        return self.beat_frame.beat_views.index(beat_view) + 1

    def index_of_beat(self, beat_view: QGraphicsView) -> int:
        """Get the index of a given beat view."""
        return self.beat_frame.beat_views.index(beat_view)

    def beat_dicts(self):
        return [
            beat.beat.managers.get.pictograph_data()
            for beat in self.beat_frame.beat_views
            if beat.is_filled
        ]

    def beat_count(self):
        return sum(1 for beat in self.beat_frame.beat_views if beat.is_filled)
