from typing import Protocol, Optional, List
from domain.models.core_models import SequenceData, BeatData
from domain.models.sequence_operations import (
    ColorSwapOperation,
    ReflectionOperation,
    RotationOperation,
)


class ISequenceWorkbenchService(Protocol):
    """Interface for sequence workbench operations"""

    def swap_colors(self, sequence: SequenceData) -> SequenceData:
        """Swap colors in sequence"""
        ...

    def reflect_sequence(self, sequence: SequenceData) -> SequenceData:
        """Reflect sequence vertically"""
        ...

    def rotate_sequence(self, sequence: SequenceData) -> SequenceData:
        """Rotate sequence"""
        ...

    def clear_sequence(self) -> SequenceData:
        """Clear sequence to start position only"""
        ...

    def export_sequence_json(self, sequence: SequenceData) -> str:
        """Export sequence as JSON string"""
        ...


class IFullScreenService(Protocol):
    """Interface for full screen viewing functionality"""

    def create_sequence_thumbnail(self, sequence: SequenceData) -> bytes:
        """Create thumbnail from sequence"""
        ...

    def show_full_screen_view(self, sequence: SequenceData) -> None:
        """Show sequence in full screen overlay"""
        ...


class IBeatDeletionService(Protocol):
    """Interface for beat deletion operations"""

    def delete_beat(self, sequence: SequenceData, beat_index: int) -> SequenceData:
        """Delete specific beat from sequence"""
        ...

    def delete_all_beats(self, sequence: SequenceData) -> SequenceData:
        """Delete all beats except start position"""
        ...

    def delete_first_beat(self, sequence: SequenceData) -> SequenceData:
        """Delete first beat after start position"""
        ...


class IGraphEditorService(Protocol):
    """Interface for graph editor service operations"""

    def update_graph_display(self, sequence: Optional[SequenceData]) -> None:
        """Update the graph editor display with sequence data"""
        ...

    def toggle_graph_visibility(self) -> bool:
        """Toggle graph editor visibility, return new visibility state"""
        ...

    def set_selected_beat(
        self, beat_data: Optional[BeatData], beat_index: Optional[int] = None
    ) -> None:
        """Set the currently selected beat for editing"""
        ...

    def get_selected_beat(self) -> Optional[BeatData]:
        """Get the currently selected beat"""
        ...

    def update_beat_adjustments(self, beat_data: BeatData) -> BeatData:
        """Apply adjustment panel modifications to beat data"""
        ...

    def is_visible(self) -> bool:
        """Check if graph editor is currently visible"""
        ...

    def set_arrow_selection(self, arrow_id: Optional[str]) -> None:
        """Set selected arrow for detailed editing"""
        ...

    def get_available_turns(self, arrow_color: str) -> List[float]:
        """Get available turn values for specified arrow color"""
        ...

    def get_available_orientations(self, arrow_color: str) -> List[str]:
        """Get available orientations for specified arrow color"""
        ...

    def apply_turn_adjustment(self, arrow_color: str, turn_value: float) -> bool:
        """Apply turn adjustment to selected arrow"""
        ...

    def apply_orientation_adjustment(self, arrow_color: str, orientation: str) -> bool:
        """Apply orientation adjustment to selected arrow"""
        ...


class IDictionaryService(Protocol):
    """Interface for dictionary management"""

    def add_sequence_to_dictionary(self, sequence: SequenceData, word: str) -> bool:
        """Add sequence to dictionary"""
        ...

    def get_word_for_sequence(self, sequence: SequenceData) -> Optional[str]:
        """Get word associated with sequence"""
        ...

    def calculate_difficulty(self, sequence: SequenceData) -> int:
        """Calculate sequence difficulty level"""
        ...
