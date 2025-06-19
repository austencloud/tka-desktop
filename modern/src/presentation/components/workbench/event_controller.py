from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication
from domain.models.core_models import SequenceData
from core.interfaces.workbench_services import (
    ISequenceWorkbenchService,
    IFullScreenService,
    IBeatDeletionService,
    IDictionaryService,
)


class WorkbenchEventController(QObject):
    """Centralized event controller for workbench operations"""

    # Output signals
    sequence_modified = pyqtSignal(SequenceData)
    operation_completed = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(
        self,
        workbench_service: ISequenceWorkbenchService,
        fullscreen_service: IFullScreenService,
        deletion_service: IBeatDeletionService,
        dictionary_service: IDictionaryService,
    ):
        super().__init__()
        self._workbench_service = workbench_service
        self._fullscreen_service = fullscreen_service
        self._deletion_service = deletion_service
        self._dictionary_service = dictionary_service

        self._current_sequence: Optional[SequenceData] = None

    def set_sequence(self, sequence: Optional[SequenceData]):
        """Set current sequence for operations"""
        self._current_sequence = sequence

    def handle_add_to_dictionary(self) -> tuple[bool, str]:
        """Handle add to dictionary operation"""
        if not self._current_sequence:
            return False, "No sequence to add to dictionary"

        try:
            result = self._dictionary_service.add_sequence_to_dictionary(
                self._current_sequence, ""
            )
            if result:
                return True, "Added to dictionary!"
            else:
                return False, "Sequence already in dictionary"
        except Exception as e:
            return False, f"Failed to add to dictionary: {e}"

    def handle_save_image(self) -> tuple[bool, str]:
        """Handle save image operation"""
        if not self._current_sequence:
            return False, "No sequence to export"

        try:
            success = self._workbench_service.export_sequence_image(
                self._current_sequence
            )
            return success, "Image saved!" if success else "Image export failed"
        except Exception as e:
            return False, f"Export failed: {e}"

    def handle_delete_beat(
        self, selected_index: Optional[int]
    ) -> tuple[bool, str, Optional[SequenceData]]:
        """Handle delete beat operation"""
        if not self._current_sequence or self._current_sequence.length == 0:
            return False, "No beats to delete", None

        if selected_index is None:
            return False, "No beat selected", None

        try:
            updated_sequence = self._deletion_service.delete_beat(
                self._current_sequence, selected_index
            )
            self._current_sequence = updated_sequence
            return True, "Beat deleted!", updated_sequence
        except Exception as e:
            return False, f"Delete failed: {e}", None

    def handle_color_swap(self) -> tuple[bool, str, Optional[SequenceData]]:
        """Handle color swap operation"""
        if not self._current_sequence:
            return False, "No sequence to swap colors", None

        try:
            swapped_sequence = self._workbench_service.swap_colors(
                self._current_sequence
            )
            self._current_sequence = swapped_sequence
            return True, "Colors swapped!", swapped_sequence
        except Exception as e:
            return False, f"Color swap failed: {e}", None

    def handle_reflection(self) -> tuple[bool, str, Optional[SequenceData]]:
        """Handle reflection operation"""
        if not self._current_sequence:
            return False, "No sequence to reflect", None

        try:
            reflected_sequence = self._workbench_service.reflect_sequence(
                self._current_sequence
            )
            self._current_sequence = reflected_sequence
            return True, "Sequence reflected!", reflected_sequence
        except Exception as e:
            return False, f"Reflection failed: {e}", None

    def handle_rotation(self) -> tuple[bool, str, Optional[SequenceData]]:
        """Handle rotation operation"""
        if not self._current_sequence:
            return False, "No sequence to rotate", None

        try:
            rotated_sequence = self._workbench_service.rotate_sequence(
                self._current_sequence
            )
            self._current_sequence = rotated_sequence
            return True, "Sequence rotated!", rotated_sequence
        except Exception as e:
            return False, f"Rotation failed: {e}", None

    def handle_clear(self) -> tuple[bool, str, Optional[SequenceData]]:
        try:
            # Allow clearing even when no sequence exists - the workbench will handle
            # clearing start position data. This enables clearing when only a start
            # position is selected (no beats added yet).
            empty_sequence = SequenceData.empty()
            self._current_sequence = empty_sequence
            return True, "Sequence cleared!", empty_sequence
        except Exception as e:
            return False, f"Clear failed: {e}", None

    def handle_fullscreen(self) -> tuple[bool, str]:
        """Handle full screen view operation"""
        if not self._current_sequence:
            return False, "No sequence to view"

        try:
            self._fullscreen_service.show_full_screen_view(self._current_sequence)
            return True, "Opening full screen view..."
        except Exception as e:
            return False, f"Full screen view failed: {e}"

    def handle_copy_json(self) -> tuple[bool, str]:
        """Handle copy JSON operation"""
        if not self._current_sequence:
            return False, "No sequence to copy"

        try:
            json_data = self._workbench_service.export_sequence_json(
                self._current_sequence
            )

            clipboard = QApplication.clipboard()
            clipboard.setText(json_data)

            return True, "JSON copied to clipboard!"
        except Exception as e:
            return False, f"JSON export failed: {e}"
