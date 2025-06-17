# Phase 1: Event-Driven Architecture + Command Pattern Implementation

**Target:** Convert TKA Desktop from tightly-coupled direct method calls to event-driven architecture with undoable operations  
**Timeline:** 2 weeks  
**Priority:** CRITICAL for legacy migration success

---

## 📋 Implementation Overview

### **Current Architecture Problem**
```python
# CURRENT: Tight coupling with direct method calls
class SequenceManagementService:
    def add_beat(self, beat):
        # 1. Add beat to sequence
        sequence = self._add_beat_internally(beat)
        
        # 2. PROBLEM: Direct calls create tight coupling
        self.layout_service.recalculate_layout(sequence)  # Tight coupling!
        self.ui_service.refresh_display(sequence)         # Tight coupling!
        self.pictograph_service.update_display(sequence)  # Tight coupling!
        
        # 3. PROBLEM: No undo capability
        # 4. PROBLEM: Hard to add new services (like legacy components)
```

### **Target Architecture Solution**
```python
# TARGET: Event-driven with undo capability
class SequenceManagementService:
    def add_beat_with_undo(self, beat):
        # 1. Create undoable command
        command = AddBeatCommand(self.current_sequence, beat)
        
        # 2. Execute command (creates event automatically)
        result = self.command_processor.execute(command)
        
        # 3. All services respond to event automatically - NO TIGHT COUPLING!
        # 4. Full undo/redo capability
        # 5. Easy to add new services (including legacy components)
```

---

## 🎯 Implementation Steps

### **Step 1: Enhance Event System (Days 1-2)**

The event bus infrastructure already exists but needs domain-specific events for TKA operations.

#### **1.1: Create TKA Domain Events**

**File:** `src/core/events/domain_events.py`
```python
"""
TKA-specific domain events for sequence, motion, and layout operations.
These events replace direct method calls between services.
"""

from dataclasses import dataclass, field
from typing import Optional, Any, Dict, List
from datetime import datetime
import uuid
from .event_bus import BaseEvent, EventPriority


# === Sequence Domain Events ===

@dataclass(frozen=True)
class SequenceCreatedEvent(BaseEvent):
    """Published when a new sequence is created."""
    sequence_id: str
    sequence_name: str
    sequence_length: int
    
    @property
    def event_type(self) -> str:
        return "sequence.created"


@dataclass(frozen=True)
class SequenceUpdatedEvent(BaseEvent):
    """Published when sequence data changes."""
    sequence_id: str
    change_type: str  # "beat_added", "beat_removed", "beat_updated", "metadata_changed"
    previous_state: Optional[Dict[str, Any]] = None
    new_state: Optional[Dict[str, Any]] = None
    
    @property
    def event_type(self) -> str:
        return f"sequence.{self.change_type}"


@dataclass(frozen=True)
class BeatAddedEvent(BaseEvent):
    """Published when a beat is added to a sequence."""
    sequence_id: str
    beat_data: Dict[str, Any]
    beat_position: int
    total_beats: int
    
    @property
    def event_type(self) -> str:
        return "sequence.beat_added"


@dataclass(frozen=True)
class BeatUpdatedEvent(BaseEvent):
    """Published when a beat's data changes."""
    sequence_id: str
    beat_number: int
    field_changed: str  # "letter", "blue_motion", "red_motion", etc.
    old_value: Any
    new_value: Any
    
    @property
    def event_type(self) -> str:
        return "sequence.beat_updated"


@dataclass(frozen=True)
class BeatRemovedEvent(BaseEvent):
    """Published when a beat is removed from a sequence."""
    sequence_id: str
    removed_beat_data: Dict[str, Any]
    old_position: int
    remaining_beats: int
    
    @property
    def event_type(self) -> str:
        return "sequence.beat_removed"


# === Motion Domain Events ===

@dataclass(frozen=True)
class MotionValidatedEvent(BaseEvent):
    """Published when motion validation occurs."""
    motion_id: str
    motion_data: Dict[str, Any]
    is_valid: bool
    validation_errors: List[str] = field(default_factory=list)
    
    @property
    def event_type(self) -> str:
        return "motion.validated"


@dataclass(frozen=True)
class MotionGeneratedEvent(BaseEvent):
    """Published when new motion is generated."""
    sequence_id: str
    beat_number: int
    color: str  # "blue" or "red"
    motion_data: Dict[str, Any]
    generation_method: str  # "manual", "random", "smart_fill", etc.
    
    @property
    def event_type(self) -> str:
        return "motion.generated"


# === Layout Domain Events ===

@dataclass(frozen=True)
class LayoutRecalculatedEvent(BaseEvent):
    """Published when layout is recalculated."""
    layout_type: str  # "beat_frame", "component", "responsive"
    layout_data: Dict[str, Any]
    trigger_reason: str  # "sequence_changed", "window_resized", "manual"
    
    @property
    def event_type(self) -> str:
        return f"layout.{self.layout_type}_recalculated"


@dataclass(frozen=True)
class ComponentResizedEvent(BaseEvent):
    """Published when UI components are resized."""
    component_name: str
    old_size: tuple[int, int]
    new_size: tuple[int, int]
    
    @property
    def event_type(self) -> str:
        return "layout.component_resized"


# === Arrow/Pictograph Domain Events ===

@dataclass(frozen=True)
class ArrowPositionedEvent(BaseEvent):
    """Published when arrow positioning is calculated."""
    sequence_id: str
    beat_number: int
    arrow_color: str
    position_data: Dict[str, Any]
    
    @property
    def event_type(self) -> str:
        return "arrow.positioned"


@dataclass(frozen=True)
class PictographUpdatedEvent(BaseEvent):
    """Published when pictograph visualization changes."""
    sequence_id: str
    beat_number: int
    update_type: str  # "arrows", "glyphs", "background", "all"
    
    @property
    def event_type(self) -> str:
        return f"pictograph.{self.update_type}_updated"


# === UI State Events ===

@dataclass(frozen=True)
class UIStateChangedEvent(BaseEvent):
    """Published when UI state changes."""
    component: str
    state_key: str
    old_value: Any
    new_value: Any
    
    @property
    def event_type(self) -> str:
        return f"ui.{self.component}.state_changed"


# === Command Events (for undo/redo) ===

@dataclass(frozen=True)
class CommandExecutedEvent(BaseEvent):
    """Published when a command is executed."""
    command_id: str
    command_type: str
    command_description: str
    can_undo: bool
    can_redo: bool
    
    @property
    def event_type(self) -> str:
        return "command.executed"


@dataclass(frozen=True)
class CommandUndoneEvent(BaseEvent):
    """Published when a command is undone."""
    command_id: str
    command_type: str
    command_description: str
    can_undo: bool
    can_redo: bool
    
    @property
    def event_type(self) -> str:
        return "command.undone"


@dataclass(frozen=True)
class CommandRedoneEvent(BaseEvent):
    """Published when a command is redone."""
    command_id: str
    command_type: str
    command_description: str
    can_undo: bool
    can_redo: bool
    
    @property
    def event_type(self) -> str:
        return "command.redone"
```

#### **1.2: Update Event Bus Registration**

