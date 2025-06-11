"""
Simple pictograph component for Kinetic Constructor v2.

This component renders pictographs using actual V1 SVG assets with pixel-perfect compatibility.
It uses the V1 positioning algorithms and SVG files to ensure visual fidelity.
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
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPainter, QBrush, QColor

from ...domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
)


def get_v2_image_path(filename: str) -> str:
    """Get the path to a v2 image file from the v2 assets directory."""
    # Only use v2's own assets directory
    assets_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "..",
        "assets",
        "images",
        filename,
    )

    normalized_path = os.path.normpath(assets_path)

    if not os.path.exists(normalized_path):
        print(f"Warning: V2 asset not found: {normalized_path}")
        print("Please copy required assets to v2/src/assets/images/")

    return normalized_path


class SimplePictographScene(QGraphicsScene):
    """
    Graphics scene for rendering pictographs using V1 assets.

    This handles the actual drawing of arrows, props, and grid elements
    based on beat data, using the exact V1 SVG files and positioning.
    Uses V1's exact 950x950 scene dimensions and positioning algorithms.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.beat_data: Optional[BeatData] = None

        # V1 EXACT DIMENSIONS: 950x950 scene with center at (475, 475)
        self.V1_SCENE_SIZE = 950
        self.V1_CENTER_X = 475
        self.V1_CENTER_Y = 475
        self.V1_RADIUS = 300  # Distance from center to outer grid points

        # Set scene to V1's exact dimensions
        self.setSceneRect(0, 0, self.V1_SCENE_SIZE, self.V1_SCENE_SIZE)

        # Set background to match V1
        self.setBackgroundBrush(QBrush(QColor(255, 255, 255)))  # Pure white like V1

        # V1 EXACT location coordinates (from diamond_grid.svg analysis)
        # HAND POINTS: Props position at hand points (inner circles), not outer points
        # Hand points are at ~143px radius from center (475, 475)
        self.V1_HAND_RADIUS = 143.1  # Distance from center to hand points

        # V1 EXACT hand point coordinates from diamond_grid.svg
        self.location_coordinates = {
            # Main cardinal directions (hand points)
            Location.NORTH: (
                0,
                -self.V1_HAND_RADIUS,
            ),  # (475, 331.9) relative to center
            Location.EAST: (self.V1_HAND_RADIUS, 0),  # (618.1, 475) relative to center
            Location.SOUTH: (0, self.V1_HAND_RADIUS),  # (475, 618.1) relative to center
            Location.WEST: (-self.V1_HAND_RADIUS, 0),  # (331.9, 475) relative to center
            # Diagonal directions (layer2 points for NE, SE, SW, NW)
            # These are also at hand point radius for consistency
            Location.NORTHEAST: (
                self.V1_HAND_RADIUS * 0.707,
                -self.V1_HAND_RADIUS * 0.707,
            ),  # ~(618.1, 331.9)
            Location.SOUTHEAST: (
                self.V1_HAND_RADIUS * 0.707,
                self.V1_HAND_RADIUS * 0.707,
            ),  # ~(618.1, 618.1)
            Location.SOUTHWEST: (
                -self.V1_HAND_RADIUS * 0.707,
                self.V1_HAND_RADIUS * 0.707,
            ),  # ~(331.9, 618.1)
            Location.NORTHWEST: (
                -self.V1_HAND_RADIUS * 0.707,
                -self.V1_HAND_RADIUS * 0.707,
            ),  # ~(331.9, 331.9)
        }

    def update_beat(self, beat_data: BeatData) -> None:
        """Update the scene with new beat data."""
        self.beat_data = beat_data
        self.clear()
        self._render_pictograph()

    def _render_pictograph(self) -> None:
        """Render the pictograph elements."""
        if not self.beat_data:
            return

        # Render grid (always box grid for now)
        self._render_grid()

        # Render props for blue and red motions
        if self.beat_data.blue_motion:
            self._render_prop("blue", self.beat_data.blue_motion)
        if self.beat_data.red_motion:
            self._render_prop("red", self.beat_data.red_motion)

        # Render arrows for blue and red motions
        if self.beat_data.blue_motion:
            self._render_arrow("blue", self.beat_data.blue_motion)
        if self.beat_data.red_motion:
            self._render_arrow("red", self.beat_data.red_motion)

        # Render letter
        self._render_letter()

    def _render_grid(self) -> None:
        """Render the grid using V1 assets copied to V2 local directory."""
        # Use V1 diamond grid now copied to V2 assets directory
        grid_svg_path = get_v2_image_path("grid/diamond_grid.svg")

        # Create and add the grid SVG item
        if os.path.exists(grid_svg_path):
            grid_item = QGraphicsSvgItem()
            renderer = QSvgRenderer(grid_svg_path)

            if renderer.isValid():
                grid_item.setSharedRenderer(renderer)

                # V1 EXACT SCALING: Grid SVG is now 950x950 (real V1 version), so scale = 1.0
                # This ensures pixel-perfect compatibility with V1
                grid_item.setScale(1.0)
                grid_item.setPos(0, 0)  # Position at scene origin

                self.addItem(grid_item)

    def _render_prop(self, color: str, motion_data: MotionData) -> None:
        """Render a prop using actual v1 SVG files with V1 exact scaling and rotation."""
        # For now, always use simple staff (can be made configurable later)
        prop_svg_path = get_v2_image_path("props/simple_staff.svg")

        if os.path.exists(prop_svg_path):
            prop_item = QGraphicsSvgItem()
            renderer = QSvgRenderer(prop_svg_path)
            if renderer.isValid():
                prop_item.setSharedRenderer(renderer)

                # V1 EXACT SCALING: Staff SVG is 252.8x77.8, scale to fit V1 proportions
                # In V1, props are typically scaled to about 1/3 of grid radius
                prop_scale = 0.8  # Increased from 0.3 to match V1 proportions
                prop_item.setScale(prop_scale)

                # V1 EXACT POSITIONING: Position at END location (final prop position)
                end_pos = self._get_location_position(motion_data.end_loc)
                target_hand_point_x = self.V1_CENTER_X + end_pos[0]
                target_hand_point_y = self.V1_CENTER_Y + end_pos[1]

                # V1 EXACT ROTATION: Apply rotation FIRST (before positioning)
                prop_rotation = self._calculate_prop_rotation(motion_data)
                bounds = prop_item.boundingRect()
                prop_item.setTransformOriginPoint(bounds.center())
                prop_item.setRotation(prop_rotation)

                # V1 EXACT COORDINATE SYSTEM: Use V1's prop positioning approach
                # This ensures the prop's center aligns with the hand point regardless of rotation
                self._place_prop_at_hand_point_v1_style(
                    prop_item, target_hand_point_x, target_hand_point_y
                )

                self.addItem(prop_item)

    def _place_prop_at_hand_point_v1_style(
        self, prop_item: QGraphicsSvgItem, target_x: float, target_y: float
    ) -> None:
        """
        Position prop using V1's exact coordinate system approach.

        This method replicates V1's place_prop_at_hand_point logic:
        1. Get prop's center point in local coordinates
        2. Convert to scene coordinates using mapToScene()
        3. Calculate offset to align center with target hand point
        4. Apply offset to position prop correctly
        """
        from PyQt6.QtCore import QPointF

        # Step 1: Get prop's center point in local coordinates (V1 approach)
        # For SVG props, use boundingRect center (V1 fallback for non-centerPoint SVGs)
        bounds = prop_item.boundingRect()
        center_point_in_local_coords = bounds.center()

        # Step 2: Convert local coordinates to scene coordinates (V1 approach)
        center_point_in_scene = prop_item.mapToScene(center_point_in_local_coords)

        # Step 3: Calculate offset needed to place center at target hand point (V1 approach)
        target_hand_point = QPointF(target_x, target_y)
        offset = target_hand_point - center_point_in_scene

        # Step 4: Apply offset to move prop (V1 approach)
        new_position = prop_item.pos() + offset
        prop_item.setPos(new_position)

    def _render_arrow(self, color: str, motion_data: MotionData) -> None:
        """Render an arrow using actual v1 SVG files."""
        arrow_svg_path = self._get_arrow_svg_file(motion_data)

        if os.path.exists(arrow_svg_path):
            arrow_item = QGraphicsSvgItem()
            renderer = QSvgRenderer(arrow_svg_path)
            if renderer.isValid():
                arrow_item.setSharedRenderer(renderer)

                # V1 EXACT SCALING: Arrow SVG is ~108x217, scale to match V1 proportions
                # In V1, arrows are typically scaled to about 1/4 of grid radius
                arrow_scale = 0.7  # Increased from 0.2 to match V1 proportions
                arrow_item.setScale(arrow_scale)

                # Calculate position and rotation
                position_x, position_y, rotation = self._calculate_arrow_position(
                    motion_data
                )

                # Apply rotation
                arrow_item.setRotation(rotation)

                # Center the arrow on its position
                bounds = arrow_item.boundingRect()
                arrow_item.setPos(
                    position_x - (bounds.width() * arrow_scale) / 2,
                    position_y - (bounds.height() * arrow_scale) / 2,
                )

                self.addItem(arrow_item)

    def _get_arrow_svg_file(self, motion_data: MotionData) -> str:
        """Get the correct arrow SVG file path using V1 logic with proper motion type mapping."""
        # Format turns value for filename (e.g., 1.0, 0.5, 1.5, etc.)
        turns_str = f"{motion_data.turns:.1f}"

        if motion_data.motion_type == MotionType.STATIC:
            return get_v2_image_path(
                f"arrows/static/from_radial/static_{turns_str}.svg"
            )
        elif motion_data.motion_type == MotionType.PRO:
            return get_v2_image_path(f"arrows/pro/from_radial/pro_{turns_str}.svg")
        elif motion_data.motion_type == MotionType.ANTI:
            # FIXED: Added missing ANTI motion type support
            return get_v2_image_path(f"arrows/anti/from_radial/anti_{turns_str}.svg")
        elif motion_data.motion_type == MotionType.DASH:
            return get_v2_image_path(f"arrows/dash/from_radial/dash_{turns_str}.svg")
        elif motion_data.motion_type == MotionType.FLOAT:
            # Float arrows don't use turns parameter
            return get_v2_image_path("arrows/float.svg")
        else:
            # Default fallback to static
            return get_v2_image_path(
                f"arrows/static/from_radial/static_{turns_str}.svg"
            )

    def _calculate_arrow_position(
        self, motion_data: MotionData
    ) -> tuple[float, float, float]:
        """Calculate arrow position and rotation using V1 exact algorithms."""
        if motion_data.motion_type == MotionType.STATIC:
            # V1 EXACT: Static arrows positioned at start location, pointing inward
            start_pos = self._get_location_position(motion_data.start_loc)
            x = (
                self.V1_CENTER_X + start_pos[0] * 0.7
            )  # Slightly closer to center (V1 style)
            y = self.V1_CENTER_Y + start_pos[1] * 0.7
            rotation = self._calculate_static_rotation(motion_data.start_loc)
            return x, y, rotation
        elif motion_data.motion_type == MotionType.PRO:
            # V1 EXACT: Pro arrows use calculated arrow location for positioning and rotation
            arrow_location = self._calculate_arrow_location(motion_data)
            arrow_pos = self._get_location_position(arrow_location)
            x = self.V1_CENTER_X + arrow_pos[0]
            y = self.V1_CENTER_Y + arrow_pos[1]

            # Use V1's pro rotation algorithm with calculated arrow location
            rotation = self._calculate_pro_rotation(motion_data, arrow_location)
            return x, y, rotation
        elif motion_data.motion_type == MotionType.ANTI:
            # V1 EXACT: Anti arrows use calculated arrow location for positioning and rotation
            arrow_location = self._calculate_arrow_location(motion_data)
            arrow_pos = self._get_location_position(arrow_location)
            x = self.V1_CENTER_X + arrow_pos[0]
            y = self.V1_CENTER_Y + arrow_pos[1]

            # Use V1's anti rotation algorithm with calculated arrow location
            rotation = self._calculate_anti_rotation(motion_data, arrow_location)
            return x, y, rotation
        elif motion_data.motion_type == MotionType.DASH:
            # V1 EXACT: Dash arrows use calculated arrow location for positioning and rotation
            arrow_location = self._calculate_arrow_location(motion_data)
            arrow_pos = self._get_location_position(arrow_location)
            x = self.V1_CENTER_X + arrow_pos[0]
            y = self.V1_CENTER_Y + arrow_pos[1]

            # Use V1's dash rotation algorithm with calculated arrow location
            rotation = self._calculate_dash_rotation(motion_data, arrow_location)
            return x, y, rotation
        else:
            # V1 EXACT: Other motion types (FLOAT, etc.) use calculated arrow location
            arrow_location = self._calculate_arrow_location(motion_data)
            arrow_pos = self._get_location_position(arrow_location)
            x = self.V1_CENTER_X + arrow_pos[0]
            y = self.V1_CENTER_Y + arrow_pos[1]

            # Use appropriate rotation calculation for motion type
            if motion_data.motion_type == MotionType.FLOAT:
                rotation = self._calculate_float_rotation(motion_data, arrow_location)
            else:
                # Default rotation calculation
                rotation = self._calculate_motion_rotation((0, 0), arrow_pos)
            return x, y, rotation

    def _get_location_position(self, location: Location) -> tuple[float, float]:
        """Get the coordinate position for a location."""
        return self.location_coordinates.get(location, (0, 0))

    def _calculate_static_rotation(self, location: Location) -> float:
        """Calculate rotation for static arrows using V1's exact algorithms."""
        # V1 static arrows use radial orientation (pointing inward)
        # These angles are from V1's StaticRotAngleCalculator
        location_angles = {
            Location.NORTH: 180.0,
            Location.NORTHEAST: 225.0,
            Location.EAST: 270.0,
            Location.SOUTHEAST: 315.0,
            Location.SOUTH: 0.0,
            Location.SOUTHWEST: 45.0,
            Location.WEST: 90.0,
            Location.NORTHWEST: 135.0,
        }
        return location_angles.get(location, 0.0)

    def _calculate_arrow_location(self, motion_data: MotionData) -> Location:
        """Calculate arrow location using V1's exact location calculation logic."""
        if motion_data.motion_type == MotionType.STATIC:
            # Static arrows: location = start_loc
            return motion_data.start_loc
        elif motion_data.motion_type in [
            MotionType.PRO,
            MotionType.ANTI,
            MotionType.FLOAT,
        ]:
            # Shift arrows: calculate location based on start/end pair
            return self._calculate_shift_arrow_location(
                motion_data.start_loc, motion_data.end_loc
            )
        elif motion_data.motion_type == MotionType.DASH:
            # Dash arrows: simplified logic (V1 has complex letter-specific logic)
            if motion_data.turns == 0:
                return motion_data.start_loc  # Simplified for zero turns
            else:
                return self._calculate_shift_arrow_location(
                    motion_data.start_loc, motion_data.end_loc
                )
        else:
            return motion_data.start_loc  # Default fallback

    def _calculate_shift_arrow_location(
        self, start_loc: Location, end_loc: Location
    ) -> Location:
        """Calculate arrow location for shift motions using V1's exact logic."""
        # V1 ShiftLocationCalculator logic: direction pairs map to arrow locations
        direction_pairs = {
            frozenset({Location.NORTH, Location.EAST}): Location.NORTHEAST,
            frozenset({Location.EAST, Location.SOUTH}): Location.SOUTHEAST,
            frozenset({Location.SOUTH, Location.WEST}): Location.SOUTHWEST,
            frozenset({Location.WEST, Location.NORTH}): Location.NORTHWEST,
            frozenset({Location.NORTHEAST, Location.NORTHWEST}): Location.NORTH,
            frozenset({Location.NORTHEAST, Location.SOUTHEAST}): Location.EAST,
            frozenset({Location.SOUTHWEST, Location.SOUTHEAST}): Location.SOUTH,
            frozenset({Location.NORTHWEST, Location.SOUTHWEST}): Location.WEST,
        }
        return direction_pairs.get(frozenset({start_loc, end_loc}), start_loc)

    def _calculate_pro_rotation(
        self, motion_data: MotionData, arrow_location: Location
    ) -> float:
        """Calculate rotation for pro arrows using V1's exact algorithms."""
        # V1 pro rotation maps from ProRotAngleCalculator
        direction_map = {
            RotationDirection.CLOCKWISE: {
                Location.NORTH: 315,
                Location.EAST: 45,
                Location.SOUTH: 135,
                Location.WEST: 225,
                Location.NORTHEAST: 0,
                Location.SOUTHEAST: 90,
                Location.SOUTHWEST: 180,
                Location.NORTHWEST: 270,
            },
            RotationDirection.COUNTER_CLOCKWISE: {
                Location.NORTH: 315,
                Location.EAST: 225,
                Location.SOUTH: 135,
                Location.WEST: 45,
                Location.NORTHEAST: 270,
                Location.SOUTHEAST: 180,
                Location.SOUTHWEST: 90,
                Location.NORTHWEST: 0,
            },
        }
        prop_rot_dir = motion_data.prop_rot_dir
        return float(direction_map.get(prop_rot_dir, {}).get(arrow_location, 0))

    def _calculate_anti_rotation(
        self, motion_data: MotionData, arrow_location: Location
    ) -> float:
        """Calculate rotation for anti arrows using V1's exact algorithms."""
        # V1 anti rotation maps from AntiRotAngleCalculator
        # For simplicity, using the radial orientation maps (IN/OUT)
        direction_map = {
            RotationDirection.CLOCKWISE: {
                Location.NORTH: 315,
                Location.EAST: 225,
                Location.SOUTH: 135,
                Location.WEST: 45,
                Location.NORTHEAST: 270,
                Location.SOUTHEAST: 180,
                Location.SOUTHWEST: 90,
                Location.NORTHWEST: 0,
            },
            RotationDirection.COUNTER_CLOCKWISE: {
                Location.NORTH: 315,
                Location.EAST: 45,
                Location.SOUTH: 135,
                Location.WEST: 225,
                Location.NORTHEAST: 0,
                Location.SOUTHEAST: 90,
                Location.SOUTHWEST: 180,
                Location.NORTHWEST: 270,
            },
        }
        prop_rot_dir = motion_data.prop_rot_dir
        return float(direction_map.get(prop_rot_dir, {}).get(arrow_location, 0))

    def _calculate_dash_rotation(
        self, motion_data: MotionData, arrow_location: Location = None
    ) -> float:
        """Calculate rotation for dash arrows using V1's exact algorithms."""
        # Use calculated arrow location if provided, otherwise calculate it
        if arrow_location is None:
            arrow_location = self._calculate_arrow_location(motion_data)

        # V1 dash rotation maps from DashRotAngleCalculator
        if motion_data.prop_rot_dir == RotationDirection.NO_ROTATION:
            # No rotation map for dash arrows
            no_rotation_map = {
                (Location.NORTH, Location.SOUTH): 90,
                (Location.EAST, Location.WEST): 180,
                (Location.SOUTH, Location.NORTH): 270,
                (Location.WEST, Location.EAST): 0,
                (Location.SOUTHEAST, Location.NORTHWEST): 225,
                (Location.SOUTHWEST, Location.NORTHEAST): 315,
                (Location.NORTHWEST, Location.SOUTHEAST): 45,
                (Location.NORTHEAST, Location.SOUTHWEST): 135,
            }
            return float(
                no_rotation_map.get((motion_data.start_loc, motion_data.end_loc), 0)
            )
        else:
            # For now, use simplified rotation calculation based on arrow location
            # This can be enhanced with V1's full orientation-based rotation
            arrow_pos = self._get_location_position(arrow_location)
            center_pos = (0, 0)
            return self._calculate_motion_rotation(center_pos, arrow_pos)

    def _calculate_float_rotation(
        self, motion_data: MotionData, arrow_location: Location
    ) -> float:
        """Calculate rotation for float arrows using V1's exact algorithms."""
        # V1 float rotation maps from FloatRotAngleCalculator
        # Simplified version - V1 has complex handpath direction calculation
        clockwise_map = {
            Location.NORTH: 315,
            Location.EAST: 45,
            Location.SOUTH: 135,
            Location.WEST: 225,
            Location.NORTHEAST: 0,
            Location.SOUTHEAST: 90,
            Location.SOUTHWEST: 180,
            Location.NORTHWEST: 270,
        }
        counter_clockwise_map = {
            Location.NORTH: 45,
            Location.EAST: 135,
            Location.SOUTH: 225,
            Location.WEST: 315,
            Location.NORTHEAST: 90,
            Location.SOUTHEAST: 180,
            Location.SOUTHWEST: 270,
            Location.NORTHWEST: 0,
        }

        # For now, use clockwise map as default
        # V1 determines this based on handpath direction calculation
        return float(clockwise_map.get(arrow_location, 0))

    def _calculate_motion_rotation(
        self, start_pos: tuple[float, float], end_pos: tuple[float, float]
    ) -> float:
        """Calculate rotation for motion arrows."""
        import math

        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]

        if dx == 0 and dy == 0:
            return 0.0

        # Calculate angle in degrees
        angle = math.degrees(math.atan2(dy, dx))

        # Adjust for arrow pointing direction
        return angle - 90.0

    def _calculate_prop_rotation(self, motion_data: MotionData) -> float:
        """
        Calculate prop rotation using V1's exact rotation algorithms.

        V1 uses different rotation maps based on:
        1. Grid mode (DIAMOND vs BOX) - determined by location
        2. Orientation (IN, OUT, CLOCK, COUNTER) - determined by motion type and prop_rot_dir
        3. Location (NORTH, SOUTH, etc.)
        """
        # Determine grid mode based on END location (V1 logic)
        # Props are positioned at end location, so rotation should be based on end location
        location = motion_data.end_loc
        if location in [Location.NORTH, Location.SOUTH, Location.EAST, Location.WEST]:
            grid_mode = "DIAMOND"
        else:  # NORTHEAST, NORTHWEST, SOUTHEAST, SOUTHWEST
            grid_mode = "BOX"

        # Determine orientation based on motion type and prop_rot_dir (simplified V1 logic)
        # For now, we'll use a simplified mapping - this can be enhanced later
        if motion_data.motion_type == MotionType.STATIC:
            # Static motions typically use IN orientation
            orientation = "IN"
        elif motion_data.prop_rot_dir == RotationDirection.CLOCKWISE:
            orientation = "CLOCK"
        elif motion_data.prop_rot_dir == RotationDirection.COUNTER_CLOCKWISE:
            orientation = "COUNTER"
        else:
            orientation = "IN"  # Default fallback

        # V1 EXACT rotation maps from prop_rot_angle_manager.py
        if grid_mode == "DIAMOND":
            angle_map = {
                "IN": {
                    Location.NORTH: 90,
                    Location.SOUTH: 270,
                    Location.WEST: 0,
                    Location.EAST: 180,
                },
                "OUT": {
                    Location.NORTH: 270,
                    Location.SOUTH: 90,
                    Location.WEST: 180,
                    Location.EAST: 0,
                },
                "CLOCK": {
                    Location.NORTH: 0,
                    Location.SOUTH: 180,
                    Location.WEST: 270,
                    Location.EAST: 90,
                },
                "COUNTER": {
                    Location.NORTH: 180,
                    Location.SOUTH: 0,
                    Location.WEST: 90,
                    Location.EAST: 270,
                },
            }
        else:  # BOX mode
            angle_map = {
                "IN": {
                    Location.NORTHEAST: 135,
                    Location.NORTHWEST: 45,
                    Location.SOUTHWEST: 315,
                    Location.SOUTHEAST: 225,
                },
                "OUT": {
                    Location.NORTHEAST: 315,
                    Location.NORTHWEST: 225,
                    Location.SOUTHWEST: 135,
                    Location.SOUTHEAST: 45,
                },
                "CLOCK": {
                    Location.NORTHEAST: 45,
                    Location.NORTHWEST: 315,
                    Location.SOUTHWEST: 225,
                    Location.SOUTHEAST: 135,
                },
                "COUNTER": {
                    Location.NORTHEAST: 225,
                    Location.NORTHWEST: 135,
                    Location.SOUTHWEST: 45,
                    Location.SOUTHEAST: 315,
                },
            }

        # Get rotation angle from V1's exact mapping
        rotation_angle = angle_map.get(orientation, {}).get(location, 0)
        return float(rotation_angle)

    def _render_letter(self) -> None:
        """Render the letter if present."""
        if not self.beat_data or not self.beat_data.letter:
            return

        from PyQt6.QtWidgets import QGraphicsTextItem
        from PyQt6.QtGui import QFont

        letter_item = QGraphicsTextItem(self.beat_data.letter)
        font = QFont("Arial", 24, QFont.Weight.Bold)
        letter_item.setFont(font)

        # V1 EXACT: Position at bottom center using V1 coordinates
        letter_item.setPos(
            self.V1_CENTER_X - 10, self.V1_CENTER_Y + self.V1_RADIUS + 20
        )

        self.addItem(letter_item)


