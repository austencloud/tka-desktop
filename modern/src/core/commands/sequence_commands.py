"""
Sequence-specific commands for undoable sequence operations.
These commands integrate with the event system and domain models.
"""

import uuid
from typing import Optional, Any, TYPE_CHECKING
from dataclasses import dataclass
from datetime import datetime

from .command_system import ICommand

if TYPE_CHECKING:
    from ..events import IEventBus

from ..events import (
    IEventBus,
    BeatAddedEvent,
    BeatRemovedEvent,
    BeatUpdatedEvent,
)

# Use absolute imports to avoid relative import issues
if TYPE_CHECKING:
    from domain.models.core_models import SequenceData, BeatData
else:
    # For runtime when imports might fail
    try:
        from domain.models.core_models import SequenceData, BeatData
    except ImportError:
        # Create type aliases that work at runtime
        SequenceData = Any
        BeatData = Any


@dataclass
class AddBeatCommand(ICommand[Any]):  # Use Any for generic parameter
    """Command to add a beat to a sequence."""

    sequence: Any  # SequenceData
    beat: Any  # BeatData
    position: int
    event_bus: Any  # IEventBus
    _command_id: str = ""
    _result_sequence: Optional[Any] = None  # Optional[SequenceData]

    def __post_init__(self):
        if not self._command_id:
            self._command_id = str(uuid.uuid4())

    @property
    def command_id(self) -> str:
        return self._command_id

    @property
    def description(self) -> str:
        letter = self.beat.letter or "blank"
        return f"Add beat '{letter}' at position {self.position + 1}"

    def execute(self) -> Any:  # SequenceData
        """Execute: Add beat to sequence and publish event."""
        if not self.can_execute():
            raise ValueError("Cannot add beat - invalid position")

        # Create new sequence with beat added
        new_beats = list(self.sequence.beats)
        new_beat = self.beat.update(beat_number=self.position + 1)
        new_beats.insert(self.position, new_beat)

        # Renumber subsequent beats
        for i in range(self.position + 1, len(new_beats)):
            new_beats[i] = new_beats[i].update(beat_number=i + 1)

        self._result_sequence = self.sequence.update(beats=new_beats)

        # Publish event for other services to respond
        self.event_bus.publish(
            BeatAddedEvent(
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                source="AddBeatCommand",
                sequence_id=self.sequence.id,
                beat_data=new_beat.to_dict(),
                beat_position=self.position,
                total_beats=len(self._result_sequence.beats),
            )
        )

        return self._result_sequence

    def undo(self) -> Any:  # SequenceData
        """Undo: Remove the beat that was added and publish event."""
        if not self.can_undo():
            raise ValueError("Cannot undo - no result sequence available")

        # Remove the beat that was added
        new_beats = list(self._result_sequence.beats)
        removed_beat = new_beats.pop(self.position)

        # Renumber subsequent beats
        for i in range(self.position, len(new_beats)):
            new_beats[i] = new_beats[i].update(beat_number=i + 1)

        original_sequence = self.sequence.update(beats=new_beats)

        # Publish event
        self.event_bus.publish(
            BeatRemovedEvent(
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                source="AddBeatCommand.undo",
                sequence_id=self.sequence.id,
                removed_beat_data=removed_beat.to_dict(),
                old_position=self.position,
                remaining_beats=len(original_sequence.beats),
            )
        )

        return original_sequence

    def can_execute(self) -> bool:
        """Check if beat can be added at the specified position."""
        return 0 <= self.position <= len(self.sequence.beats)

    def can_undo(self) -> bool:
        """Check if command can be undone."""
        return self._result_sequence is not None