**File:** `src/core/events/__init__.py`
```python
"""Event system exports for easy importing."""

from .event_bus import (
    TypeSafeEventBus, 
    IEventBus, 
    get_event_bus, 
    reset_event_bus,
    BaseEvent,
    EventPriority
)

from .domain_events import (
    # Sequence events
    SequenceCreatedEvent,
    SequenceUpdatedEvent, 
    BeatAddedEvent,
    BeatUpdatedEvent,
    BeatRemovedEvent,
    
    # Motion events
    MotionValidatedEvent,
    MotionGeneratedEvent,
    
    # Layout events
    LayoutRecalculatedEvent,
    ComponentResizedEvent,
    
    # Arrow/Pictograph events
    ArrowPositionedEvent,
    PictographUpdatedEvent,
    
    # UI events
    UIStateChangedEvent,
    
    # Command events
    CommandExecutedEvent,
    CommandUndoneEvent,
    CommandRedoneEvent,
)

__all__ = [
    # Event bus core
    "TypeSafeEventBus", "IEventBus", "get_event_bus", "reset_event_bus",
    "BaseEvent", "EventPriority",
    
    # Domain events
    "SequenceCreatedEvent", "SequenceUpdatedEvent", "BeatAddedEvent",
    "BeatUpdatedEvent", "BeatRemovedEvent", "MotionValidatedEvent",
    "MotionGeneratedEvent", "LayoutRecalculatedEvent", "ComponentResizedEvent",
    "ArrowPositionedEvent", "PictographUpdatedEvent", "UIStateChangedEvent",
    "CommandExecutedEvent", "CommandUndoneEvent", "CommandRedoneEvent",
]
```

### **Step 2: Implement Command Pattern (Days 3-4)**

#### **2.1: Create Command Infrastructure**

**File:** `src/core/commands/__init__.py`
```python
"""Command pattern infrastructure for undoable operations."""

from .command_system import (
    ICommand,
    CommandProcessor,
    CommandResult,
    CommandError,
)

from .sequence_commands import (
    AddBeatCommand,
    RemoveBeatCommand,
    UpdateBeatCommand,
    UpdateSequenceCommand,
)

__all__ = [
    "ICommand", "CommandProcessor", "CommandResult", "CommandError",
    "AddBeatCommand", "RemoveBeatCommand", "UpdateBeatCommand", "UpdateSequenceCommand",
]
```

**File:** `src/core/commands/command_system.py`
```python
"""
Command pattern implementation for undoable operations.
Provides type-safe, undoable commands with event integration.
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Any, Dict
from dataclasses import dataclass
import uuid
import logging
from datetime import datetime

from ..events import IEventBus, CommandExecutedEvent, CommandUndoneEvent, CommandRedoneEvent

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class CommandResult(Generic[T]):
    """Result of command execution."""
    success: bool
    result: Optional[T] = None
    error_message: Optional[str] = None
    command_id: str = ""


class CommandError(Exception):
    """Exception raised when command execution fails."""
    def __init__(self, message: str, command_id: str = ""):
        super().__init__(message)
        self.command_id = command_id


class ICommand(Generic[T], ABC):
    """Interface for undoable commands."""

    @property
    @abstractmethod
    def command_id(self) -> str:
        """Unique identifier for this command instance."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of what this command does."""
        pass

    @abstractmethod
    def execute(self) -> T:
        """Execute the command and return result."""
        pass

    @abstractmethod
    def undo(self) -> T:
        """Undo the command and return previous state."""
        pass

    @abstractmethod
    def can_execute(self) -> bool:
        """Check if command can be executed in current state."""
        pass

    @abstractmethod
    def can_undo(self) -> bool:
        """Check if command can be undone."""
        pass


class CommandProcessor:
    """
    Processes commands with undo/redo support and event integration.
    
    Features:
    - Command history management
    - Undo/redo capability 
    - Event publishing for command lifecycle
    - Error handling and recovery
    """

    def __init__(self, event_bus: IEventBus, max_history: int = 100):
        self.event_bus = event_bus
        self.max_history = max_history
        self._history: List[ICommand] = []
        self._current_index = -1
        self._logger = logging.getLogger(__name__)

    def execute(self, command: ICommand[T]) -> CommandResult[T]:
        """Execute command and add to history with event publishing."""
        command_id = command.command_id
        
        try:
            # Validate command can be executed
            if not command.can_execute():
                error_msg = f"Command cannot be executed: {command.description}"
                self._logger.warning(error_msg)
                return CommandResult(
                    success=False,
                    error_message=error_msg,
                    command_id=command_id
                )

            # Execute the command
            self._logger.info(f"Executing command: {command.description}")
            result = command.execute()

            # Add to history (clear redo stack if we're not at the end)
            self._history = self._history[:self._current_index + 1]
            self._history.append(command)
            self._current_index += 1

            # Limit history size
            if len(self._history) > self.max_history:
                self._history = self._history[-self.max_history:]
                self._current_index = len(self._history) - 1

            # Publish command executed event
            self.event_bus.publish(CommandExecutedEvent(
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                source="CommandProcessor",
                command_id=command_id,
                command_type=type(command).__name__,
                command_description=command.description,
                can_undo=self.can_undo(),
                can_redo=self.can_redo(),
            ))

            self._logger.info(f"Command executed successfully: {command.description}")
            return CommandResult(success=True, result=result, command_id=command_id)

        except Exception as e:
            error_msg = f"Command execution failed: {command.description} - {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            return CommandResult(
                success=False,
                error_message=error_msg,
                command_id=command_id
            )

    def undo(self) -> CommandResult:
        """Undo the last command with event publishing."""
        if not self.can_undo():
            return CommandResult(success=False, error_message="No commands to undo")

        command = self._history[self._current_index]
        command_id = command.command_id

        try:
            if not command.can_undo():
                error_msg = f"Command cannot be undone: {command.description}"
                return CommandResult(success=False, error_message=error_msg, command_id=command_id)

            self._logger.info(f"Undoing command: {command.description}")
            result = command.undo()
            self._current_index -= 1

            # Publish command undone event
            self.event_bus.publish(CommandUndoneEvent(
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                source="CommandProcessor",
                command_id=command_id,
                command_type=type(command).__name__,
                command_description=command.description,
                can_undo=self.can_undo(),
                can_redo=self.can_redo(),
            ))

            self._logger.info(f"Command undone successfully: {command.description}")
            return CommandResult(success=True, result=result, command_id=command_id)

        except Exception as e:
            error_msg = f"Command undo failed: {command.description} - {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            return CommandResult(success=False, error_message=error_msg, command_id=command_id)

    def redo(self) -> CommandResult:
        """Redo the next command with event publishing."""
        if not self.can_redo():
            return CommandResult(success=False, error_message="No commands to redo")

        self._current_index += 1
        command = self._history[self._current_index]
        command_id = command.command_id

        try:
            if not command.can_execute():
                self._current_index -= 1  # Revert on failure
                error_msg = f"Command cannot be redone: {command.description}"
                return CommandResult(success=False, error_message=error_msg, command_id=command_id)

            self._logger.info(f"Redoing command: {command.description}")
            result = command.execute()

            # Publish command redone event
            self.event_bus.publish(CommandRedoneEvent(
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                source="CommandProcessor",
                command_id=command_id,
                command_type=type(command).__name__,
                command_description=command.description,
                can_undo=self.can_undo(),
                can_redo=self.can_redo(),
            ))

            self._logger.info(f"Command redone successfully: {command.description}")
            return CommandResult(success=True, result=result, command_id=command_id)

        except Exception as e:
            self._current_index -= 1  # Revert on failure
            error_msg = f"Command redo failed: {command.description} - {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            return CommandResult(success=False, error_message=error_msg, command_id=command_id)

    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return self._current_index >= 0

    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return self._current_index < len(self._history) - 1

    def get_undo_description(self) -> Optional[str]:
        """Get description of command that would be undone."""
        if self.can_undo():
            return self._history[self._current_index].description
        return None

    def get_redo_description(self) -> Optional[str]:
        """Get description of command that would be redone."""
        if self.can_redo():
            return self._history[self._current_index + 1].description
        return None

    def clear_history(self) -> None:
        """Clear command history."""
        self._history.clear()
        self._current_index = -1
        self._logger.info("Command history cleared")

    def get_history_summary(self) -> List[Dict[str, Any]]:
        """Get summary of command history for debugging."""
        return [
            {
                "index": i,
                "description": cmd.description,
                "type": type(cmd).__name__,
                "is_current": i == self._current_index,
            }
            for i, cmd in enumerate(self._history)
        ]
```

