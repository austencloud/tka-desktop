"""
Enhanced Beat Resizer Service

Implements sophisticated beat sizing logic with precise
dimension calculations and intelligent responsive behavior.
"""

from typing import Tuple, Optional, TYPE_CHECKING, Union
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QScrollArea, QWidget

if TYPE_CHECKING:
    from presentation.components.workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )
    from presentation.components.workbench.beat_frame.beat_frame import (
        BeatFrame,
    )

# Type alias for beat frame components
BeatFrameType = Union["SequenceBeatFrame", "BeatFrame"]


def ensure_positive_size(size: int, min_value: int = 1) -> int:
    """Ensure a size value is positive to avoid Qt warnings"""
    return max(size, min_value)


class BeatResizerService:
    """
    Enhanced beat frame resizer with validated sizing algorithms.

    Provides intelligent beat sizing that considers:
    - Available container space    - Number of columns in current layout
    - Fixed height ratio for optimal display
    - Dynamic scroll bar management
    """

    def __init__(self):
        self._last_calculated_size = None
        self._size_cache = {}

    def resize_beat_frame(
        self, beat_frame: BeatFrameType, num_rows: int, num_columns: int
    ) -> int:
        """
        Complete beat frame resize using validated algorithm.

        Args:
            beat_frame: The beat frame widget
            num_rows: Number of rows in current layout
            num_columns: Number of columns in current layout

        Returns:
            Calculated beat size in pixels
        """
        width, height = self.calculate_dimensions(beat_frame)
        beat_size = self.calculate_beat_size(width, height, num_columns)
        self.resize_beats(beat_frame, beat_size)
        self.configure_scroll_behavior(beat_frame, num_rows)
        return beat_size

    def calculate_dimensions(self, beat_frame: BeatFrameType) -> Tuple[int, int]:
        """
        Calculate available container dimensions using validated logic.

        Algorithm:
        - Takes half the main widget width
        - Subtracts button panel and scrollbar widths
        - Applies 0.8 factor for padding
        - Subtracts graph editor height from available height
        """
        # Find the main widget and related components
        main_widget = self._find_main_widget(beat_frame)
        scroll_area = self._find_scroll_area_parent(beat_frame)

        if not main_widget or not scroll_area:
            # Fallback to widget size
            return int(beat_frame.width() * 0.8), int(beat_frame.height() * 0.8)

        # Validated calculation
        scrollbar_width = scroll_area.verticalScrollBar().width()

        # Main widget width divided by 2 (workbench takes half the screen)
        half_main_width = main_widget.width() // 2

        # Find button panel width (or estimate if not found)
        button_panel_width = self._get_button_panel_width(main_widget)

        # Calculate available width with validated formula
        available_width = half_main_width - button_panel_width - scrollbar_width
        width = int(available_width * 0.8)

        # Calculate available height (subtract graph editor space)
        graph_editor_height = self._get_graph_editor_height(main_widget)
        available_height = main_widget.height() - int(graph_editor_height * 0.8)

        return width, available_height

    def calculate_beat_size(self, width: int, height: int, num_columns: int) -> int:
        """
        Calculate optimal beat size using validated algorithm.

        Algorithm:
        - Width constraint: available_width // num_columns
        - Height constraint: available_height // 6 (fixed ratio!)
        - Final size: min(width_constraint, height_constraint)
        """
        # Caching for performance
        cache_key = (width, height, num_columns)
        if cache_key in self._size_cache:
            return self._size_cache[cache_key]

        if num_columns == 0:
            beat_size = 0
        else:
            # Validated calculation - THIS IS THE KEY LOGIC!
            width_constraint = int(width // num_columns)
            height_constraint = int(height // 6)  # Fixed ratio of 6!
            beat_size = min(width_constraint, height_constraint)

        # Ensure positive size (safety check)
        beat_size = ensure_positive_size(beat_size)

        self._size_cache[cache_key] = beat_size
        return beat_size

    def resize_beats(self, beat_frame: BeatFrameType, beat_size: int):
        """
        Resize beat views using validated logic.

        Algorithm:
        - Sets fixed size to calculated beat_size
        - Sets minimum size to beat_size - 48 for inner content
        - Applies same sizing to start position view
        """
        # Safety check
        safe_size = ensure_positive_size(beat_size)
        min_size = ensure_positive_size(safe_size - 48)

        # Resize all beat views
        beat_views = getattr(beat_frame, "_beat_views", [])
        for beat_view in beat_views:
            beat_view.setFixedSize(safe_size, safe_size)
            if hasattr(beat_view, "setMinimumSize"):
                beat_view.setMinimumSize(min_size, min_size)

        # Also resize start position view (consistent behavior)
        start_position_view = getattr(beat_frame, "_start_position_view", None)
        if start_position_view:
            start_position_view.setFixedSize(safe_size, safe_size)
            if hasattr(start_position_view, "setMinimumSize"):
                start_position_view.setMinimumSize(min_size, min_size)

    def configure_scroll_behavior(self, beat_frame: BeatFrameType, num_rows: int):
        """
        Configure scroll bar behavior using validated logic.

        Algorithm:
        - Show scrollbar if rows > 4
        - Hide scrollbar if rows <= 4
        """
        scroll_area = self._find_scroll_area_parent(beat_frame)
        if scroll_area:
            if num_rows > 4:
                scroll_area.setVerticalScrollBarPolicy(
                    Qt.ScrollBarPolicy.ScrollBarAlwaysOn
                )
            else:
                scroll_area.setVerticalScrollBarPolicy(
                    Qt.ScrollBarPolicy.ScrollBarAlwaysOff
                )

    def _find_main_widget(self, widget: QWidget) -> Optional[QWidget]:
        """Find the main widget by traversing up the parent hierarchy"""
        parent = widget.parent()
        while parent:
            # Look for a widget that looks like a main widget
            if (
                isinstance(parent, QWidget) and parent.width() > 1000
            ):  # Reasonable main window size
                return parent
            parent = parent.parent()
        return None

    def _find_scroll_area_parent(self, widget: QWidget) -> Optional[QScrollArea]:
        """Find QScrollArea parent widget"""
        parent = widget.parent()
        while parent:
            if isinstance(parent, QScrollArea):
                return parent
            parent = parent.parent()
        return None

    def _get_button_panel_width(self, main_widget: QWidget) -> int:
        """Get button panel width or reasonable estimate"""
        # Try to find button panel, otherwise use reasonable default
        button_panel = self._find_child_by_name(main_widget, "button_panel")
        if button_panel and hasattr(button_panel, "width"):
            return button_panel.width()
        return 200  # Reasonable default

    def _get_graph_editor_height(self, main_widget: QWidget) -> int:
        """Get graph editor height or reasonable estimate"""
        # Try to find graph editor, otherwise use reasonable default
        graph_editor = self._find_child_by_name(main_widget, "graph_editor")
        if graph_editor and hasattr(graph_editor, "height"):
            return graph_editor.height()
        return int(main_widget.height() * 0.3)  # Reasonable default (30% of height)

    def _find_child_by_name(self, widget: QWidget, name: str) -> Optional[QWidget]:
        """Find child widget by object name"""
        for child in widget.findChildren(QWidget):
            if child.objectName() == name:
                return child
        return None

    def clear_cache(self):
        """Clear size calculation cache"""
        self._size_cache.clear()
        self._last_calculated_size = None
