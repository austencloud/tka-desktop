"""
Production-ready Pictograph Component for V2 System.

This is the main pictograph component that will be used throughout the V2 system.
It replaces the SimplePictographComponent and provides full V1 compatibility
with proper coordinate system handling for props and arrows.
"""

import os
from typing import Optional

from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGraphicsView,
    QWidget,
    QVBoxLayout,
    QSizePolicy,
)
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import pyqtSignal, Qt, QPointF
from PyQt6.QtGui import QPainter, QBrush, QColor, QTransform

# UI Component (presentation layer)
from ...domain.models.beat_data import BeatData  # ✅ Domain model
from ...domain.models.motion_data import MotionData  # ✅ Domain model
from ...domain.enums.motion_type import MotionType  # ✅ Domain enum

from ...domain.models.pictograph_data import PictographData
from ...domain.services.pictograph_service import IPictographService


def get_v1_image_path(filename: str) -> str:
    """
    Get the path to a v1 image file.

    This function looks for images in the v1 images directory structure.
    """
    # Try multiple possible locations for the v1 images
    possible_paths = [
        # Original v1 location (primary)
        os.path.join("v1", "src", "images", filename),
        # Alternative v1 location
        os.path.join("v1", "images", filename),
        # In the copied assets directory (fallback)
        os.path.join("v2", "src", "assets", "images", filename),
        # Relative to this file (go up to project root, then into v1)
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "..",
            "..",
            "..",
            "v1",
            "src",
            "images",
            filename,
        ),
    ]

    for path in possible_paths:
        normalized_path = os.path.normpath(path)
        if os.path.exists(normalized_path):
            return normalized_path

    # If not found, print warning and return first path for debugging
    print(f"Warning: Could not find v1 image file: {filename}")
    print(f"Tried paths: {[os.path.normpath(p) for p in possible_paths]}")
    return os.path.normpath(possible_paths[0])