#### **2.2: Create Sequence-Specific Commands**

**File:** `src/core/commands/sequence_commands.py`
```python
"""
Sequence-specific commands for undoable sequence operations.
These commands integrate with the event system and domain models.
"""

import uuid
from typing import Optional
from dataclasses import dataclass

from .command_system import ICommand
from ..events import IEventBus, BeatAddedEvent, BeatRemovedEvent, BeatUpdatedEvent, SequenceUpdatedEvent
from ...domain.models.core_models import SequenceData, BeatData


@dataclass
class AddBeatCommand(ICommand[SequenceData]):
    """Command to add a beat to a sequence."""
    
    sequence: SequenceData
    beat: BeatData
    position: int
    event_bus: IEventBus
    _command_id: str = ""
    _result_sequence: Optional[SequenceData] = None

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

    def execute(self) -> SequenceData:
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
        self.event_bus.publish(BeatAddedEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            source="AddBeatCommand",
            sequence_id=self.sequence.id,
            beat_data=new_beat.to_dict(),
            beat_position=self.position,
            total_beats=len(self._result_sequence.beats),
        ))

        return self._result_sequence

    def undo(self) -> SequenceData:
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
        self.event_bus.publish(BeatRemovedEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            source="AddBeatCommand.undo",
            sequence_id=self.sequence.id,
            removed_beat_data=removed_beat.to_dict(),
            old_position=self.position,
            remaining_beats=len(original_sequence.beats),
        ))

        return original_sequence

    def can_execute(self) -> bool:
        """Check if beat can be added at the specified position."""
        return 0 <= self.position <= len(self.sequence.beats)

    def can_undo(self) -> bool:
        """Check if command can be undone."""
        return self._result_sequence is not None


@dataclass
class RemoveBeatCommand(ICommand[SequenceData]):
    """Command to remove a beat from a sequence."""
    
    sequence: SequenceData
    position: int
    event_bus: IEventBus
    _command_id: str = ""
    _removed_beat: Optional[BeatData] = None

    def __post_init__(self):
        if not self._command_id:
            self._command_id = str(uuid.uuid4())

    @property
    def command_id(self) -> str:
        return self._command_id

    @property
    def description(self) -> str:
        return f"Remove beat at position {self.position + 1}"

    def execute(self) -> SequenceData:
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
        self.event_bus.publish(BeatRemovedEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            source="RemoveBeatCommand",
            sequence_id=self.sequence.id,
            removed_beat_data=self._removed_beat.to_dict(),
            old_position=self.position,
            remaining_beats=len(result_sequence.beats),
        ))

        return result_sequence

    def undo(self) -> SequenceData:
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
        self.event_bus.publish(BeatAddedEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            source="RemoveBeatCommand.undo",
            sequence_id=self.sequence.id,
            beat_data=restored_beat.to_dict(),
            beat_position=self.position,
            total_beats=len(original_sequence.beats),
        ))

        return original_sequence

    def can_execute(self) -> bool:
        """Check if beat can be removed from the specified position."""
        return 0 <= self.position < len(self.sequence.beats)

    def can_undo(self) -> bool:
        """Check if command can be undone."""
        return self._removed_beat is not None


@dataclass 
class UpdateBeatCommand(ICommand[SequenceData]):
    """Command to update a beat's properties."""
    
    sequence: SequenceData
    beat_number: int
    field_name: str
    new_value: any
    event_bus: IEventBus
    _command_id: str = ""
    _old_value: any = None

    def __post_init__(self):
        if not self._command_id:
            self._command_id = str(uuid.uuid4())

    @property
    def command_id(self) -> str:
        return self._command_id

    @property
    def description(self) -> str:
        return f"Update beat {self.beat_number} {self.field_name} to {self.new_value}"

    def execute(self) -> SequenceData:
        """Execute: Update beat field and publish event."""
        if not self.can_execute():
            raise ValueError(f"Cannot update beat {self.beat_number} - invalid beat number")

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
        self.event_bus.publish(BeatUpdatedEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            source="UpdateBeatCommand",
            sequence_id=self.sequence.id,
            beat_number=self.beat_number,
            field_changed=self.field_name,
            old_value=self._old_value,
            new_value=self.new_value,
        ))

        return result_sequence

    def undo(self) -> SequenceData:
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
        self.event_bus.publish(BeatUpdatedEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            source="UpdateBeatCommand.undo",
            sequence_id=self.sequence.id,
            beat_number=self.beat_number,
            field_changed=self.field_name,
            old_value=self.new_value,
            new_value=self._old_value,
        ))

        return original_sequence

    def can_execute(self) -> bool:
        """Check if beat can be updated."""
        return any(beat.beat_number == self.beat_number for beat in self.sequence.beats)

    def can_undo(self) -> bool:
        """Check if command can be undone."""
        return self._old_value is not None
```

### **Step 3: Convert Services to Event-Driven (Days 5-7)**

Now we convert the existing services to use events instead of direct method calls.

#### **3.1: Update Sequence Management Service**

**File:** `src/application/services/core/sequence_management_service.py` (modifications)

Add these imports at the top:
```python
from core.events import (
    IEventBus, get_event_bus,
    SequenceCreatedEvent, BeatAddedEvent, BeatUpdatedEvent, BeatRemovedEvent
)
from core.commands import CommandProcessor, AddBeatCommand, RemoveBeatCommand, UpdateBeatCommand
```

