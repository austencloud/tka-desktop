"""
SignalCoordinator

Manages signal connections, emissions, and coordination between construct tab components.
Responsible for connecting signals between components and handling signal routing.
"""

from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal

from domain.models.core_models import SequenceData
from .start_position_handler import StartPositionHandler
from .option_picker_manager import OptionPickerManager
from .sequence_manager import SequenceManager
from .layout_manager import ConstructTabLayoutManager


class SignalCoordinator(QObject):
    """
    Coordinates signals between construct tab components.

    Responsibilities:
    - Connecting signals between components
    - Managing signal routing and forwarding
    - Handling component state changes
    - Coordinating transitions between UI states

    Signals:
    - sequence_created: Emitted when a new sequence is created
    - sequence_modified: Emitted when sequence is modified
    - start_position_set: Emitted when start position is set
    """

    sequence_created = pyqtSignal(object)  # SequenceData object
    sequence_modified = pyqtSignal(object)  # SequenceData object
    start_position_set = pyqtSignal(str)  # position key

    def __init__(
        self,
        layout_manager: ConstructTabLayoutManager,
        start_position_handler: StartPositionHandler,
        option_picker_manager: OptionPickerManager,
        sequence_manager: SequenceManager,
    ):
        super().__init__()
        self.layout_manager = layout_manager
        self.start_position_handler = start_position_handler
        self.option_picker_manager = option_picker_manager
        self.sequence_manager = sequence_manager

        self._setup_signal_connections()

    def _setup_signal_connections(self):
        """Setup all signal connections between components"""

        # Start position picker to start position handler
        if self.layout_manager.start_position_picker:
            self.layout_manager.start_position_picker.start_position_selected.connect(
                self.start_position_handler.handle_start_position_selected
            )

        # Start position handler signals
        self.start_position_handler.start_position_created.connect(
            self._handle_start_position_created
        )
        self.start_position_handler.transition_requested.connect(
            self.layout_manager.transition_to_option_picker
        )

        # Option picker manager signals
        self.option_picker_manager.beat_data_selected.connect(
            self.sequence_manager.add_beat_to_sequence
        )

        # Sequence manager signals
        self.sequence_manager.sequence_modified.connect(self._handle_sequence_modified)
        self.sequence_manager.sequence_cleared.connect(self._handle_sequence_cleared)

        # Workbench signals (if available)
        if self.layout_manager.workbench:
            self.layout_manager.workbench.sequence_modified.connect(
                self.sequence_manager.handle_workbench_modified
            )
            self.layout_manager.workbench.operation_completed.connect(
                self._handle_operation_completed
            )

    def _handle_start_position_created(self, position_key: str, start_position_data):
        """Handle start position creation"""
        print(f"✅ Signal coordinator: Start position created: {position_key}")

        # Populate option picker with valid combinations
        self.option_picker_manager.populate_from_start_position(
            position_key, start_position_data
        )

        # Emit external signal
        self.start_position_set.emit(position_key)

    def _handle_sequence_modified(self, sequence: SequenceData):
        """Handle sequence modification"""
        print(
            f"✅ Signal coordinator: Sequence modified with {sequence.length if sequence else 0} beats"
        )

        # Check if sequence was cleared and handle transition
        if sequence is None or sequence.length == 0:
            print("🗑️ Sequence cleared detected, transitioning to start position picker")
            self.layout_manager.transition_to_start_position_picker()
        else:
            # Refresh option picker based on sequence state
            self.option_picker_manager.refresh_from_sequence(sequence)

        # Emit external signal
        self.sequence_modified.emit(sequence)

    def _handle_sequence_cleared(self):
        """Handle sequence clearing"""
        print("✅ Signal coordinator: Sequence cleared")
        self.layout_manager.transition_to_start_position_picker()

    def _handle_operation_completed(self, message: str):
        """Handle workbench operation completion"""
        print(f"✅ Signal coordinator: Operation completed: {message}")

    def clear_sequence(self):
        """Clear the current sequence (public interface)"""
        self.sequence_manager.clear_sequence()

    def connect_external_workbench_signals(self, workbench):
        """Connect signals to an external workbench if needed"""
        if workbench:
            workbench.sequence_modified.connect(
                self.sequence_manager.handle_workbench_modified
            )
            workbench.operation_completed.connect(self._handle_operation_completed)
