from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QGridLayout, QFrame, QSizePolicy
from PyQt6.QtCore import Qt, QSize

from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat import Beat
from base_widgets.pictograph.elements.views.beat_view import (
    LegacyBeatView,
)

from main_window.main_widget.sequence_workbench.legacy_beat_frame.start_pos_beat import (
    StartPositionBeat,
)
from main_window.main_widget.sequence_workbench.legacy_beat_frame.start_pos_beat_view import (
    StartPositionBeatView,
)
from ..layout_beat_view import LayoutBeatView

if TYPE_CHECKING:
    from ..beat_layout_tab import BeatLayoutTab


class LayoutBeatFrame(QFrame):
    """Displays a live preview of the selected beat layout options."""

    rows = 0
    cols = 0
    current_num_beats = 16
    beat_views: list[Union[LegacyBeatView]] = []
    start_pos_view: StartPositionBeatView = None
    current_layout: tuple[int, int] = (4, 4)

    def __init__(self, beat_layout_tab: "BeatLayoutTab"):
        super().__init__(beat_layout_tab)
        self.beat_layout_tab = beat_layout_tab

        self._setup_layout()
        self._init_beats()
        # self.update_preview()

    def _init_beats(self):
        """Initialize the start position and beat views."""
        self.start_pos_view = StartPositionBeatView(self)
        self.start_pos = StartPositionBeat(self)
        self.beat_views = [LayoutBeatView(self, number=i + 1) for i in range(64)]
        for beat in self.beat_views:
            beat.hide()

    def _setup_layout(self):
        """Set up the grid layout for the beat frame."""
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def update_preview(self):
        """Update the preview based on the current layout."""
        self.rows, self.cols = self.current_layout  # Fixed order
        num_beats = (
            self.beat_layout_tab.controls.length_selector.num_beats_spinbox.value()
        )
        self._perform_relayout(num_beats)

    def _perform_relayout(self, num_beats: int):
        """Relayout the widgets based on the specified number of beats."""
        # Remove all existing items from the layout
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.hide()

        # Handle the start position beat view
        start_pos = StartPositionBeat(self)
        self.start_pos_view.set_start_pos(start_pos)
        start_pos.elements.grid.hide()
        self.layout.addWidget(self.start_pos_view, 0, 0)
        self.start_pos_view.setVisible(True)

        # Add beat views to the layout
        index = 0
        for row in range(self.rows):
            for col in range(1, self.cols + 1):  # Start at column 1 for beat views
                if index < num_beats:
                    beat_view = self.beat_views[index]
                    beat = Beat(self)
                    beat_view.set_beat(beat, index + 1)
                    beat.elements.grid.hide()
                    self.layout.addWidget(beat_view, row, col)
                    beat_view.setVisible(True)
                    index += 1
                else:
                    # Stop once we've added the specified number of beats
                    break
            if index >= num_beats:
                break

        # Hide unused beat views
        for unused_index in range(index, len(self.beat_views)):
            self.beat_views[unused_index].setVisible(False)
        self.resize_beats()

    def _calculate_beat_size(self) -> QSize:
        """Calculate the size of each beat view cell."""
        available_width = self.width() - self.layout.horizontalSpacing() * (
            self.cols + 1
        )
        available_height = self.height() - self.layout.verticalSpacing() * (
            self.rows + 1
        )
        cell_size = min(
            available_width // (self.cols + 1), available_height // (self.rows + 1)
        )
        return QSize(cell_size, cell_size)

    def resizeEvent(self, event):
        """Recalculate cell sizes when the frame is resized."""
        super().resizeEvent(event)
        self.resize_beats()

    def resize_beats(self):
        cell_size = self._calculate_beat_size()
        for beat_view in self.beat_views:
            beat_view.setFixedSize(cell_size)
        self.start_pos_view.setFixedSize(cell_size)