Update the service class:
```python
class SequenceManagementService(ISequenceManagementService):
    """
    Event-driven sequence management service.
    
    REPLACES: Direct method calls with event publishing
    ADDS: Command pattern for undo/redo capability
    """

    def __init__(self, event_bus: Optional[IEventBus] = None):
        # Event system integration
        self.event_bus = event_bus or get_event_bus()
        self.command_processor = CommandProcessor(self.event_bus)
        
        # Current state (will be managed by commands)
        self._current_sequence: Optional[SequenceData] = None
        
        # Legacy compatibility (for gradual migration)
        self._dictionary_cache = {}
        self._difficulty_cache = {}

    # NEW: Event-driven methods with undo capability

    def create_sequence_with_events(self, name: str, length: int = 16) -> SequenceData:
        """Create sequence and publish creation event."""
        sequence = self.create_sequence(name, length)  # Use existing logic
        
        # Publish creation event instead of calling other services directly
        self.event_bus.publish(SequenceCreatedEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            source="SequenceManagementService",
            sequence_id=sequence.id,
            sequence_name=sequence.name,
            sequence_length=sequence.length,
        ))
        
        self._current_sequence = sequence
        return sequence

    def add_beat_with_undo(self, beat: BeatData, position: Optional[int] = None) -> SequenceData:
        """Add beat using command pattern with undo support."""
        if not self._current_sequence:
            raise ValueError("No active sequence")

        if position is None:
            position = len(self._current_sequence.beats)

        # Create and execute command (this publishes events automatically)
        command = AddBeatCommand(
            sequence=self._current_sequence,
            beat=beat,
            position=position,
            event_bus=self.event_bus
        )

        result = self.command_processor.execute(command)
        if result.success:
            self._current_sequence = result.result
            return result.result
        else:
            raise RuntimeError(f"Failed to add beat: {result.error_message}")

    def remove_beat_with_undo(self, position: int) -> SequenceData:
        """Remove beat using command pattern with undo support."""
        if not self._current_sequence:
            raise ValueError("No active sequence")

        command = RemoveBeatCommand(
            sequence=self._current_sequence,
            position=position,
            event_bus=self.event_bus
        )

        result = self.command_processor.execute(command)
        if result.success:
            self._current_sequence = result.result
            return result.result
        else:
            raise RuntimeError(f"Failed to remove beat: {result.error_message}")

    def update_beat_with_undo(self, beat_number: int, field_name: str, new_value: Any) -> SequenceData:
        """Update beat field using command pattern with undo support."""
        if not self._current_sequence:
            raise ValueError("No active sequence")

        command = UpdateBeatCommand(
            sequence=self._current_sequence,
            beat_number=beat_number,
            field_name=field_name,
            new_value=new_value,
            event_bus=self.event_bus
        )

        result = self.command_processor.execute(command)
        if result.success:
            self._current_sequence = result.result
            return result.result
        else:
            raise RuntimeError(f"Failed to update beat: {result.error_message}")

    # NEW: Undo/Redo methods

    def undo_last_operation(self) -> Optional[SequenceData]:
        """Undo the last operation."""
        result = self.command_processor.undo()
        if result.success:
            self._current_sequence = result.result
            return result.result
        return None

    def redo_last_operation(self) -> Optional[SequenceData]:
        """Redo the last undone operation."""
        result = self.command_processor.redo()
        if result.success:
            self._current_sequence = result.result
            return result.result
        return None

    def can_undo(self) -> bool:
        """Check if undo is available."""
        return self.command_processor.can_undo()

    def can_redo(self) -> bool:
        """Check if redo is available."""
        return self.command_processor.can_redo()

    def get_undo_description(self) -> Optional[str]:
        """Get description of operation that would be undone."""
        return self.command_processor.get_undo_description()

    def get_redo_description(self) -> Optional[str]:
        """Get description of operation that would be redone."""
        return self.command_processor.get_redo_description()

    # Keep all existing methods for backward compatibility during migration
    # ... (all existing methods remain unchanged)
```

#### **3.2: Update Layout Management Service to Respond to Events**

**File:** `src/application/services/layout/layout_management_service.py` (modifications)

Add these imports:
```python
from core.events import (
    IEventBus, get_event_bus,
    BeatAddedEvent, BeatRemovedEvent, BeatUpdatedEvent, SequenceCreatedEvent,
    LayoutRecalculatedEvent
)
```

Update the service class:
```python
class LayoutManagementService(ILayoutService):
    """
    Event-driven layout management service.
    
    REPLACES: Being called directly by other services
    ADDS: Automatic response to sequence events
    """

    def __init__(self, event_bus: Optional[IEventBus] = None):
        # Existing initialization
        self._layout_presets = self._load_layout_presets()
        self._density_scaling = {
            "low": 0.8, "normal": 1.0, "high": 1.2, "extra_high": 1.5,
        }
        self._default_configs = self._load_default_configs()
        self._main_window_size = QSize(1400, 900)
        self._layout_ratio = (10, 10)
        
        # NEW: Event system integration
        self.event_bus = event_bus or get_event_bus()
        self._subscription_ids: List[str] = []
        
        # Subscribe to relevant events
        self._setup_event_subscriptions()

    def _setup_event_subscriptions(self):
        """Subscribe to events that require layout recalculation."""
        
        # Subscribe to sequence events
        sub_id = self.event_bus.subscribe(
            "sequence.beat_added",
            self._on_beat_added,
            priority=EventPriority.HIGH
        )
        self._subscription_ids.append(sub_id)

        sub_id = self.event_bus.subscribe(
            "sequence.beat_removed", 
            self._on_beat_removed,
            priority=EventPriority.HIGH
        )
        self._subscription_ids.append(sub_id)

        sub_id = self.event_bus.subscribe(
            "sequence.created",
            self._on_sequence_created,
            priority=EventPriority.HIGH
        )
        self._subscription_ids.append(sub_id)

        # Subscribe to UI resize events
        sub_id = self.event_bus.subscribe(
            "layout.component_resized",
            self._on_component_resized,
            priority=EventPriority.NORMAL
        )
        self._subscription_ids.append(sub_id)

    # NEW: Event handlers

    def _on_beat_added(self, event: BeatAddedEvent):
        """Handle beat added event by recalculating layout."""
        logger.info(f"Layout service responding to beat added: sequence {event.sequence_id}")
        
        # Recalculate layout for the updated sequence
        # This replaces the direct call that used to happen in SequenceManagementService
        try:
            # Get current window size (in real implementation, this would come from UI state)
            container_size = (self._main_window_size.width(), self._main_window_size.height())
            
            # Trigger layout recalculation
            layout_result = self._recalculate_beat_frame_layout(
                beat_count=event.total_beats,
                container_size=container_size,
                trigger_reason="beat_added"
            )
            
            # Publish layout updated event for other services
            self.event_bus.publish(LayoutRecalculatedEvent(
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                source="LayoutManagementService",
                layout_type="beat_frame",
                layout_data=layout_result,
                trigger_reason="beat_added"
            ))
            
        except Exception as e:
            logger.error(f"Failed to recalculate layout after beat added: {e}")

    def _on_beat_removed(self, event: BeatRemovedEvent):
        """Handle beat removed event by recalculating layout."""
        logger.info(f"Layout service responding to beat removed: sequence {event.sequence_id}")
        
        try:
            container_size = (self._main_window_size.width(), self._main_window_size.height())
            
            layout_result = self._recalculate_beat_frame_layout(
                beat_count=event.remaining_beats,
                container_size=container_size,
                trigger_reason="beat_removed"
            )
            
            self.event_bus.publish(LayoutRecalculatedEvent(
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                source="LayoutManagementService",
                layout_type="beat_frame",
                layout_data=layout_result,
                trigger_reason="beat_removed"
            ))
            
        except Exception as e:
            logger.error(f"Failed to recalculate layout after beat removed: {e}")

    def _on_sequence_created(self, event: SequenceCreatedEvent):
        """Handle sequence created event by setting up initial layout."""
        logger.info(f"Layout service responding to sequence created: {event.sequence_name}")
        
        try:
            container_size = (self._main_window_size.width(), self._main_window_size.height())
            
            layout_result = self._recalculate_beat_frame_layout(
                beat_count=event.sequence_length,
                container_size=container_size,
                trigger_reason="sequence_created"
            )
            
            self.event_bus.publish(LayoutRecalculatedEvent(
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                source="LayoutManagementService",
                layout_type="beat_frame",
                layout_data=layout_result,
                trigger_reason="sequence_created"
            ))
            
        except Exception as e:
            logger.error(f"Failed to setup layout for new sequence: {e}")

    def _on_component_resized(self, event: ComponentResizedEvent):
        """Handle component resize event by recalculating responsive layout."""
        logger.info(f"Layout service responding to component resize: {event.component_name}")
        
        # Recalculate layout for the resized component
        # This ensures responsive design works automatically

    # NEW: Helper method for layout recalculation

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

    def cleanup(self):
        """Clean up event subscriptions when service is destroyed."""
        for sub_id in self._subscription_ids:
            self.event_bus.unsubscribe(sub_id)
        self._subscription_ids.clear()

    # Keep all existing methods unchanged for backward compatibility
    # ... (all existing methods remain)
```

