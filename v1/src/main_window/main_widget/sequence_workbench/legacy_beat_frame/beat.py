from typing import TYPE_CHECKING, Union
from v1.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat_grabber import (
    BeatGrabber,
)
from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat_start_text_manager import (
    BeatStartTextItem,
)

from .beat_number_item import BeatNumberItem

if TYPE_CHECKING:
    from v1.src.main_window.main_widget.sequence_workbench.legacy_beat_frame.legacy_beat_frame import (
        LegacyBeatFrame,
    )

    from base_widgets.pictograph.elements.views.beat_view import BeatView


class Beat(LegacyPictograph):
    view: "BeatView" = None
    is_placeholder = False
    parent_beat = None
    beat_number = 0

    def __init__(self, beat_frame: "LegacyBeatFrame", duration: Union[int, float] = 1):
        super().__init__()
        self.beat_number_item = BeatNumberItem(self)
        self.grabber = BeatGrabber(self)
        self.duration = duration
        self.start_text_item = BeatStartTextItem(self)
