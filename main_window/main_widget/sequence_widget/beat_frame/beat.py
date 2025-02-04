from typing import TYPE_CHECKING, Union
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from base_widgets.base_pictograph.glyphs.beat_reversal_group import BeatReversalGroup
from main_window.main_widget.sequence_widget.beat_frame.beat_grabber import BeatGrabber
from main_window.main_widget.sequence_widget.beat_frame.beat_start_text_manager import (
    BeatStartTextItem,
)
from .beat_number_item import BeatNumberItem

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.beat_frame.sequence_widget_beat_frame import (
        SequenceWorkbenchBeatFrame,
    )
    from .beat_view import BeatView


class Beat(BasePictograph):
    view: "BeatView" = None
    is_placeholder = False
    parent_beat = None
    beat_number = 0
    blue_reversal = False
    red_reversal = False

    def __init__(
        self, beat_frame: "SequenceWorkbenchBeatFrame", duration: Union[int, float] = 1
    ):
        super().__init__(beat_frame.main_widget)
        self.main_widget = beat_frame.main_widget
        self.reversal_glyph = BeatReversalGroup(self)
        self.beat_number_item = BeatNumberItem(self)
        self.grabber = BeatGrabber(self)
        self.duration = duration
        self.start_text_item = BeatStartTextItem(self)