#### **3.3: Update Motion Generation Service to Respond to Events**

**File:** `src/application/services/motion/motion_generation_service.py` (modifications)

Add these imports:
```python
from core.events import (
    IEventBus, get_event_bus,
    BeatUpdatedEvent, MotionGeneratedEvent, MotionValidatedEvent
)
```

Update the service class:
```python
class MotionGenerationService(IMotionGenerationService):
    """
    Event-driven motion generation service.
    
    REPLACES: Being called directly for motion generation
    ADDS: Automatic motion generation based on beat updates
    """

    def __init__(self, validation_service=None, event_bus: Optional[IEventBus] = None):
        # Existing initialization
        self._motion_datasets = self._load_motion_datasets()
        self._letter_specific_rules = self._load_letter_specific_rules()
        self._validation_service = validation_service
        
        # NEW: Event system integration
        self.event_bus = event_bus or get_event_bus()
        self._subscription_ids: List[str] = []
        
        # Subscribe to relevant events
        self._setup_event_subscriptions()

    def _setup_event_subscriptions(self):
        """Subscribe to events that trigger motion generation."""
        
        # Subscribe to beat updates that affect letters
        sub_id = self.event_bus.subscribe(
            "sequence.beat_updated",
            self._on_beat_updated,
            priority=EventPriority.NORMAL,
            filter_func=lambda event: event.field_changed == "letter"
        )
        self._subscription_ids.append(sub_id)

    def _on_beat_updated(self, event: BeatUpdatedEvent):
        """Handle beat letter updates by generating motions."""
        if event.field_changed != "letter" or not event.new_value:
            return
            
        logger.info(f"Motion service generating motions for letter: {event.new_value}")
        
        try:
            # Generate motion combinations for the new letter
            combinations = self.generate_motion_combinations_for_letter(event.new_value)
            
            if combinations:
                # Use the first valid combination (in real app, user might choose)
                blue_motion, red_motion = combinations[0]
                
                # Publish motion generated events
                self.event_bus.publish(MotionGeneratedEvent(
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source="MotionGenerationService",
                    sequence_id=event.sequence_id,
                    beat_number=event.beat_number,
                    color="blue",
                    motion_data=blue_motion.to_dict(),
                    generation_method="auto_from_letter"
                ))
                
                self.event_bus.publish(MotionGeneratedEvent(
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source="MotionGenerationService",
                    sequence_id=event.sequence_id,
                    beat_number=event.beat_number,
                    color="red",
                    motion_data=red_motion.to_dict(),
                    generation_method="auto_from_letter"
                ))
                
        except Exception as e:
            logger.error(f"Failed to generate motions for letter {event.new_value}: {e}")

    def cleanup(self):
        """Clean up event subscriptions when service is destroyed."""
        for sub_id in self._subscription_ids:
            self.event_bus.unsubscribe(sub_id)
        self._subscription_ids.clear()

    # Keep all existing methods unchanged
    # ... (all existing methods remain)
```

### **Step 4: Update Dependency Injection (Days 8-9)**

#### **4.1: Register Event System and Commands in DI Container**

**File:** `src/modern/main.py` (modifications to `_configure_services` method)

```python
def _configure_services(self):
    if self.splash:
        self.splash.update_progress(20, "Configuring event-driven services...")

    # NEW: Register event bus first (other services depend on it)
    from core.events import get_event_bus
    event_bus = get_event_bus()
    self.container.register_instance(IEventBus, event_bus)

    # NEW: Register command processor
    from core.commands import CommandProcessor
    command_processor = CommandProcessor(event_bus)
    self.container.register_instance(CommandProcessor, command_processor)

    # Update existing service registrations to use event bus
    layout_management_service = LayoutManagementService(event_bus=event_bus)
    self.container.register_instance(ILayoutService, layout_management_service)

    ui_state_service = UIStateManagementService()
    self.container.register_instance(IUIStateManagementService, ui_state_service)

    # Update motion services with event bus
    self._register_motion_services_with_events(event_bus)
    self._register_layout_services_with_events(event_bus)
    self._register_pictograph_services_with_events(event_bus)

    # Get UI state service for settings functionality
    self.ui_state_service = self.container.resolve(IUIStateManagementService)

    # Configure workbench services after UI state service is available
    configure_workbench_services(self.container)

    if self.splash:
        self.splash.update_progress(40, "Event-driven services configured")

def _register_motion_services_with_events(self, event_bus: IEventBus):
    """Register motion services with event bus integration."""
    from application.services.motion.motion_validation_service import (
        MotionValidationService, IMotionValidationService,
    )
    from application.services.motion.motion_generation_service import (
        MotionGenerationService, IMotionGenerationService,
    )
    from application.services.motion.motion_orientation_service import (
        MotionOrientationService, IMotionOrientationService,
    )

    # Register with event bus integration
    validation_service = MotionValidationService(event_bus=event_bus)
    self.container.register_instance(IMotionValidationService, validation_service)

    generation_service = MotionGenerationService(
        validation_service=validation_service,
        event_bus=event_bus
    )
    self.container.register_instance(IMotionGenerationService, generation_service)

    orientation_service = MotionOrientationService(event_bus=event_bus)
    self.container.register_instance(IMotionOrientationService, orientation_service)
```

#### **4.2: Update Interface Definitions**

