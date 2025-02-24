from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtGui import QKeyEvent


from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat_frame_layout_manager import BeatFrameLayoutManager

from .start_pos_beat import StartPositionBeat
from .start_pos_beat_view import StartPositionBeatView
from .start_position_adder import StartPositionAdder
from ..beat_factory import BeatFactory
from .beat_adder import BeatAdder
from .beat_duration_manager import BeatDurationManager
from .beat_frame_key_event_handler import BeatFrameKeyEventHandler
from .beat_frame_populator import BeatFramePopulator
from .beat_frame_resizer import BeatFrameResizer
from .beat_frame_updater import BeatFrameUpdater

from .image_export_manager.image_export_manager import ImageExportManager
from .beat_selection_overlay import BeatSelectionOverlay
from .beat_view import BeatView
from base_widgets.base_beat_frame import BaseBeatFrame

if TYPE_CHECKING:
    from ..sequence_workbench import SequenceWorkbench


class SequenceBeatFrame(BaseBeatFrame):
    beat_views: list[BeatView] = []
    start_pos_view: StartPositionBeatView = None
    layout: "QGridLayout" = None
    initialized = True
    sequence_changed = False

    def __init__(self, sequence_workbench: "SequenceWorkbench") -> None:
        super().__init__(sequence_workbench.main_widget)
        self.main_widget = sequence_workbench.main_widget
        self.sequence_workbench = sequence_workbench
        self._init_beats()
        self._setup_components()
        self.layout_manager.setup_layout()

    def _init_beats(self):
        self.start_pos_view = StartPositionBeatView(self)
        self.start_pos = StartPositionBeat(self)
        self.beat_views = [BeatView(self, number=i + 1) for i in range(64)]
        for beat in self.beat_views:
            beat.hide()

    def _setup_components(self) -> None:
        self.beat_factory = BeatFactory(self)
        self.selection_overlay = BeatSelectionOverlay(self)
        self.layout_manager = BeatFrameLayoutManager(self)
        self.image_export_manager = ImageExportManager(self, SequenceBeatFrame)
        self.populator = BeatFramePopulator(self)
        self.beat_adder = BeatAdder(self)
        self.start_position_adder = StartPositionAdder(self)
        self.duration_manager = BeatDurationManager(self)
        self.updater = BeatFrameUpdater(self)
        self.key_event_handler = BeatFrameKeyEventHandler(self)
        self.resizer = BeatFrameResizer(self)

    def keyPressEvent(self, event: "QKeyEvent") -> None:
        self.key_event_handler.keyPressEvent(event)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.resizer.resize_beat_frame()
