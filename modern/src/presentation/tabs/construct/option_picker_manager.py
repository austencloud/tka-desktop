"""
OptionPickerManager

Manages option picker initialization, population, and option selection for the construct tab.
Responsible for coordinating between the option picker component and sequence management.
"""

from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal
import time

from domain.models.core_models import SequenceData, BeatData
from presentation.components.option_picker.option_picker import OptionPicker
from .data_conversion_service import DataConversionService


class OptionPickerManager(QObject):
    """
    Manages option picker operations and interactions.

    Responsibilities:
    - Handling option picker population from start positions
    - Managing option selection events
    - Refreshing options based on sequence state
    - Converting data formats for option picker compatibility

    Signals:
    - beat_data_selected: Emitted when a beat option is selected
    """

    beat_data_selected = pyqtSignal(object)  # BeatData object

    def __init__(
        self,
        option_picker: Optional[OptionPicker],
        data_conversion_service: DataConversionService,
    ):
        super().__init__()
        self.option_picker = option_picker
        self.data_conversion_service = data_conversion_service

        # Track last refresh to prevent duplicates
        self._last_refresh_sequence_id = None
        self._last_refresh_length = None

        # Connect option picker signals if available
        if self.option_picker:
            self.option_picker.beat_data_selected.connect(
                self._handle_beat_data_selected
            )

    def populate_from_start_position(
        self, position_key: str, start_position_data: BeatData
    ):
        """Populate option picker with valid motion combinations based on start position (Legacy behavior)"""
        if self.option_picker is None:
            print("❌ Option picker not available, cannot populate")
            return

        try:
            print(f"\n🔍 DEBUG: Populating option picker for start position")
            print(f"   Position key: {position_key}")
            print(f"   Start position data: {start_position_data}")

            # Convert start position data to sequence format for motion combination service
            start_position_dict = start_position_data.to_dict()

            # CRITICAL FIX: Ensure end_pos is in the start position data
            extracted_end_pos = (
                self.data_conversion_service.extract_end_position_from_position_key(
                    position_key
                )
            )
            if "end_pos" not in start_position_dict:
                start_position_dict["end_pos"] = extracted_end_pos
                print(
                    f"🔧 Added missing end_pos to start position: {start_position_dict['end_pos']}"
                )

            print(f"   Extracted end position: {extracted_end_pos}")
            print(f"   Complete start position dict: {start_position_dict}")

            sequence_data = [
                {"metadata": "sequence_info"},  # Metadata entry
                start_position_dict,  # Start position entry with end_pos
            ]  # Load motion combinations into option picker

            print(f"   Sequence data being passed to option picker:")
            for i, entry in enumerate(sequence_data):
                print(f"      [{i}]: {entry}")

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

    def refresh_from_sequence(self, sequence: SequenceData):
        """Refresh option picker based on current sequence state - PURE Modern IMPLEMENTATION"""
        if not self.option_picker or not sequence or sequence.length == 0:
            return

        start_time = time.perf_counter()

        try:
            # PURE Modern: Work directly with SequenceData - no conversion needed!
            self.option_picker.refresh_options_from_modern_sequence(sequence)

            total_time = (time.perf_counter() - start_time) * 1000
            print(f"⚡ PURE Modern OPTION REFRESH: {total_time:.1f}ms")
            print(
                f"🔄 Option picker refreshed for sequence with {sequence.length} beats"
            )

        except Exception as e:
            print(f"❌ Error refreshing option picker from sequence: {e}")
            import traceback

            traceback.print_exc()

    def _handle_beat_data_selected(self, beat_data: BeatData):
        """Handle beat data selection from option picker and forward the signal"""
        print(f"✅ Option picker manager: Beat data selected: {beat_data.letter}")
        print(
            f"   Beat data preview: Blue {beat_data.blue_motion.start_loc}→{beat_data.blue_motion.end_loc}, Red {beat_data.red_motion.start_loc}→{beat_data.red_motion.end_loc}"
        )

        # Forward the signal to the main construct tab
        self.beat_data_selected.emit(beat_data)

    def is_available(self) -> bool:
        """Check if option picker is available and functional"""
        return self.option_picker is not None