class PictographScene(QGraphicsScene):
    """
    Graphics scene for rendering pictographs.

    This handles the actual drawing of arrows, props, and grid elements
    based on the immutable pictograph data.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pictograph_data: Optional[PictographData] = None
        self.setSceneRect(0, 0, 400, 400)

        # Set background
        self.setBackgroundBrush(QBrush(QColor(250, 250, 250)))

    def update_pictograph(self, pictograph_data: PictographData) -> None:
        """Update the scene with new pictograph data."""
        self.pictograph_data = pictograph_data
        self.clear()
        self._render_pictograph()

    def _render_pictograph(self) -> None:
        """Render the pictograph elements."""
        if not self.pictograph_data:
            return

        # Render grid
        self._render_grid()

        # Render props
        self._render_props()

        # Render arrows
        self._render_arrows()

        # Render letter
        self._render_letter()

    def _render_grid(self) -> None:
        """Render the grid using actual v1 SVG files."""
        if not self.pictograph_data:
            return

        # Determine grid mode
        grid_mode = self.pictograph_data.grid_data.grid_mode

        # Load the appropriate grid SVG
        if grid_mode == GridMode.DIAMOND:
            grid_svg_path = get_v1_image_path("grid/diamond_grid.svg")
        else:  # BOX mode
            grid_svg_path = get_v1_image_path("grid/box_grid.svg")

        # Create and add the grid SVG item
        if os.path.exists(grid_svg_path):
            grid_item = QGraphicsSvgItem()
            renderer = QSvgRenderer(grid_svg_path)
            if renderer.isValid():
                grid_item.setSharedRenderer(renderer)
                # Position the grid at the center
                grid_item.setPos(0, 0)  # v1 grids are positioned at origin
                self.addItem(grid_item)

    def _render_props(self) -> None:
        """Render the props."""
        if not self.pictograph_data:
            return

        for color, prop_data in self.pictograph_data.props.items():
            if prop_data.is_visible:
                self._render_prop(prop_data)

    def _render_prop(self, prop_data: PropData) -> None:
        """Render a single prop using actual v1 SVG files."""
        # Get the prop SVG file path based on prop type
        prop_type = (
            prop_data.prop_type.value
            if hasattr(prop_data.prop_type, "value")
            else str(prop_data.prop_type)
        )

        # Map prop types to SVG files (matching v1 naming convention)
        prop_svg_filename = f"props/{prop_type.lower()}.svg"

        # Special cases for v1 prop naming
        if prop_type.lower() == "simplestaff":
            prop_svg_filename = "props/simple_staff.svg"
        elif prop_type.lower() == "hand":
            # Hands have different files for left/right (blue/red)
            hand_type = "left_hand" if prop_data.color == "blue" else "right_hand"
            prop_svg_filename = f"hands/{hand_type}.svg"

        prop_svg_path = get_v1_image_path(prop_svg_filename)

        # Create and add the prop SVG item
        if os.path.exists(prop_svg_path):
            prop_item = QGraphicsSvgItem()
            renderer = QSvgRenderer(prop_svg_path)
            if renderer.isValid():
                prop_item.setSharedRenderer(renderer)

                # Apply color transformation if needed (v1 does this for most props)
                if prop_type.lower() != "hand":
                    # TODO: Implement color transformation like v1 does
                    pass

                # Scale the prop to appropriate size (v1 props are typically smaller)
                prop_scale = 0.3  # Scale down to 30% of original size
                prop_item.setScale(prop_scale)

                # Center the prop on its position
                bounds = prop_item.boundingRect()
                prop_item.setPos(
                    prop_data.position_x - (bounds.width() * prop_scale) / 2,
                    prop_data.position_y - (bounds.height() * prop_scale) / 2,
                )

                self.addItem(prop_item)

    def _render_arrows(self) -> None:
        """Render the arrows."""
        if not self.pictograph_data:
            return

        for color, arrow_data in self.pictograph_data.arrows.items():
            if arrow_data.is_visible:
                self._render_arrow(arrow_data)

    def _render_arrow(self, arrow_data: ArrowData) -> None:
        """Render a single arrow using actual v1 SVG files."""
        if not arrow_data.motion_data:
            return

        # Get arrow SVG file path using v1 logic
        arrow_svg_path = self._get_arrow_svg_file(arrow_data)

        # Create and add the arrow SVG item
        if os.path.exists(arrow_svg_path):
            arrow_item = QGraphicsSvgItem()
            renderer = QSvgRenderer(arrow_svg_path)
            if renderer.isValid():
                arrow_item.setSharedRenderer(renderer)

                # Apply color transformation (v1 does this for all arrows)
                # TODO: Implement color transformation like v1 does

                # Scale the arrow to appropriate size (v1 arrows are typically smaller)
                arrow_scale = 0.4  # Scale down to 40% of original size
                arrow_item.setScale(arrow_scale)

                # Apply rotation
                arrow_item.setRotation(arrow_data.rotation_angle)

                # Center the arrow on its position
                bounds = arrow_item.boundingRect()
                arrow_item.setPos(
                    arrow_data.position_x - (bounds.width() * arrow_scale) / 2,
                    arrow_data.position_y - (bounds.height() * arrow_scale) / 2,
                )

                self.addItem(arrow_item)

    def _get_arrow_svg_file(self, arrow_data: ArrowData) -> str:
        """Get the correct arrow SVG file path using v1 logic."""
        motion = arrow_data.motion_data

        if not motion:
            return get_v1_image_path(
                "arrows/static/from_radial/static_0.0.svg"
            )  # Default fallback

        # Handle float arrows (special case)
        if motion.motion_type == MotionType.FLOAT:
            return get_v1_image_path("arrows/float.svg")

        # Get turns value
        turns = arrow_data.turns if hasattr(arrow_data, "turns") else motion.turns

        # Determine motion type string
        motion_type_str = motion.motion_type.value.lower()

        # Determine orientation path (radial vs nonradial)
        start_ori = getattr(motion, "start_ori", "in")

        if start_ori in ["in", "out"]:
            # Radial orientation
            orientation_path = "from_radial"
        else:
            # Non-radial orientation (clock, counter)
            orientation_path = "from_nonradial"

        # Construct the file path following v1 structure
        # arrows/{motion_type}/{orientation}/{motion_type}_{turns}.svg
        arrow_filename = (
            f"arrows/{motion_type_str}/{orientation_path}/{motion_type_str}_{turns}.svg"
        )

        return get_v1_image_path(arrow_filename)

    def _render_letter(self) -> None:
        """Render the letter if present."""
        if not self.pictograph_data or not self.pictograph_data.letter:
            return

        from PyQt6.QtWidgets import QGraphicsTextItem
        from PyQt6.QtGui import QFont

        letter_item = QGraphicsTextItem(self.pictograph_data.letter)
        font = QFont("Arial", 24, QFont.Weight.Bold)
        letter_item.setFont(font)

        # Position at bottom center
        center = self.pictograph_data.grid_data
        letter_item.setPos(center.center_x - 10, center.center_y + center.radius + 20)

        self.addItem(letter_item)


class PictographComponent(ViewableComponentBase):
    """
    Main pictograph component using the new architecture.

    This component handles pictograph display and updates using
    dependency injection and immutable data models.
    """

    # Signals
    pictograph_updated = pyqtSignal(object)  # PictographData

    def __init__(
        self,
        container: IContainer,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(container, parent)

        # Current state
        self.current_pictograph: Optional[PictographData] = None
        self.pictograph_service: Optional[IPictographService] = None
        self.scene: Optional[PictographScene] = None
        self.view: Optional[QGraphicsView] = None

    def _create_widget(self, parent: Optional[QWidget]) -> QWidget:
        """Create the underlying QWidget."""
        widget = QWidget(parent)
        widget.setMinimumSize(400, 400)
        return widget

    def _initialize_component(self) -> None:
        """Initialize component-specific logic."""
        # Inject dependencies
        self.pictograph_service = self.get_dependency(IPictographService)

        # Setup UI
        self._setup_ui()

        # Create default pictograph
        self.current_pictograph = self.pictograph_service.create_pictograph()
        self._update_display()

    def _cleanup_component(self) -> None:
        """Clean up component-specific resources."""
        if self.scene:
            self.scene.clear()
        self.current_pictograph = None

    def _setup_ui(self) -> None:
        """Setup the UI components."""
        layout = QVBoxLayout(self.widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create graphics scene and view
        self.scene = PictographScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Configure view for proper scaling and aspect ratio
        self.view.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Fit in view with aspect ratio maintained
        self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

        layout.addWidget(self.view)

        # Set default size with 1:1 aspect ratio
        self.widget.setMinimumSize(300, 300)
        self.widget.resize(400, 400)

    def update_from_beat(self, beat_data: BeatData) -> None:
        """
        Update the pictograph from beat data.

        Args:
            beat_data: Beat data to display
        """
        if not self.pictograph_service:
            return

        if not self.current_pictograph:
            self.current_pictograph = self.pictograph_service.create_pictograph(
                beat_data
            )
        else:
            self.current_pictograph = (
                self.pictograph_service.update_pictograph_from_beat(
                    self.current_pictograph, beat_data
                )
            )

        self._update_display()
        self.pictograph_updated.emit(self.current_pictograph)

    def update_pictograph(self, pictograph_data: PictographData) -> None:
        """
        Update with new pictograph data.

        Args:
            pictograph_data: New pictograph data to display
        """
        self.current_pictograph = pictograph_data
        self._update_display()
        self.pictograph_updated.emit(self.current_pictograph)

    def get_current_pictograph(self) -> Optional[PictographData]:
        """Get the current pictograph data."""
        return self.current_pictograph

    def clear_pictograph(self) -> None:
        """Clear the pictograph display."""
        if not self.pictograph_service:
            return
        self.current_pictograph = self.pictograph_service.create_pictograph()
        self._update_display()
        self.pictograph_updated.emit(self.current_pictograph)

    def _update_display(self) -> None:
        """Update the visual display."""
        if self.current_pictograph and self.scene:
            self.scene.update_pictograph(self.current_pictograph)
            # Ensure proper scaling after update
            self._fit_view()

    def _fit_view(self) -> None:
        """Fit the view to maintain proper aspect ratio and scaling."""
        if self.view and self.scene:
            self.view.fitInView(
                self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio
            )
