from typing import Optional, TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QStackedWidget
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QRect, QEasingCurve
from PyQt6.QtGui import QResizeEvent

from src.core.interfaces.workbench_services import IGraphEditorService
from src.domain.models.core_models import SequenceData, BeatData
from .modern_pictograph_container import ModernPictographContainer
from .modern_adjustment_panel import ModernAdjustmentPanel
from .modern_toggle_tab import ModernToggleTab

if TYPE_CHECKING:
    from ..modern_sequence_workbench import ModernSequenceWorkbench


class ModernGraphEditor(QFrame):
    """Modern graph editor component following v2 architecture patterns"""

    # Signals for communication
    beat_modified = pyqtSignal(BeatData)
    arrow_selected = pyqtSignal(str)  # arrow_id
    visibility_changed = pyqtSignal(bool)  # is_visible

    def __init__(
        self,
        graph_service: IGraphEditorService,
        parent: Optional["ModernSequenceWorkbench"] = None,
    ):
        super().__init__(parent)

        self._graph_service = graph_service
        self._parent_workbench = parent

        # State
        self._is_visible = False
        self._current_sequence: Optional[SequenceData] = None
        self._selected_beat: Optional[BeatData] = None
        self._selected_beat_index: Optional[int] = None
        self._selected_arrow_id: Optional[str] = None

        # Animation system
        self._animations = []

        # Components (will be created in setup)
        self._pictograph_container: Optional[ModernPictographContainer] = None
        self._adjustment_panel: Optional[ModernAdjustmentPanel] = None
        self._toggle_tab: Optional[ModernToggleTab] = None

        self._setup_ui()
        self._setup_animations()
        self._connect_signals()

        # Start hidden like v1
        self.hide()

    def _setup_ui(self):
        """Setup the UI layout matching V1's graph editor structure"""
        self.setFrameStyle(QFrame.Shape.Box)
        self.setFixedHeight(0)  # Start collapsed

        # Main horizontal layout (pictograph + adjustment panels)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(12)

        # Left section: Pictograph container (center-aligned like v1)
        self._pictograph_container = ModernPictographContainer(self)

        # Right section: Adjustment panel with stacked controls
        self._adjustment_panel = ModernAdjustmentPanel(self)

        # Add to layout with proper stretch (pictograph fixed, panels flexible)
        main_layout.addStretch(1)  # Left spacer
        main_layout.addWidget(self._pictograph_container, 0)  # Fixed size pictograph
        main_layout.addStretch(1)  # Center spacer
        main_layout.addWidget(self._adjustment_panel, 2)  # Flexible adjustment panel
        main_layout.addStretch(1)  # Right spacer

        # Toggle tab (positioned absolutely like v1)
        self._toggle_tab = ModernToggleTab(self)

    def _setup_animations(self):
        """Setup animation system for smooth show/hide transitions"""
        self._height_animation = QPropertyAnimation(self, b"maximumHeight")
        self._height_animation.setDuration(300)
        self._height_animation.setEasingCurve(QEasingCurve.Type.OutQuad)

        self._geometry_animation = QPropertyAnimation(self, b"geometry")
        self._geometry_animation.setDuration(300)
        self._geometry_animation.setEasingCurve(QEasingCurve.Type.OutQuad)

    def _connect_signals(self):
        """Connect internal component signals"""
        if self._toggle_tab:
            self._toggle_tab.toggle_requested.connect(self.toggle_visibility)

        if self._pictograph_container:
            self._pictograph_container.arrow_selected.connect(self._on_arrow_selected)

        if self._adjustment_panel:
            self._adjustment_panel.beat_modified.connect(self._on_beat_modified)
            self._adjustment_panel.turn_applied.connect(self._on_turn_applied)
            self._adjustment_panel.orientation_applied.connect(
                self._on_orientation_applied
            )

    # Public API Methods
    def set_sequence(self, sequence: Optional[SequenceData]):
        """Set the current sequence for display/editing"""
        self._current_sequence = sequence
        self._graph_service.update_graph_display(sequence)
        self._update_display()

    def set_selected_beat(
        self, beat_data: Optional[BeatData], beat_index: Optional[int] = None
    ):
        """Set the currently selected beat for editing"""
        self._selected_beat = beat_data
        self._selected_beat_index = beat_index
        self._graph_service.set_selected_beat(beat_data, beat_index)

        # Update pictograph container
        if self._pictograph_container:
            self._pictograph_container.set_beat(beat_data)

        # Update adjustment panel
        if self._adjustment_panel:
            self._adjustment_panel.set_beat(beat_data)

    def toggle_visibility(self):
        """Toggle graph editor visibility with animation"""
        if self._is_visible:
            self._animate_hide()
        else:
            self._animate_show()

    def is_visible(self) -> bool:
        """Check if graph editor is currently visible"""
        return self._is_visible

    def get_preferred_height(self) -> int:
        """Calculate preferred height based on parent size (like v1)"""
        if not self._parent_workbench:
            return 200

        parent_height = self._parent_workbench.height()
        parent_width = self._parent_workbench.width()

        # Use v1's sizing logic: min(height//3.5, width//4)
        return min(int(parent_height // 3.5), parent_width // 4)

    # Animation Methods
    def _animate_show(self):
        """Animate showing the graph editor"""
        if self._is_visible:
            return

        self._is_visible = True
        self.show()

        target_height = self.get_preferred_height()

        # Start from height 0, animate to target height
        self.setMaximumHeight(0)
        self._height_animation.setStartValue(0)
        self._height_animation.setEndValue(target_height)

        # Position at bottom of parent
        if self._parent_workbench:
            parent_rect = self._parent_workbench.rect()
            start_rect = QRect(0, parent_rect.height(), parent_rect.width(), 0)
            end_rect = QRect(
                0,
                parent_rect.height() - target_height,
                parent_rect.width(),
                target_height,
            )

            self._geometry_animation.setStartValue(start_rect)
            self._geometry_animation.setEndValue(end_rect)

        # Start animations
        self._height_animation.start()
        self._geometry_animation.start()

        # Update toggle tab position
        if self._toggle_tab:
            self._toggle_tab.update_position()

        self.visibility_changed.emit(True)

    def _animate_hide(self):
        """Animate hiding the graph editor"""
        if not self._is_visible:
            return

        self._is_visible = False

        current_height = self.height()

        # Animate from current height to 0
        self._height_animation.setStartValue(current_height)
        self._height_animation.setEndValue(0)

        # Position animation
        if self._parent_workbench:
            parent_rect = self._parent_workbench.rect()
            start_rect = self.geometry()
            end_rect = QRect(0, parent_rect.height(), parent_rect.width(), 0)

            self._geometry_animation.setStartValue(start_rect)
            self._geometry_animation.setEndValue(end_rect)

        # Connect hide signal to animation completion
        self._height_animation.finished.connect(self.hide)

        # Start animations
        self._height_animation.start()
        self._geometry_animation.start()

        # Update toggle tab position
        if self._toggle_tab:
            self._toggle_tab.update_position()

        self.visibility_changed.emit(False)

    # Event Handlers
    def _on_arrow_selected(self, arrow_id: str):
        """Handle arrow selection from pictograph container"""
        self._selected_arrow_id = arrow_id
        self._graph_service.set_arrow_selection(arrow_id)
        self.arrow_selected.emit(arrow_id)

        # Update adjustment panel for selected arrow
        if self._adjustment_panel:
            self._adjustment_panel.set_selected_arrow(arrow_id)

    def _on_beat_modified(self, beat_data: BeatData):
        """Handle beat modification from adjustment panel"""
        self._selected_beat = beat_data

        # Apply modifications through service
        updated_beat = self._graph_service.update_beat_adjustments(beat_data)

        # Update pictograph display
        if self._pictograph_container:
            self._pictograph_container.set_beat(updated_beat)

        self.beat_modified.emit(updated_beat)

    def _on_turn_applied(self, arrow_color: str, turn_value: float):
        """Handle turn adjustment application"""
        success = self._graph_service.apply_turn_adjustment(arrow_color, turn_value)
        if success and self._selected_beat:
            self._refresh_display()

    def _on_orientation_applied(self, arrow_color: str, orientation: str):
        """Handle orientation adjustment application"""
        success = self._graph_service.apply_orientation_adjustment(
            arrow_color, orientation
        )
        if success and self._selected_beat:
            self._refresh_display()

    def _update_display(self):
        """Update all display components based on current state"""
        if self._pictograph_container:
            self._pictograph_container.set_beat(self._selected_beat)

        if self._adjustment_panel:
            self._adjustment_panel.set_beat(self._selected_beat)

    def _refresh_display(self):
        """Refresh display after modifications"""
        if self._selected_beat:
            updated_beat = self._graph_service.get_selected_beat()
            if updated_beat:
                self._selected_beat = updated_beat
                self._update_display()

    def resizeEvent(self, event: QResizeEvent):
        """Handle resize events"""
        super().resizeEvent(event)

        if self._is_visible:
            # Update height based on new parent size
            new_height = self.get_preferred_height()
            self.setMaximumHeight(new_height)
            self.setFixedHeight(new_height)

        # Update toggle tab position
        if self._toggle_tab:
            self._toggle_tab.update_position()
