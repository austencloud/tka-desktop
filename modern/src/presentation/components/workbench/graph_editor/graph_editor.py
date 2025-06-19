from typing import Optional, TYPE_CHECKING
from PyQt6.QtWidgets import QHBoxLayout, QFrame
from PyQt6.QtCore import pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer, Qt
from PyQt6.QtGui import QResizeEvent, QKeyEvent

from core.interfaces.workbench_services import IGraphEditorService
from domain.models.core_models import SequenceData, BeatData
from .pictograph_container import GraphEditorPictographContainer
from .adjustment_panel import AdjustmentPanel
from .modern_toggle_tab import ModernToggleTab

if TYPE_CHECKING:
    from presentation.components.workbench.workbench import (
        ModernSequenceWorkbench,
    )


class GraphEditor(QFrame):
    """Modern graph editor component following modern architecture patterns"""

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
        self._pictograph_container: Optional[GraphEditorPictographContainer] = None
        self._adjustment_panel: Optional[AdjustmentPanel] = None
        self._toggle_tab: Optional[ModernToggleTab] = None

        self._setup_ui()
        self._setup_animations()
        self._connect_signals()

        # Start hidden like legacy
        self.hide()

    def _setup_ui(self):
        """Setup the frosted glass sliding panel UI"""
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setFixedHeight(0)  # Start collapsed

        # Enable focus for hotkey handling
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Frosted glass styling with better containment (Qt-compatible)
        self.setStyleSheet(
            """
            ModernGraphEditor {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(255, 255, 255, 0.15),
                    stop: 0.5 rgba(255, 255, 255, 0.10),
                    stop: 1 rgba(255, 255, 255, 0.05)
                );
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 16px 16px 0px 0px;
            }
        """
        )

        # Main horizontal layout matching Legacy's structure exactly
        main_layout = QHBoxLayout(self)
        # Increase margins to ensure content stays within rounded borders
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # Left adjustment controls (stretch=1, like Legacy's left_stack)
        self._left_adjustment_panel = AdjustmentPanel(self, side="left")

        # Central pictograph container (stretch=0, fixed size like Legacy)
        self._pictograph_container = GraphEditorPictographContainer(self)

        # Right adjustment controls (stretch=1, like Legacy's right_stack)
        self._right_adjustment_panel = AdjustmentPanel(self, side="right")

        # Add to layout with Legacy's exact proportions
        main_layout.addWidget(
            self._left_adjustment_panel, 1
        )  # Left controls (stretch=1)
        main_layout.addWidget(
            self._pictograph_container, 0
        )  # Pictograph (stretch=0, fixed)
        main_layout.addWidget(
            self._right_adjustment_panel, 1
        )  # Right controls (stretch=1)

        # Keep reference to both panels for compatibility
        self._adjustment_panel = (
            self._right_adjustment_panel
        )  # Toggle tab (positioned absolutely)
        self._toggle_tab = ModernToggleTab(self)

        # Ensure toggle tab is visible immediately
        self._toggle_tab.show()
        self._toggle_tab.raise_()

        # Set size policy to prevent unwanted expansion beyond allocated space
        from PyQt6.QtWidgets import QSizePolicy

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def _setup_animations(self):
        """Setup smooth sliding animation system"""
        # Single height animation for clean sliding effect
        self._height_animation = QPropertyAnimation(self, b"maximumHeight")
        self._height_animation.setDuration(400)  # Slightly longer for smoother feel
        self._height_animation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )  # Smoother easing

        # Connect animation events
        self._height_animation.finished.connect(self._on_animation_finished)

        # Track animation state
        self._animating = False

    def _connect_signals(self):
        """Connect internal component signals"""
        if self._toggle_tab:
            self._toggle_tab.toggle_requested.connect(self.toggle_visibility)

        if self._pictograph_container:
            self._pictograph_container.arrow_selected.connect(self._on_arrow_selected)

        # Connect signals for both adjustment panels
        if self._left_adjustment_panel:
            self._left_adjustment_panel.beat_modified.connect(self._on_beat_modified)
            self._left_adjustment_panel.turn_applied.connect(self._on_turn_applied)

        if self._right_adjustment_panel:
            self._right_adjustment_panel.beat_modified.connect(self._on_beat_modified)
            self._right_adjustment_panel.turn_applied.connect(self._on_turn_applied)

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

        # Update both adjustment panels
        if self._left_adjustment_panel:
            self._left_adjustment_panel.set_beat(beat_data)
        if self._right_adjustment_panel:
            self._right_adjustment_panel.set_beat(beat_data)

    def toggle_visibility(self):
        """Toggle graph editor visibility with smooth sliding animation"""
        # Prevent multiple animations
        if self._animating:
            return

        if self._is_visible:
            self._slide_down()
        else:
            self._slide_up()

    def is_visible(self) -> bool:
        """Check if graph editor is currently visible"""
        return self._is_visible

    def get_preferred_height(self) -> int:
        """Calculate preferred height constrained within available parent space"""
        if not self._parent_workbench:
            return 250

        parent_height = self._parent_workbench.height()
        parent_width = self._parent_workbench.width()

        # Calculate available space within the workbench
        # Account for other components: indicators, beat frame, margins, etc.
        available_height = self._calculate_available_height()

        # Use legacy's sizing logic but constrain to available space
        calculated_height = min(int(parent_height // 3.5), parent_width // 4)

        # Ensure we don't exceed available space or go below minimum
        max_allowed = max(available_height - 50, 150)  # 50px buffer, 150px minimum
        constrained_height = min(calculated_height, max_allowed)

        return max(constrained_height, 150)  # Absolute minimum 150px

    def _calculate_available_height(self) -> int:
        """Calculate available height within the parent workbench"""
        if not self._parent_workbench:
            return 300

        parent_height = self._parent_workbench.height()

        # Estimate space used by other workbench components
        # Based on ModernSequenceWorkbench layout:
        # - Indicators section: ~80px
        # - Beat frame section: takes remaining space but needs minimum
        # - Margins and spacing: ~40px

        estimated_other_content = 120  # Conservative estimate
        available = parent_height - estimated_other_content

        # Ensure we have reasonable space available
        return max(available, 200)

    # Sliding Animation Methods
    def _slide_up(self):
        """Slide the graph editor up from bottom (show)"""
        if self._is_visible or self._animating:
            return

        print("🔼 Starting slide up animation")
        self._animating = True
        self._is_visible = True

        # Show the widget first
        self.show()

        target_height = self.get_preferred_height()

        # Ensure target height doesn't exceed available space
        available_height = self._calculate_available_height()
        max_allowed_height = max(available_height - 50, 150)  # 50px buffer
        target_height = min(target_height, max_allowed_height)

        # Set maximum height constraint to prevent layout expansion
        self.setMaximumHeight(target_height)
        self.setMinimumHeight(0)

        # Configure animation from 0 to constrained target height
        self._height_animation.setStartValue(0)
        self._height_animation.setEndValue(target_height)

        # Start animation
        self._height_animation.start()

        # Update toggle tab position with animation to hug top of frame
        if self._toggle_tab:
            self._toggle_tab.update_position(animate=True)

        # Emit signal
        self.visibility_changed.emit(True)

    def _slide_down(self):
        """Slide the graph editor down to bottom (hide)"""
        if not self._is_visible or self._animating:
            return

        print("🔽 Starting slide down animation")
        self._animating = True
        self._is_visible = False

        current_height = self.height()

        # Clear height constraints for smooth animation
        self.setMaximumHeight(16777215)
        self.setMinimumHeight(0)

        # Configure animation from current height to 0
        self._height_animation.setStartValue(current_height)
        self._height_animation.setEndValue(0)

        # Start animation
        self._height_animation.start()

        # Update toggle tab position with animation back to bottom
        if self._toggle_tab:
            self._toggle_tab.update_position(animate=True)

        # Emit signal
        self.visibility_changed.emit(False)

    def _on_animation_finished(self):
        """Handle animation completion"""
        print(f"✅ Animation finished. Visible: {self._is_visible}")
        self._animating = False

        if not self._is_visible:
            # Hide the widget after slide down animation
            self.hide()
            # Reset height constraints
            self.setMaximumHeight(16777215)
            self.setMinimumHeight(0)
        else:
            # Lock height after slide up animation to prevent layout issues
            target_height = self.get_preferred_height()

            # Ensure we don't exceed available space
            available_height = self._calculate_available_height()
            max_allowed_height = max(available_height - 50, 150)  # 50px buffer
            constrained_height = min(target_height, max_allowed_height)

            self.setFixedHeight(constrained_height)

    # Event Handlers
    def _on_arrow_selected(self, arrow_id: str):
        """Handle arrow selection from pictograph container"""
        self._selected_arrow_id = arrow_id
        self._graph_service.set_arrow_selection(arrow_id)
        self.arrow_selected.emit(arrow_id)

        # Update both adjustment panels for selected arrow
        if self._left_adjustment_panel:
            self._left_adjustment_panel.set_selected_arrow(arrow_id)
        if self._right_adjustment_panel:
            self._right_adjustment_panel.set_selected_arrow(arrow_id)

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

    def _update_display(self):
        """Update all display components based on current state"""
        if self._pictograph_container:
            self._pictograph_container.set_beat(self._selected_beat)

        if self._left_adjustment_panel:
            self._left_adjustment_panel.set_beat(self._selected_beat)
        if self._right_adjustment_panel:
            self._right_adjustment_panel.set_beat(self._selected_beat)

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

        # Don't interfere with animations
        if self._animating:
            return

        if self._is_visible:
            # Update height based on new parent size
            new_height = self.get_preferred_height()
            self.setFixedHeight(new_height)

        # Update toggle tab position (no animation during resize)
        if self._toggle_tab:
            self._toggle_tab.update_position(animate=False)

    def keyPressEvent(self, event: QKeyEvent):
        """Handle key press events for hotkeys."""
        # Only handle hotkeys when graph editor is visible and has focus
        if not self._is_visible:
            super().keyPressEvent(event)
            return

        # Try to handle through hotkey service
        if hasattr(self._graph_service, "_hotkey_service"):
            handled = self._graph_service._hotkey_service.handle_key_event(event)
            if handled:
                return

        # Pass to parent if not handled
        super().keyPressEvent(event)
