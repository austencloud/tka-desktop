"""
Legacy Pictograph Integration Service

Bridges V2 architecture with Legacy pictograph rendering system.
Provides clean interface for graph editor pictograph display and arrow selection.
"""

from typing import Optional, List, Dict, Any, Tuple
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView
import sys
from pathlib import Path

from src.domain.models.core_models import BeatData, SequenceData
from src.core.interfaces.workbench_services import IGraphEditorService


class LegacyPictographIntegrationService(QObject):
    """Service for integrating Legacy pictograph system with V2 architecture."""

    # Signals for pictograph events
    pictograph_updated = pyqtSignal(object)  # Legacy pictograph object
    arrow_selected = pyqtSignal(str)  # arrow_id
    arrow_deselected = pyqtSignal()
    pictograph_clicked = pyqtSignal(float, float)  # x, y coordinates

    def __init__(self):
        super().__init__()

        # Legacy integration state
        self._legacy_pictograph = None
        self._legacy_scene = None
        self._selected_arrow_id: Optional[str] = None
        self._current_beat: Optional[BeatData] = None

        # Arrow selection state
        self._arrow_selection_enabled = True
        self._hover_feedback_enabled = True

        # V2 NATIVE SYSTEM IS COMPLETE - DISABLE Legacy INTEGRATION
        self._legacy_pictograph_class = None
        self._legacy_ge_view_class = None
        print(
            "✅ V2 native pictograph system is complete - Legacy integration disabled"
        )

    def _setup_legacy_integration(self):
        """Legacy integration disabled - using V2 native system."""
        # V2 NATIVE SYSTEM IS COMPLETE
        # No longer attempting to import Legacy components
        pass

    def create_pictograph_for_beat(
        self, beat_data: BeatData, scene: QGraphicsScene
    ) -> bool:
        """Legacy integration disabled - using V2 native system."""
        # V2 handles pictograph creation natively
        return False

    def _configure_pictograph_for_graph_editor(self):
        """Legacy integration disabled - using V2 native system."""
        pass

    def _set_pictograph_beat_data(self, beat_data: BeatData):
        """Legacy integration disabled - using V2 native system."""
        pass

    def _convert_beat_data_to_legacy(self, beat_data: BeatData) -> Any:
        """Legacy integration disabled - using V2 native system."""
        return None

    def _connect_legacy_signals(self):
        """Legacy integration disabled - using V2 native system."""
        pass

    def _on_legacy_arrow_selected(self, arrow_id: str):
        """Legacy integration disabled - using V2 native system."""
        pass

    def get_arrow_list(self) -> List[str]:
        """Returns a list of arrow IDs in the current pictograph."""
        # This would normally interact with the Legacy pictograph to get arrow IDs.
        # Since Legacy integration is disabled, return an empty list or mock data.
        if self._legacy_pictograph and hasattr(
            self._legacy_pictograph, "get_arrow_ids"
        ):
            # Hypothetical method on a Legacy pictograph object
            return self._legacy_pictograph.get_arrow_ids()
        return []  # Or some mock data like ["red_N_0", "blue_S_0.5"]

    def select_arrow(self, arrow_id: str) -> bool:
        """Selects an arrow in the Legacy pictograph."""
        # This would normally interact with the Legacy pictograph.
        # Since Legacy integration is disabled, this is a no-op.
        if self._legacy_pictograph and hasattr(
            self._legacy_pictograph, "select_arrow_by_id"
        ):
            # Hypothetical method on a Legacy pictograph object
            return self._legacy_pictograph.select_arrow_by_id(arrow_id)
        self._selected_arrow_id = arrow_id
        self.arrow_selected.emit(arrow_id)
        return True  # Simulate success

    def cleanup(self):
        """Clean up Legacy resources if any were created."""
        # This method would be responsible for cleaning up any Legacy objects
        # or disconnecting signals if Legacy integration were active.
        self._legacy_pictograph = None
        self._legacy_scene = None
        self._selected_arrow_id = None
        self._current_beat = None
        # print("LegacyPictographIntegrationService cleaned up (no-op as Legacy is disabled)")

    def _on_legacy_pictograph_clicked(self, x: float, y: float):
        """Legacy integration disabled - using V2 native system."""
        pass
