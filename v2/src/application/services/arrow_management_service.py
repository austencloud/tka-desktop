"""
Arrow Management Service - Unified Arrow Operations

Consolidates arrow-related services into a single cohesive service:
- Arrow positioning pipeline (arrow_positioning_service)
- Arrow mirroring logic (arrow_mirror_service)
- Default placement calculations (default_placement_service)
- Placement key generation (placement_key_service)
- Motion orientation for arrows (motion_orientation_service)

This service provides a clean, unified interface for arrow operations
while maintaining the proven algorithms from the individual services.
Prop positioning has been moved to PropManagementService.
"""

from typing import Tuple, Dict, Any, Optional
from abc import ABC, abstractmethod
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QTransform

try:
    from PyQt6.QtSvgWidgets import QGraphicsSvgItem
except ImportError:
    # Fallback for testing or when SVG widgets not available
    QGraphicsSvgItem = None
from enum import Enum

from domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    Location,
    RotationDirection,
    Orientation,
)
from domain.models.pictograph_models import (
    ArrowData,
    PictographData,
    GridData,
    GridMode,
)


class IArrowManagementService(ABC):
    """Unified interface for arrow management operations."""

    @abstractmethod
    def calculate_arrow_position(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> Tuple[float, float, float]:
        """Calculate complete arrow position and rotation."""
        pass

    @abstractmethod
    def should_mirror_arrow(self, arrow_data: ArrowData) -> bool:
        """Determine if arrow should be mirrored based on motion type."""
        pass

    @abstractmethod
    def calculate_all_arrow_positions(
        self, pictograph_data: PictographData
    ) -> PictographData:
        """Calculate positions for all arrows in pictograph."""
        pass


class ArrowManagementService(IArrowManagementService):
    """
    Unified arrow management service for arrow operations only.

    Provides comprehensive arrow management including:
    - Positioning calculations with pixel-perfect accuracy
    - Mirroring logic based on motion type and rotation
    - Default placement and adjustment calculations

    Prop positioning has been moved to PropManagementService.
    """

    def __init__(self):
        # Arrow positioning constants
        self.CENTER_X = 200
        self.CENTER_Y = 200
        self.SCENE_SIZE = 400

        # Layer2 coordinates for shift arrows
        self.LAYER2_POINTS = {
            Location.NORTH: QPointF(200, 100),
            Location.SOUTH: QPointF(200, 300),
            Location.EAST: QPointF(300, 200),
            Location.WEST: QPointF(100, 200),
            Location.NORTHEAST: QPointF(270, 130),
            Location.NORTHWEST: QPointF(130, 130),
            Location.SOUTHEAST: QPointF(270, 270),
            Location.SOUTHWEST: QPointF(130, 270),
        }

        # Hand point coordinates for static/dash arrows
        self.HAND_POINTS = {
            Location.NORTH: QPointF(200, 150),
            Location.SOUTH: QPointF(200, 250),
            Location.EAST: QPointF(250, 200),
            Location.WEST: QPointF(150, 200),
            Location.NORTHEAST: QPointF(235, 165),
            Location.NORTHWEST: QPointF(165, 165),
            Location.SOUTHEAST: QPointF(235, 235),
            Location.SOUTHWEST: QPointF(165, 235),
        }

        # Arrow mirroring conditions
        self.mirror_conditions = {
            "anti": {"cw": True, "ccw": False},
            "other": {"cw": False, "ccw": True},
        }

    def calculate_arrow_position(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> Tuple[float, float, float]:
        """
        Calculate complete arrow position and rotation using unified pipeline.

        Implements the complete positioning pipeline:
        1. Calculate arrow location from motion
        2. Compute initial position (layer2 vs hand points)
        3. Calculate rotation angle
        4. Apply adjustments (default placement + special rules)
        5. Return final position and rotation
        """
        if not arrow_data.motion_data:
            return self.CENTER_X, self.CENTER_Y, 0.0

        motion = arrow_data.motion_data

        # Step 1: Calculate arrow location
        arrow_location = self._calculate_arrow_location(motion)

        # Step 2: Compute initial position
        initial_position = self._compute_initial_position(motion, arrow_location)

        # Step 3: Calculate rotation
        rotation = self._calculate_arrow_rotation(motion, arrow_location)

        # Step 4: Get adjustment
        adjustment = self._calculate_adjustment(arrow_data, pictograph_data)

        # Step 5: Apply final positioning formula
        final_x = initial_position.x() + adjustment.x()
        final_y = initial_position.y() + adjustment.y()

        return final_x, final_y, rotation

    def should_mirror_arrow(self, arrow_data: ArrowData) -> bool:
        """Determine if arrow should be mirrored based on motion type and rotation."""
        if not arrow_data.motion_data:
            return False

        motion_type = arrow_data.motion_data.motion_type.value.lower()
        prop_rot_dir = arrow_data.motion_data.prop_rot_dir.value.lower()

        if motion_type == "anti":
            return self.mirror_conditions["anti"].get(prop_rot_dir, False)
        else:
            return self.mirror_conditions["other"].get(prop_rot_dir, False)

    def apply_mirror_transform(self, arrow_item: Any, should_mirror: bool) -> None:
        """Apply mirror transformation to arrow graphics item."""
        center_x = arrow_item.boundingRect().center().x()
        center_y = arrow_item.boundingRect().center().y()

        transform = QTransform()
        transform.translate(center_x, center_y)
        transform.scale(-1 if should_mirror else 1, 1)
        transform.translate(-center_x, -center_y)

        arrow_item.setTransform(transform)

    def calculate_all_arrow_positions(
        self, pictograph_data: PictographData
    ) -> PictographData:
        """Calculate positions for all arrows in the pictograph."""
        updated_pictograph = pictograph_data

        for color, arrow_data in pictograph_data.arrows.items():
            if arrow_data.is_visible and arrow_data.motion_data:
                x, y, rotation = self.calculate_arrow_position(
                    arrow_data, pictograph_data
                )

                updated_pictograph = updated_pictograph.update_arrow(
                    color, position_x=x, position_y=y, rotation_angle=rotation
                )

        return updated_pictograph

    def _calculate_arrow_location(self, motion: MotionData) -> Location:
        """Calculate arrow location based on motion type."""
        if motion.motion_type in [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT]:
            return motion.end_loc
        elif motion.motion_type in [MotionType.STATIC, MotionType.DASH]:
            return motion.start_loc
        else:
            return Location.NORTH  # Default fallback

    def _compute_initial_position(
        self, motion: MotionData, arrow_location: Location
    ) -> QPointF:
        """Compute initial position using placement strategy."""
        if motion.motion_type in [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT]:
            return self._get_layer2_coords(arrow_location)
        elif motion.motion_type in [MotionType.STATIC, MotionType.DASH]:
            return self._get_hand_point_coords(arrow_location)
        else:
            return QPointF(self.CENTER_X, self.CENTER_Y)

    def _get_layer2_coords(self, location: Location) -> QPointF:
        """Get layer2 point coordinates for shift arrows."""
        return self.LAYER2_POINTS.get(location, QPointF(self.CENTER_X, self.CENTER_Y))

    def _get_hand_point_coords(self, location: Location) -> QPointF:
        """Get hand point coordinates for static/dash arrows."""
        return self.HAND_POINTS.get(location, QPointF(self.CENTER_X, self.CENTER_Y))

    def _calculate_arrow_rotation(
        self, motion: MotionData, location: Location
    ) -> float:
        """Calculate arrow rotation angle."""
        # Base rotation from location
        location_rotations = {
            Location.NORTH: 0,
            Location.NORTHEAST: 45,
            Location.EAST: 90,
            Location.SOUTHEAST: 135,
            Location.SOUTH: 180,
            Location.SOUTHWEST: 225,
            Location.WEST: 270,
            Location.NORTHWEST: 315,
        }

        base_rotation = location_rotations.get(location, 0)

        # Apply motion-specific adjustments
        if motion.motion_type == MotionType.ANTI:
            base_rotation += 180

        return base_rotation % 360

    def _calculate_adjustment(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> QPointF:
        """Calculate positioning adjustment using default placement system."""
        motion = arrow_data.motion_data
        if not motion:
            return QPointF(0, 0)

        # Generate placement key
        placement_key = self._generate_placement_key(motion)

        # Get default adjustment
        return self._get_default_adjustment(motion, placement_key)

    def _generate_placement_key(
        self,
        motion_data: MotionData,
        grid_mode: str = "diamond",
        prop_state: str = "alpha",
    ) -> str:
        """Generate placement key for default placement lookup."""
        motion_type = motion_data.motion_type.value
        end_orientation = self._calculate_end_orientation(motion_data)

        # Determine layer from end orientation
        layer = "layer1" if end_orientation == Orientation.IN else "layer2"

        return f"{motion_type}_to_{layer}_{prop_state}"

    def _get_default_adjustment(
        self, motion_data: MotionData, placement_key: str
    ) -> QPointF:
        """Get default adjustment from placement data."""
        # Simplified default adjustments - in production this would load from JSON
        default_adjustments = {
            "pro_to_layer1_alpha": QPointF(0, -10),
            "anti_to_layer2_alpha": QPointF(0, 10),
            "static_to_layer1_alpha": QPointF(-5, 0),
            "dash_to_layer1_alpha": QPointF(5, 0),
        }

        return default_adjustments.get(placement_key, QPointF(0, 0))

    def _calculate_end_orientation(
        self, motion_data: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> Orientation:
        """Calculate end orientation for placement calculations."""
        motion_type = motion_data.motion_type
        turns = motion_data.turns

        if turns in {0, 1, 2, 3}:
            if motion_type in [MotionType.PRO, MotionType.STATIC]:
                return (
                    start_orientation
                    if int(turns) % 2 == 0
                    else self._switch_orientation(start_orientation)
                )
            elif motion_type in [MotionType.ANTI, MotionType.DASH]:
                return (
                    self._switch_orientation(start_orientation)
                    if int(turns) % 2 == 0
                    else start_orientation
                )

        return start_orientation

    def _switch_orientation(self, orientation: Orientation) -> Orientation:
        """Switch between IN and OUT orientations."""
        return Orientation.OUT if orientation == Orientation.IN else Orientation.IN
