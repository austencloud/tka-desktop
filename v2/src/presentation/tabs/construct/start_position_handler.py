"""
StartPositionHandler

Manages start position selection, data creation, and related operations for the construct tab.
Responsible for handling start position picker interactions and creating start position data.
"""

from typing import Optional, Callable
from PyQt6.QtCore import QObject, pyqtSignal

from domain.models.core_models import BeatData
from .data_conversion_service import DataConversionService


class StartPositionHandler(QObject):
    """
    Handles start position selection and data creation.
    
    Responsibilities:
    - Processing start position selection events
    - Creating start position data from position keys
    - Managing start position to option picker transitions
    - Integrating with the pictograph dataset service
    
    Signals:
    - start_position_created: Emitted when start position data is created
    - transition_requested: Emitted when transition to option picker is needed
    """
    
    start_position_created = pyqtSignal(str, object)  # position_key, BeatData
    transition_requested = pyqtSignal()  # Request transition to option picker
    
    def __init__(
        self,
        data_conversion_service: DataConversionService,
        workbench_setter: Optional[Callable[[BeatData], None]] = None
    ):
        super().__init__()
        self.data_conversion_service = data_conversion_service
        self.workbench_setter = workbench_setter
    
    def handle_start_position_selected(self, position_key: str):
        """Handle start position selection from the picker"""
        print(f"✅ Start position handler: Position selected: {position_key}")

        # Create start position data (separate from sequence like Legacy)
        start_position_data = self._create_start_position_data(position_key)

        # Set start position in workbench (this does NOT create a sequence)
        if self.workbench_setter:
            self.workbench_setter(start_position_data)

        # Emit signal with the created data
        self.start_position_created.emit(position_key, start_position_data)
        
        # Request transition to option picker
        self.transition_requested.emit()

    def _create_start_position_data(self, position_key: str) -> BeatData:
        """Create start position data from position key using real dataset (separate from sequence beats)"""
        try:
            from application.services.data.pictograph_dataset_service import (
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
                beat_dict["end_pos"] = self.data_conversion_service.extract_end_position_from_position_key(
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
                fallback_dict["end_pos"] = self.data_conversion_service.extract_end_position_from_position_key(
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
            fallback_dict["end_pos"] = self.data_conversion_service.extract_end_position_from_position_key(
                position_key
            )

            return fallback_beat
