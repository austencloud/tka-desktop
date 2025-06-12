from typing import Protocol, Optional
from ...domain.models.core_models import SequenceData
from ...domain.models.sequence_operations import (
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
    """Interface for graph editor functionality"""

    def update_graph_display(self, sequence: SequenceData) -> None:
        """Update graph editor display"""
        ...

    def toggle_graph_visibility(self) -> bool:
        """Toggle graph editor visibility"""
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
