from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
from PyQt6.QtCore import QEvent
from base_widgets.base_beat_frame import BaseBeatFrame
from .act_beat_frame_drag_drop_handler import ActBeatFrameDragDropHandler
from .act_frame_initializer import ActBeatFrameInitializer
from .act_populator import ActPopulator
from .act_beat_view import ActBeatView
from .act_step_label import ActStepLabel
from .act_beat_frame_layout_manager import ActBeatFrameLayoutManager
from ......sequence_workbench.sequence_beat_frame.beat_selection_overlay import (
    BeatSelectionOverlay,
)

if TYPE_CHECKING:
    from ..act_beat_scroll import ActBeatScroll


class ActBeatFrame(BaseBeatFrame):
    layout: "QGridLayout"

    def __init__(self, beat_scroll_area: "ActBeatScroll"):
        super().__init__(beat_scroll_area.act_sheet.write_tab.main_widget)
        self.beat_scroll_area = beat_scroll_area
        self.act_sheet = beat_scroll_area.act_sheet
        self.write_tab = self.act_sheet.write_tab
        self.beats: list[ActBeatView] = []
        self.step_labels: list[ActStepLabel] = []
        self.beat_step_map: dict[ActBeatView, ActStepLabel] = {}
        self.selection_overlay = BeatSelectionOverlay(self)
        self.layout_manager = ActBeatFrameLayoutManager(self)
        self.initializer = ActBeatFrameInitializer(self)
        self.drag_drop_handler = ActBeatFrameDragDropHandler(self)
        self.populator = ActPopulator(self)

        self.setAcceptDrops(True)
        self.installEventFilter(self)

    def eventFilter(
        self, source, event: Union[QDragEnterEvent, QDragMoveEvent, QDropEvent]
    ):
        """Delegate drag-and-drop events to the drag-drop handler."""
        if event.type() in (
            QEvent.Type.DragEnter,
            QEvent.Type.DragMove,
            QEvent.Type.Drop,
        ):
            return self._handle_drag_event(event)
        return super().eventFilter(source, event)

    def _handle_drag_event(
        self, event: Union[QDragEnterEvent, QDragMoveEvent, QDropEvent]
    ) -> bool:
        if event.type() == QEvent.Type.DragEnter:
            self.drag_drop_handler.dragEnterEvent(event)
        elif event.type() == QEvent.Type.DragMove:
            self.drag_drop_handler.dragMoveEvent(event)
        elif event.type() == QEvent.Type.Drop:
            self.drag_drop_handler.dropEvent(event)
        return True

    def resizeEvent(self, event):
        """Resize each beat and label, adjusting the layout dynamically."""
        super().resizeEvent(event)
        scrollbar_width = (
            self.act_sheet.act_container.beat_scroll.verticalScrollBar().width()
        )
        width_without_scrollbar = self.width() - scrollbar_width
        self.beat_size = int(width_without_scrollbar // self.act_sheet.DEFAULT_COLUMNS)
        self.steps_label_height = int(self.beat_size * (2 / 3))