class SimplePictographComponent(QWidget):
    """
    Simple pictograph component using V1 assets.

    This component displays pictographs with pixel-perfect V1 compatibility
    while using the modern V2 architecture.
    """

    # Signals
    pictograph_updated = pyqtSignal(object)  # BeatData

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        # Current state
        self.current_beat: Optional[BeatData] = None
        self.scene: Optional[SimplePictographScene] = None
        self.view: Optional[QGraphicsView] = None

        # Setup UI
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the UI components with proper scaling to fit container."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create graphics scene and view with V1 dimensions
        self.scene = SimplePictographScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # Configure view for proper scaling
        self.view.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Remove frame to match V1 appearance
        self.view.setFrameStyle(0)

        layout.addWidget(self.view)

        # FORCE SQUARE ASPECT RATIO: Override size policies
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Set default size with 1:1 aspect ratio
        self.setMinimumSize(100, 100)  # Smaller minimum for flexibility
        self.resize(200, 200)  # Default square size

        # Initial fit after setup
        self._fit_view()

    def update_from_beat(self, beat_data: BeatData) -> None:
        """
        Update the pictograph from beat data.

        Args:
            beat_data: Beat data to display
        """
        self.current_beat = beat_data
        if self.scene:
            self.scene.update_beat(beat_data)
            # Force immediate fit after scene update
            self._fit_view()
        self.pictograph_updated.emit(beat_data)

    def get_current_beat(self) -> Optional[BeatData]:
        """Get the current beat data."""
        return self.current_beat

    def clear_pictograph(self) -> None:
        """Clear the pictograph display."""
        self.current_beat = None
        if self.scene:
            self.scene.clear()

    def _fit_view(self) -> None:
        """Fit the view to properly scale and center the pictograph in container."""
        if self.view and self.scene:
            # Reset any previous transformations
            self.view.resetTransform()

            # Get the container size
            container_size = min(self.view.width(), self.view.height())

            # Calculate appropriate scale factor
            # We want the grid to fill most of the container (about 90%)
            scene_size = self.scene.V1_SCENE_SIZE  # 950
            target_scale = (container_size * 0.9) / scene_size

            # Apply the scale transformation
            self.view.scale(target_scale, target_scale)

            # Center the scene in the view
            self.view.centerOn(self.scene.V1_CENTER_X, self.scene.V1_CENTER_Y)

    def resizeEvent(self, event) -> None:
        """Handle resize events to maintain proper scaling."""
        super().resizeEvent(event)

        # Always refit the view after resize to maintain proper scaling
        self._fit_view()

    def showEvent(self, event) -> None:
        """Handle show events to ensure proper initial scaling."""
        super().showEvent(event)
        self._fit_view()