@dataclass
class RemoveBeatCommand(ICommand[Any]):  # ICommand[SequenceData]
    """Command to remove a beat from a sequence."""

    sequence: Any  # SequenceData
    position: int
    event_bus: Any  # IEventBus
    _command_id: str = ""
    _removed_beat: Optional[Any] = None  # Optional[BeatData]

    def __post_init__(self):
        if not self._command_id:
            self._command_id = str(uuid.uuid4())

    @property
    def command_id(self) -> str:
        return self._command_id

    @property
    def description(self) -> str:
        return f"Remove beat at position {self.position + 1}"

    def execute(self) -> Any:  # SequenceData
        """Execute: Remove beat from sequence and publish event."""
        if not self.can_execute():
            raise ValueError("Cannot remove beat - invalid position")

        # Store removed beat for undo
        self._removed_beat = self.sequence.beats[self.position]

        # Create new sequence with beat removed
        new_beats = list(self.sequence.beats)
        new_beats.pop(self.position)

        # Renumber subsequent beats
        for i in range(self.position, len(new_beats)):
            new_beats[i] = new_beats[i].update(beat_number=i + 1)

        result_sequence = self.sequence.update(beats=new_beats)

        # Publish event
        self.event_bus.publish(
            BeatRemovedEvent(
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                source="RemoveBeatCommand",
                sequence_id=self.sequence.id,
                removed_beat_data=self._removed_beat.to_dict(),
                old_position=self.position,
                remaining_beats=len(result_sequence.beats),
            )
        )

        return result_sequence

    def undo(self) -> Any:  # SequenceData
        """Undo: Re-add the removed beat and publish event."""
        if not self.can_undo():
            raise ValueError("Cannot undo - no removed beat stored")

        # Re-insert the removed beat
        new_beats = list(self.sequence.beats)
        restored_beat = self._removed_beat.update(beat_number=self.position + 1)
        new_beats.insert(self.position, restored_beat)

        # Renumber subsequent beats
        for i in range(self.position + 1, len(new_beats)):
            new_beats[i] = new_beats[i].update(beat_number=i + 1)

        original_sequence = self.sequence.update(beats=new_beats)

        # Publish event
        self.event_bus.publish(
            BeatAddedEvent(
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                source="RemoveBeatCommand.undo",
                sequence_id=self.sequence.id,
                beat_data=restored_beat.to_dict(),
                beat_position=self.position,
                total_beats=len(original_sequence.beats),
            )
        )

        return original_sequence

    def can_execute(self) -> bool:
        """Check if beat can be removed from the specified position."""
        return 0 <= self.position < len(self.sequence.beats)

    def can_undo(self) -> bool:
        """Check if command can be undone."""
        return self._removed_beat is not None


@dataclass
class UpdateBeatCommand(ICommand[Any]):  # ICommand[SequenceData]
    """Command to update a beat's properties."""

    sequence: Any  # SequenceData
    beat_number: int
    field_name: str
    new_value: Any
    event_bus: Any  # IEventBus
    _command_id: str = ""
    _old_value: Any = None

    def __post_init__(self):
        if not self._command_id:
            self._command_id = str(uuid.uuid4())

    @property
    def command_id(self) -> str:
        return self._command_id

    @property
    def description(self) -> str:
        return f"Update beat {self.beat_number} {self.field_name} to {self.new_value}"

    def execute(self) -> Any:  # SequenceData
        """Execute: Update beat field and publish event."""
        if not self.can_execute():
            raise ValueError(
                f"Cannot update beat {self.beat_number} - invalid beat number"
            )

        # Find the beat to update
        beat_to_update = None
        for beat in self.sequence.beats:
            if beat.beat_number == self.beat_number:
                beat_to_update = beat
                break

        if not beat_to_update:
            raise ValueError(f"Beat {self.beat_number} not found")

        # Store old value for undo
        self._old_value = getattr(beat_to_update, self.field_name)

        # Update the beat
        update_dict = {self.field_name: self.new_value}
        updated_beat = beat_to_update.update(**update_dict)

        # Create new sequence with updated beat
        new_beats = []
        for beat in self.sequence.beats:
            if beat.beat_number == self.beat_number:
                new_beats.append(updated_beat)
            else:
                new_beats.append(beat)

        result_sequence = self.sequence.update(beats=new_beats)

        # Publish event
        self.event_bus.publish(
            BeatUpdatedEvent(
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                source="UpdateBeatCommand",
                sequence_id=self.sequence.id,
                beat_number=self.beat_number,
                field_changed=self.field_name,
                old_value=self._old_value,
                new_value=self.new_value,
            )
        )

        return result_sequence

    def undo(self) -> Any:  # SequenceData
        """Undo: Restore the old field value and publish event."""
        if not self.can_undo():
            raise ValueError("Cannot undo - no old value stored")

        # Find the beat to restore
        beat_to_restore = None
        for beat in self.sequence.beats:
            if beat.beat_number == self.beat_number:
                beat_to_restore = beat
                break

        if not beat_to_restore:
            raise ValueError(f"Beat {self.beat_number} not found")

        # Restore old value
        update_dict = {self.field_name: self._old_value}
        restored_beat = beat_to_restore.update(**update_dict)

        # Create sequence with restored beat
        new_beats = []
        for beat in self.sequence.beats:
            if beat.beat_number == self.beat_number:
                new_beats.append(restored_beat)
            else:
                new_beats.append(beat)

        original_sequence = self.sequence.update(beats=new_beats)

        # Publish event
        self.event_bus.publish(
            BeatUpdatedEvent(
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                source="UpdateBeatCommand.undo",
                sequence_id=self.sequence.id,
                beat_number=self.beat_number,
                field_changed=self.field_name,
                old_value=self.new_value,
                new_value=self._old_value,
            )
        )

        return original_sequence

    def can_execute(self) -> bool:
        """Check if beat can be updated."""
        return any(beat.beat_number == self.beat_number for beat in self.sequence.beats)

    def can_undo(self) -> bool:
        """Check if command can be undone."""
        return self._old_value is not None
