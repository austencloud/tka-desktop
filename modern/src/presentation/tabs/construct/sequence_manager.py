"""
SequenceManager

Manages sequence operations, workbench interactions, and sequence state for the construct tab.
Responsible for handling beat additions, sequence modifications, and workbench coordination.
"""

from typing import Optional, Callable
from PyQt6.QtCore import QObject, pyqtSignal

from domain.models.core_models import SequenceData, BeatData


class SequenceManager(QObject):
    """
    Manages sequence operations and workbench interactions.

    Responsibilities:
    - Adding beats to sequences
    - Managing sequence state changes
    - Coordinating with workbench component
    - Handling sequence clearing operations

    Signals:
    - sequence_modified: Emitted when sequence is modified
    - sequence_cleared: Emitted when sequence is cleared
    """

    sequence_modified = pyqtSignal(object)  # SequenceData object
    sequence_cleared = pyqtSignal()

    def __init__(
        self,
        workbench_getter: Optional[Callable[[], object]] = None,
        workbench_setter: Optional[Callable[[SequenceData], None]] = None,
    ):
        super().__init__()
        self.workbench_getter = workbench_getter
        self.workbench_setter = workbench_setter

        # Flag to prevent circular signal emissions during operations
        self._emitting_signal = False

    def add_beat_to_sequence(self, beat_data: BeatData):
        """Add a beat to the current sequence"""
        print(f"✅ Sequence manager: Adding beat: {beat_data.letter}")

        # Get current sequence or create empty one if none exists
        current_sequence = self._get_current_sequence()
        if current_sequence is None:
            current_sequence = SequenceData.empty()
            print("📝 Created empty sequence for first beat")

        try:
            # Use the exact beat data that was provided
            new_beat = beat_data.update(
                beat_number=current_sequence.length + 1,
                duration=1.0,  # Ensure valid duration
            )
            print(
                f"📝 Created new beat: {new_beat.letter} (beat #{new_beat.beat_number})"
            )
            print(
                f"   Motion data: Blue {new_beat.blue_motion.start_loc}→{new_beat.blue_motion.end_loc}, Red {new_beat.red_motion.start_loc}→{new_beat.red_motion.end_loc}"
            )

            # Add beat to sequence
            updated_beats = current_sequence.beats + [new_beat]
            updated_sequence = current_sequence.update(beats=updated_beats)

            print(f"📊 Sequence updated: {len(updated_beats)} beats")

            # Update workbench (this will trigger the workbench signal, which will flow back to us)
            if self.workbench_setter:
                self.workbench_setter(updated_sequence)
                print("✅ Workbench sequence updated")
            else:
                # If no workbench setter, emit signal directly
                self._emit_sequence_modified(updated_sequence)

        except Exception as e:
            print(f"❌ Error adding beat to sequence: {e}")
            import traceback

            traceback.print_exc()

    def clear_sequence(self):
        """Clear the current sequence - V1 behavior: hide all beats, keep start position visible"""
        if self.workbench_setter:
            # Clear sequence - beat frame will hide all beat views, start position stays visible
            self.workbench_setter(SequenceData.empty())

        print("🗑️ Sequence cleared")
        self.sequence_cleared.emit()

    def handle_workbench_modified(self, sequence: SequenceData):
        """Handle workbench sequence modification with circular emission protection"""
        if self._emitting_signal:
            print("🔄 Sequence manager: Preventing circular signal emission")
            return

        try:
            self._emitting_signal = True

            print(
                f"📡 Sequence manager: Handling workbench modification for {sequence.length if sequence else 0} beats"
            )

            # Emit the sequence_modified signal for the signal coordinator to handle reactivity
            self.sequence_modified.emit(sequence)
            print("✅ Sequence manager: Signal emitted successfully")
        except Exception as e:
            print(f"❌ Sequence manager: Signal emission failed: {e}")
            import traceback

            traceback.print_exc()
        finally:
            self._emitting_signal = False

    def _get_current_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence from workbench"""
        if self.workbench_getter:
            try:
                workbench = self.workbench_getter()
                if workbench and hasattr(workbench, "get_sequence"):
                    return workbench.get_sequence()
            except Exception as e:
                print(f"❌ Error getting current sequence: {e}")
        return None

    def _emit_sequence_modified(self, sequence: SequenceData):
        """Emit sequence modified signal with circular emission protection"""
        if not self._emitting_signal:
            try:
                self._emitting_signal = True
                self.sequence_modified.emit(sequence)
                print("📡 Sequence modified signal emitted")
            finally:
                self._emitting_signal = False
        else:
            print("🔄 Skipping signal emission to prevent circular calls")

    def get_current_sequence_length(self) -> int:
        """Get the length of the current sequence"""
        current_sequence = self._get_current_sequence()
        return current_sequence.length if current_sequence else 0
