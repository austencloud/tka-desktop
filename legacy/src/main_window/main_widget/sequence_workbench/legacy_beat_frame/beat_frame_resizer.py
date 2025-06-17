from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget  # Import QWidget
from utils.ui_utils import ensure_positive_size

if TYPE_CHECKING:
    from legacy.src.main_window.main_widget.sequence_workbench.legacy_beat_frame.legacy_beat_frame import (
        LegacyBeatFrame,
    )


class BeatFrameResizer:
    def __init__(self, beat_frame: "LegacyBeatFrame"):
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
        available_height = int(
            self.sequence_workbench.height()
            - self.sequence_workbench.graph_editor.get_graph_editor_height() * 0.8
        )

        return width, available_height

    def calculate_beat_size(self, width: int, height: int) -> int:
        num_cols = self.beat_frame.layout_manager.get_cols()

        if num_cols == 0:
            return 0
        else:
            return min(int(width // num_cols), int(height // 6))

    def resize_beats(self, beat_size: int) -> None:
        # Ensure beat_size is positive to avoid Qt warnings
        safe_size = ensure_positive_size(beat_size)
        for beat in self.beat_frame.beat_views:
            beat.setFixedSize(safe_size, safe_size)
            # If the view has a setMinimumSize method, ensure it's also positive
            if hasattr(beat, "setMinimumSize"):
                min_size = ensure_positive_size(safe_size - 48)
                beat.setMinimumSize(min_size, min_size)

        # Also apply to start position view
        self.start_pos_view.setFixedSize(safe_size, safe_size)
        if hasattr(self.start_pos_view, "setMinimumSize"):
            min_size = ensure_positive_size(safe_size - 48)
            self.start_pos_view.setMinimumSize(min_size, min_size)

    def update_views(self, beat_size: int) -> None:
        self.selection_overlay.update_overlay_position()
