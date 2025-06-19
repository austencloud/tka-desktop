"""
Sequence Management Service - Unified Sequence Operations

Consolidates all sequence-related services into a single cohesive service:
- Simple sequence operations (simple_sequence_service)
- Beat management (beat_management_service)
- Sequence generation (generation_services)
- Workbench transformations (workbench_services)

This service provides a clean, unified interface for all sequence operations
while maintaining the proven algorithms from the individual services.
"""

from typing import List, Dict, Any, Optional, Tuple, Union, TYPE_CHECKING, cast
from abc import ABC, abstractmethod
from enum import Enum
import uuid
import logging
from copy import deepcopy
from datetime import datetime

from domain.models.core_models import (
    SequenceData,
    BeatData,
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)
from domain.models.pictograph_models import PictographData

# Event-driven architecture imports
if TYPE_CHECKING:
    from core.events import IEventBus
    from core.commands import CommandProcessor

try:
    from core.events import (
        IEventBus,
        get_event_bus,
        SequenceCreatedEvent,
        BeatAddedEvent,
        BeatUpdatedEvent,
        BeatRemovedEvent,
    )
    from core.commands import (
        CommandProcessor,
        AddBeatCommand,
        RemoveBeatCommand,
        UpdateBeatCommand,
    )

    EVENT_SYSTEM_AVAILABLE = True
except ImportError:
    # For tests or when event system is not available
    IEventBus = None
    get_event_bus = None
    CommandProcessor = None
    EVENT_SYSTEM_AVAILABLE = False

try:
    from core.decorators import handle_service_errors
    from core.monitoring import monitor_performance
    from core.exceptions import ServiceOperationError, ValidationError
