from typing import TYPE_CHECKING, Union
from base_widgets.pictograph.pictograph import Pictograph
from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat_grabber import (
    BeatGrabber,
)
from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat_start_text_manager import (
    BeatStartTextItem,
)

from .beat_number_item import BeatNumberItem

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )

    from .beat_view import BeatView


class Beat(Pictograph):
    view: "BeatView" = None
    is_placeholder = False
    parent_beat = None
    beat_number = 0

    def __init__(
        self, beat_frame: "SequenceBeatFrame", duration: Union[int, float] = 1
    ):
        super().__init__()
        self.beat_number_item = BeatNumberItem(self)
        self.grabber = BeatGrabber(self)
        self.duration = duration
        self.start_text_item = BeatStartTextItem(self)
