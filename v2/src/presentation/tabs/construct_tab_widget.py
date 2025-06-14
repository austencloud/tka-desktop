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

# StartPositionPicker imported locally in _create_start_position_widget method
from src.application.services.option_picker_state_service import (
    OptionPickerStateService,
)
from src.presentation.factories.workbench_factory import create_modern_workbench


class ConstructTabWidget(QWidget):
    sequence_created = pyqtSignal(object)  # SequenceData object
    sequence_modified = pyqtSignal(object)  # SequenceData object
    start_position_set = pyqtSignal(
        str
    )  # Emits position key when start position is set

    def __init__(
        self,
        container: SimpleContainer,
        parent: Optional[QWidget] = None,
        progress_callback=None,
    ):
        super().__init__(parent)
        self.container = container
        self.progress_callback = progress_callback
        self.state_service = OptionPickerStateService()

        # Flag to prevent circular signal emissions during clear operations
        self._emitting_signal = False

        self._setup_ui_with_progress()
        self._connect_signals()

    def _setup_ui_with_progress(self):
        """Setup UI with granular progress updates"""
        if self.progress_callback:
            self.progress_callback("Setting up construct tab layout...", 0.1)

        # Main horizontal layout: 50/50 split like V1
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(12, 12, 12, 12)

        if self.progress_callback:
            self.progress_callback("Creating sequence workbench panel...", 0.2)

        # Left panel: Sequence Workbench (50% width)
        workbench_panel = self._create_workbench_panel()
        main_layout.addWidget(workbench_panel, 1)  # Equal weight = 50%

        if self.progress_callback:
            self.progress_callback("Creating option picker panel...", 0.5)

        # Right panel: Option Picker (50% width)
        picker_panel = self._create_picker_panel_with_progress()
        main_layout.addWidget(picker_panel, 1)  # Equal weight = 50%

        if self.progress_callback:
            self.progress_callback("Construct tab layout complete!", 1.0)

    def _create_workbench_panel(self) -> QWidget:
        """Create the left panel containing sequence workbench"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Create modern workbench with integrated button panel
        self.workbench = create_modern_workbench(self.container, panel)
        layout.addWidget(self.workbench)

        return panel

    def _create_picker_panel_with_progress(self) -> QWidget:
        """Create the right panel containing start pos picker and option picker"""
        if self.progress_callback:
            self.progress_callback("Creating picker panel layout...", 0.6)

        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Create stacked widget for picker views (like V1)
        self.picker_stack = QStackedWidget()

        if self.progress_callback:
            self.progress_callback("Initializing start position picker...", 0.7)

        # Index 0: Start Position Picker
        start_pos_widget = self._create_start_position_widget()
        self.picker_stack.addWidget(start_pos_widget)

        if self.progress_callback:
            self.progress_callback("Loading option picker dataset...", 0.8)

        # Index 1: Option Picker
        option_widget = self._create_option_picker_widget_with_progress()
        self.picker_stack.addWidget(option_widget)

        if self.progress_callback:
            self.progress_callback("Configuring picker transitions...", 0.9)

        # Start with start position picker visible
        self.picker_stack.setCurrentIndex(0)

        layout.addWidget(self.picker_stack)
        return panel

    def _create_start_position_widget(self) -> QWidget:
        """Create start position picker widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title = QLabel("Select Start Position")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        from ..components.start_position_picker.start_position_picker import (
            StartPositionPicker,
        )

        self.start_position_picker = StartPositionPicker()
        self.start_position_picker.start_position_selected.connect(
            self._handle_start_position_selected
        )
        layout.addWidget(self.start_position_picker)

        return widget

    def _create_option_picker_widget_with_progress(self) -> QWidget:
        """Create option picker widget with progress updates for the heavy initialization"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        try:
            # Create progress callback for ModernOptionPicker's internal initialization
            def option_picker_progress(step: str, progress: float):
                if self.progress_callback:
                    # Map option picker progress (0.0-1.0) to our remaining range
                    mapped_progress = 0.8 + (progress * 0.1)  # 0.8 to 0.9 range
                    self.progress_callback(f"Option picker: {step}", mapped_progress)

            self.option_picker = ModernOptionPicker(
                self.container, progress_callback=option_picker_progress
            )
            self.option_picker.initialize()
            self.option_picker.option_selected.connect(self._handle_option_selected)
            layout.addWidget(self.option_picker.widget)
        except RuntimeError as e:
            print(f"❌ Failed to create option picker: {e}")
            # Create fallback widget
            fallback_label = QLabel("Option picker unavailable")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(fallback_label)
            self.option_picker = None

        return widget

    def _connect_signals(self):
        self.state_service.state_changed.connect(self._on_state_changed)
        self.state_service.option_picker_ready.connect(
            self._transition_to_option_picker
        )
        if self.workbench:
            self.workbench.sequence_modified.connect(self._on_workbench_modified)
            self.workbench.operation_completed.connect(self._on_operation_completed)

    def _handle_start_position_selected(self, position_key: str):
        print(f"✅ Construct tab: Start position selected: {position_key}")

        # Create start position data (separate from sequence like V1)
        start_position_data = self._create_start_position_data(position_key)

        # Set start position in workbench (this does NOT create a sequence)
        if self.workbench:
            self.workbench.set_start_position(start_position_data)

        # Populate option picker with valid combinations
        self._populate_option_picker_from_start_position(
            position_key, start_position_data
        )

        # Transition to option picker view
        self._transition_to_option_picker()

        # Emit signal for external listeners
        self.start_position_set.emit(position_key)

    def _transition_to_option_picker(self):
        """Switch from start position picker to option picker - key fix from v1"""
        print("🔄 Transitioning to option picker view")
        if self.picker_stack:
            self.picker_stack.setCurrentIndex(1)

    def _transition_to_start_position_picker(self):
        """Switch back to start position picker"""
        print("🔄 Transitioning to start position picker view")
        if self.picker_stack:
            self.picker_stack.setCurrentIndex(0)

    def _handle_option_selected(self, option_id: str):
        print(f"✅ Construct tab: Option selected: {option_id}")

        # Get current sequence or create empty one if none exists
        current_sequence = self.workbench.get_sequence() if self.workbench else None
        if current_sequence is None:
            current_sequence = SequenceData.empty()
            print("📝 Created empty sequence for first beat")

        try:
            # Get real beat data from option picker
            real_beat = None
            if self.option_picker and hasattr(
                self.option_picker, "get_beat_data_for_option"
            ):
                # Get beat data from option picker using the actual selected option
                real_beat = self.option_picker.get_beat_data_for_option(option_id)
                if real_beat:
                    print(
                        f"✅ Using actual option data: {real_beat.letter} with motion data"
                    )
                    if real_beat.blue_motion:
                        print(
                            f"   Blue motion: {real_beat.blue_motion.motion_type.value}"
                        )
                    if real_beat.red_motion:
                        print(
                            f"   Red motion: {real_beat.red_motion.motion_type.value}"
                        )
                else:
                    print(f"❌ No beat data found for option: {option_id}")
            else:
                print("❌ Option picker does not have get_beat_data_for_option method")

            if real_beat:
                # Update beat number for sequence position
                new_beat = real_beat.update(
                    beat_number=current_sequence.length + 1,
                    duration=1.0,  # Ensure valid duration
                )
                print(
                    f"📝 Created new beat: {new_beat.letter} (beat #{new_beat.beat_number})"
                )
            else:
                # Only fallback if option picker completely failed
                print("⚠️ Option picker failed, creating placeholder beat")
                new_beat = BeatData.empty().update(
                    beat_number=current_sequence.length + 1,
                    duration=1.0,
                    letter=f"Placeholder{current_sequence.length + 1}",
                    is_blank=False,
                )

            # Add beat to sequence
            updated_beats = current_sequence.beats + [new_beat]
            updated_sequence = current_sequence.update(beats=updated_beats)

            print(f"📊 Sequence updated: {len(updated_beats)} beats")

            # Update workbench
            if self.workbench:
                self.workbench.set_sequence(updated_sequence)
                print("✅ Workbench sequence updated")

            # Emit signal (with protection)
            if not self._emitting_signal:
                try:
                    self._emitting_signal = True
                    self.sequence_modified.emit(updated_sequence)
                    print("📡 Sequence modified signal emitted")
                finally:
                    self._emitting_signal = False
            else:
                print("🔄 Skipping signal emission to prevent circular calls")

        except Exception as e:
            print(f"❌ Error in option selection: {e}")
            import traceback

            traceback.print_exc()

            # Emergency fallback
            try:
                new_beat = BeatData.empty().update(
                    beat_number=current_sequence.length + 1,
                    duration=1.0,
                    letter=f"Error{current_sequence.length + 1}",
                    is_blank=False,
                )
                updated_beats = current_sequence.beats + [new_beat]
                updated_sequence = current_sequence.update(beats=updated_beats)

                if self.workbench:
                    self.workbench.set_sequence(updated_sequence)
                self.sequence_modified.emit(updated_sequence)
                print("🚑 Emergency fallback beat added")

            except Exception as fallback_error:
                print(f"❌ Even emergency fallback failed: {fallback_error}")

    def _create_start_position_data(self, position_key: str) -> BeatData:
        """Create start position data from position key using real dataset (separate from sequence beats)"""
        try:
            from ...application.services.pictograph_dataset_service import (
                PictographDatasetService,
            )

            dataset_service = PictographDatasetService()
            # Get real start position data from dataset
            real_start_position = dataset_service.get_start_position_pictograph(
                position_key, "diamond"
            )

            if real_start_position:
                # Ensure it has proper beat number for start position
                return real_start_position.update(
                    beat_number=1,  # Start position is always beat 1
                    duration=1.0,  # Standard duration
                )
            else:
                print(
                    f"⚠️ No real data found for position {position_key}, using fallback"
                )
                # Fallback to empty beat with position key as letter
                return BeatData.empty().update(
                    letter=position_key,
                    beat_number=1,
                    duration=1.0,
                    is_blank=False,
                )

        except Exception as e:
            print(f"❌ Error loading real start position data: {e}")
            # Fallback to basic beat data
            return BeatData.empty().update(
                letter=position_key,
                beat_number=1,
                duration=1.0,
                is_blank=False,
            )

    def _populate_option_picker_from_start_position(
        self, position_key: str, start_position_data: BeatData
    ):
        """Populate option picker with valid motion combinations based on start position (V1 behavior)"""
        if self.option_picker is None:
            print("❌ Option picker not available, cannot populate")
            return

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
            # Fallback to refresh options if option picker is still available
            if self.option_picker is not None:
                try:
                    self.option_picker.refresh_options()
                    print("⚠️ Using fallback options for option picker")
                except Exception as fallback_error:
                    print(f"❌ Even fallback options failed: {fallback_error}")

    def _create_start_sequence(self, position_key: str) -> SequenceData:
        """Create empty sequence (deprecated - start position should not create sequence)"""
        print("⚠️ _create_start_sequence called - this should not happen in V2")
        return SequenceData.empty()

    def clear_sequence(self):
        """Clear the current sequence and reset to start position picker"""
        if self.workbench:
            self.workbench.set_sequence(SequenceData.empty())

        # Transition back to start position picker
        self._transition_to_start_position_picker()

        print("🗑️ Sequence cleared, returned to start position picker")

    def _on_state_changed(self, new_state):
        print(f"🔄 Construct tab state changed: {new_state}")

    def _on_workbench_modified(self, sequence: SequenceData):
        """Handle workbench sequence modification with circular emission protection"""
        if self._emitting_signal:
            print("🔄 Construct tab: Preventing circular signal emission")
            return

        try:
            self._emitting_signal = True
            print(
                f"📡 Construct tab: Emitting sequence_modified for {sequence.length if sequence else 0} beats"
            )
            self.sequence_modified.emit(sequence)
            print("✅ Construct tab: Signal emitted successfully")
        except Exception as e:
            print(f"❌ Construct tab: Signal emission failed: {e}")
            import traceback

            traceback.print_exc()
        finally:
            self._emitting_signal = False

    def _on_operation_completed(self, message: str):
        print(f"✅ Operation completed: {message}")