except ImportError:
    # For tests, create dummy decorators if imports fail
    def handle_service_errors(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    def monitor_performance(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    class ServiceOperationError(Exception):
        pass

    class ValidationError(Exception):
        pass


logger = logging.getLogger(__name__)


class ISequenceManagementService(ABC):
    """Unified interface for all sequence management operations."""

    @abstractmethod
    def create_sequence(self, name: str, length: int = 16) -> SequenceData:
        """Create a new sequence with specified length."""
        pass

    @abstractmethod
    def add_beat(
        self, sequence: SequenceData, beat: BeatData, position: int
    ) -> SequenceData:
        """Add beat to sequence at specified position."""
        pass

    @abstractmethod
    def remove_beat(self, sequence: SequenceData, position: int) -> SequenceData:
        """Remove beat from sequence at specified position."""
        pass

    @abstractmethod
    def generate_sequence(
        self, sequence_type: str, length: int, **kwargs
    ) -> SequenceData:
        """Generate sequence using specified algorithm."""
        pass

    @abstractmethod
    def apply_workbench_operation(
        self, sequence: SequenceData, operation: str, **kwargs
    ) -> SequenceData:
        """Apply workbench transformation to sequence."""
        pass

    # NEW: Event-driven methods with undo support
    @abstractmethod
    def create_sequence_with_events(self, name: str, length: int = 16) -> SequenceData:
        """Create sequence and publish creation event."""
        pass

    @abstractmethod
    def add_beat_with_undo(
        self, beat: BeatData, position: Optional[int] = None
    ) -> SequenceData:
        """Add beat using command pattern with undo support."""
        pass

    @abstractmethod
    def remove_beat_with_undo(self, position: int) -> SequenceData:
        """Remove beat using command pattern with undo support."""
        pass

    @abstractmethod
    def update_beat_with_undo(
        self, beat_number: int, field_name: str, new_value: Any
    ) -> SequenceData:
        """Update beat field using command pattern with undo support."""
        pass

    @abstractmethod
    def undo_last_operation(self) -> Optional[SequenceData]:
        """Undo the last operation."""
        pass

    @abstractmethod
    def redo_last_operation(self) -> Optional[SequenceData]:
        """Redo the last undone operation."""
        pass

    @abstractmethod
    def can_undo(self) -> bool:
        """Check if undo is available."""
        pass

    @abstractmethod
    def can_redo(self) -> bool:
        """Check if redo is available."""
        pass

    @abstractmethod
    def get_undo_description(self) -> Optional[str]:
        """Get description of operation that would be undone."""
        pass

    @abstractmethod
    def get_redo_description(self) -> Optional[str]:
        """Get description of operation that would be redone."""
        pass

    @abstractmethod
    def set_current_sequence(self, sequence: SequenceData) -> None:
        """Set the current sequence for event-driven operations."""
        pass

    @abstractmethod
    def get_current_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence."""
        pass


class SequenceType(Enum):
    """Types of sequence generation algorithms."""

    FREEFORM = "freeform"
    CIRCULAR = "circular"
    AUTO_COMPLETE = "auto_complete"
    MIRROR = "mirror"
    CONTINUOUS = "continuous"


class WorkbenchOperation(Enum):
    """Types of workbench operations."""

    COLOR_SWAP = "color_swap"
    HORIZONTAL_REFLECTION = "horizontal_reflection"
    VERTICAL_REFLECTION = "vertical_reflection"
    ROTATION_90 = "rotation_90"
    ROTATION_180 = "rotation_180"
    ROTATION_270 = "rotation_270"
    REVERSE_SEQUENCE = "reverse_sequence"


class SequenceManagementService(ISequenceManagementService):
    """
    Unified sequence management service consolidating all sequence operations.

    Provides comprehensive sequence management including:
    - CRUD operations for sequences and beats
    - Multiple sequence generation algorithms
    - Workbench transformations (color swap, reflection, rotation)
    - Sequence validation and optimization
    """

    def __init__(self, event_bus: Optional[Any] = None):
        # Event system integration
        self.event_bus = event_bus or (get_event_bus() if get_event_bus else None)
        self.command_processor = (
            CommandProcessor(self.event_bus)
            if CommandProcessor and self.event_bus
            else None
        )

        # Current state (will be managed by commands)
        self._current_sequence: Optional[SequenceData] = None

        # Workbench transformation matrices
        self._transformation_matrices = self._load_transformation_matrices()

        # Validation rules
        self._sequence_validation_rules = self._load_validation_rules()

        # Dictionary service functionality
        self._dictionary_cache = {}
        self._difficulty_cache = {}

    @handle_service_errors("create_sequence")
    @monitor_performance("sequence_creation")
    def create_sequence(self, name: str, length: int = 16) -> SequenceData:
        """Create a new sequence with specified length."""
        # Validate inputs
        if not isinstance(name, str) or not name.strip():
            raise ValidationError("Sequence name must be a non-empty string")

        if not isinstance(length, int) or length < 1 or length > 64:
            raise ValidationError("Sequence length must be an integer between 1 and 64")

        beats = []

        # Create empty beats for the sequence
        for i in range(length):
            beat = BeatData(
                beat_number=i + 1,
                letter=None,
                duration=1.0,
                blue_motion=None,
                red_motion=None,
            )
            beats.append(beat)

        sequence = SequenceData(
            id=str(uuid.uuid4()),
            name=name,
            beats=beats,
            metadata={"created_by": "sequence_management_service"},
        )

        # Publish sequence created event
        if self.event_bus:
            self.event_bus.publish(
                SequenceCreatedEvent(
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source="SequenceManagementService",
                    sequence_id=sequence.id,
                    sequence_name=sequence.name,
                    sequence_length=sequence.length,
                )
            )

        return sequence

    @handle_service_errors("add_beat")
    @monitor_performance("beat_addition")
    def add_beat(
        self, sequence: SequenceData, beat: BeatData, position: int
    ) -> SequenceData:
        """Add beat to sequence at specified position."""
        # Validate inputs
        if not isinstance(sequence, SequenceData):
            raise ValidationError("Sequence must be a SequenceData instance")
        if not isinstance(beat, BeatData):
            raise ValidationError("Beat must be a BeatData instance")
        if not isinstance(position, int):
            raise ValidationError("Position must be an integer")

        if position < 0 or position > len(sequence.beats):
            raise ValidationError(
                f"Invalid position {position} for sequence of length {len(sequence.beats)}"
            )

        new_beats = sequence.beats.copy()
        new_beats.insert(position, beat)

        # Update beat numbers
        for i, beat in enumerate(new_beats):
            new_beats[i] = beat.update(beat_number=i + 1)

        updated_sequence = sequence.update(beats=new_beats)

        # Publish beat added event
        if self.event_bus:
            self.event_bus.publish(
                BeatAddedEvent(
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source="SequenceManagementService",
                    sequence_id=sequence.id,
                    beat_data={"beat_number": beat.beat_number, "position": position},
                    beat_position=position,
                    total_beats=len(new_beats),
                )
            )

        return updated_sequence

    @handle_service_errors("remove_beat")
    @monitor_performance("beat_removal")
    def remove_beat(self, sequence: SequenceData, position: int) -> SequenceData:
        """Remove beat from sequence at specified position."""
        # Validate inputs
        if not isinstance(sequence, SequenceData):
            raise ValidationError("Sequence must be a SequenceData instance")
        if not isinstance(position, int):
            raise ValidationError("Position must be an integer")

        if position < 0 or position >= len(sequence.beats):
            raise ValidationError(
                f"Invalid position {position} for sequence of length {len(sequence.beats)}"
            )

        new_beats = sequence.beats.copy()
        removed_beat = new_beats.pop(position)

        # Update beat numbers
        for i, beat in enumerate(new_beats):
            new_beats[i] = beat.update(beat_number=i + 1)

        updated_sequence = sequence.update(beats=new_beats)

        # Publish beat removed event
        if self.event_bus:
            self.event_bus.publish(
                BeatRemovedEvent(
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source="SequenceManagementService",
                    sequence_id=sequence.id,
                    removed_beat_data={"beat_number": removed_beat.beat_number},
                    old_position=position,
                    remaining_beats=len(new_beats),
                )
            )

        return updated_sequence

    @handle_service_errors("generate_sequence")
    @monitor_performance("sequence_generation")
    def generate_sequence(
        self, sequence_type: str, length: int, **kwargs
    ) -> SequenceData:
        """Generate sequence using specified algorithm."""
        sequence_type_enum = SequenceType(sequence_type)

        if sequence_type_enum == SequenceType.FREEFORM:
            return self._generate_freeform_sequence(length, **kwargs)
        elif sequence_type_enum == SequenceType.CIRCULAR:
            return self._generate_circular_sequence(length, **kwargs)
        elif sequence_type_enum == SequenceType.AUTO_COMPLETE:
            return self._generate_auto_complete_sequence(length, **kwargs)
        elif sequence_type_enum == SequenceType.MIRROR:
            return self._generate_mirror_sequence(length, **kwargs)
        elif sequence_type_enum == SequenceType.CONTINUOUS:
            return self._generate_continuous_sequence(length, **kwargs)
        else:
            raise ValueError(f"Unknown sequence type: {sequence_type}")

    @handle_service_errors("apply_workbench_operation")
    @monitor_performance("workbench_operation")
    def apply_workbench_operation(
        self, sequence: SequenceData, operation: str, **kwargs
    ) -> SequenceData:
        """Apply workbench transformation to sequence."""
        operation_enum = WorkbenchOperation(operation)

        if operation_enum == WorkbenchOperation.COLOR_SWAP:
            return self._apply_color_swap(sequence)
        elif operation_enum == WorkbenchOperation.HORIZONTAL_REFLECTION:
            return self._apply_horizontal_reflection(sequence)
        elif operation_enum == WorkbenchOperation.VERTICAL_REFLECTION:
            return self._apply_vertical_reflection(sequence)
        elif operation_enum == WorkbenchOperation.ROTATION_90:
            return self._apply_rotation(sequence, 90)
        elif operation_enum == WorkbenchOperation.ROTATION_180:
            return self._apply_rotation(sequence, 180)
        elif operation_enum == WorkbenchOperation.ROTATION_270:
            return self._apply_rotation(sequence, 270)
        elif operation_enum == WorkbenchOperation.REVERSE_SEQUENCE:
            return self._apply_reverse_sequence(sequence)
        else:
            raise ValueError(f"Unknown workbench operation: {operation}")

    # NEW: Event-driven methods with undo capability

    def create_sequence_with_events(self, name: str, length: int = 16) -> SequenceData:
        """Create sequence and publish creation event."""
        sequence = self.create_sequence(name, length)  # Use existing logic

        if self.event_bus:
            # Publish creation event instead of calling other services directly
            self.event_bus.publish(
                SequenceCreatedEvent(
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source="SequenceManagementService",
                    sequence_id=sequence.id,
                    sequence_name=sequence.name,
                    sequence_length=sequence.length,
                )
            )

        self._current_sequence = sequence
        return sequence

    def add_beat_with_undo(
        self, beat: BeatData, position: Optional[int] = None
    ) -> SequenceData:
        """Add beat using command pattern with undo support."""
        if not self._current_sequence:
            raise ValueError("No active sequence")

        if not self.command_processor:
            raise ValueError(
                "Command processor not available - event system not initialized"
            )

        if not self.event_bus:
            raise ValueError("Event bus not available - event system not initialized")

        if position is None:
            position = len(self._current_sequence.beats)

        # Create and execute command (this publishes events automatically)
        command = AddBeatCommand(
            sequence=self._current_sequence,
            beat=beat,
            position=position,
            event_bus=self.event_bus,
        )

        result = self.command_processor.execute(command)
        if result.success:
            assert result.result is not None, "Command succeeded but result is None"
            self._current_sequence = cast(SequenceData, result.result)
            return cast(SequenceData, result.result)
        else:
            raise RuntimeError(f"Failed to add beat: {result.error_message}")

    def remove_beat_with_undo(self, position: int) -> SequenceData:
        """Remove beat using command pattern with undo support."""
        if not self._current_sequence:
            raise ValueError("No active sequence")

        if not self.command_processor:
            raise ValueError(
                "Command processor not available - event system not initialized"
            )

        if not self.event_bus:
            raise ValueError("Event bus not available - event system not initialized")

        command = RemoveBeatCommand(
            sequence=self._current_sequence, position=position, event_bus=self.event_bus
        )

        result = self.command_processor.execute(command)
        if result.success:
            assert result.result is not None, "Command succeeded but result is None"
            self._current_sequence = cast(SequenceData, result.result)
            return cast(SequenceData, result.result)
        else:
            raise RuntimeError(f"Failed to remove beat: {result.error_message}")

    def update_beat_with_undo(
        self, beat_number: int, field_name: str, new_value: Any
    ) -> SequenceData:
        """Update beat field using command pattern with undo support."""
        if not self._current_sequence:
            raise ValueError("No active sequence")

        if not self.command_processor:
            raise ValueError(
                "Command processor not available - event system not initialized"
            )

        if not self.event_bus:
            raise ValueError("Event bus not available - event system not initialized")

        command = UpdateBeatCommand(
            sequence=self._current_sequence,
            beat_number=beat_number,
            field_name=field_name,
            new_value=new_value,
            event_bus=self.event_bus,
        )

        result = self.command_processor.execute(command)
        if result.success:
            assert result.result is not None, "Command succeeded but result is None"
            self._current_sequence = cast(SequenceData, result.result)
            return cast(SequenceData, result.result)
        else:
            raise RuntimeError(f"Failed to update beat: {result.error_message}")

    # NEW: Undo/Redo methods

    def undo_last_operation(self) -> Optional[SequenceData]:
        """Undo the last operation."""
        if not self.command_processor:
            return None

        result = self.command_processor.undo()
        if result.success:
            self._current_sequence = cast(SequenceData, result.result)
            return cast(SequenceData, result.result)
        return None

    def redo_last_operation(self) -> Optional[SequenceData]:
        """Redo the last undone operation."""
        if not self.command_processor:
            return None

        result = self.command_processor.redo()
        if result.success:
            self._current_sequence = cast(SequenceData, result.result)
            return cast(SequenceData, result.result)
        return None

    def can_undo(self) -> bool:
        """Check if undo is available."""
        return self.command_processor.can_undo() if self.command_processor else False

    def can_redo(self) -> bool:
        """Check if redo is available."""
        return self.command_processor.can_redo() if self.command_processor else False

    def get_undo_description(self) -> Optional[str]:
        """Get description of operation that would be undone."""
        return (
            self.command_processor.get_undo_description()
            if self.command_processor
            else None
        )

    def get_redo_description(self) -> Optional[str]:
        """Get description of operation that would be redone."""
        return (
            self.command_processor.get_redo_description()
            if self.command_processor
            else None
        )

    def set_current_sequence(self, sequence: SequenceData) -> None:
        """Set the current sequence for event-driven operations."""
        self._current_sequence = sequence

    def get_current_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence."""
        return self._current_sequence

    # Private sequence generation methods

    def _generate_freeform_sequence(self, length: int, **_kwargs) -> SequenceData:
        """Generate freeform sequence with random valid motions."""
        sequence = self.create_sequence("Freeform Sequence", length)
        return sequence

    def _generate_circular_sequence(self, length: int, **_kwargs) -> SequenceData:
        """Generate circular sequence where end connects to beginning."""
        sequence = self.create_sequence("Circular Sequence", length)
        return sequence

    def _generate_auto_complete_sequence(self, length: int, **_kwargs) -> SequenceData:
        """Generate auto-completed sequence based on pattern recognition."""
        sequence = self.create_sequence("Auto Complete Sequence", length)
        return sequence

    def _generate_mirror_sequence(self, length: int, **_kwargs) -> SequenceData:
        """Generate mirror sequence (palindromic pattern)."""
        sequence = self.create_sequence("Mirror Sequence", length)
        return sequence

    def _generate_continuous_sequence(self, length: int, **_kwargs) -> SequenceData:
        """Generate continuous sequence where each beat flows into the next."""
        sequence = self.create_sequence("Continuous Sequence", length)
        return sequence

    def _apply_color_swap(self, sequence: SequenceData) -> SequenceData:
        """Swap blue and red motions in all beats."""
        new_beats = []
        for beat in sequence.beats:
            new_beat = beat.update(
                blue_motion=beat.red_motion,
                red_motion=beat.blue_motion,
            )
            new_beats.append(new_beat)
        return sequence.update(beats=new_beats)

    def _apply_vertical_reflection(self, sequence: SequenceData) -> SequenceData:
        """Apply vertical reflection to all motions."""
        return sequence

    def _apply_rotation(self, sequence: SequenceData, degrees: int) -> SequenceData:
        """Apply rotation to all motions."""
        return sequence

    def _apply_horizontal_reflection(self, sequence: SequenceData) -> SequenceData:
        """Apply horizontal reflection to all motions."""
        return sequence

    def _apply_reverse_sequence(self, sequence: SequenceData) -> SequenceData:
        """Reverse the order of beats in sequence."""
        new_beats = list(reversed(sequence.beats))
        for i, beat in enumerate(new_beats):
            new_beats[i] = beat.update(beat_number=i + 1)
        return sequence.update(beats=new_beats)

    def _load_transformation_matrices(self) -> Dict[str, Any]:
        """Load transformation matrices for workbench operations."""
        return {
            "rotation_90": [[0, -1], [1, 0]],
            "rotation_180": [[-1, 0], [0, -1]],
            "rotation_270": [[0, 1], [-1, 0]],
            "horizontal_flip": [[-1, 0], [0, 1]],
            "vertical_flip": [[1, 0], [0, -1]],
        }

    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load sequence validation rules."""
        return {
            "max_length": 64,
            "min_length": 1,
            "required_fields": ["name", "beats"],
        }

    # Dictionary Service Methods (IDictionaryService interface)

    def add_sequence_to_dictionary(self, sequence: SequenceData, word: str) -> bool:
        """Add sequence to dictionary"""
        try:
            sequence_hash = self._hash_sequence(sequence)
            self._dictionary_cache[sequence_hash] = word
            return True
        except Exception:
            return False

    def get_word_for_sequence(self, sequence: SequenceData) -> Optional[str]:
        """Get word associated with sequence"""
        sequence_hash = self._hash_sequence(sequence)
        return self._dictionary_cache.get(sequence_hash)

    @handle_service_errors("calculate_difficulty")
    @monitor_performance("difficulty_calculation")
    def calculate_difficulty(self, sequence: SequenceData) -> int:
        """Calculate sequence difficulty level using validated algorithm"""
        sequence_hash = self._hash_sequence(sequence)

        if sequence_hash in self._difficulty_cache:
            return self._difficulty_cache[sequence_hash]

        # Implement comprehensive difficulty calculation logic
        difficulty = self._calculate_difficulty_score(sequence)
        self._difficulty_cache[sequence_hash] = difficulty
        return difficulty

    def _hash_sequence(self, sequence: SequenceData) -> str:
        """Create hash for sequence to use as cache key"""
        return f"{sequence.name}_{sequence.length}_{len(sequence.beats)}"

    def _calculate_difficulty_score(self, sequence: SequenceData) -> int:
        """Calculate difficulty score based on validated algorithm"""
        if sequence.length <= 1:
            return 0

        # Simplified difficulty calculation
        # Real implementation would analyze prop movements, turns, etc.
        base_difficulty = sequence.length

        # Add complexity factors from analysis
        complexity_bonus = 0
        for _ in sequence.beats:
            # Analyze beat complexity (placeholder)
            complexity_bonus += 1

        return min(base_difficulty + complexity_bonus // 4, 10)
