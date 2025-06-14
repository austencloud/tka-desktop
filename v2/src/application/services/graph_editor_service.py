from typing import Optional, List, Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal

from ...core.interfaces.workbench_services import IGraphEditorService
from domain.models.core_models import SequenceData, BeatData
from .v1_pictograph_integration_service import V1PictographIntegrationService


class GraphEditorService(QObject):
    """Modern graph editor service implementing v2 architecture patterns with V1 integration"""

    # Signals for state changes
    graph_updated = pyqtSignal(SequenceData)
    beat_selected = pyqtSignal(BeatData, int)
    arrow_selected = pyqtSignal(str)
    visibility_changed = pyqtSignal(bool)
    pictograph_ready = pyqtSignal(object)  # V1 pictograph object

    def __init__(self):
        super().__init__()

        # Current state
        self._current_sequence: Optional[SequenceData] = None
        self._selected_beat: Optional[BeatData] = None
        self._selected_beat_index: Optional[int] = None
        self._selected_arrow_id: Optional[str] = None
        self._is_visible = False

        # Arrow state cache for adjustments
        self._arrow_states: Dict[str, Dict[str, Any]] = {}

        # V1 integration service
        self._v1_integration = V1PictographIntegrationService()
        self._connect_v1_signals()

    def update_graph_display(self, sequence: Optional[SequenceData]) -> None:
        """Update the graph editor display with sequence data"""
        self._current_sequence = sequence

        # Reset selections when sequence changes
        if sequence != self._current_sequence:
            self._selected_beat = None
            self._selected_beat_index = None
            self._selected_arrow_id = None
            self._arrow_states.clear()

        if sequence:
            self.graph_updated.emit(sequence)

    def toggle_graph_visibility(self) -> bool:
        """Toggle graph editor visibility, return new visibility state"""
        self._is_visible = not self._is_visible
        self.visibility_changed.emit(self._is_visible)
        return self._is_visible

    def set_selected_beat(
        self, beat_data: Optional[BeatData], beat_index: Optional[int] = None
    ) -> None:
        """Set the currently selected beat for editing"""
        self._selected_beat = beat_data
        self._selected_beat_index = beat_index

        # Reset arrow selection when beat changes
        self._selected_arrow_id = None

        # Update arrow states cache for this beat
        if beat_data:
            self._update_arrow_states_cache(beat_data)
            self.beat_selected.emit(beat_data, beat_index or -1)

    def get_selected_beat(self) -> Optional[BeatData]:
        """Get the currently selected beat"""
        return self._selected_beat

    def _connect_v1_signals(self):
        """Connect V1 integration service signals."""
        self._v1_integration.pictograph_updated.connect(self.pictograph_ready.emit)
        self._v1_integration.arrow_selected.connect(self._on_v1_arrow_selected)
        self._v1_integration.arrow_deselected.connect(self._on_v1_arrow_deselected)

    def _on_v1_arrow_selected(self, arrow_id: str):
        """Handle arrow selection from V1 pictograph."""
        self._selected_arrow_id = arrow_id
        self.arrow_selected.emit(arrow_id)

    def _on_v1_arrow_deselected(self):
        """Handle arrow deselection from V1 pictograph."""
        self._selected_arrow_id = None

    def create_pictograph_for_beat(self, beat_data: BeatData, scene) -> bool:
        """Create V1 pictograph for the given beat in the provided scene."""
        return self._v1_integration.create_pictograph_for_beat(beat_data, scene)

    def update_beat_adjustments(self, beat_data: BeatData) -> BeatData:
        """Apply adjustment panel modifications to beat data"""
        # Update V1 pictograph with new beat data
        if hasattr(self, "_current_scene") and self._current_scene:
            self._v1_integration.create_pictograph_for_beat(
                beat_data, self._current_scene
            )

        self._selected_beat = beat_data
        return beat_data

    def is_visible(self) -> bool:
        """Check if graph editor is currently visible"""
        return self._is_visible

    def set_arrow_selection(self, arrow_id: Optional[str]) -> None:
        """Set selected arrow for detailed editing"""
        self._selected_arrow_id = arrow_id
        if arrow_id:
            self.arrow_selected.emit(arrow_id)

    def get_available_turns(self, arrow_color: str) -> List[float]:
        """Get available turn values for specified arrow color"""
        # Standard turn values from v1 (0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0)
        return [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

    def get_available_orientations(self, arrow_color: str) -> List[str]:
        """Get available orientations for specified arrow color"""
        # Standard orientations from v1
        return ["in", "out", "clock", "counter"]

    def apply_turn_adjustment(self, arrow_color: str, turn_value: float) -> bool:
        """Apply turn adjustment to selected arrow"""
        if not self._selected_beat or not self._selected_arrow_id:
            return False

        # Update arrow state cache
        if self._selected_arrow_id not in self._arrow_states:
            self._arrow_states[self._selected_arrow_id] = {}

        self._arrow_states[self._selected_arrow_id]["turns"] = turn_value

        # This would integrate with v1's arrow modification logic
        # For now, just cache the change (to be implemented with v1 integration)
        return True

    def apply_orientation_adjustment(self, arrow_color: str, orientation: str) -> bool:
        """Apply orientation adjustment to selected arrow"""
        if not self._selected_beat or not self._selected_arrow_id:
            return False

        # Update arrow state cache
        if self._selected_arrow_id not in self._arrow_states:
            self._arrow_states[self._selected_arrow_id] = {}

        self._arrow_states[self._selected_arrow_id]["orientation"] = orientation

        # This would integrate with v1's arrow modification logic
        # For now, just cache the change (to be implemented with v1 integration)
        return True

    def _update_arrow_states_cache(self, beat_data: BeatData):
        """Update internal cache of arrow states from beat data"""
        # This would extract arrow information from beat data
        # Implementation depends on v1 data structure integration
        pass

    # Additional methods for v1 integration
    def get_arrow_state(self, arrow_id: str) -> Dict[str, Any]:
        """Get current state of a specific arrow"""
        return self._arrow_states.get(arrow_id, {})

    def clear_arrow_selection(self):
        """Clear current arrow selection"""
        self._selected_arrow_id = None

    def has_unsaved_changes(self) -> bool:
        """Check if there are unsaved changes in the graph editor"""
        return len(self._arrow_states) > 0

    def apply_all_changes(self) -> Optional[BeatData]:
        """Apply all cached changes to the current beat"""
        if not self._selected_beat:
            return None

        # This would apply all cached arrow state changes to the beat
        # Implementation depends on v1 data structure integration
        modified_beat = self._selected_beat  # Placeholder

        # Clear cache after applying
        self._arrow_states.clear()

        return modified_beat
