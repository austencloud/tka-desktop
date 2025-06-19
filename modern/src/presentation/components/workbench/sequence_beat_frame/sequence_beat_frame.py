"""
Modern Beat Frame Component for Modern Sequence Workbench

This component provides the core beat grid system with dynamic layout,
replacing Legacy's SequenceBeatFrame with modern architecture patterns.
"""

from typing import Optional, List, Dict, TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QScrollArea,
    QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal

from domain.models.core_models import SequenceData, BeatData
from core.interfaces.core_services import ILayoutService
from application.services.layout.beat_resizer_service import (
    BeatResizerService,
)
from .beat_view import BeatView
from .start_position_view import StartPositionView
from .beat_selection_manager import BeatSelectionManager

# Event-driven architecture imports
if TYPE_CHECKING:
    from core.events import IEventBus

try:
    from core.events import (
        get_event_bus,
        SequenceCreatedEvent,
        BeatAddedEvent,
        BeatRemovedEvent,
        BeatUpdatedEvent,
        LayoutRecalculatedEvent,
        EventPriority,
    )

    EVENT_SYSTEM_AVAILABLE = True
except ImportError:
    # For tests or when event system is not available
    get_event_bus = None
    EVENT_SYSTEM_AVAILABLE = False


class SequenceBeatFrame(QScrollArea):
    """
    Modern beat frame with dynamic grid layout and Modern architecture patterns.

    Replaces Legacy's SequenceBeatFrame with:
    - Dependency injection instead of global state
    - Immutable sequence data
    - Service-based layout calculations
    - Modern PyQt6 patterns
    """

    # Signals for communication
    beat_selected = pyqtSignal(int)  # beat_index
    beat_modified = pyqtSignal(int, object)  # beat_index, BeatData object
    sequence_modified = pyqtSignal(object)  # SequenceData object
    layout_changed = pyqtSignal(int, int)  # rows, columns

    def __init__(
        self,
        layout_service: ILayoutService,
        event_bus: Optional["IEventBus"] = None,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)  # Injected dependencies
        self._layout_service = layout_service
        self._resizer_service = BeatResizerService()

        # Event system integration
        self.event_bus = event_bus or (
            get_event_bus() if EVENT_SYSTEM_AVAILABLE else None
        )
        self._subscription_ids: List[str] = []

        # Current state
        self._current_sequence: Optional[SequenceData] = None
        self._beat_views: List[BeatView] = []
        self._current_layout: Dict[str, int] = {"rows": 1, "columns": 8}

        # UI components (will be initialized in _setup_ui)
        self._container_widget: QWidget
        self._grid_layout: QGridLayout
        self._start_position_view: StartPositionView
        self._selection_manager: BeatSelectionManager

        self._setup_ui()
        self._setup_styling()
        self._setup_event_subscriptions()

    def _setup_ui(self):
        """Setup the UI layout to match legacy exactly"""
        # Configure scroll area
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setFrameStyle(QFrame.Shape.NoFrame)

        # Create container widget
        self._container_widget = QWidget()
        self.setWidget(self._container_widget)

        # Create grid layout directly like legacy - no header section or info labels
        self._grid_layout = QGridLayout(self._container_widget)
        self._grid_layout.setSpacing(0)  # Zero spacing like legacy
        self._grid_layout.setContentsMargins(0, 0, 0, 0)  # Zero margins like legacy
        self._grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Initialize beat views (pre-allocate for performance)
        self._initialize_beat_views()

        # Create selection manager
        self._selection_manager = BeatSelectionManager(self._container_widget)
        self._selection_manager.selection_changed.connect(self._on_selection_changed)

        # Setup start position view
        self._setup_start_position()

    def _setup_styling(self):
        """Apply modern styling to the beat frame"""
        self.setStyleSheet(
            """
            QScrollArea {
                background: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
        """
        )

    def _initialize_beat_views(self):
        """Pre-allocate beat views for performance (Legacy pattern but optimized)"""
        # Create 64 beat views (maximum sequence length)
        for i in range(64):
            beat_view = BeatView(beat_number=i + 1, parent=self._container_widget)
            beat_view.beat_clicked.connect(lambda idx=i: self._on_beat_clicked(idx))
            beat_view.beat_modified.connect(
                lambda data, idx=i: self._on_beat_modified(idx, data)
            )
            beat_view.hide()  # Initially hidden
            self._beat_views.append(beat_view)

    def _setup_start_position(self):
        """Setup start position view"""
        self._start_position_view = StartPositionView(parent=self._container_widget)
        self._start_position_view.position_clicked.connect(
            self._on_start_position_clicked
        )

        # Add to grid at (0, 0)
        self._grid_layout.addWidget(self._start_position_view, 0, 0, 1, 1)

    def _setup_event_subscriptions(self):
        """Setup event subscriptions for reactive UI updates."""
        if not self.event_bus or not EVENT_SYSTEM_AVAILABLE:
            return

        # Subscribe to sequence events
        sub_id = self.event_bus.subscribe(
            "sequence.created", self._on_sequence_created, priority=EventPriority.NORMAL
        )
        self._subscription_ids.append(sub_id)

        sub_id = self.event_bus.subscribe(
            "sequence.beat_added", self._on_beat_added, priority=EventPriority.NORMAL
        )
        self._subscription_ids.append(sub_id)

        sub_id = self.event_bus.subscribe(
            "sequence.beat_removed",
            self._on_beat_removed,
            priority=EventPriority.NORMAL,
        )
        self._subscription_ids.append(sub_id)

        sub_id = self.event_bus.subscribe(
            "sequence.beat_updated",
            self._on_beat_updated,
            priority=EventPriority.NORMAL,
        )
        self._subscription_ids.append(sub_id)

        # Subscribe to layout events
        sub_id = self.event_bus.subscribe(
            "layout.beat_frame_recalculated",
            self._on_layout_recalculated,
            priority=EventPriority.NORMAL,
        )
        self._subscription_ids.append(sub_id)

    def cleanup(self):
        """Clean up event subscriptions when component is destroyed."""
        if self.event_bus:
            for sub_id in self._subscription_ids:
                self.event_bus.unsubscribe(sub_id)
            self._subscription_ids.clear()

    # Public API methods
    def set_sequence(self, sequence: Optional[SequenceData]):
        """Set the current sequence and update display"""
        self._current_sequence = sequence
        self._update_layout()
        self._update_display()

    def get_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence"""
        return self._current_sequence

    def set_start_position(self, start_position_data: BeatData):
        """Set the start position data (separate from sequence beats like legacy)"""
        if self._start_position_view:
            self._start_position_view.set_position_data(start_position_data)

    def get_selected_beat_index(self) -> Optional[int]:
        """Get the currently selected beat index"""
        return (
            self._selection_manager.get_selected_index()
            if self._selection_manager
            else None
        )

    def select_beat(self, beat_index: int):
        """Programmatically select a beat"""
        if self._selection_manager and 0 <= beat_index < len(self._beat_views):
            self._selection_manager.select_beat(beat_index)

    def clear_selection(self):
        """Clear beat selection"""
        if self._selection_manager:
            self._selection_manager.clear_selection()

    # Layout management    def _update_layout(self):
    def _update_layout(self):
        """Update grid layout based on sequence length"""
        if not self._current_sequence:
            self._apply_layout(1, 8)  # Default layout
            return  # Calculate optimal layout using service

        # Special case: empty sequence should still show start position with minimal layout
        if self._current_sequence.length == 0:
            self._apply_layout(1, 1)  # 1 row, 1 column for start position only
            return

        container_size = (self.width(), self.height())
        layout_config = self._layout_service.calculate_beat_frame_layout(
            self._current_sequence, container_size
        )

        rows = layout_config.get("rows", 1)
        columns = layout_config.get(
            "columns", min(8, len(self._current_sequence.beats))
        )
        self._apply_layout(rows, columns)

    def _apply_layout(self, rows: int, columns: int):
        """Apply the specified grid layout like legacy"""
        # Clear existing layout (except start position)
        for i in range(len(self._beat_views)):
            self._grid_layout.removeWidget(self._beat_views[i])
            self._beat_views[i].hide()

        # Update layout info (no label in legacy)
        self._current_layout = {"rows": rows, "columns": columns}

        # Add beats to new layout
        beat_count = self._current_sequence.length if self._current_sequence else 0

        # Only add beat views if there are beats and columns > 0
        if beat_count > 0 and columns > 0:
            for i in range(min(beat_count, len(self._beat_views))):
                row = i // columns
                col = (i % columns) + 1  # +1 to account for start position

                beat_view = self._beat_views[i]
                self._grid_layout.addWidget(beat_view, row, col, 1, 1)
                beat_view.show()

        # CRITICAL: Apply Legacy's beat sizing after layout change
        # Ensure we have at least 1 column for resizing calculations
        resize_columns = max(columns, 1)
        self._resizer_service.resize_beat_frame(self, rows, resize_columns)

        # Emit layout changed signal
        self.layout_changed.emit(rows, columns)

    def _update_display(self):
        """Update all display elements like legacy (no info labels)"""
        # Always ensure start position is visible at (0,0) - Legacy behavior
        if self._start_position_view:
            self._start_position_view.show()

        if not self._current_sequence:
            # No sequence beats to display, but start position remains visible
            # Hide beat numbers on all beat views when no sequence
            for beat_view in self._beat_views:
                beat_view.set_beat_number_visible(False)
            return

        # Update beat views with sequence data
        for i, beat_data in enumerate(self._current_sequence.beats):
            if i < len(self._beat_views):
                beat_view = self._beat_views[i]
                beat_view.set_beat_data(beat_data)

                # Enable beat number overlay for sequence beats (like Legacy)
                beat_view.set_beat_number_visible(True)

        # Start position is always separate from sequence beats (Legacy behavior)
        # Start position data is managed independently via set_start_position()
        # Start position always shows START text overlay (handled in StartPositionView)

    # Event handlers
    def _on_beat_clicked(self, beat_index: int):
        """Handle beat click events"""
        if self._selection_manager:
            self._selection_manager.select_beat(beat_index)

    def _on_beat_modified(self, beat_index: int, beat_data: BeatData):
        """Handle beat modification events"""
        if not self._current_sequence or beat_index >= len(
            self._current_sequence.beats
        ):
            return

        # Create new sequence with modified beat (immutable pattern)
        new_beats = list(self._current_sequence.beats)
        new_beats[beat_index] = beat_data

        new_sequence = self._current_sequence.update(beats=new_beats)

        self._current_sequence = new_sequence
        self.beat_modified.emit(beat_index, beat_data)
        self.sequence_modified.emit(new_sequence)

    def _on_selection_changed(self, beat_index: Optional[int]):
        """Handle selection change events"""
        if beat_index is not None:
            self.beat_selected.emit(beat_index)

    def _on_start_position_clicked(self):
        """Handle start position click events"""
        # Clear beat selection when start position is clicked
        self.clear_selection()  # Responsive design

    def resizeEvent(self, event):
        """Handle resize events with Legacy's complete resizing logic"""
        super().resizeEvent(event)

        # Recalculate layout if needed for new size
        if self._current_sequence and self._layout_service:
            container_size = (event.size().width(), event.size().height())
            new_layout = self._layout_service.calculate_beat_frame_layout(
                self._current_sequence, container_size
            )

            current_layout = self._current_layout
            layout_changed = (
                new_layout["rows"] != current_layout["rows"]
                or new_layout["columns"] != current_layout["columns"]
            )

            if layout_changed:
                self._apply_layout(new_layout["rows"], new_layout["columns"])

            # CRITICAL: Always resize beats using Legacy's exact sizing logic
            # This was missing in Modern - causing beats to be 1/8 or 1/9 instead of 1/6!
            self._resizer_service.resize_beat_frame(
                self, new_layout["rows"], new_layout["columns"]
            )

    # Event handlers for domain events
    def _on_sequence_created(self, event: SequenceCreatedEvent):
        """Handle sequence created event by updating display."""
        # Note: We don't automatically load the sequence here since the UI
        # should explicitly call set_sequence() when ready
        pass

    def _on_beat_added(self, event: BeatAddedEvent):
        """Handle beat added event by refreshing layout if this is our sequence."""
        if (
            self._current_sequence
            and hasattr(event, "sequence_id")
            and self._current_sequence.id == event.sequence_id
        ):
            # Refresh layout to accommodate new beat
            self._update_layout()
            self._update_display()

    def _on_beat_removed(self, event: BeatRemovedEvent):
        """Handle beat removed event by refreshing layout if this is our sequence."""
        if (
            self._current_sequence
            and hasattr(event, "sequence_id")
            and self._current_sequence.id == event.sequence_id
        ):
            # Refresh layout to accommodate removed beat
            self._update_layout()
            self._update_display()

    def _on_beat_updated(self, event: BeatUpdatedEvent):
        """Handle beat updated event by refreshing display if this is our sequence."""
        if (
            self._current_sequence
            and hasattr(event, "sequence_id")
            and self._current_sequence.id == event.sequence_id
        ):
            # Refresh display to show updated beat
            self._update_display()

    def _on_layout_recalculated(self, event: LayoutRecalculatedEvent):
        """Handle layout recalculated event by applying new layout."""
        if (
            hasattr(event, "layout_type")
            and event.layout_type == "beat_frame"
            and hasattr(event, "layout_data")
        ):
            layout_data = event.layout_data
            if "rows" in layout_data and "columns" in layout_data:
                self._apply_layout(layout_data["rows"], layout_data["columns"])
