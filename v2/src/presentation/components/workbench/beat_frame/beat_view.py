"""
Modern Beat View Component

Individual beat widget for the V2 sequence workbench, replacing V1's BeatView
with modern architecture patterns and V2 pictograph integration.
"""

from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QMouseEvent, QPainter, QPen, QColor

from presentation.components.pictograph.pictograph_component import PictographComponent
from src.domain.models.core_models import BeatData


class ModernBeatView(QFrame):
    """
    Modern beat view widget with V2 pictograph integration.

    Replaces V1's BeatView with:
    - Clean separation of concerns
    - V2 pictograph rendering integration
    - Modern PyQt6 patterns
    - Responsive design
    """

    # Signals
    beat_clicked = pyqtSignal()
    beat_double_clicked = pyqtSignal()
    beat_modified = pyqtSignal(object)  # BeatData object
    beat_context_menu = pyqtSignal()

    def __init__(self, beat_number: int, parent: Optional[QWidget] = None):
        super().__init__(parent)

        # Properties
        self._beat_number = beat_number
        self._beat_data: Optional[BeatData] = None
        self._is_selected = False
        self._is_highlighted = False

        # UI components (will be initialized in _setup_ui)
        self._pictograph_component: Optional[PictographComponent] = None

        self._setup_ui()
        self._setup_styling()

    def _setup_ui(self):
        """Setup the UI components to match v1 layout exactly"""
        self.setFixedSize(120, 120)
        self.setFrameStyle(QFrame.Shape.Box)

        # Use zero margins and spacing like v1
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Remove beat number label - v1 doesn't have labels above pictographs
        # Beat numbers are rendered directly on the pictograph scene

        # Pictograph component fills the entire container like v1
        self._pictograph_component = PictographComponent(parent=self)
        if self._pictograph_component:
            self._pictograph_component.setMinimumSize(120, 120)  # Fill container
        layout.addWidget(self._pictograph_component)

        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)

    def _setup_styling(self):
        """Apply modern styling"""
        self.setStyleSheet(
            """
            QFrame {
                background: rgba(255, 255, 255, 0.08);
                border: 2px solid rgba(255, 255, 255, 0.15);
                border-radius: 8px;
            }
            QFrame:hover {
                background: rgba(255, 255, 255, 0.12);
                border-color: rgba(74, 144, 226, 0.5);
            }
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
                border: none;
            }
        """
        )

    # Public API
    def set_beat_data(self, beat_data: BeatData):
        """Set the beat data and update display"""
        self._beat_data = beat_data
        self._update_display()

    def get_beat_data(self) -> Optional[BeatData]:
        """Get the current beat data"""
        return self._beat_data

    def get_beat_number(self) -> int:
        """Get the beat number"""
        return self._beat_number

    def set_selected(self, selected: bool):
        """Set selection state"""
        if self._is_selected != selected:
            self._is_selected = selected
            self._update_selection_style()

    def is_selected(self) -> bool:
        """Check if beat is selected"""
        return self._is_selected

    def set_highlighted(self, highlighted: bool):
        """Set highlight state (for hover, etc.)"""
        if self._is_highlighted != highlighted:
            self._is_highlighted = highlighted
            self._update_highlight_style()

    def is_highlighted(self) -> bool:
        """Check if beat is highlighted"""
        return self._is_highlighted

    # Display updates
    def _update_display(self):
        """Update the visual display based on beat data"""
        if not self._beat_data:
            self._show_empty_state()
            return

        # No beat label in v1 - beat numbers are rendered on the pictograph scene
        # Update pictograph with beat data
        self._update_pictograph()

    def _update_pictograph(self):
        """Update pictograph display using V2 pictograph component"""
        if not self._beat_data or not self._pictograph_component:
            return

        # Update the pictograph component with beat data
        self._pictograph_component.update_from_beat(self._beat_data)

    def _show_empty_state(self):
        """Show empty state when no beat data"""
        # No beat label in v1 - just clear the pictograph

        # Clear pictograph component
        if self._pictograph_component:
            self._pictograph_component.clear_pictograph()

    def _update_selection_style(self):
        """Update styling based on selection state"""
        if self._is_selected:
            self.setStyleSheet(
                """
                QFrame {
                    background: rgba(74, 144, 226, 0.2);
                    border: 2px solid rgba(74, 144, 226, 0.8);
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

    def _update_highlight_style(self):
        """Update styling based on highlight state"""
        if self._is_highlighted and not self._is_selected:
            self.setStyleSheet(
                """
                QFrame {
                    background: rgba(255, 255, 255, 0.15);
                    border: 2px solid rgba(74, 144, 226, 0.6);
                    border-radius: 8px;
                }
                QLabel {
                    color: white;
                    background: transparent;
                    border: none;
                }
            """
            )
        elif not self._is_selected:
            self._setup_styling()  # Reset to default

    # Event handlers
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press events"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.beat_clicked.emit()
        elif event.button() == Qt.MouseButton.RightButton:
            self.beat_context_menu.emit()
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """Handle mouse double click events"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.beat_double_clicked.emit()
        super().mouseDoubleClickEvent(event)

    def enterEvent(self, event):
        """Handle mouse enter events"""
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.set_highlighted(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave events"""
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.set_highlighted(False)
        super().leaveEvent(event)

    def paintEvent(self, event):
        """Custom paint event for additional visual effects"""
        super().paintEvent(event)

        # Add selection indicator if selected
        if self._is_selected:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Draw selection indicator in top-right corner
            pen = QPen(QColor(74, 144, 226), 3)
            painter.setPen(pen)

            # Draw a small circle indicator
            indicator_size = 8
            x = self.width() - indicator_size - 4
            y = 4
            painter.drawEllipse(x, y, indicator_size, indicator_size)

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
        if self._beat_data:
            accessible_desc = f"Beat {self._beat_number}, Letter {self._beat_data.letter}, Duration {self._beat_data.duration}"
        else:
            accessible_desc = f"Empty beat slot {self._beat_number}"
        self.setAccessibleDescription(accessible_desc)

    # Keyboard support
    def keyPressEvent(self, event):
        """Handle keyboard events"""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.beat_clicked.emit()
        elif event.key() == Qt.Key.Key_Delete:
            # Emit signal to delete this beat
            if self._beat_data:
                self.beat_modified.emit(BeatData.empty())
        super().keyPressEvent(event)
