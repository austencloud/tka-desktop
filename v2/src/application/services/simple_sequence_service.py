"""
Simple sequence service implementations for Kinetic Constructor v2.

These provide basic implementations of the core services for the demo.
"""

import uuid
from typing import List, Dict, Any, Optional
from PyQt6.QtCore import QSize

from ...core.interfaces.core_services import (
    ILayoutService,
    ISettingsService,
    ISequenceDataService,
    IValidationService,
)
from domain.models.core_models import SequenceData, BeatData


class SimpleLayoutService(ILayoutService):
    """Simple implementation of layout service."""

    def __init__(self):
        self._main_window_size = QSize(1200, 800)
        self._layout_ratio = (2, 1)  # workbench:picker

    def get_main_window_size(self) -> QSize:
        return self._main_window_size

    def get_workbench_size(self) -> QSize:
        total_width = self._main_window_size.width()
        workbench_width = int(
            total_width * self._layout_ratio[0] / sum(self._layout_ratio)
        )
        return QSize(workbench_width, self._main_window_size.height())

    def get_picker_size(self) -> QSize:
        total_width = self._main_window_size.width()
        picker_width = int(
            total_width * self._layout_ratio[1] / sum(self._layout_ratio)
        )
        return QSize(picker_width, self._main_window_size.height())

    def get_layout_ratio(self) -> tuple[int, int]:
        return self._layout_ratio

    def set_layout_ratio(self, ratio: tuple[int, int]) -> None:
        self._layout_ratio = ratio

    def calculate_component_size(
        self, component_type: str, parent_size: QSize
    ) -> QSize:
        return parent_size


class SimpleSettingsService(ISettingsService):
    """Simple implementation of settings service."""

    def __init__(self):
        self._settings: Dict[str, Any] = {}

    def get_setting(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        self._settings[key] = value

    def save_settings(self) -> None:
        # In a real implementation, this would save to file
        pass

    def load_settings(self) -> None:
        # In a real implementation, this would load from file
        pass


class SimpleSequenceDataService(ISequenceDataService):
    """Simple implementation of sequence data service."""

    def __init__(self):
        self._sequences: Dict[str, Dict[str, Any]] = {}
        self._current_sequence_id: Optional[str] = None

    def get_all_sequences(self) -> List[Dict[str, Any]]:
        return list(self._sequences.values())

    def get_sequence_by_id(self, sequence_id: str) -> Optional[Dict[str, Any]]:
        return self._sequences.get(sequence_id)

    def save_sequence(self, sequence_data: Dict[str, Any]) -> bool:
        sequence_id = sequence_data.get("id")
        if sequence_id:
            self._sequences[sequence_id] = sequence_data
            return True
        return False

    def delete_sequence(self, sequence_id: str) -> bool:
        if sequence_id in self._sequences:
            del self._sequences[sequence_id]
            return True
        return False

    def create_new_sequence(self, name: str) -> Dict[str, Any]:
        sequence_id = str(uuid.uuid4())
        sequence_data = {
            "id": sequence_id,
            "name": name,
            "beats": [],
            "length": 0,
            "total_duration": 0.0,
            "is_valid": True,
        }
        self._sequences[sequence_id] = sequence_data
        self._current_sequence_id = sequence_id
        return sequence_data

    def get_current_sequence(self) -> Optional[Dict[str, Any]]:
        if self._current_sequence_id:
            return self._sequences.get(self._current_sequence_id)
        return None

    def set_current_sequence(self, sequence_id: str) -> None:
        self._current_sequence_id = sequence_id


class SimpleValidationService(IValidationService):
    """Simple implementation of validation service."""

    def validate_sequence(self, sequence_data: Dict[str, Any]) -> bool:
        # Basic validation - check required fields
        required_fields = ["id", "name", "beats"]
        return all(field in sequence_data for field in required_fields)

    def validate_beat(self, beat_data: Dict[str, Any]) -> bool:
        # Basic validation - check required fields
        required_fields = ["letter", "duration"]
        return all(field in beat_data for field in required_fields)

    def validate_motion(self, motion_data: Dict[str, Any]) -> bool:
        # Basic validation - check required fields
        required_fields = ["motion_type", "start_loc", "end_loc"]
        return all(field in motion_data for field in required_fields)

    def get_validation_errors(self, data: Dict[str, Any]) -> List[str]:
        errors = []
        if not isinstance(data, dict):
            errors.append("Data must be a dictionary")
        return errors


class SequenceService:
    """High-level sequence service that coordinates other services."""

    def __init__(self):
        # These would normally be injected via dependency injection
        self._data_service = SimpleSequenceDataService()
        self._validation_service = SimpleValidationService()

    def create_new_sequence(self, name: str) -> SequenceData:
        """Create a new sequence."""
        sequence_dict = self._data_service.create_new_sequence(name)
        return self._dict_to_sequence_data(sequence_dict)

    def load_current_sequence(self) -> SequenceData:
        """Load the current sequence."""
        sequence_dict = self._data_service.get_current_sequence()
        if sequence_dict:
            return self._dict_to_sequence_data(sequence_dict)
        else:
            # Return empty sequence if none exists
            return SequenceData(id=str(uuid.uuid4()), name="Empty Sequence", beats=[])

    def add_beat_to_sequence(self, beat: BeatData) -> SequenceData:
        """Add a beat to the current sequence."""
        current_sequence = self._data_service.get_current_sequence()
        if current_sequence:
            current_sequence["beats"].append(beat.__dict__)
            current_sequence["length"] = len(current_sequence["beats"])
            current_sequence["total_duration"] += beat.duration
            self._data_service.save_sequence(current_sequence)
            return self._dict_to_sequence_data(current_sequence)
        else:
            # Create new sequence with this beat
            new_sequence = self.create_new_sequence("New Sequence")
            return self.add_beat_to_sequence(beat)

    def _dict_to_sequence_data(self, sequence_dict: Dict[str, Any]) -> SequenceData:
        """Convert dictionary to SequenceData object."""
        beats = []
        for beat_dict in sequence_dict.get("beats", []):
            if isinstance(beat_dict, dict):
                beat = BeatData(
                    letter=beat_dict.get("letter", "A"),
                    duration=beat_dict.get("duration", 1.0),
                    blue_motion=beat_dict.get("blue_motion"),
                    red_motion=beat_dict.get("red_motion"),
                )
                beats.append(beat)

        return SequenceData(
            id=sequence_dict["id"], name=sequence_dict["name"], beats=beats
        )
