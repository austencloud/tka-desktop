from typing import Dict, Any, Optional, Tuple, List, Union, TYPE_CHECKING
from enum import Enum
from dataclasses import dataclass
import math
import logging
import uuid
from datetime import datetime

from PyQt6.QtCore import QSize
from core.decorators import handle_service_errors
from core.monitoring import monitor_performance
from domain.models.core_models import SequenceData
from core.interfaces.core_services import ILayoutService


class BeatLayoutCalculator:
    """
    Handles comprehensive beat layout calculations with detailed default layouts.

    This class preserves the original carefully designed beat layout logic
    with comprehensive default layouts for beat counts 0-64 and beyond.
    Responsible for determining optimal rows/columns for beat sequences.
    """

    def __init__(self):
        """Initialize the beat layout calculator."""
        # No initialization needed - all methods are stateless calculations
        pass

    @handle_service_errors("calculate_beat_frame_layout")
    @monitor_performance("layout_calculation")
    def calculate_beat_frame_layout(
        self, sequence: SequenceData, container_size: Tuple[int, int]
    ) -> Dict[str, Any]:
        """Calculate layout for beat frames using your original carefully designed algorithm."""
        beat_count = len(sequence.beats)

        # Your original complete default layouts (rows, columns) for all beat counts
        # This preserves your careful layout design decisions
        default_layouts = {
            "0": [1, 0],
            "1": [1, 1],
            "2": [1, 2],
            "3": [1, 3],
            "4": [1, 4],
            "5": [2, 4],
            "6": [2, 4],
            "7": [2, 4],
            "8": [2, 4],
            "9": [3, 4],
            "10": [3, 4],
            "11": [3, 4],
            "12": [4, 3],
            "13": [4, 4],
            "14": [4, 4],
            "15": [4, 4],
            "16": [4, 4],
            "17": [4, 5],
            "18": [4, 5],
            "19": [4, 5],
            "20": [4, 5],
            "21": [6, 4],
            "22": [6, 4],
            "23": [6, 4],
            "24": [6, 4],
            "25": [7, 4],
            "26": [7, 4],
            "27": [7, 4],
            "28": [7, 4],
            "29": [8, 4],
            "30": [8, 4],
            "31": [8, 4],
            "32": [8, 4],
            "33": [9, 4],
            "34": [9, 4],
            "35": [9, 4],
            "36": [9, 4],
            "37": [10, 4],
            "38": [10, 4],
            "39": [10, 4],
            "40": [10, 4],
            "41": [11, 4],
            "42": [11, 4],
            "43": [11, 4],
            "44": [11, 4],
            "45": [11, 4],
            "46": [12, 4],
            "47": [12, 4],
            "48": [12, 4],
            "49": [13, 4],
            "50": [13, 4],
            "51": [13, 4],
            "52": [13, 4],
            "53": [14, 4],
            "54": [14, 4],
            "55": [14, 4],
            "56": [14, 4],
            "57": [15, 4],
            "58": [15, 4],
            "59": [15, 4],
            "60": [15, 4],
            "61": [16, 4],
            "62": [16, 4],
            "63": [16, 4],
            "64": [16, 4],
        }

        # Use your original layout logic
        beat_count_str = str(beat_count)
        if beat_count_str in default_layouts:
            rows, columns = default_layouts[beat_count_str]
            return {"rows": rows, "columns": columns}

        # For beat counts beyond 64, use your pattern (maintain 4 columns, increase rows)
        if beat_count > 64:
            columns = 4
            rows = math.ceil(beat_count / columns)
            return {"rows": rows, "columns": columns}

        # Fallback (should rarely be used with your comprehensive layout table)
        return {"rows": 1, "columns": beat_count}

    @handle_service_errors("get_optimal_grid_layout")
    @monitor_performance("grid_layout_optimization")
    def get_optimal_grid_layout(
        self, item_count: int, container_size: Tuple[int, int]
    ) -> Tuple[int, int]:
        """Get optimal grid layout (rows, cols) for items."""
        if item_count <= 0:
            return (0, 0)

        container_width, container_height = container_size
        aspect_ratio = (
            container_width / container_height if container_height > 0 else 1.0
        )

        # Calculate optimal number of columns based on aspect ratio
        cols = max(1, int(math.sqrt(item_count * aspect_ratio)))
        rows = math.ceil(item_count / cols)

        # Adjust if the layout doesn't fit well
        while cols > 1 and rows * container_height / cols > container_width:
            cols -= 1
            rows = math.ceil(item_count / cols)

        return (rows, cols)

    def _calculate_horizontal_beat_layout(
        self,
        beat_count: int,
        container_size: Tuple[int, int],
        base_size: Tuple[int, int],
        padding: int,
        spacing: int,
    ) -> Dict[str, Any]:
        """Calculate horizontal layout for beats."""
        width, height = container_size
        beat_width, beat_height = base_size

        total_width = beat_count * beat_width + (beat_count - 1) * spacing + 2 * padding

        # Scale if necessary
        if total_width > width:
            scale = (width - 2 * padding - (beat_count - 1) * spacing) / (
                beat_count * beat_width
            )
            beat_width = int(beat_width * scale)
            beat_height = int(beat_height * scale)

        return {
            "layout_type": "horizontal",
            "beat_size": (beat_width, beat_height),
            "spacing": spacing,
            "padding": padding,
            "total_size": (total_width, beat_height + 2 * padding),
        }

    def _calculate_grid_beat_layout(
        self,
        beat_count: int,
        container_size: Tuple[int, int],
        base_size: Tuple[int, int],
        padding: int,
        spacing: int,
    ) -> Dict[str, Any]:
        """Calculate grid layout for beats."""
        rows, cols = self.get_optimal_grid_layout(beat_count, container_size)
        beat_width, beat_height = base_size

        return {
            "layout_type": "grid",
            "rows": rows,
            "columns": cols,
            "beat_size": (beat_width, beat_height),
            "spacing": spacing,
            "padding": padding,
            "total_size": (
                cols * beat_width + (cols - 1) * spacing + 2 * padding,
                rows * beat_height + (rows - 1) * spacing + 2 * padding,
            ),
        }

    def _recalculate_beat_frame_layout(
        self, beat_count: int, container_size: Tuple[int, int], trigger_reason: str
    ) -> Dict[str, Any]:
        """Recalculate beat frame layout and return result."""
        if beat_count == 0:
            return {"positions": {}, "sizes": {}, "total_size": (0, 0)}

        # Use existing logic but with event-driven trigger
        base_size = (120, 120)  # Default beat frame size
        padding = 10
        spacing = 5

        if beat_count <= 8:  # Use horizontal layout
            return self._calculate_horizontal_beat_layout(
                beat_count, container_size, base_size, padding, spacing
            )
        else:  # Use grid layout
            return self._calculate_grid_beat_layout(
                beat_count, container_size, base_size, padding, spacing
            )
