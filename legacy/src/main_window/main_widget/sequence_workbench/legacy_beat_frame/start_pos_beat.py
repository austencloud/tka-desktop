from typing import TYPE_CHECKING

from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat import Beat

if TYPE_CHECKING:
    from legacy.src.main_window.main_widget.sequence_workbench.legacy_beat_frame.legacy_beat_frame import (
        LegacyBeatFrame,
    )


class StartPositionBeat(Beat):
    def __init__(self, beat_frame: "LegacyBeatFrame") -> None:
        super().__init__(beat_frame)
        self.beat_frame = beat_frame
