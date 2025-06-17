"""
Command pattern implementation for undoable operations.
Provides type-safe, undoable commands with event integration.
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Any, Dict, TYPE_CHECKING
from dataclasses import dataclass
import uuid
import logging
from datetime import datetime

if TYPE_CHECKING:
    from ..events import IEventBus

from ..events import (
    IEventBus,
    CommandExecutedEvent,
    CommandUndoneEvent,
    CommandRedoneEvent,
)

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

    def __init__(self, event_bus: Any, max_history: int = 100):
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
                    success=False, error_message=error_msg, command_id=command_id
                )

            # Execute the command
            self._logger.info(f"Executing command: {command.description}")
            result = command.execute()

            # Add to history (clear redo stack if we're not at the end)
            self._history = self._history[: self._current_index + 1]
            self._history.append(command)
            self._current_index += 1

            # Limit history size
            if len(self._history) > self.max_history:
                self._history = self._history[-self.max_history :]
                self._current_index = len(self._history) - 1

            # Publish command executed event
            self.event_bus.publish(
                CommandExecutedEvent(
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source="CommandProcessor",
                    command_id=command_id,
                    command_type=type(command).__name__,
                    command_description=command.description,
                    can_undo=self.can_undo(),
                    can_redo=self.can_redo(),
                )
            )

            self._logger.info(f"Command executed successfully: {command.description}")
            return CommandResult(success=True, result=result, command_id=command_id)

        except Exception as e:
            error_msg = f"Command execution failed: {command.description} - {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            return CommandResult(
                success=False, error_message=error_msg, command_id=command_id
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
                return CommandResult(
                    success=False, error_message=error_msg, command_id=command_id
                )

            self._logger.info(f"Undoing command: {command.description}")
            result = command.undo()
            self._current_index -= 1

            # Publish command undone event
            self.event_bus.publish(
                CommandUndoneEvent(
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source="CommandProcessor",
                    command_id=command_id,
                    command_type=type(command).__name__,
                    command_description=command.description,
                    can_undo=self.can_undo(),
                    can_redo=self.can_redo(),
                )
            )

            self._logger.info(f"Command undone successfully: {command.description}")
            return CommandResult(success=True, result=result, command_id=command_id)

        except Exception as e:
            error_msg = f"Command undo failed: {command.description} - {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            return CommandResult(
                success=False, error_message=error_msg, command_id=command_id
            )

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
                return CommandResult(
                    success=False, error_message=error_msg, command_id=command_id
                )

            self._logger.info(f"Redoing command: {command.description}")
            result = command.execute()

            # Publish command redone event
            self.event_bus.publish(
                CommandRedoneEvent(
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source="CommandProcessor",
                    command_id=command_id,
                    command_type=type(command).__name__,
                    command_description=command.description,
                    can_undo=self.can_undo(),
                    can_redo=self.can_redo(),
                )
            )

            self._logger.info(f"Command redone successfully: {command.description}")
            return CommandResult(success=True, result=result, command_id=command_id)

        except Exception as e:
            self._current_index -= 1  # Revert on failure
            error_msg = f"Command redo failed: {command.description} - {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            return CommandResult(
                success=False, error_message=error_msg, command_id=command_id
            )

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
