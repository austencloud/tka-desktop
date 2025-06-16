"""
Enhanced Beat Layout Service

Provides intelligent beat frame layout calculations with comprehensive
default layouts, user override support, and dynamic sequence adaptation.
"""

from abc import ABC, abstractmethod
import json
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from PyQt6.QtCore import QSettings

from domain.models.core_models import SequenceData


def get_data_path(filename: str) -> str:
    """Helper function to get data file paths"""
    import os

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, "..", "..", "..", "..")
    return os.path.join(project_root, "data", filename)


@dataclass
class LayoutConfig:
    """Configuration for the enhanced layout system"""

    grow_sequence: bool = True
    overrides_file: str = "beat_layout_overrides.json"


class IBeatLayoutService(ABC):
    """Interface for beat layout operations."""

    @abstractmethod
    def calculate_beat_frame_layout(
        self, sequence: SequenceData, container_size: Tuple[int, int]
    ) -> Dict[str, int]:
        """Calculate layout for beat frames in a sequence."""
        pass

    @abstractmethod
    def calculate_optimal_layout(self, beat_count: int) -> Dict[str, int]:
        """Calculate optimal grid layout for given beat count."""
        pass

    @abstractmethod
    def get_current_layout(self, sequence: SequenceData) -> Tuple[int, int]:
        """Get current layout as tuple"""
        pass

    @abstractmethod
    def clear_cache(self):
        """Clear layout cache (for settings changes)"""
        pass

    @abstractmethod
    def set_layout_override(self, beat_count: int, rows: int, columns: int):
        """Set user layout override"""
        pass

    @abstractmethod
    def get_optimal_grid_layout(
        self, item_count: int, container_size: Tuple[int, int]
    ) -> Tuple[int, int]:
        """Get optimal grid layout (rows, cols) for items."""
        pass

    @abstractmethod
    def get_layout_configurations(self) -> Dict[int, Dict[str, int]]:
        """Get all predefined layout configurations"""
        pass

    @abstractmethod
    def update_layout_configuration(self, beat_count: int, rows: int, columns: int):
        """Update layout configuration for specific beat count"""
        pass


class BeatLayoutService:
    """
    Enhanced beat frame layout service with comprehensive defaults
    and intelligent sequence adaptation.
    """

    def __init__(self, config: Optional[LayoutConfig] = None):
        self.config = config or LayoutConfig()
        self.settings = QSettings("TKA", "KineticConstructor")
        self._layout_cache = {}
        self._overrides_cache = None

        # Complete default layouts (rows, columns) for all beat counts
        self._default_layouts = {
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

    def calculate_beat_frame_layout(
        self, sequence: SequenceData, container_size: Tuple[int, int]
    ) -> Dict[str, int]:
        """
        Calculate layout using intelligent sequence adaptation.

        Args:
            sequence: Current sequence data
            container_size: Available container size (width, height)

        Returns:
            Dictionary with 'rows' and 'columns' keys
        """
        # Dynamic sequence growth logic
        beat_count = len(sequence.beats)
        if self._get_grow_sequence_setting():
            filled_count = self._count_filled_beats(sequence)
            beat_count = filled_count if filled_count > 0 else beat_count

        return self._get_layout_for_beat_count(beat_count)

    def calculate_optimal_layout(self, beat_count: int) -> Dict[str, int]:
        """
        Calculate optimal grid layout for given beat count.

        Args:
            beat_count: Number of beats in sequence

        Returns:
            Dictionary with 'rows' and 'columns' keys
        """
        return self._get_layout_for_beat_count(beat_count)

    def _get_layout_for_beat_count(self, beat_count: int) -> Dict[str, int]:
        """Get layout with caching and override support"""
        # Check cache first
        cache_key = str(beat_count)
        if cache_key in self._layout_cache:
            return self._layout_cache[cache_key]

        # Load overrides (priority system)
        overrides = self._load_overrides()
        if cache_key in overrides:
            layout = overrides[cache_key]
        else:
            # Use built-in default layouts
            layout = self._default_layouts.get(cache_key, [1, max(1, beat_count)])

        # Convert format [rows, cols] to dictionary
        result = {"rows": layout[0], "columns": layout[1]}
        self._layout_cache[cache_key] = result
        return result

    def _load_overrides(self) -> Dict[str, List[int]]:
        """Load user overrides from JSON file"""
        if self._overrides_cache is not None:
            return self._overrides_cache

        overrides_path = get_data_path(self.config.overrides_file)
        if not os.path.exists(overrides_path):
            self._overrides_cache = {}
            return self._overrides_cache

        try:
            with open(overrides_path, "r") as file:
                content = file.read().strip()
                if not content:
                    self._overrides_cache = {}
                    return self._overrides_cache

                self._overrides_cache = json.loads(content)
                return self._overrides_cache
        except (FileNotFoundError, json.JSONDecodeError):
            self._overrides_cache = {}
            return self._overrides_cache

    def _get_grow_sequence_setting(self) -> bool:
        """Get grow sequence setting from QSettings"""
        return self.settings.value("global/grow_sequence", True, type=bool)

    def _count_filled_beats(self, sequence: SequenceData) -> int:
        """Count filled beats in sequence"""
        return len([beat for beat in sequence.beats if beat is not None])

    def set_layout_override(self, beat_count: int, rows: int, columns: int):
        """Set user layout override"""
        overrides = self._load_overrides()
        overrides[str(beat_count)] = [rows, columns]
        self._save_overrides(overrides)

        # Clear cache to force reload
        self._overrides_cache = None
        if str(beat_count) in self._layout_cache:
            del self._layout_cache[str(beat_count)]

    def _save_overrides(self, overrides: Dict[str, List[int]]):
        """Save overrides to JSON file"""
        overrides_path = get_data_path(self.config.overrides_file)
        os.makedirs(os.path.dirname(overrides_path), exist_ok=True)

        # Inline list formatting
        class InlineListEncoder(json.JSONEncoder):
            def encode(self, obj):
                if isinstance(obj, dict):
                    formatted_items = []
                    for key, value in obj.items():
                        if isinstance(value, list):
                            value_str = json.dumps(value, separators=(",", ":"))
                        else:
                            value_str = json.dumps(value)
                        formatted_items.append(f'  "{key}": {value_str}')
                    return "{\n" + ",\n".join(formatted_items) + "\n}"
                return super().encode(obj)

        with open(overrides_path, "w") as file:
            json.dump(overrides, file, cls=InlineListEncoder, indent=2)

    def get_current_layout(self, sequence: SequenceData) -> Tuple[int, int]:
        """Get current layout as tuple"""
        layout = self.calculate_beat_frame_layout(sequence, (800, 600))
        return layout["rows"], layout["columns"]

    def clear_cache(self):
        """Clear layout cache (for settings changes)"""
        self._layout_cache.clear()
        self._overrides_cache = None
