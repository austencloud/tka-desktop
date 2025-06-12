"""
Start Position View Component

Displays the start position in the sequence workbench beat frame,
integrating with V2's start position picker and pictograph system.
"""

from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QMouseEvent

from src.presentation.components.pictograph_component import PictographComponent
from src.domain.models.core_models import BeatData
from src.presentation.components.start_text_overlay import StartTextOverlay


class StartPositionView(QFrame):
    """
    Start position display widget for the sequence workbench.

    Shows the initial position of a sequence with pictograph rendering
    and integrates with the V2 start position picker workflow.
    """

    # Signals
    position_clicked = pyqtSignal()
    position_double_clicked = pyqtSignal()
    position_context_menu = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        # Properties
        self._position_data: Optional[BeatData] = None
        self._position_key: Optional[str] = None
        self._is_highlighted = False

        # UI components (will be initialized in _setup_ui)
        self._pictograph_component: Optional[PictographComponent] = None
        self._start_text_overlay: Optional[StartTextOverlay] = None

        self._setup_ui()
        self._setup_styling()

    def _setup_ui(self):
        """Setup the UI components to match v1 start position layout exactly"""
        self.setFixedSize(120, 120)
        self.setFrameStyle(QFrame.Shape.Box)

        # Use zero margins and spacing like v1
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Remove title and position labels - v1 displays "START" text directly on the pictograph scene

        # Pictograph component fills the entire container like v1
        self._pictograph_component = PictographComponent(parent=self)
        self._pictograph_component.setMinimumSize(120, 120)  # Fill container
        layout.addWidget(self._pictograph_component)

        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)

        # Initialize with START text overlay (always visible like v1)
        # Use a timer to ensure the pictograph component is fully initialized
        from PyQt6.QtCore import QTimer

        QTimer.singleShot(100, self._initialize_start_text)

    def _setup_styling(self):
        """Apply modern styling with start position theme"""
        self.setStyleSheet(
            """
            QFrame {
                background: rgba(46, 204, 113, 0.15);
                border: 2px solid rgba(46, 204, 113, 0.4);
                border-radius: 8px;
            }
            QFrame:hover {
                background: rgba(46, 204, 113, 0.25);
                border-color: rgba(46, 204, 113, 0.6);
            }
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
                border: none;
            }
        """
        )

    # Public API
    def set_position_data(self, beat_data: BeatData):
        """Set the start position data and update display"""
        self._position_data = beat_data
        self._update_display()

    def set_position_key(self, position_key: str):
        """Set the position key (e.g., 'alpha1', 'beta3')"""
        self._position_key = position_key
        self._update_display()

    def get_position_data(self) -> Optional[BeatData]:
        """Get the current position data"""
        return self._position_data

    def get_position_key(self) -> Optional[str]:
        """Get the current position key"""
        return self._position_key

    def set_highlighted(self, highlighted: bool):
        """Set highlight state"""
        if self._is_highlighted != highlighted:
            self._is_highlighted = highlighted
            self._update_highlight_style()

    def is_highlighted(self) -> bool:
        """Check if position is highlighted"""
        return self._is_highlighted

    # Display updates
    def _update_display(self):
        """Update the visual display based on position data"""
        if not self._position_data and not self._position_key:
            self._show_empty_state()
            return

        # No position label in v1 - "START" text is overlaid on the pictograph scene
        # Update pictograph
        self._update_pictograph()

    def _update_pictograph(self):
        """Update pictograph display using V2 pictograph component with START text overlay"""
        if not self._pictograph_component:
            return

        if self._position_data:
            # Update the pictograph component with position data
            self._pictograph_component.update_from_beat(self._position_data)
        else:
            # Show empty state (just grid background)
            self._pictograph_component.clear_pictograph()

        # ALWAYS add START text overlay like v1 (visible in both states)
        self._add_start_text_overlay()

    def _show_empty_state(self):
        """Show empty state when no position data"""
        # No position label in v1 - just clear the pictograph

        # Clear pictograph component
        if self._pictograph_component:
            self._pictograph_component.clear_pictograph()

        # Always show START text overlay, even in empty state (v1 behavior)
        self._add_start_text_overlay()

    def _initialize_start_text(self):
        """Initialize START text overlay after component is ready"""
        # Ensure pictograph component is ready
        if self._pictograph_component and self._pictograph_component.scene:
            self._add_start_text_overlay()
        else:
            # Retry after a short delay if component not ready
            from PyQt6.QtCore import QTimer

            QTimer.singleShot(200, self._initialize_start_text)

    def _add_start_text_overlay(self):
        """Add START text overlay to the pictograph like v1"""
        if not self._pictograph_component or not self._pictograph_component.scene:
            return

        if self._start_text_overlay:
            try:
                scene = self._start_text_overlay.scene()
                if (
                    hasattr(self._start_text_overlay, "scene")
                    and scene
                    and hasattr(scene, "removeItem")
                ):
                    scene.removeItem(self._start_text_overlay)
                self._start_text_overlay.deleteLater()
            except (RuntimeError, AttributeError):
                pass
            finally:
                self._start_text_overlay = None

        try:
            self._start_text_overlay = StartTextOverlay(
                self._pictograph_component.scene
            )
            self._start_text_overlay.show_start_text()
        except Exception as e:
            print(f"Failed to create start text overlay: {e}")
            self._start_text_overlay = None

    def _update_highlight_style(self):
        """Update styling based on highlight state"""
        if self._is_highlighted:
            self.setStyleSheet(
                """
                QFrame {
                    background: rgba(46, 204, 113, 0.3);
                    border: 2px solid rgba(46, 204, 113, 0.8);
                    border-radius: 8px;
                }
                QLabel {
                    color: white;
                    background: transparent;
                    border: none;
                }
            """
            )
        else:
            self._setup_styling()  # Reset to default

    # Event handlers
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press events"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.position_clicked.emit()
        elif event.button() == Qt.MouseButton.RightButton:
            self.position_context_menu.emit()
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """Handle mouse double click events"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.position_double_clicked.emit()
        super().mouseDoubleClickEvent(event)

    def enterEvent(self, event):
        """Handle mouse enter events"""
        self.set_highlighted(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave events"""
        self.set_highlighted(False)
        super().leaveEvent(event)

    def sizeHint(self) -> QSize:
        """Provide size hint for layout management"""
        return QSize(120, 120)

    def minimumSizeHint(self) -> QSize:
        """Provide minimum size hint"""
        return QSize(100, 100)

    # Accessibility support
    def setAccessibleName(self, name: str):
        """Set accessible name for screen readers"""
        super().setAccessibleName(name)
        if self._position_key:
            accessible_desc = f"Start position {self._position_key}"
        elif self._position_data:
            accessible_desc = f"Start position with letter {self._position_data.letter}"
        else:
            accessible_desc = "Start position not set, click to select"
        self.setAccessibleDescription(accessible_desc)

    # Keyboard support
    def keyPressEvent(self, event):
        """Handle keyboard events"""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.position_clicked.emit()
        super().keyPressEvent(event)

    # Animation support (for future enhancements)
    def pulse_animation(self):
        """Pulse animation to draw attention to start position"""
        # TODO: Implement smooth pulse animation
        # This could be used when transitioning from start position picker
        pass

    def set_loading_state(self, loading: bool):
        """Set loading state while position is being processed"""
        if loading:
            # No position label in v1 - could add loading indicator to pictograph if needed
            pass
        else:
            self._update_display()
