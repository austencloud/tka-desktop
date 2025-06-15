# **Task 2.5: Command Pattern for Undo/Redo**

**Timeline**: Week 2 of Phase 2  
**Priority**: HIGH  
**Goal**: Implement comprehensive command pattern with undo/redo functionality

---

## **Implement Command Infrastructure:**

### **FILE: src/core/commands/command_system.py**

```python
"""
Command pattern implementation for undo/redo functionality.
Provides type-safe, undoable operations.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Any
from dataclasses import dataclass
import logging

T = TypeVar("T")

class ICommand(Generic[T], ABC):
    """Interface for undoable commands."""

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
        """Check if command can be executed."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get human-readable description of the command."""
        pass

@dataclass(frozen=True)
class AddBeatCommand(ICommand[SequenceData]):
    """Command to add a beat to a sequence."""
    sequence: SequenceData
    beat: BeatData
    position: int

    def execute(self) -> SequenceData:
        if not self.can_execute():
            raise ValueError("Cannot add beat at invalid position")
        return self.sequence.add_beat_at_position(self.beat, self.position)

    def undo(self) -> SequenceData:
        return self.sequence.remove_beat_at_position(self.position)

    def can_execute(self) -> bool:
        return 0 <= self.position <= len(self.sequence.beats)

    def get_description(self) -> str:
        return f"Add beat '{self.beat.letter}' at position {self.position + 1}"

@dataclass(frozen=True)
class UpdateBeatCommand(ICommand[SequenceData]):
    """Command to update a beat in a sequence."""
    sequence: SequenceData
    beat_index: int
    field_updates: Dict[str, Any]
    previous_values: Dict[str, Any]

    def execute(self) -> SequenceData:
        if not self.can_execute():
            raise ValueError("Cannot update beat at invalid index")
        return self.sequence.update_beat(self.beat_index, **self.field_updates)

    def undo(self) -> SequenceData:
        return self.sequence.update_beat(self.beat_index, **self.previous_values)

    def can_execute(self) -> bool:
        return 0 <= self.beat_index < len(self.sequence.beats)

    def get_description(self) -> str:
        changes = ", ".join(f"{k}={v}" for k, v in self.field_updates.items())
        return f"Update beat {self.beat_index + 1}: {changes}"

class CommandProcessor:
    """Processes commands with undo/redo support."""

    def __init__(self, event_bus: IEventBus, max_history: int = 100):
        self.event_bus = event_bus
        self.max_history = max_history
        self._history: List[ICommand] = []
        self._current_index = -1
        self._logger = logging.getLogger(__name__)

    def execute(self, command: ICommand[T]) -> T:
        """Execute command and add to history."""
        if not command.can_execute():
            raise ValueError(f"Command cannot be executed: {command.get_description()}")

        try:
            result = command.execute()

            # Clear redo history if we're not at the end
            self._history = self._history[:self._current_index + 1]

            # Add command to history
            self._history.append(command)
            self._current_index += 1

            # Limit history size
            if len(self._history) > self.max_history:
                self._history = self._history[-self.max_history:]
                self._current_index = len(self._history) - 1

            self._logger.debug(f"Executed: {command.get_description()}")

            # Publish command executed event
            self.event_bus.publish(CommandExecutedEvent(
                timestamp=time.time(),
                source_component="CommandProcessor",
                command_description=command.get_description(),
                can_undo=self.can_undo(),
                can_redo=self.can_redo()
            ))

            return result

        except Exception as e:
            self._logger.error(f"Command execution failed: {command.get_description()}: {e}")
            raise

    def undo(self) -> Optional[Any]:
        """Undo the last command."""
        if not self.can_undo():
            return None

        command = self._history[self._current_index]
        try:
            result = command.undo()
            self._current_index -= 1

            self._logger.debug(f"Undid: {command.get_description()}")

            # Publish undo event
            self.event_bus.publish(CommandUndoneEvent(
                timestamp=time.time(),
                source_component="CommandProcessor",
                command_description=command.get_description(),
                can_undo=self.can_undo(),
                can_redo=self.can_redo()
            ))

            return result

        except Exception as e:
            self._logger.error(f"Command undo failed: {command.get_description()}: {e}")
            raise

    def redo(self) -> Optional[Any]:
        """Redo the next command."""
        if not self.can_redo():
            return None

        self._current_index += 1
        command = self._history[self._current_index]

        try:
            result = command.execute()

            self._logger.debug(f"Redid: {command.get_description()}")

            # Publish redo event
            self.event_bus.publish(CommandRedoneEvent(
                timestamp=time.time(),
                source_component="CommandProcessor",
                command_description=command.get_description(),
                can_undo=self.can_undo(),
                can_redo=self.can_redo()
            ))

            return result

        except Exception as e:
            self._logger.error(f"Command redo failed: {command.get_description()}: {e}")
            self._current_index -= 1  # Revert index on failure
            raise

    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return self._current_index >= 0

    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return self._current_index < len(self._history) - 1

    def get_undo_description(self) -> Optional[str]:
        """Get description of command that would be undone."""
        if self.can_undo():
            return self._history[self._current_index].get_description()
        return None

    def get_redo_description(self) -> Optional[str]:
        """Get description of command that would be redone."""
        if self.can_redo():
            return self._history[self._current_index + 1].get_description()
        return None

    def clear_history(self):
        """Clear command history."""
        self._history.clear()
        self._current_index = -1

# Command Events
@dataclass(frozen=True)
class CommandExecutedEvent(BaseEvent):
    """Published when a command is executed."""
    command_description: str
    can_undo: bool
    can_redo: bool

@dataclass(frozen=True)
class CommandUndoneEvent(BaseEvent):
    """Published when a command is undone."""
    command_description: str
    can_undo: bool
    can_redo: bool

@dataclass(frozen=True)
class CommandRedoneEvent(BaseEvent):
    """Published when a command is redone."""
    command_description: str
    can_undo: bool
    can_redo: bool
```

---

## **Success Criteria:**

By the end of Task 2.5:

- ✅ **Command pattern infrastructure** implemented
- ✅ **Undo/redo functionality** working
- ✅ **Command history management** in place
- ✅ **Type-safe commands** with validation
- ✅ **Event integration** for UI updates

---

## **Next Step**

After completing command infrastructure, proceed to: [Task 2.6: Service Integration with Commands](02_service_command_integration.md)