**File:** `src/core/interfaces/core_services.py` (add event bus interface)

```python
# Add this import at the top
from core.events import IEventBus

# Add this interface
class IEventBus(ABC):
    """Interface for event bus (imported from core.events)."""
    pass  # Implementation is in core.events.IEventBus

# Update existing interfaces to show event integration
class ISequenceManagementService(ABC):
    """Enhanced interface with event-driven operations and undo support."""

    # Existing methods remain unchanged for backward compatibility
    @abstractmethod
    def create_sequence(self, name: str, length: int = 16) -> Any:
        """Create a new sequence with specified length."""
        pass

    # NEW: Event-driven methods with undo support
    @abstractmethod  
    def create_sequence_with_events(self, name: str, length: int = 16) -> Any:
        """Create sequence and publish creation event."""
        pass

    @abstractmethod
    def add_beat_with_undo(self, beat: Any, position: Optional[int] = None) -> Any:
        """Add beat using command pattern with undo support."""
        pass

    @abstractmethod
    def remove_beat_with_undo(self, position: int) -> Any:
        """Remove beat using command pattern with undo support."""
        pass

    @abstractmethod
    def update_beat_with_undo(self, beat_number: int, field_name: str, new_value: Any) -> Any:
        """Update beat field using command pattern with undo support."""
        pass

    @abstractmethod
    def undo_last_operation(self) -> Optional[Any]:
        """Undo the last operation."""
        pass

    @abstractmethod
    def redo_last_operation(self) -> Optional[Any]:
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
```

### **Step 5: Create Migration Bridge (Days 10)**

For smooth migration, create a bridge that allows legacy code to work with the new event-driven system.

#### **5.1: Legacy Compatibility Bridge**

**File:** `src/core/migration/legacy_bridge.py`
```python
"""
Legacy compatibility bridge for gradual migration to event-driven architecture.

This bridge allows legacy code to work with new event-driven services while
gradually migrating to the new patterns.
"""

from typing import Any, Optional, Callable, Dict
import logging
from core.events import IEventBus, get_event_bus

logger = logging.getLogger(__name__)


class LegacyEventBridge:
    """
    Bridge that converts between legacy direct method calls and event-driven architecture.
    
    USAGE DURING MIGRATION:
    1. Wrap legacy services with this bridge
    2. Legacy code continues to work unchanged
    3. New event-driven services respond to legacy operations
    4. Gradually replace legacy calls with event-driven calls
    """

    def __init__(self, event_bus: Optional[IEventBus] = None):
        self.event_bus = event_bus or get_event_bus()
        self._legacy_method_mappings: Dict[str, Callable] = {}

    def register_legacy_method(self, method_name: str, event_publisher: Callable):
        """Register a legacy method that should publish events when called."""
        self._legacy_method_mappings[method_name] = event_publisher

    def wrap_legacy_service(self, legacy_service: Any, service_name: str) -> Any:
        """
        Wrap a legacy service to publish events when methods are called.
        
        This allows legacy services to work with new event-driven services.
        """
        
        class LegacyServiceWrapper:
            def __init__(self, wrapped_service, bridge):
                self._wrapped_service = wrapped_service
                self._bridge = bridge
                self._service_name = service_name

            def __getattr__(self, name):
                original_method = getattr(self._wrapped_service, name)
                
                if callable(original_method):
                    def wrapped_method(*args, **kwargs):
                        # Call original method
                        result = original_method(*args, **kwargs)
                        
                        # Publish event for new services to respond
                        if name in self._bridge._legacy_method_mappings:
                            try:
                                event_publisher = self._bridge._legacy_method_mappings[name]
                                event_publisher(result, *args, **kwargs)
                            except Exception as e:
                                logger.error(f"Failed to publish event for legacy method {name}: {e}")
                        
                        return result
                    
                    return wrapped_method
                else:
                    return original_method

        return LegacyServiceWrapper(legacy_service, self)

# Example usage during migration:
"""
# In main.py during gradual migration

# 1. Create bridge
legacy_bridge = LegacyEventBridge(event_bus)

# 2. Register legacy method mappings
def publish_sequence_created(result, *args, **kwargs):
    event_bus.publish(SequenceCreatedEvent(
        sequence_id=result.id,
        sequence_name=result.name,
        sequence_length=result.length
    ))

legacy_bridge.register_legacy_method("create_sequence", publish_sequence_created)

# 3. Wrap legacy service
legacy_sequence_service = get_legacy_sequence_service()
wrapped_service = legacy_bridge.wrap_legacy_service(legacy_sequence_service, "sequence")

# 4. Legacy code continues to work, but now publishes events
sequence = wrapped_service.create_sequence("Test", 16)  # Publishes SequenceCreatedEvent
"""
```

### **Step 6: Testing and Validation (Days 11-14)**

#### **6.1: Create Event System Tests**

**File:** `tests/test_event_driven_architecture.py`
```python
"""
Tests for event-driven architecture implementation.
Validates that events are published and handled correctly.
"""

import pytest
from unittest.mock import Mock, call
from core.events import get_event_bus, reset_event_bus, BeatAddedEvent, SequenceCreatedEvent
from core.commands import AddBeatCommand, CommandProcessor
from domain.models.core_models import SequenceData, BeatData, MotionType, Location, RotationDirection


class TestEventDrivenArchitecture:
    """Test suite for event-driven architecture."""

    def setup_method(self):
        """Reset event bus for each test."""
        reset_event_bus()
        self.event_bus = get_event_bus()

    def test_event_filtering_works_correctly(self):
        """Test that event filtering prevents unwanted handler calls."""
        # Arrange
        letter_change_handler = Mock()
        motion_change_handler = Mock()
        
        # Subscribe with filters
        self.event_bus.subscribe(
            "sequence.beat_updated",
            letter_change_handler,
            filter_func=lambda event: event.field_changed == "letter"
        )
        
        self.event_bus.subscribe(
            "sequence.beat_updated", 
            motion_change_handler,
            filter_func=lambda event: event.field_changed == "blue_motion"
        )
        
        # Act - Publish letter change event
        from core.events.domain_events import BeatUpdatedEvent
        letter_event = BeatUpdatedEvent(
            event_id="test1",
            source="test",
            sequence_id="seq123",
            beat_number=1,
            field_changed="letter",
            old_value="A",
            new_value="B"
        )
        
        self.event_bus.publish(letter_event)
        
        # Assert - Only letter handler called
        letter_change_handler.assert_called_once_with(letter_event)
        motion_change_handler.assert_not_called()
        
        # Reset mocks
        letter_change_handler.reset_mock()
        motion_change_handler.reset_mock()
        
        # Act - Publish motion change event
        motion_event = BeatUpdatedEvent(
            event_id="test2",
            source="test",
            sequence_id="seq123",
            beat_number=1,
            field_changed="blue_motion",
            old_value=None,
            new_value={"motion_type": "pro"}
        )
        
        self.event_bus.publish(motion_event)
        
        # Assert - Only motion handler called
        letter_change_handler.assert_not_called()
        motion_change_handler.assert_called_once_with(motion_event)

    def test_command_history_maintained(self):
        """Test that command history is properly maintained."""
        # Arrange
        sequence = SequenceData(name="Test", beats=[])
        command_processor = CommandProcessor(self.event_bus)
        
        # Act - Execute multiple commands
        cmd1 = AddBeatCommand(sequence, BeatData(letter="A"), 0, self.event_bus)
        result1 = command_processor.execute(cmd1)
        
        cmd2 = AddBeatCommand(result1.result, BeatData(letter="B"), 1, self.event_bus)
        result2 = command_processor.execute(cmd2)
        
        # Assert - History contains both commands
        history = command_processor.get_history_summary()
        assert len(history) == 2
        assert history[0]["description"] == "Add beat 'A' at position 1"
        assert history[1]["description"] == "Add beat 'B' at position 2"
        assert history[1]["is_current"] == True
        
        # Test undo/redo descriptions
        assert command_processor.get_undo_description() == "Add beat 'B' at position 2"
        assert command_processor.get_redo_description() is None
        
        # Undo and test
        command_processor.undo()
        assert command_processor.get_undo_description() == "Add beat 'A' at position 1" 
        assert command_processor.get_redo_description() == "Add beat 'B' at position 2"
```

