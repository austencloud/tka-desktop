"""
Workbench Button Interface for Sprint 2 Integration
===================================================

Clean interface for button panel integration with ModernSequenceWorkbench.
This interface provides the essential methods that the Sprint 2 button panel
needs to interact with the sequence workbench without requiring full refactoring.

Phase 0 - Days 2-3: Strategic partial refactoring for Sprint 2 preparation.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from PyQt6.QtCore import QObject, pyqtSignal

from domain.models.core_models import SequenceData, BeatData


class IWorkbenchButtonInterface(ABC):
    """
    Interface for button panel integration with sequence workbench.

    This interface defines the essential operations that button panels
    need to perform on the sequence workbench, providing a clean
    separation between UI components and workbench logic.
    """

    @abstractmethod
    def clear_sequence(self) -> None:
        """Clear the current sequence, preserving start position."""
        pass

    @abstractmethod
    def delete_selected_beat(self) -> None:
        """Delete the currently selected beat from the sequence."""
        pass

    @abstractmethod
    def get_current_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence being edited."""
        pass

    @abstractmethod
    def get_selected_beat_index(self) -> Optional[int]:
        """Get the index of the currently selected beat."""
        pass

    @abstractmethod
    def get_start_position(self) -> Optional[BeatData]:
        """Get the current start position data."""
        pass

    @abstractmethod
    def update_sequence_display(self) -> None:
        """Update the visual display of the sequence."""
        pass

    @abstractmethod
    def export_sequence_image(self) -> bool:
        """Export the current sequence as an image."""
        pass

    @abstractmethod
    def export_sequence_json(self) -> str:
        """Export the current sequence as JSON."""
        pass

    @abstractmethod
    def swap_colors(self) -> None:
        """Swap blue and red colors in the sequence."""
        pass

    @abstractmethod
    def mirror_sequence(self) -> None:
        """Mirror the sequence horizontally."""
        pass

    @abstractmethod
    def rotate_sequence(self) -> None:
        """Rotate the sequence."""
        pass

    @abstractmethod
    def add_to_dictionary(self) -> bool:
        """Add the current sequence to the dictionary."""
        pass

    @abstractmethod
    def show_fullscreen(self) -> None:
        """Show the sequence in fullscreen mode."""
        pass


class WorkbenchButtonSignals(QObject):
    """
    Signal emitter for workbench button operations.

    Provides signals that button panels can connect to for
    receiving feedback about workbench operations.
    """

    # Operation completion signals
    operation_completed = pyqtSignal(str)  # message
    operation_failed = pyqtSignal(str)  # error message

    # Sequence state signals
    sequence_cleared = pyqtSignal()
    beat_deleted = pyqtSignal(int)  # beat index
    sequence_modified = pyqtSignal(object)  # SequenceData object

    # Export signals
    image_exported = pyqtSignal(str)  # file path
    json_exported = pyqtSignal(str)  # json data

    # Dictionary signals
    added_to_dictionary = pyqtSignal(str)  # word

    # Transform signals
    colors_swapped = pyqtSignal()
    sequence_mirrored = pyqtSignal()
    sequence_rotated = pyqtSignal()


class ButtonOperationResult:
    """
    Result object for button operations.

    Provides structured feedback about the success or failure
    of button operations, including error messages and data.
    """

    def __init__(self, success: bool, message: str = "", data: any = None):
        self.success = success
        self.message = message
        self.data = data

    @classmethod
    def success(cls, message: str = "Operation completed", data: any = None):
        """Create a successful result."""
        return cls(True, message, data)

    @classmethod
    def failure(cls, message: str = "Operation failed", data: any = None):
        """Create a failed result."""
        return cls(False, message, data)

    def __bool__(self):
        """Allow boolean evaluation of result."""
        return self.success


class WorkbenchButtonInterfaceSignals(QObject):
    """Signal container for button interface adapter"""

    sequence_modified = pyqtSignal(object)  # SequenceData object
    operation_completed = pyqtSignal(str)
    operation_failed = pyqtSignal(str)


class WorkbenchButtonInterfaceAdapter:
    """Adapter for Legacy button interface compatibility"""

    def __init__(self, workbench):
        self._workbench = workbench
        self.signals = WorkbenchButtonInterfaceSignals()

    def add_to_dictionary(self) -> bool:
        """Legacy method for Legacy compatibility"""
        if hasattr(self._workbench, "_handle_add_to_dictionary"):
            try:
                self._workbench._handle_add_to_dictionary()
                return True
            except Exception:
                return False
        return False

    def save_image(self) -> bool:
        """Legacy method for Legacy compatibility"""
        if hasattr(self._workbench, "_handle_save_image"):
            try:
                self._workbench._handle_save_image()
                return True
            except Exception:
                return False
        return False

    def delete_beat(self) -> bool:
        """Legacy method for Legacy compatibility"""
        if hasattr(self._workbench, "_handle_delete_beat"):
            try:
                self._workbench._handle_delete_beat()
                return True
            except Exception:
                return False
        return False

    def clear_sequence(self) -> bool:
        """Legacy method for Legacy compatibility"""
        if hasattr(self._workbench, "_handle_clear"):
            try:
                self._workbench._handle_clear()
                return True
            except Exception:
                return False
        return False

    def mirror_sequence(self) -> bool:
        """Legacy method for Legacy compatibility"""
        if hasattr(self._workbench, "_handle_reflection"):
            try:
                self._workbench._handle_reflection()
                return True
            except Exception:
                return False
        return False

    def swap_colors(self) -> bool:
        """Legacy method for Legacy compatibility"""
        if hasattr(self._workbench, "_handle_color_swap"):
            try:
                self._workbench._handle_color_swap()
                return True
            except Exception:
                return False
        return False

    def rotate_sequence(self) -> bool:
        """Legacy method for Legacy compatibility"""
        if hasattr(self._workbench, "_handle_rotation"):
            try:
                self._workbench._handle_rotation()
                return True
            except Exception:
                return False
        return False

    def copy_json(self) -> bool:
        """Legacy method for Legacy compatibility"""
        if hasattr(self._workbench, "_handle_copy_json"):
            try:
                self._workbench._handle_copy_json()
                return True
            except Exception:
                return False
        return False

    def view_fullscreen(self) -> bool:
        """Legacy method for Legacy compatibility"""
        if hasattr(self._workbench, "_handle_fullscreen"):
            try:
                self._workbench._handle_fullscreen()
                return True
            except Exception:
                return False
        return False
