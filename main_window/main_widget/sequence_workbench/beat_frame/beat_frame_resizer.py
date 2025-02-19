from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget  # Import QWidget

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )


class BeatFrameResizer:
    def __init__(self, beat_frame: "SequenceBeatFrame"):
        # super().__init__(beat_frame)
        self.beat_frame = beat_frame
        self.sequence_workbench = beat_frame.sequence_workbench
        self.main_widget = beat_frame.main_widget
        self.scroll_area = self.sequence_workbench.scroll_area
        self.selection_overlay = beat_frame.selection_overlay
        self.start_pos_view = beat_frame.start_pos_view


    def resize_beat_frame(self) -> None:
        width, height = self.calculate_dimensions()
        beat_size = self.calculate_beat_size(width, height)
        self.resize_beats(beat_size)
        self.update_views(beat_size)

    def calculate_dimensions(self) -> tuple[int, int]:
        scrollbar_width = self.scroll_area.verticalScrollBar().width()

        available_width = (
            self.main_widget.width() // 2
            - self.sequence_workbench.button_panel.width()
            - scrollbar_width
        )
        width = int(available_width * 0.8)
        available_height = (
            self.sequence_workbench.height()
            - self.sequence_workbench.graph_editor.get_graph_editor_height() * 0.8
        )

        return width, available_height

    def calculate_beat_size(self, width: int, height: int) -> int:
        num_cols = max(1, self.beat_frame.layout.columnCount() - 1)
        if num_cols == 0:
            return 0
        return min(int(width // 5), int(height // 6))

    def resize_beats(self, beat_size: int) -> None:
        for beat in self.beat_frame.beat_views:
            beat.setFixedSize(beat_size, beat_size)
        self.start_pos_view.setFixedSize(beat_size, beat_size)

    def update_views(self, beat_size: int) -> None:
        self.selection_overlay.update_overlay_position()
