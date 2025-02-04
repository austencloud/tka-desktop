from typing import TYPE_CHECKING


from main_window.main_widget.sequence_widget.beat_frame.beat import Beat


if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.beat_frame.sequence_widget_beat_frame import (
        SequenceWorkbenchBeatFrame,
    )


class StartPositionBeat(Beat):
    def __init__(self, beat_frame: "SequenceWorkbenchBeatFrame") -> None:
        super().__init__(beat_frame)
        self.main_widget = beat_frame.main_widget
        self.beat_frame = beat_frame
