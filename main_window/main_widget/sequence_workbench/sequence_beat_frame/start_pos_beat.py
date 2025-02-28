from typing import TYPE_CHECKING

from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat import Beat

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )


class StartPositionBeat(Beat):
    def __init__(self, beat_frame: "SequenceBeatFrame") -> None:
        super().__init__(beat_frame)
        self.beat_frame = beat_frame
