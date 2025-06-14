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
    sequence_modified = pyqtSignal(SequenceData)

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


class WorkbenchButtonInterfaceAdapter:
    """
    Adapter that implements the button interface for existing workbench.

    This adapter allows the existing ModernSequenceWorkbench to implement
    the IWorkbenchButtonInterface without requiring full refactoring.
    It acts as a bridge between the new interface and existing implementation.
    """

    def __init__(self, workbench):
        """Initialize with reference to existing workbench."""
        self.workbench = workbench
        self.signals = WorkbenchButtonSignals()

        # Connect to existing workbench signals if available
        if hasattr(workbench, "sequence_modified"):
            workbench.sequence_modified.connect(self.signals.sequence_modified)
        if hasattr(workbench, "operation_completed"):
            workbench.operation_completed.connect(self.signals.operation_completed)
        if hasattr(workbench, "error_occurred"):
            workbench.error_occurred.connect(self.signals.operation_failed)

    def clear_sequence(self) -> ButtonOperationResult:
        """Clear sequence using existing workbench method."""
        try:
            if hasattr(self.workbench, "_handle_clear"):
                self.workbench._handle_clear()
                self.signals.sequence_cleared.emit()
                return ButtonOperationResult.success("Sequence cleared")
            else:
                return ButtonOperationResult.failure("Clear method not available")
        except Exception as e:
            return ButtonOperationResult.failure(f"Clear failed: {e}")

    def delete_selected_beat(self) -> ButtonOperationResult:
        """Delete selected beat using existing workbench method."""
        try:
            if hasattr(self.workbench, "_handle_delete_beat"):
                self.workbench._handle_delete_beat()
                return ButtonOperationResult.success("Beat deleted")
            else:
                return ButtonOperationResult.failure("Delete method not available")
        except Exception as e:
            return ButtonOperationResult.failure(f"Delete failed: {e}")

    def get_current_sequence(self) -> Optional[SequenceData]:
        """Get current sequence from workbench."""
        if hasattr(self.workbench, "get_sequence"):
            return self.workbench.get_sequence()
        elif hasattr(self.workbench, "_current_sequence"):
            return self.workbench._current_sequence
        return None

    def get_selected_beat_index(self) -> Optional[int]:
        """Get selected beat index from workbench."""
        if hasattr(self.workbench, "_beat_frame") and self.workbench._beat_frame:
            if hasattr(self.workbench._beat_frame, "get_selected_beat_index"):
                return self.workbench._beat_frame.get_selected_beat_index()
        return None

    def get_start_position(self) -> Optional[BeatData]:
        """Get start position from workbench."""
        if hasattr(self.workbench, "get_start_position"):
            return self.workbench.get_start_position()
        elif hasattr(self.workbench, "_start_position_data"):
            return self.workbench._start_position_data
        return None

    def update_sequence_display(self) -> ButtonOperationResult:
        """Update sequence display using existing workbench method."""
        try:
            if hasattr(self.workbench, "_update_display"):
                self.workbench._update_display()
                return ButtonOperationResult.success("Display updated")
            else:
                return ButtonOperationResult.failure("Update method not available")
        except Exception as e:
            return ButtonOperationResult.failure(f"Update failed: {e}")

    def export_sequence_image(self) -> ButtonOperationResult:
        """Export sequence image using existing workbench method."""
        try:
            if hasattr(self.workbench, "_handle_save_image"):
                self.workbench._handle_save_image()
                return ButtonOperationResult.success("Image exported")
            else:
                return ButtonOperationResult.failure("Export method not available")
        except Exception as e:
            return ButtonOperationResult.failure(f"Export failed: {e}")

    def export_sequence_json(self) -> ButtonOperationResult:
        """Export sequence JSON using existing workbench method."""
        try:
            if hasattr(self.workbench, "_handle_copy_json"):
                self.workbench._handle_copy_json()
                return ButtonOperationResult.success("JSON exported")
            else:
                return ButtonOperationResult.failure("JSON export method not available")
        except Exception as e:
            return ButtonOperationResult.failure(f"JSON export failed: {e}")

    def swap_colors(self) -> ButtonOperationResult:
        """Swap colors using existing workbench method."""
        try:
            if hasattr(self.workbench, "_handle_color_swap"):
                self.workbench._handle_color_swap()
                self.signals.colors_swapped.emit()
                return ButtonOperationResult.success("Colors swapped")
            else:
                return ButtonOperationResult.failure("Color swap method not available")
        except Exception as e:
            return ButtonOperationResult.failure(f"Color swap failed: {e}")

    def mirror_sequence(self) -> ButtonOperationResult:
        """Mirror sequence using existing workbench method."""
        try:
            if hasattr(self.workbench, "_handle_reflection"):
                self.workbench._handle_reflection()
                self.signals.sequence_mirrored.emit()
                return ButtonOperationResult.success("Sequence mirrored")
            else:
                return ButtonOperationResult.failure("Mirror method not available")
        except Exception as e:
            return ButtonOperationResult.failure(f"Mirror failed: {e}")

    def rotate_sequence(self) -> ButtonOperationResult:
        """Rotate sequence using existing workbench method."""
        try:
            if hasattr(self.workbench, "_handle_rotation"):
                self.workbench._handle_rotation()
                self.signals.sequence_rotated.emit()
                return ButtonOperationResult.success("Sequence rotated")
            else:
                return ButtonOperationResult.failure("Rotation method not available")
        except Exception as e:
            return ButtonOperationResult.failure(f"Rotation failed: {e}")

    def add_to_dictionary(self) -> ButtonOperationResult:
        """Add to dictionary using existing workbench method."""
        try:
            if hasattr(self.workbench, "_handle_add_to_dictionary"):
                self.workbench._handle_add_to_dictionary()
                return ButtonOperationResult.success("Added to dictionary")
            else:
                return ButtonOperationResult.failure("Dictionary method not available")
        except Exception as e:
            return ButtonOperationResult.failure(f"Dictionary add failed: {e}")

    def show_fullscreen(self) -> ButtonOperationResult:
        """Show fullscreen using existing workbench method."""
        try:
            if hasattr(self.workbench, "_handle_fullscreen"):
                self.workbench._handle_fullscreen()
                return ButtonOperationResult.success("Fullscreen opened")
            else:
                return ButtonOperationResult.failure("Fullscreen method not available")
        except Exception as e:
            return ButtonOperationResult.failure(f"Fullscreen failed: {e}")


