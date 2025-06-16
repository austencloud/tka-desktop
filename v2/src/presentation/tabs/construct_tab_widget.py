from typing import Tuple, Optional, List, Dict, Any
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

from core.dependency_injection.di_container import SimpleContainer
from src.domain.models.core_models import SequenceData, BeatData
from src.presentation.components.option_picker.modern_option_picker import (
    ModernOptionPicker,
)

# StartPositionPicker imported locally in _create_start_position_widget method
from application.services.ui.ui_state_management_service import (
    UIStateManagementService,
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
        self.state_service = UIStateManagementService()

        # Flag to prevent circular signal emissions during clear operations
        self._emitting_signal = False

        # Performance optimization: Cache for position calculations
        self._position_cache = {}
        self._sequence_conversion_cache = {}

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
            # Use only the new precise signal that fixes the pictograph selection bug
            # self.option_picker.option_selected.connect(self._handle_option_selected)  # Disabled - old buggy method
            self.option_picker.beat_data_selected.connect(
                self._handle_beat_data_selected
            )
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
        # TODO: Update signal connections for consolidated UIStateManagementService
        # self.state_service.state_changed.connect(self._on_state_changed)
        # self.state_service.option_picker_ready.connect(
        #     self._transition_to_option_picker
        # )
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
        self._transition_to_option_picker()  # Emit signal for external listeners
        self.start_position_set.emit(position_key)

    def _transition_to_option_picker(self):
        """Switch from start position picker to option picker - key fix from v1"""
        if self.picker_stack:
            self.picker_stack.setCurrentIndex(1)

    def _transition_to_start_position_picker(self):
        """Switch back to start position picker"""
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

    def _handle_beat_data_selected(self, beat_data: BeatData):
        """Handle precise beat data selection (new method that fixes the bug)"""
        print(f"✅ Construct tab: Precise beat data selected: {beat_data.letter}")
        print(
            f"   Beat data preview: Blue {beat_data.blue_motion.start_loc}→{beat_data.blue_motion.end_loc}, Red {beat_data.red_motion.start_loc}→{beat_data.red_motion.end_loc}"
        )

        # Get current sequence or create empty one if none exists
        current_sequence = self.workbench.get_sequence() if self.workbench else None
        if current_sequence is None:
            current_sequence = SequenceData.empty()
            print("📝 Created empty sequence for first beat")

        try:
            # Use the exact beat data that was clicked (this fixes the bug!)
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

            print(
                f"📊 Sequence updated: {len(updated_beats)} beats"
            )  # Update workbench
            if self.workbench:
                self.workbench.set_sequence(updated_sequence)
                print("✅ Workbench sequence updated")
                # Note: Option picker refresh will be triggered by workbench signal

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
            print(f"❌ Error in precise beat data selection: {e}")
            import traceback

            traceback.print_exc()

    def _create_start_position_data(self, position_key: str) -> BeatData:
        """Create start position data from position key using real dataset (separate from sequence beats)"""
        try:
            from ...application.services.old_services_before_consolidation.pictograph_dataset_service import (
                PictographDatasetService,
            )

            dataset_service = PictographDatasetService()
            # Get real start position data from dataset
            real_start_position = dataset_service.get_start_position_pictograph(
                position_key, "diamond"
            )

            if real_start_position:
                # Ensure it has proper beat number for start position AND end_pos for option picker
                beat_data = real_start_position.update(
                    beat_number=1,  # Start position is always beat 1
                    duration=1.0,  # Standard duration
                )

                # CRITICAL FIX: Add end_pos to beat data for option picker
                beat_dict = beat_data.to_dict()
                beat_dict["end_pos"] = self._extract_end_position_from_position_key(
                    position_key
                )

                print(
                    f"🎯 Created start position data with end_pos: {beat_dict['end_pos']}"
                )
                return beat_data
            else:
                print(
                    f"⚠️ No real data found for position {position_key}, using fallback"
                )
                # Fallback to empty beat with position key as letter
                fallback_beat = BeatData.empty().update(
                    letter=position_key,
                    beat_number=1,
                    duration=1.0,
                    is_blank=False,
                )

                # Add end_pos to fallback too
                fallback_dict = fallback_beat.to_dict()
                fallback_dict["end_pos"] = self._extract_end_position_from_position_key(
                    position_key
                )

                return fallback_beat

        except Exception as e:
            print(f"❌ Error loading real start position data: {e}")
            # Fallback to basic beat data
            fallback_beat = BeatData.empty().update(
                letter=position_key,
                beat_number=1,
                duration=1.0,
                is_blank=False,
            )

            # Add end_pos to fallback
            fallback_dict = fallback_beat.to_dict()
            fallback_dict["end_pos"] = self._extract_end_position_from_position_key(
                position_key
            )

            return fallback_beat

    def _extract_end_position_from_position_key(self, position_key: str) -> str:
        """Extract the actual end position from a position key like 'beta5_beta5'"""
        # Position keys are in format "start_end", we want the end part
        if "_" in position_key:
            parts = position_key.split("_")
            if len(parts) == 2:
                return parts[1]  # Return the end position part

        # Fallback: if no underscore, assume it's already the position
        return position_key

    def _get_cached_end_position(self, beat: BeatData) -> str:
        """Get end position with caching to eliminate redundant calculations"""
        # Create cache key from motion data
        blue_end = (
            beat.blue_motion.end_loc.value
            if beat.blue_motion and beat.blue_motion.end_loc
            else "s"
        )
        red_end = (
            beat.red_motion.end_loc.value
            if beat.red_motion and beat.red_motion.end_loc
            else "s"
        )

        cache_key = f"{blue_end}_{red_end}"

        # Check cache first
        if cache_key in self._position_cache:
            return self._position_cache[cache_key]

        # Calculate and cache the result
        position_map = {
            ("n", "n"): "alpha1",
            ("n", "e"): "alpha2",
            ("n", "s"): "alpha3",
            ("n", "w"): "alpha4",
            ("e", "n"): "alpha5",
            ("e", "e"): "alpha6",
            ("e", "s"): "alpha7",
            ("e", "w"): "alpha8",
            ("s", "n"): "beta1",
            ("s", "e"): "beta2",
            ("s", "s"): "beta3",
            ("s", "w"): "beta4",
            ("w", "n"): "beta5",
            ("w", "e"): "beta6",
            ("w", "s"): "beta7",
            ("w", "w"): "beta8",
        }

        end_pos = position_map.get((blue_end, red_end), "beta5")
        self._position_cache[cache_key] = end_pos
        return end_pos

    def _populate_option_picker_from_start_position(
        self, position_key: str, start_position_data: BeatData
    ):
        """Populate option picker with valid motion combinations based on start position (V1 behavior)"""
        if self.option_picker is None:
            print("❌ Option picker not available, cannot populate")
            return

        try:
            # Convert start position data to sequence format for motion combination service
            start_position_dict = start_position_data.to_dict()

            # CRITICAL FIX: Ensure end_pos is in the start position data
            if "end_pos" not in start_position_dict:
                start_position_dict["end_pos"] = (
                    self._extract_end_position_from_position_key(position_key)
                )
                print(
                    f"🔧 Added missing end_pos to start position: {start_position_dict['end_pos']}"
                )

            sequence_data = [
                {"metadata": "sequence_info"},  # Metadata entry
                start_position_dict,  # Start position entry with end_pos
            ]  # Load motion combinations into option picker
            self.option_picker.load_motion_combinations(sequence_data)

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

            # Check if sequence was cleared (empty) and transition back to start position picker
            if sequence is None or sequence.length == 0:
                print(
                    "🗑️ Sequence cleared detected, transitioning to start position picker"
                )
                self._transition_to_start_position_picker()
            else:
                # DYNAMIC OPTION PICKER UPDATE: Refresh options based on sequence state
                self._refresh_option_picker_from_sequence(sequence)

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

    def _refresh_option_picker_from_sequence(self, sequence: SequenceData):
        """Refresh option picker based on current sequence state - PURE V2 IMPLEMENTATION"""
        if not self.option_picker or not sequence or sequence.length == 0:
            return

        import time

        start_time = time.perf_counter()

        try:
            # PURE V2: Work directly with SequenceData - no conversion needed!
            self.option_picker.refresh_options_from_v2_sequence(sequence)

            total_time = (time.perf_counter() - start_time) * 1000
            print(f"⚡ PURE V2 OPTION REFRESH: {total_time:.1f}ms")
            print(
                f"🔄 Option picker refreshed for sequence with {sequence.length} beats"
            )

        except Exception as e:
            print(f"❌ Error refreshing option picker from sequence: {e}")
            import traceback

            traceback.print_exc()

    def _convert_sequence_to_v1_format(
        self, sequence: SequenceData
    ) -> List[Dict[str, Any]]:
        """Convert V2 SequenceData to V1-compatible format for option picker with caching"""
        # Create cache key from sequence hash
        sequence_hash = hash(
            tuple(beat.letter + str(beat.beat_number) for beat in sequence.beats)
        )

        # Check cache first
        if sequence_hash in self._sequence_conversion_cache:
            return self._sequence_conversion_cache[sequence_hash]

        try:
            # Start with metadata entry (V1 format)
            v1_sequence = [{"metadata": "sequence_info"}]

            # Convert each beat to V1 format
            for beat in sequence.beats:
                if beat and not beat.is_blank:
                    beat_dict = beat.to_dict()

                    # Ensure V1-compatible structure
                    if "metadata" not in beat_dict:
                        beat_dict["metadata"] = {}

                    # CRITICAL FIX: Use end_pos from metadata if available, otherwise calculate
                    if "end_pos" not in beat_dict:
                        # First try to get end_pos from beat metadata
                        metadata_end_pos = (
                            beat.metadata.get("end_pos") if beat.metadata else None
                        )

                        if metadata_end_pos:
                            # Use the correct end position from metadata
                            beat_dict["end_pos"] = metadata_end_pos
                            print(
                                f"🎯 Using metadata end_pos: {metadata_end_pos} for beat {beat.letter}"
                            )
                        elif beat.blue_motion and beat.red_motion:
                            # Optimized: Use cached position calculation
                            end_pos = self._get_cached_end_position(beat)
                            beat_dict["end_pos"] = end_pos
                            print(
                                f"🎯 Cached end_pos: {end_pos} for beat {beat.letter} from motion data"
                            )
                        else:
                            # Final fallback
                            beat_dict["end_pos"] = "beta5"
                            print(
                                f"⚠️ Using fallback end_pos: beta5 for beat {beat.letter}"
                            )

                    v1_sequence.append(beat_dict)

            # Cache the result for future use
            self._sequence_conversion_cache[sequence_hash] = v1_sequence

            # Limit cache size to prevent memory issues
            if len(self._sequence_conversion_cache) > 100:
                # Remove oldest entries (simple FIFO)
                oldest_key = next(iter(self._sequence_conversion_cache))
                del self._sequence_conversion_cache[oldest_key]

            return v1_sequence

        except Exception as e:
            print(f"❌ Error converting sequence to V1 format: {e}")
            return [{"metadata": "sequence_info"}]  # Fallback to empty sequence

    def _on_operation_completed(self, message: str):
        print(f"✅ Operation completed: {message}")