#### **6.2: Create Integration Tests**

**File:** `tests/test_service_integration.py`
```python
"""
Integration tests for event-driven service communication.
Tests real service interactions through events.
"""

import pytest
from unittest.mock import patch
from core.events import get_event_bus, reset_event_bus
from application.services.core.sequence_management_service import SequenceManagementService
from application.services.layout.layout_management_service import LayoutManagementService
from application.services.motion.motion_generation_service import MotionGenerationService
from domain.models.core_models import BeatData


class TestServiceIntegration:
    """Integration tests for event-driven services."""

    def setup_method(self):
        """Setup services with event integration."""
        reset_event_bus()
        self.event_bus = get_event_bus()
        
        # Create services with event integration
        self.sequence_service = SequenceManagementService(event_bus=self.event_bus)
        self.layout_service = LayoutManagementService(event_bus=self.event_bus)
        self.motion_service = MotionGenerationService(event_bus=self.event_bus)

    def teardown_method(self):
        """Clean up services."""
        self.layout_service.cleanup()
        self.motion_service.cleanup()

    def test_sequence_creation_triggers_layout_setup(self):
        """Test that creating a sequence automatically sets up layout."""
        with patch.object(self.layout_service, '_on_sequence_created') as mock_layout:
            # Act
            sequence = self.sequence_service.create_sequence_with_events("Test Sequence", 8)
            
            # Assert
            mock_layout.assert_called_once()
            call_args = mock_layout.call_args[0][0]
            assert call_args.sequence_name == "Test Sequence"
            assert call_args.sequence_length == 8

    def test_beat_letter_change_triggers_motion_generation(self):
        """Test that changing a beat letter automatically generates motions."""
        # Arrange
        sequence = self.sequence_service.create_sequence_with_events("Test", 2)
        
        with patch.object(self.motion_service, '_on_beat_updated') as mock_motion:
            # Act - Update beat letter (this should trigger motion generation)
            updated_sequence = self.sequence_service.update_beat_with_undo(1, "letter", "A")
            
            # Assert
            mock_motion.assert_called_once()
            call_args = mock_motion.call_args[0][0]
            assert call_args.field_changed == "letter"
            assert call_args.new_value == "A"

    def test_adding_beat_triggers_layout_recalculation(self):
        """Test that adding a beat triggers layout recalculation."""
        # Arrange
        sequence = self.sequence_service.create_sequence_with_events("Test", 2)
        
        with patch.object(self.layout_service, '_on_beat_added') as mock_layout:
            # Act
            beat = BeatData(letter="X")
            self.sequence_service.add_beat_with_undo(beat, 1)
            
            # Assert
            mock_layout.assert_called_once()
            call_args = mock_layout.call_args[0][0]
            assert call_args.beat_position == 1
            assert call_args.total_beats == 3

    def test_undo_redo_maintains_service_consistency(self):
        """Test that undo/redo operations maintain consistency across services."""
        # Arrange
        sequence = self.sequence_service.create_sequence_with_events("Test", 1)
        
        # Track events
        events_received = []
        def track_events(event):
            events_received.append(event)
            
        self.event_bus.subscribe("sequence.beat_added", track_events)
        self.event_bus.subscribe("sequence.beat_removed", track_events)
        
        # Act - Add beat, then undo
        beat = BeatData(letter="A")
        self.sequence_service.add_beat_with_undo(beat, 1)
        self.sequence_service.undo_last_operation()
        
        # Assert - Should have received both events
        assert len(events_received) == 2
        assert events_received[0].event_type == "sequence.beat_added"
        assert events_received[1].event_type == "sequence.beat_removed"
        
        # Verify undo/redo state
        assert self.sequence_service.can_redo()
        assert not self.sequence_service.can_undo()
        
        # Test redo
        self.sequence_service.redo_last_operation()
        assert len(events_received) == 3
        assert events_received[2].event_type == "sequence.beat_added"
```

#### **6.3: Create Performance Tests**

**File:** `tests/test_event_performance.py`
```python
"""
Performance tests for event-driven architecture.
Ensures events don't introduce significant overhead.
"""

import time
import pytest
from core.events import get_event_bus, reset_event_bus
from application.services.core.sequence_management_service import SequenceManagementService
from domain.models.core_models import BeatData


class TestEventPerformance:
    """Performance tests for event system."""

    def setup_method(self):
        reset_event_bus()
        self.event_bus = get_event_bus()
        self.sequence_service = SequenceManagementService(event_bus=self.event_bus)

    def test_bulk_beat_operations_performance(self):
        """Test performance of bulk beat operations with events."""
        sequence = self.sequence_service.create_sequence_with_events("Performance Test", 0)
        
        # Measure time for 100 beat additions
        start_time = time.perf_counter()
        
        for i in range(100):
            beat = BeatData(letter=f"Beat{i}")
            sequence = self.sequence_service.add_beat_with_undo(beat, i)
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        
        # Assert reasonable performance (should be well under 1 second)
        assert total_time < 1.0, f"Bulk operations took {total_time:.2f}s, expected < 1.0s"
        
        # Verify final state
        assert len(sequence.beats) == 100

    def test_event_subscription_overhead(self):
        """Test that having many event subscribers doesn't significantly impact performance."""
        # Add many event subscribers
        handlers = []
        for i in range(100):
            def handler(event, index=i):
                pass  # Minimal processing
            handlers.append(handler)
            self.event_bus.subscribe("sequence.beat_added", handler)
        
        sequence = self.sequence_service.create_sequence_with_events("Subscriber Test", 0)
        
        # Measure event publishing performance
        start_time = time.perf_counter()
        
        for i in range(10):
            beat = BeatData(letter=f"Test{i}")
            self.sequence_service.add_beat_with_undo(beat, i)
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        
        # Should handle 100 subscribers with minimal overhead
        assert total_time < 0.5, f"100 subscribers caused {total_time:.2f}s overhead"

    def test_command_history_memory_usage(self):
        """Test that command history doesn't grow unbounded."""
        sequence = self.sequence_service.create_sequence_with_events("Memory Test", 0)
        
        # Add more commands than history limit
        for i in range(150):  # More than default limit of 100
            beat = BeatData(letter=f"Beat{i}")
            self.sequence_service.add_beat_with_undo(beat, i)
        
        # Verify history is limited
        history = self.sequence_service.command_processor.get_history_summary()
        assert len(history) <= 100, "Command history should be limited to prevent memory leaks"
```

