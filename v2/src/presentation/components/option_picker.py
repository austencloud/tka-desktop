"""
Modern option picker component for Kinetic Constructor v2.

This component displays actual pictographs (visual representations with arrows, props, and grids)
that users can click to select. It uses the V1 SVG assets and positioning algorithms to ensure
pixel-perfect visual compatibility.

REPLACES: Legacy option picker with AppContext dependencies
PROVIDES: Clean pictograph display using REAL v1 SVG assets
"""

from typing import List, Optional
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QGridLayout,
    QFrame,
    QSizePolicy,
)
from PyQt6.QtCore import pyqtSignal, Qt, QObject
from PyQt6.QtGui import QFont

from ...core.dependency_injection.simple_container import SimpleContainer
from ...core.interfaces.core_services import ILayoutService
from ...domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
)
from .simple_pictograph_component import SimplePictographComponent


class ClickablePictographFrame(QFrame):
    """A clickable frame that contains an actual pictograph visualization."""

    clicked = pyqtSignal(str)  # Emits the beat ID when clicked

    def __init__(self, beat_data: BeatData, parent=None):
        super().__init__(parent)
        self.beat_data = beat_data
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(2)

        # FORCE SQUARE DIMENSIONS: Set both min and max to same square size
        square_size = 180  # Consistent square size for all pictographs
        self.setMinimumSize(square_size, square_size)
        self.setMaximumSize(square_size, square_size)
        self.setFixedSize(square_size, square_size)  # Force exact square

        # Create layout with minimal margins to maximize pictograph space
        layout = QVBoxLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)  # Minimal margins
        layout.setSpacing(0)  # No spacing

        # Create actual pictograph component using V1 assets
        self.pictograph_component = SimplePictographComponent()

        # Ensure pictograph component fills the available space
        self.pictograph_component.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.pictograph_component.update_from_beat(beat_data)
        layout.addWidget(self.pictograph_component)

        # Style the frame
        self.setStyleSheet(
            """
            ClickablePictographFrame {
                background-color: white;
                border: 2px solid #dee2e6;
                border-radius: 8px;
            }
            ClickablePictographFrame:hover {
                border-color: #007bff;
                background-color: #f8f9fa;
            }
        """
        )

    def mousePressEvent(self, event):
        """Handle mouse press to emit clicked signal."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(f"beat_{self.beat_data.letter}")
        super().mousePressEvent(event)


class ModernOptionPicker(QObject):
    """
    Modern option picker component using dependency injection.

    Displays actual pictographs (visual representations with arrows, props, and grids)
    that users can click to select. Uses V1 SVG assets for pixel-perfect compatibility.

    REPLACES: Legacy option picker with AppContext dependencies
    ELIMINATES: Global state access, layout patches, mw coupling
    """

    option_selected = pyqtSignal(str)

    def __init__(self, container: SimpleContainer):
        super().__init__()
        self.container = container
        self.widget: Optional[QWidget] = None
        self._beat_options: List[BeatData] = []
        self._beat_frames: List[ClickablePictographFrame] = []
        self._layout_service: Optional[ILayoutService] = None

    def initialize(self) -> None:
        """Initialize the option picker widget."""
        # Resolve dependencies
        self._layout_service = self.container.resolve(ILayoutService)

        # Create the widget
        self.widget = self._create_widget()

        # Load initial beat options
        self._load_beat_options()

    def _create_widget(self) -> QWidget:
        """Create the main widget."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Title
        title = QLabel("Choose Your Next Pictograph")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Scroll area for pictograph options
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Options container with grid layout for pictographs
        self.options_container = QWidget()
        self.options_layout = QGridLayout(self.options_container)
        self.options_layout.setSpacing(10)

        scroll_area.setWidget(self.options_container)
        layout.addWidget(scroll_area)

        # Apply styling
        widget.setStyleSheet(
            """
            QWidget {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
            }
        """
        )

        return widget

    def _load_beat_options(self) -> None:
        """Load available beat options."""
        # Create sample beats for demonstration
        # In a real implementation, these would come from a data service
        self._beat_options = [
            # Static beat
            BeatData(
                letter="A",
                blue_motion=MotionData(
                    motion_type=MotionType.STATIC,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.NORTH,
                    end_loc=Location.NORTH,
                ),
                red_motion=MotionData(
                    motion_type=MotionType.STATIC,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.SOUTH,
                    end_loc=Location.SOUTH,
                ),
            ),
            # Pro motion beat
            BeatData(
                letter="B",
                blue_motion=MotionData(
                    motion_type=MotionType.PRO,
                    prop_rot_dir=RotationDirection.CLOCKWISE,
                    start_loc=Location.NORTH,
                    end_loc=Location.EAST,
                    turns=1.0,
                ),
                red_motion=MotionData(
                    motion_type=MotionType.PRO,
                    prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                    start_loc=Location.SOUTH,
                    end_loc=Location.WEST,
                    turns=1.0,
                ),
            ),
            # Dash motion beat
            BeatData(
                letter="C",
                blue_motion=MotionData(
                    motion_type=MotionType.DASH,
                    prop_rot_dir=RotationDirection.CLOCKWISE,
                    start_loc=Location.NORTH,
                    end_loc=Location.SOUTH,
                ),
                red_motion=MotionData(
                    motion_type=MotionType.DASH,
                    prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                    start_loc=Location.EAST,
                    end_loc=Location.WEST,
                ),
            ),
        ]

        self._update_beat_display()

    def _update_beat_display(self) -> None:
        """Update the beat display."""
        # Clear existing beat frames
        for frame in self._beat_frames:
            frame.setParent(None)
        self._beat_frames.clear()

        # Add beat frames in a grid
        columns = 3  # 3 beats per row
        for i, beat in enumerate(self._beat_options):
            row = i // columns
            col = i % columns

            # Create clickable frame
            frame = ClickablePictographFrame(beat)
            frame.clicked.connect(self._handle_beat_click)

            self.options_layout.addWidget(frame, row, col)
            self._beat_frames.append(frame)

    def _handle_beat_click(self, beat_id: str) -> None:
        """Handle beat click."""
        print(f"Beat selected: {beat_id}")
        self.option_selected.emit(beat_id)

    def refresh_options(self) -> None:
        """Refresh the available options."""
        self._load_beat_options()

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable the option picker."""
        if self.widget:
            self.widget.setEnabled(enabled)

    def get_size(self) -> tuple[int, int]:
        """Get the recommended size for the option picker."""
        if self._layout_service:
            picker_size = self._layout_service.get_picker_size()
            return (picker_size.width(), picker_size.height())
        return (300, 600)  # Default size
