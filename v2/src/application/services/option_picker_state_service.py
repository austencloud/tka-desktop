"""
Option Picker State Service for Kinetic Constructor v2

This service manages the state transitions between start position selection
and the main option picker, replicating v1's workflow.
"""

from typing import Optional, Dict, Any, List
from PyQt6.QtCore import QObject, pyqtSignal
from enum import Enum

from ...domain.models.core_models import BeatData, MotionData


class OptionPickerState(Enum):
    """States for the option picker workflow."""
    
    START_POSITION_SELECTION = "start_position_selection"
    OPTION_PICKER_ACTIVE = "option_picker_active"
    SEQUENCE_BUILDING = "sequence_building"


class OptionPickerStateService(QObject):
    """
    Service that manages the option picker state machine.
    
    Handles transitions:
    1. Initial state: START_POSITION_SELECTION
    2. After start position selected: OPTION_PICKER_ACTIVE
    3. During sequence building: SEQUENCE_BUILDING
    """
    
    # Signals for state transitions
    state_changed = pyqtSignal(str)  # Emits new state
    start_position_set = pyqtSignal(str)  # Emits selected start position
    option_picker_ready = pyqtSignal()  # Option picker should be shown
    
    def __init__(self):
        super().__init__()
        self._current_state = OptionPickerState.START_POSITION_SELECTION
        self._selected_start_position: Optional[str] = None
        self._sequence_data: List[Dict[str, Any]] = []
        
    @property
    def current_state(self) -> OptionPickerState:
        """Get the current state."""
        return self._current_state
    
    @property
    def selected_start_position(self) -> Optional[str]:
        """Get the currently selected start position."""
        return self._selected_start_position
    
    @property
    def sequence_data(self) -> List[Dict[str, Any]]:
        """Get the current sequence data."""
        return self._sequence_data.copy()
    
    def initialize(self) -> None:
        """Initialize the state service."""
        self._transition_to_state(OptionPickerState.START_POSITION_SELECTION)
        print("🎯 Option picker state service initialized - showing start position picker")
    
    def select_start_position(self, position_key: str) -> None:
        """
        Handle start position selection.
        
        Args:
            position_key: The selected position key (e.g., "alpha1_alpha1")
        """
        if self._current_state != OptionPickerState.START_POSITION_SELECTION:
            print(f"⚠️ Cannot select start position in state: {self._current_state}")
            return
            
        self._selected_start_position = position_key
        
        # Create start position entry for sequence
        start_position_data = self._create_start_position_data(position_key)
        self._sequence_data = [{"metadata": "sequence_info"}, start_position_data]
        
        # Transition to option picker
        self._transition_to_state(OptionPickerState.OPTION_PICKER_ACTIVE)
        
        # Emit signals
        self.start_position_set.emit(position_key)
        self.option_picker_ready.emit()
        
        print(f"✅ Start position selected: {position_key}")
        print("🎯 Transitioning to option picker")
    
    def add_beat_to_sequence(self, beat_data: BeatData) -> None:
        """
        Add a beat to the current sequence.
        
        Args:
            beat_data: The beat data to add
        """
        if self._current_state != OptionPickerState.OPTION_PICKER_ACTIVE:
            print(f"⚠️ Cannot add beat in state: {self._current_state}")
            return
            
        # Convert beat data to sequence format
        beat_dict = self._beat_data_to_dict(beat_data)
        self._sequence_data.append(beat_dict)
        
        # Transition to sequence building state
        self._transition_to_state(OptionPickerState.SEQUENCE_BUILDING)
        
        print(f"✅ Beat added to sequence: {beat_data.letter}")
    
    def reset_to_start_position_selection(self) -> None:
        """Reset back to start position selection."""
        self._selected_start_position = None
        self._sequence_data = []
        self._transition_to_state(OptionPickerState.START_POSITION_SELECTION)
        
        print("🔄 Reset to start position selection")
    
    def get_last_beat_data(self) -> Optional[Dict[str, Any]]:
        """Get the last beat in the sequence."""
        if len(self._sequence_data) <= 1:  # Only metadata
            return None
        return self._sequence_data[-1]
    
    def is_ready_for_options(self) -> bool:
        """Check if the system is ready to show options."""
        return (
            self._current_state in [
                OptionPickerState.OPTION_PICKER_ACTIVE,
                OptionPickerState.SEQUENCE_BUILDING
            ] and 
            self._selected_start_position is not None
        )
    
    def _transition_to_state(self, new_state: OptionPickerState) -> None:
        """Transition to a new state."""
        if new_state == self._current_state:
            return
            
        old_state = self._current_state
        self._current_state = new_state
        
        print(f"🔄 State transition: {old_state.value} → {new_state.value}")
        self.state_changed.emit(new_state.value)
    
    def _create_start_position_data(self, position_key: str) -> Dict[str, Any]:
        """
        Create start position data entry for the sequence.
        
        Args:
            position_key: The position key (e.g., "alpha1_alpha1")
            
        Returns:
            Dictionary representing the start position data
        """
        start_pos, end_pos = position_key.split("_")
        
        # Map position keys to basic data
        position_data_map = {
            "alpha1": {
                "letter": "A",
                "blue_start_loc": "n", "blue_end_loc": "n",
                "red_start_loc": "s", "red_end_loc": "s"
            },
            "beta5": {
                "letter": "B", 
                "blue_start_loc": "ne", "blue_end_loc": "ne",
                "red_start_loc": "sw", "red_end_loc": "sw"
            },
            "gamma11": {
                "letter": "Γ",
                "blue_start_loc": "e", "blue_end_loc": "e", 
                "red_start_loc": "w", "red_end_loc": "w"
            },
            "alpha2": {
                "letter": "A",
                "blue_start_loc": "n", "blue_end_loc": "n",
                "red_start_loc": "s", "red_end_loc": "s"
            },
            "beta4": {
                "letter": "B",
                "blue_start_loc": "nw", "blue_end_loc": "nw",
                "red_start_loc": "se", "red_end_loc": "se"
            },
            "gamma12": {
                "letter": "Γ",
                "blue_start_loc": "w", "blue_end_loc": "w",
                "red_start_loc": "e", "red_end_loc": "e"
            }
        }
        
        base_data = position_data_map.get(start_pos, position_data_map["alpha1"])
        
        return {
            "beat": 0,
            "letter": base_data["letter"],
            "end_pos": end_pos,
            "timing": "together",
            "direction": "same",
            "blue_attributes": {
                "start_loc": base_data["blue_start_loc"],
                "end_loc": base_data["blue_end_loc"],
                "start_ori": "in",
                "end_ori": "in",
                "prop_rot_dir": "no_rot",
                "turns": 0,
                "motion_type": "static"
            },
            "red_attributes": {
                "start_loc": base_data["red_start_loc"],
                "end_loc": base_data["red_end_loc"],
                "start_ori": "in", 
                "end_ori": "in",
                "prop_rot_dir": "no_rot",
                "turns": 0,
                "motion_type": "static"
            }
        }
    
    def _beat_data_to_dict(self, beat_data: BeatData) -> Dict[str, Any]:
        """
        Convert BeatData to dictionary format for sequence storage.
        
        Args:
            beat_data: The beat data to convert
            
        Returns:
            Dictionary representation of the beat
        """
        return {
            "beat": beat_data.beat_number,
            "letter": beat_data.letter,
            "duration": beat_data.duration,
            "blue_attributes": {
                "start_loc": beat_data.blue_motion.start_loc.value if beat_data.blue_motion else "n",
                "end_loc": beat_data.blue_motion.end_loc.value if beat_data.blue_motion else "n",
                "start_ori": beat_data.blue_motion.start_ori if beat_data.blue_motion else "in",
                "end_ori": beat_data.blue_motion.end_ori if beat_data.blue_motion else "in",
                "prop_rot_dir": beat_data.blue_motion.prop_rot_dir.value if beat_data.blue_motion else "no_rot",
                "turns": beat_data.blue_motion.turns if beat_data.blue_motion else 0,
                "motion_type": beat_data.blue_motion.motion_type.value if beat_data.blue_motion else "static"
            },
            "red_attributes": {
                "start_loc": beat_data.red_motion.start_loc.value if beat_data.red_motion else "s",
                "end_loc": beat_data.red_motion.end_loc.value if beat_data.red_motion else "s",
                "start_ori": beat_data.red_motion.start_ori if beat_data.red_motion else "in",
                "end_ori": beat_data.red_motion.end_ori if beat_data.red_motion else "in",
                "prop_rot_dir": beat_data.red_motion.prop_rot_dir.value if beat_data.red_motion else "no_rot",
                "turns": beat_data.red_motion.turns if beat_data.red_motion else 0,
                "motion_type": beat_data.red_motion.motion_type.value if beat_data.red_motion else "static"
            }
        }
