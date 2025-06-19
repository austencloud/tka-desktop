from typing import Optional, TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal
from domain.models.core_models import SequenceData
from core.interfaces.workbench_services import IGraphEditorService

if TYPE_CHECKING:
    from .graph_editor.graph_editor import GraphEditor


class WorkbenchGraphSection(QWidget):
    """Graph editor section component for sequence visualization"""

    # Signals for parent workbench
    beat_modified = pyqtSignal(int, object)
    arrow_selected = pyqtSignal(object)
    visibility_changed = pyqtSignal(bool)

    def __init__(
        self, graph_service: IGraphEditorService, parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self._graph_service = graph_service
        self._graph_editor: Optional["GraphEditor"] = None
        self._current_sequence: Optional[SequenceData] = None
        self._current_beat_index: int = 0  # Track current beat index

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Setup graph editor component with proper layout"""
        from .graph_editor.graph_editor import GraphEditor

        # Create layout for this section
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create graph editor with this section as parent context
        self._graph_editor = GraphEditor(graph_service=self._graph_service, parent=None)

        # Add graph editor to layout
        layout.addWidget(self._graph_editor)

        # Set initial size - important for toggle tab visibility!
        self.setMinimumHeight(60)  # Minimum height for toggle tab visibility
        self.setMaximumHeight(400)  # Reasonable maximum

    def _connect_signals(self):
        """Connect graph editor signals"""
        if self._graph_editor:
            # Connect with adapter methods to handle signature conversion
            self._graph_editor.beat_modified.connect(self._on_beat_modified)
            self._graph_editor.arrow_selected.connect(self._on_arrow_selected)
            self._graph_editor.visibility_changed.connect(self.visibility_changed)

    def _on_beat_modified(self, beat_data):
        """Handle beat modification from graph editor and convert signal signature"""
        # Convert from ModernGraphEditor's beat_modified(BeatData)
        # to parent workbench's expected beat_modified(int, object)
        self.beat_modified.emit(self._current_beat_index, beat_data)

    def _on_arrow_selected(self, arrow_id: str):
        """Handle arrow selection from graph editor and convert signal signature"""
        # Convert from ModernGraphEditor's arrow_selected(str)
        # to parent workbench's expected arrow_selected(object)
        self.arrow_selected.emit(arrow_id)

    def set_sequence(self, sequence: Optional[SequenceData]):
        """Update graph with new sequence"""
        self._current_sequence = sequence
        try:
            self._graph_service.update_graph_display(sequence)
        except Exception as e:
            print(f"⚠️ Graph editor update failed (non-critical): {e}")

    def set_selected_beat(self, beat_index: int):
        """Set the currently selected beat index"""
        self._current_beat_index = beat_index

    def update_toggle_position(self, animate: bool = True):
        """Update graph toggle tab position"""
        if self._graph_editor and hasattr(self._graph_editor, "_toggle_tab"):
            if self._graph_editor._toggle_tab:
                self._graph_editor._toggle_tab.update_position(animate=animate)

    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        if self._graph_editor:
            self._graph_editor.resize(self.size())
            self.update_toggle_position(animate=False)
