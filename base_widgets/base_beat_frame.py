from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame

from main_window.main_widget.sequence_widget.beat_frame.beat_view import BeatView
from main_window.main_widget.sequence_widget.beat_frame.beat_frame_getter import (
    BeatFrameGetter,
)


if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.beat_frame.start_pos_beat_view import (
        StartPositionBeatView,
    )
    from main_window.main_widget.sequence_widget.sequence_widget import (
        SequenceWorkbench,
    )
    from main_window.main_widget.main_widget import MainWidget
    from main_window.main_widget.browse_tab.browse_tab import (
        BrowseTab,
    )


class BaseBeatFrame(QFrame):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget
        self.json_manager = main_widget.json_manager
        self.settings_manager = main_widget.main_window.settings_manager
        self.sequence_widget: "SequenceWorkbench" = None
        self.browse_tab: "BrowseTab" = None
        self.start_pos_view: "StartPositionBeatView" = None
        self.initialized = True
        self.sequence_changed = False
        self.setObjectName("beat_frame")
        self.setStyleSheet("QFrame#beat_frame { background: transparent; }")
        self.get = BeatFrameGetter(self)

    def _init_beats(self):
        self.beats = [BeatView(self, number=i + 1) for i in range(64)]
        for beat in self.beats:
            beat.hide()
