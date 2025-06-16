"""
V1 Beat Frame Resizer Service - Direct Port

Ports V1's sophisticated resizing and responsive behavior to V2,
including intelligent beat sizing and dynamic scroll management.
"""

from typing import Tuple, Optional, TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QScrollArea

if TYPE_CHECKING:
    from presentation.components.workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )


class V1BeatFrameResizerService:
    """
    Direct port of V1's beat frame resizing logic.

    Maintains V1's intelligent sizing including:
    - Dynamic beat size calculations
    - Container-aware sizing
    - Scroll bar management
    - Performance optimizations
    """

    def __init__(self):
        self._last_calculated_size = None
        self._size_cache = {}

    def calculate_beat_size(
        self,
        beat_frame: "SequenceBeatFrame",
        container_width: int,
        container_height: int,
        num_columns: int,
    ) -> int:
        """
        Calculate optimal beat size using V1's exact algorithm.

        Args:
            beat_frame: The beat frame widget
            container_width: Available width
            container_height: Available height
            num_columns: Number of columns in current layout

        Returns:
            Optimal beat size in pixels
        """
        # V1's caching for performance
        cache_key = (container_width, container_height, num_columns)
        if cache_key in self._size_cache:
            return self._size_cache[cache_key]

        if num_columns == 0:
            beat_size = 0
        else:
            # V1's exact calculation
            beat_size = min(
                int(container_width // num_columns), int(container_height // 6)
            )

        # Ensure positive size (V1's safety check)
        beat_size = max(beat_size, 1)

        self._size_cache[cache_key] = beat_size
        return beat_size

    def calculate_container_dimensions(
        self, beat_frame: "SequenceBeatFrame"
    ) -> Tuple[int, int]:
        """
        Calculate available container dimensions using V1's logic.

        Args:
            beat_frame: The beat frame widget

        Returns:
            Tuple of (width, height) available for beats
        """
        # Get the scroll area parent (V1 equivalent)
        scroll_area = self._find_scroll_area_parent(beat_frame)

        if scroll_area:
            # V1's calculation with scroll bar consideration
            scrollbar_width = scroll_area.verticalScrollBar().width()
            available_width = int(scroll_area.width() * 0.8) - scrollbar_width
            available_height = int(scroll_area.height() * 0.8)
        else:
            # Fallback to widget size
            available_width = int(beat_frame.width() * 0.8)
            available_height = int(beat_frame.height() * 0.8)

        return available_width, available_height

    def _find_scroll_area_parent(self, widget) -> Optional[QScrollArea]:
        """Find QScrollArea parent widget"""
        parent = widget.parent()
        while parent:
            if isinstance(parent, QScrollArea):
                return parent
            parent = parent.parent()
        return None

    def configure_scroll_behavior(self, scroll_area: QScrollArea, num_rows: int):
        """
        Configure scroll bar behavior using V1's logic.

        Args:
            scroll_area: The scroll area widget
            num_rows: Number of rows in current layout
        """
        # V1's exact scroll bar logic
        if num_rows > 4:
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        else:
            scroll_area.setVerticalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOff
            )

    def resize_beat_views(
        self, beat_views: list, beat_size: int, start_position_view=None
    ):
        """
        Resize beat views using V1's exact logic.

        Args:
            beat_views: List of beat view widgets
            beat_size: Target size for beats
            start_position_view: Start position view widget
        """
        # V1's safety check
        safe_size = max(beat_size, 1)
        min_size = max(safe_size - 48, 1)

        # Resize all beat views
        for beat_view in beat_views:
            beat_view.setFixedSize(safe_size, safe_size)
            if hasattr(beat_view, "setMinimumSize"):
                beat_view.setMinimumSize(min_size, min_size)

        # Also resize start position view (V1 behavior)
        if start_position_view:
            start_position_view.setFixedSize(safe_size, safe_size)
            if hasattr(start_position_view, "setMinimumSize"):
                start_position_view.setMinimumSize(min_size, min_size)

    def clear_cache(self):
        """Clear size calculation cache"""
        self._size_cache.clear()
        self._last_calculated_size = None
