from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame

from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat_frame_getter import (
    BeatFrameGetter,
)
from base_widgets.pictograph.elements.views.beat_view import (
    LegacyBeatView,
)

from main_window.main_widget.sequence_workbench.legacy_beat_frame.start_pos_beat_view import (
    StartPositionBeatView,
)
from src.legacy_settings_manager.global_settings.app_context import AppContext


if TYPE_CHECKING:

    from main_window.main_widget.sequence_workbench.sequence_workbench import (
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
        self.sequence_workbench: "SequenceWorkbench" = None
        self.browse_tab: "BrowseTab" = None
        self.start_pos_view: "StartPositionBeatView" = None
        self.initialized = True
        self.sequence_changed = False
        self.setObjectName("beat_frame")
        self.setStyleSheet("QFrame#beat_frame { background: transparent; }")
        self.get = BeatFrameGetter(self)
        self.json_manager = AppContext.json_manager()

    def _init_beats(self):
        self.beats = [LegacyBeatView(self, number=i + 1) for i in range(64)]
        for beat in self.beats:
            beat.hide()