class WorkbenchButtonInterfaceSignals(QObject):
    """Signal container for button interface adapter"""

    sequence_modified = pyqtSignal(SequenceData)
    operation_completed = pyqtSignal(str)
    operation_failed = pyqtSignal(str)


class WorkbenchButtonInterfaceAdapter:
    """Adapter for V1 button interface compatibility"""

    def __init__(self, workbench):
        self._workbench = workbench
        self.signals = WorkbenchButtonInterfaceSignals()

    def add_to_dictionary(self) -> bool:
        """Legacy method for V1 compatibility"""
        if hasattr(self._workbench, "_handle_add_to_dictionary"):
            try:
                self._workbench._handle_add_to_dictionary()
                return True
            except Exception:
                return False
        return False

    def save_image(self) -> bool:
        """Legacy method for V1 compatibility"""
        if hasattr(self._workbench, "_handle_save_image"):
            try:
                self._workbench._handle_save_image()
                return True
            except Exception:
                return False
        return False

    def delete_beat(self) -> bool:
        """Legacy method for V1 compatibility"""
        if hasattr(self._workbench, "_handle_delete_beat"):
            try:
                self._workbench._handle_delete_beat()
                return True
            except Exception:
                return False
        return False

    def clear_sequence(self) -> bool:
        """Legacy method for V1 compatibility"""
        if hasattr(self._workbench, "_handle_clear"):
            try:
                self._workbench._handle_clear()
                return True
            except Exception:
                return False
        return False

    def mirror_sequence(self) -> bool:
        """Legacy method for V1 compatibility"""
        if hasattr(self._workbench, "_handle_reflection"):
            try:
                self._workbench._handle_reflection()
                return True
            except Exception:
                return False
        return False

    def swap_colors(self) -> bool:
        """Legacy method for V1 compatibility"""
        if hasattr(self._workbench, "_handle_color_swap"):
            try:
                self._workbench._handle_color_swap()
                return True
            except Exception:
                return False
        return False

    def rotate_sequence(self) -> bool:
        """Legacy method for V1 compatibility"""
        if hasattr(self._workbench, "_handle_rotation"):
            try:
                self._workbench._handle_rotation()
                return True
            except Exception:
                return False
        return False

    def copy_json(self) -> bool:
        """Legacy method for V1 compatibility"""
        if hasattr(self._workbench, "_handle_copy_json"):
            try:
                self._workbench._handle_copy_json()
                return True
            except Exception:
                return False
        return False

    def view_fullscreen(self) -> bool:
        """Legacy method for V1 compatibility"""
        if hasattr(self._workbench, "_handle_fullscreen"):
            try:
                self._workbench._handle_fullscreen()
                return True
            except Exception:
                return False
        return False
