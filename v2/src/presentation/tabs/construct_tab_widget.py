from typing import Tuple, Optional
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QSplitter,
    QStackedWidget,
    QPushButton,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from src.core.dependency_injection.simple_container import SimpleContainer
from src.domain.models.core_models import SequenceData, BeatData
from src.presentation.components.option_picker import ModernOptionPicker
from src.presentation.components.start_position_picker import StartPositionPicker
from src.application.services.option_picker_state_service import (
    OptionPickerStateService,
)
from src.presentation.factories.workbench_factory import create_modern_workbench


class ConstructTabWidget(QWidget):
    sequence_created = pyqtSignal(SequenceData)
    sequence_modified = pyqtSignal(SequenceData)
    start_position_set = pyqtSignal(
        str
    )  # Emits position key when start position is set

    def __init__(self, container: SimpleContainer, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.container = container
        self.state_service = OptionPickerStateService()
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(10)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)

        workbench_panel = self._create_workbench_panel()
        splitter.addWidget(workbench_panel)

        picker_panel = self._create_picker_panel()
        splitter.addWidget(picker_panel)

        # V1 parity: Use 1:1 (50%:50%) ratio for construct tab (not 2:1 like browse tab)
        splitter.setStretchFactor(0, 1)  # Workbench panel gets 1 part (50%)
        splitter.setStretchFactor(1, 1)  # Picker panel gets 1 part (50%)

    def _create_workbench_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)

        title = QLabel("🎬 Sequence Workbench")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        self.workbench = create_modern_workbench(self.container, panel)
        layout.addWidget(self.workbench)

        # Add clear sequence button
        self.clear_button = QPushButton("🗑️ Clear Sequence")
        self.clear_button.setStyleSheet(
            """
            QPushButton {
                background: rgba(220, 53, 69, 0.8);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover {
                background: rgba(220, 53, 69, 1.0);
            }
        """
        )
        self.clear_button.clicked.connect(self.clear_sequence)
        layout.addWidget(self.clear_button)

        return panel

    def _create_picker_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create stacked widget like v1 - this is the key fix
        self.picker_stack = QStackedWidget()

        # Index 0: Start Position Picker
        start_pos_widget = self._create_start_position_widget()
        self.picker_stack.addWidget(start_pos_widget)

        # Index 1: Option Picker
        option_widget = self._create_option_picker_widget()
        self.picker_stack.addWidget(option_widget)

        # Start with start position picker visible
        self.picker_stack.setCurrentIndex(0)

        layout.addWidget(self.picker_stack)
        return panel

    def _create_start_position_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title = QLabel("Select Start Position")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.start_position_picker = StartPositionPicker()
        self.start_position_picker.start_position_selected.connect(
            self._handle_start_position_selected
        )
        layout.addWidget(self.start_position_picker)

        return widget

    def _create_option_picker_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title = QLabel("Available Options")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.option_picker = ModernOptionPicker(self.container)
        self.option_picker.initialize()
        self.option_picker.option_selected.connect(self._handle_option_selected)
        layout.addWidget(self.option_picker.widget)

        return widget

    def _connect_signals(self):
        self.state_service.state_changed.connect(self._on_state_changed)
        self.state_service.option_picker_ready.connect(
            self._transition_to_option_picker
        )
        self.workbench.sequence_modified.connect(self._on_workbench_modified)
        self.workbench.operation_completed.connect(self._on_operation_completed)

    def _handle_start_position_selected(self, position_key: str):
        print(f"🎯 Construct tab: Start position selected: {position_key}")
        self.state_service.select_start_position(position_key)

        # Create start position data (separate from sequence beats like v1)
        start_position_data = self._create_start_position_data(position_key)

        # Set start position in workbench (NOT as sequence beat)
        self.workbench.set_start_position(start_position_data)

        # Populate option picker with valid motion combinations based on start position
        self._populate_option_picker_from_start_position(
            position_key, start_position_data
        )

        # Emit start position signal (not sequence creation)
        self.start_position_set.emit(position_key)

    def _transition_to_option_picker(self):
        """Switch from start position picker to option picker - key fix from v1"""
        print("🔄 Transitioning to option picker view")
        self.picker_stack.setCurrentIndex(1)

    def _transition_to_start_position_picker(self):
        """Switch back to start position picker"""
        print("🔄 Transitioning to start position picker view")
        self.picker_stack.setCurrentIndex(0)

    def _handle_option_selected(self, option_id: str):
        print(f"✅ Construct tab: Option selected: {option_id}")

        current_sequence = self.workbench.get_sequence()
        if current_sequence:
            new_beat = BeatData(
                letter="X", duration=4, beat_number=current_sequence.length + 1
            )
            updated_beats = current_sequence.beats + [new_beat]
            updated_sequence = current_sequence.update(beats=updated_beats)

            self.workbench.set_sequence(updated_sequence)
            self.sequence_modified.emit(updated_sequence)

    def _create_start_position_data(self, position_key: str) -> BeatData:
        """Create start position data from position key (separate from sequence beats)"""
        from ...application.services.pictograph_dataset_service import (
            PictographDatasetService,
        )

        # Use dataset service to get actual start position data
        dataset_service = PictographDatasetService()
        start_position_data = dataset_service.get_start_position_pictograph(
            position_key, "diamond"
        )

        if start_position_data is None:
            # Fallback if dataset service returns None
            from ...domain.models.core_models import (
                MotionData,
                MotionType,
                Location,
                RotationDirection,
            )

            # Create a basic start position
            blue_motion = MotionData(
                motion_type=MotionType.STATIC,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.NORTH,
                turns=0.0,
                start_ori="in",
                end_ori="in",
            )

            red_motion = MotionData(
                motion_type=MotionType.STATIC,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.SOUTH,
                turns=0.0,
                start_ori="out",
                end_ori="out",
            )

            start_position_data = BeatData(
                beat_number=1,
                letter="Σ",
                duration=1.0,
                blue_motion=blue_motion,
                red_motion=red_motion,
            )

        return start_position_data

    def _populate_option_picker_from_start_position(
        self, position_key: str, start_position_data: BeatData
    ):
        """Populate option picker with valid motion combinations based on start position (V1 behavior)"""
        try:
            # Convert start position data to sequence format for motion combination service
            sequence_data = [
                {"metadata": "sequence_info"},  # Metadata entry
                start_position_data.to_dict(),  # Start position entry
            ]

            # Load motion combinations into option picker
            self.option_picker.load_motion_combinations(sequence_data)

            print(
                f"✅ Option picker populated with combinations from start position: {position_key}"
            )

        except Exception as e:
            print(f"❌ Error populating option picker: {e}")
            # Fallback to sample data
            self.option_picker._load_sample_beat_options()

    def _create_start_sequence(self, position_key: str) -> SequenceData:
        """Create empty sequence (deprecated - start position should not create sequence)"""
        # This method is deprecated - start position should not create sequence beats
        return SequenceData.empty()

    def _on_state_changed(self, new_state: str):
        print(f"🔄 Construct tab state: {new_state}")

    def _on_workbench_modified(self, sequence: SequenceData):
        print(f"🔧 Construct tab: Workbench modified sequence: {sequence.length} beats")
        self.sequence_modified.emit(sequence)

    def _on_operation_completed(self, message: str):
        print(f"✅ Construct tab: {message}")

    def get_current_sequence(self) -> Optional[SequenceData]:
        return self.workbench.get_sequence()

    def clear_sequence(self):
        """Clear sequence and reset to start position picker"""
        print("🗑️ Clearing sequence and resetting to start position picker")
        self.state_service.reset_to_start_position_selection()
        empty_sequence = SequenceData.empty()
        self.workbench.set_sequence(empty_sequence)
        self._transition_to_start_position_picker()

    def reset(self):
        self.clear_sequence()

    def resizeEvent(self, event):
        """Handle resize events to ensure start position picker remains responsive"""
        super().resizeEvent(event)
        if hasattr(self, "start_position_picker"):
            self.start_position_picker.update_layout_for_size(self.size())