---

## 🎯 **Migration Strategy During Implementation**

### **Week 1: Foundation (Days 1-7)**
1. **Days 1-2:** Implement domain events and enhance event bus
2. **Days 3-4:** Create command pattern infrastructure  
3. **Days 5-7:** Convert core services (sequence, layout, motion) to event-driven

### **Week 2: Integration and Testing (Days 8-14)**
4. **Days 8-9:** Update dependency injection and service registration
5. **Days 10:** Create legacy compatibility bridge
6. **Days 11-14:** Comprehensive testing and validation

### **Gradual Migration Approach**

```python
# Phase 1: Both old and new methods available (backward compatibility)
class SequenceManagementService:
    
    # OLD: Direct method calls (keep for compatibility)
    def add_beat(self, sequence, beat, position):
        # Original implementation
        return self._add_beat_internal(sequence, beat, position)
    
    # NEW: Event-driven with undo (gradually adopt)
    def add_beat_with_undo(self, beat, position=None):
        # New implementation with events and undo
        command = AddBeatCommand(...)
        return self.command_processor.execute(command)

# Migration path:
# 1. Week 1: Add new methods alongside old ones
# 2. Week 2: Update UI components to use new methods
# 3. Week 3: Deprecate old methods
# 4. Week 4: Remove old methods
```

---

## ✅ **Success Criteria**

After Phase 1 implementation, you should have:

### **Event-Driven Architecture**
- ✅ All core services communicate via events instead of direct calls
- ✅ Easy to add new services (including legacy components) without tight coupling
- ✅ Clear separation between business logic and service coordination

### **Command Pattern with Undo/Redo**
- ✅ All sequence operations are undoable
- ✅ Complete command history for debugging complex operations
- ✅ Transactional operations that can be safely reverted

### **Legacy Migration Ready**
- ✅ Event system can integrate legacy components seamlessly
- ✅ Legacy bridge allows gradual migration without breaking existing code
- ✅ New architecture doesn't disrupt current functionality

### **Production Quality**
- ✅ Comprehensive test coverage for event-driven patterns
- ✅ Performance testing shows minimal overhead
- ✅ Error handling and logging for event failures

---

## 🔧 **Testing Your Implementation**

### **Manual Testing Checklist**

1. **Create a sequence** → Should publish `SequenceCreatedEvent` → Layout service responds automatically
2. **Add a beat** → Should publish `BeatAddedEvent` → Layout recalculates automatically  
3. **Update beat letter** → Should publish `BeatUpdatedEvent` → Motion service generates motions automatically
4. **Undo operation** → Should publish reverse event → All services respond appropriately
5. **Add multiple services** → All should respond to same events without interference

### **Key Test Commands**
```bash
# Run event system tests
python -m pytest tests/test_event_driven_architecture.py -v

# Run integration tests  
python -m pytest tests/test_service_integration.py -v

# Run performance tests
python -m pytest tests/test_event_performance.py -v

# Test with real UI
python main.py  # Verify undo/redo buttons work, services respond to changes
```

---

## 🎉 **Expected Outcomes**

After Phase 1, your architecture will be **transformed**:

### **Before (Tight Coupling)**
```python
# Nightmare: Adding a new service requires modifying existing services
sequence_service.add_beat(beat)
layout_service.recalculate()     # Hard-coded dependency
ui_service.refresh()             # Hard-coded dependency  
pictograph_service.update()      # Hard-coded dependency
# Adding legacy service = modify all existing services!
```

### **After (Event-Driven)**
```python
# Dream: Adding a new service requires zero changes to existing services
sequence_service.add_beat_with_undo(beat)  # Publishes BeatAddedEvent
# ALL services respond automatically:
# - LayoutService listens and recalculates
# - UIService listens and refreshes  
# - PictographService listens and updates
# - LegacyService listens and integrates seamlessly!
# - NewService just subscribes to events - no changes needed anywhere!
```

This Phase 1 foundation will make legacy migration **dramatically easier** and provide the bulletproof architecture you need for the next 5+ years of development.beat_added_event_triggers_layout_recalculation(self):
        """Test that adding a beat triggers automatic layout recalculation."""
        # Arrange
        layout_handler = Mock()
        self.event_bus.subscribe("sequence.beat_added", layout_handler)
        
        # Create test data
        sequence = SequenceData(name="Test Sequence", beats=[])
        beat = BeatData(letter="A")
        
        # Act - Execute add beat command
        command = AddBeatCommand(
            sequence=sequence,
            beat=beat,
            position=0,
            event_bus=self.event_bus
        )
        
        command_processor = CommandProcessor(self.event_bus)
        result = command_processor.execute(command)
        
        # Assert
        assert result.success
        layout_handler.assert_called_once()
        
        # Verify event data
        call_args = layout_handler.call_args[0][0]
        assert isinstance(call_args, BeatAddedEvent)
        assert call_args.sequence_id == sequence.id
        assert call_args.beat_position == 0
        assert call_args.total_beats == 1

    def test_command_undo_publishes_reverse_event(self):
        """Test that undoing a command publishes the reverse event."""
        # Arrange
        beat_removed_handler = Mock()
        self.event_bus.subscribe("sequence.beat_removed", beat_removed_handler)
        
        # Create sequence with one beat
        beat = BeatData(letter="A")
        sequence = SequenceData(name="Test", beats=[beat])
        
        # Add another beat then undo
        new_beat = BeatData(letter="B")
        command = AddBeatCommand(
            sequence=sequence,
            beat=new_beat,
            position=1,
            event_bus=self.event_bus
        )
        
        command_processor = CommandProcessor(self.event_bus)
        command_processor.execute(command)
        
        # Act - Undo the command
        undo_result = command_processor.undo()
        
        # Assert
        assert undo_result.success
        beat_removed_handler.assert_called_once()

    def test_multiple_services_respond_to_same_event(self):
        """Test that multiple services can respond to the same event."""
        # Arrange
        layout_handler = Mock()
        ui_handler = Mock()
        pictograph_handler = Mock()
        
        self.event_bus.subscribe("sequence.beat_added", layout_handler)
        self.event_bus.subscribe("sequence.beat_added", ui_handler)  
        self.event_bus.subscribe("sequence.beat_added", pictograph_handler)
        
        # Act - Publish beat added event
        event = BeatAddedEvent(
            event_id="test",
            source="test",
            sequence_id="seq123",
            beat_data={"letter": "A"},
            beat_position=0,
            total_beats=1
        )
        
        self.event_bus.publish(event)
        
        # Assert - All handlers called
        layout_handler.assert_called_once_with(event)
        ui_handler.assert_called_once_with(event)
        pictograph_handler.assert_called_once_with(event)

    def test_