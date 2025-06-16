"""
V1 Beat Frame Layout Manager Service - Direct Port

Ports V1's complete layout management system to V2, including
grid arrangement, beat positioning, and optimization strategies.
"""

from typing import Dict, List, Tuple, Optional, TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QWidget

from domain.models.core_models import SequenceData, BeatData
from .v1_beat_layout_service import V1BeatLayoutService
from .v1_beat_frame_resizer_service import V1BeatFrameResizerService

if TYPE_CHECKING:
    from presentation.components.workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )


class V1BeatFrameLayoutManagerService:
    """
    Direct port of V1's BeatFrameLayoutManager.

    Provides complete V1 layout management including:
    - Grid arrangement with start position
    - Beat view show/hide optimization
    - Layout state tracking
    - Performance-optimized rearrangement
    """

    def __init__(self):
        self.layout_service = V1BeatLayoutService()
        self.resizer_service = V1BeatFrameResizerService()
        self._current_layout_state = {"rows": 1, "columns": 8, "beat_count": 0}

    def setup_initial_layout(
        self,
        beat_frame: "SequenceBeatFrame",
        grid_layout: QGridLayout,
        start_position_view: QWidget,
        beat_views: List[QWidget],
    ):
        """
        Setup initial layout using V1's exact pattern.

        Args:
            beat_frame: The beat frame widget
            grid_layout: The grid layout to configure
            start_position_view: Start position widget
            beat_views: List of beat view widgets
        """
        # V1's layout configuration
        grid_layout.setSpacing(0)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add start position at (0, 0) - V1 pattern
        grid_layout.addWidget(start_position_view, 0, 0)
        start_position_view.show()

        # Initially hide all beat views (V1 optimization)
        for beat_view in beat_views:
            beat_view.hide()

        # Configure default layout for 16 beats (V1 default)
        self.configure_beat_frame_layout(
            beat_frame, grid_layout, start_position_view, beat_views, 16
        )

    def configure_beat_frame_layout(
        self,
        beat_frame: "SequenceBeatFrame",
        grid_layout: QGridLayout,
        start_position_view: QWidget,
        beat_views: List[QWidget],
        num_beats: int,
        sequence: Optional[SequenceData] = None,
    ):
        """
        Configure beat frame layout using V1's exact algorithm.

        Args:
            beat_frame: The beat frame widget
            grid_layout: The grid layout to configure
            start_position_view: Start position widget
            beat_views: List of beat view widgets
            num_beats: Number of beats to display
            sequence: Optional sequence for grow_sequence logic
        """
        # Use V1's layout calculation
        if sequence:
            layout_config = self.layout_service.calculate_beat_frame_layout(
                sequence, (beat_frame.width(), beat_frame.height())
            )
            rows = layout_config["rows"]
            columns = layout_config["columns"]
        else:
            # Fallback to direct calculation
            layout_config = self.layout_service._get_layout_for_beat_count(num_beats)
            rows = layout_config["rows"]
            columns = layout_config["columns"]

        # V1's scroll bar management
        scroll_area = self.resizer_service._find_scroll_area_parent(beat_frame)
        if scroll_area:
            self.resizer_service.configure_scroll_behavior(scroll_area, rows)

        # Perform the layout rearrangement
        self._rearrange_beats(
            grid_layout, start_position_view, beat_views, num_beats, rows, columns
        )

        # Update state tracking
        self._current_layout_state = {
            "rows": rows,
            "columns": columns,
            "beat_count": num_beats,
        }

    def _rearrange_beats(
        self,
        grid_layout: QGridLayout,
        start_position_view: QWidget,
        beat_views: List[QWidget],
        num_beats: int,
        rows: int,
        columns: int,
    ):
        """
        Rearrange beats in grid using V1's exact algorithm.

        This is a direct port of V1's rearrange_beats method.
        """
        # V1's optimization: Clear layout while preserving widgets
        while grid_layout.count():
            item = grid_layout.takeAt(0)
            if item and item.widget():
                item.widget().hide()

        # Always show start position at (0, 0)
        grid_layout.addWidget(start_position_view, 0, 0, 1, 1)
        start_position_view.show()

        # V1's exact grid arrangement algorithm
        index = 0
        for row in range(rows):
            for col in range(1, columns + 1):  # +1 to skip start position column
                if index < num_beats and index < len(beat_views):
                    beat_view = beat_views[index]

                    # Add to grid layout
                    grid_layout.addWidget(beat_view, row, col)

                    # Update beat number (V1 behavior)
                    if hasattr(beat_view, "beat") and hasattr(
                        beat_view.beat, "beat_number_item"
                    ):
                        beat_view.beat.beat_number_item.update_beat_number(index + 1)

                    # Show the beat view
                    beat_view.show()

                    index += 1
                else:
                    # V1 optimization: Hide unused beats
                    if index < len(beat_views):
                        beat_views[index].hide()
                    break

        # Hide any remaining beats (V1 cleanup)
        while index < len(beat_views):
            beat_views[index].hide()
            index += 1

    def get_current_layout_dimensions(self) -> Tuple[int, int]:
        """Get current layout dimensions (V1 compatibility)"""
        return self._current_layout_state["rows"], self._current_layout_state["columns"]

    def get_current_beat_count(self) -> int:
        """Get current beat count (V1 compatibility)"""
        return self._current_layout_state["beat_count"]

    def calculate_grid_dimensions_from_layout(
        self, grid_layout: QGridLayout
    ) -> Tuple[int, int]:
        """
        Calculate current grid dimensions by examining layout.
        Direct port of V1's calculate_current_layout method.
        """
        max_row = 0
        max_col = 0

        for i in range(grid_layout.count()):
            item = grid_layout.itemAt(i)
            if item and item.widget():
                position = grid_layout.getItemPosition(i)
                if position:
                    max_row = max(max_row, position[0])
                    max_col = max(max_col, position[1])

        return max_row + 1, max_col

    def adjust_layout_to_sequence_length(
        self,
        beat_frame: "SequenceBeatFrame",
        grid_layout: QGridLayout,
        start_position_view: QWidget,
        beat_views: List[QWidget],
        sequence: SequenceData,
    ):
        """
        Adjust layout to sequence length using V1's grow sequence logic.

        Direct port of V1's adjust_layout_to_sequence_length method.
        """
        # Count filled beats (V1 equivalent)
        filled_count = len([beat for beat in sequence.beats if beat is not None])

        self.configure_beat_frame_layout(
            beat_frame,
            grid_layout,
            start_position_view,
            beat_views,
            filled_count,
            sequence,
        )

    def resize_for_container(
        self,
        beat_frame: "SequenceBeatFrame",
        beat_views: List[QWidget],
        start_position_view: QWidget,
        container_width: int,
        container_height: int,
    ):
        """
        Resize beats for container using V1's resizing logic.

        Direct port of V1's resize_beat_frame functionality.
        """
        # Calculate available dimensions
        available_width, available_height = (
            self.resizer_service.calculate_container_dimensions(beat_frame)
        )

        # Get current layout
        rows, columns = self.get_current_layout_dimensions()

        # Calculate beat size
        beat_size = self.resizer_service.calculate_beat_size(
            beat_frame, available_width, available_height, columns
        )

        # Resize all beat views
        self.resizer_service.resize_beat_views(
            beat_views, beat_size, start_position_view
        )

    def clear_caches(self):
        """Clear all service caches"""
        self.layout_service.clear_cache()
        self.resizer_service.clear_cache()
