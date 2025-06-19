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

from typing import Tuple, Dict, Any, Optional, Union, TYPE_CHECKING, List
from abc import ABC, abstractmethod
import uuid
from datetime import datetime

# Conditional Qt imports to avoid DLL loading issues during testing
try:
    from PyQt6.QtCore import QPointF
    from PyQt6.QtGui import QTransform

    QT_AVAILABLE = True
except ImportError:
    # Fallback for testing or when Qt is not available
    class MockQPointF:
        def __init__(self, x=0.0, y=0.0):
            self._x = x
            self._y = y

        def x(self):
            return self._x

        def y(self):
            return self._y

    class MockQTransform:
        def translate(self, x, y):
            pass

        def scale(self, x, y):
            pass

    QPointF = MockQPointF
    QTransform = MockQTransform
    QT_AVAILABLE = False

if TYPE_CHECKING:
    from PyQt6.QtCore import QPointF as QPointFType
    from PyQt6.QtGui import QTransform as QTransformType

    # Use Any to avoid type conflicts between real Qt types and mock types
    from typing import Any
    PointType = Any
    TransformType = Any
else:
    # Runtime: Allow both real Qt types and mock types
    from typing import Any
    PointType = Any
    TransformType = Any
    
from application.services.positioning.default_placement_service import (
    DefaultPlacementService,
)

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
from .placement_key_service import PlacementKeyService
from domain.models.letter_type_classifier import LetterTypeClassifier
from .dash_location_service import DashLocationService

# Event-driven architecture imports
if TYPE_CHECKING:
    from core.events import IEventBus
    from .special_placement_service import SpecialPlacementService

try:
    from core.events import (
        get_event_bus,
        ArrowPositionedEvent,
        EventPriority,
    )

    EVENT_SYSTEM_AVAILABLE = True
except ImportError:
    # For tests or when event system is not available
    get_event_bus = None
    ArrowPositionedEvent = None
    EventPriority = None
    EVENT_SYSTEM_AVAILABLE = False


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
    def apply_mirror_transform(self, arrow_item: Any, should_mirror: bool) -> None:
        """Apply mirror transformation to arrow graphics item."""
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

    def __init__(self, event_bus: Optional["IEventBus"] = None):
        # CRITICAL FIX: Use correct scene coordinates matching PictographScene
        # Arrow positioning constants - must match PictographScene dimensions
        self.CENTER_X = 475
        self.CENTER_Y = 475
        self.SCENE_SIZE = 950

        # Event system integration
        self.event_bus = event_bus or (
            get_event_bus() if EVENT_SYSTEM_AVAILABLE else None
        )
        self._subscription_ids: List[str] = []

        # Initialize placement services
        self.default_placement_service = DefaultPlacementService()
        self.placement_key_service = (
            PlacementKeyService()
        )  # Initialize dash location service
        self.dash_location_service = (
            DashLocationService()
        )  # Cache special placement service to avoid reloading JSON files on every call
        self._special_placement_service: Optional["SpecialPlacementService"] = None

        # CRITICAL FIX: Use correct coordinates from circle_coords.json
        # Hand point coordinates (for STATIC/DASH arrows) - inner grid positions where props are placed
        self.HAND_POINTS = {
            Location.NORTH: QPointF(475.0, 331.9),
            Location.EAST: QPointF(618.1, 475.0),
            Location.SOUTH: QPointF(475.0, 618.1),
            Location.WEST: QPointF(331.9, 475.0),
            # Diagonal hand points (calculated from radius)
            Location.NORTHEAST: QPointF(618.1, 331.9),
            Location.SOUTHEAST: QPointF(618.1, 618.1),
            Location.SOUTHWEST: QPointF(331.9, 618.1),
            Location.NORTHWEST: QPointF(331.9, 331.9),
        }

        # Layer2 point coordinates (for PRO/ANTI/FLOAT arrows) - using DIAMOND layer2 points from circle_coords.json
        self.LAYER2_POINTS = {
            # Diamond layer2 points are diagonal positions
            Location.NORTHEAST: QPointF(618.1, 331.9),
            Location.SOUTHEAST: QPointF(618.1, 618.1),
            Location.SOUTHWEST: QPointF(331.9, 618.1),
            Location.NORTHWEST: QPointF(331.9, 331.9),
            # For cardinal directions, map to nearest diagonal
            Location.NORTH: QPointF(618.1, 331.9),  # Maps to NE
            Location.EAST: QPointF(618.1, 618.1),  # Maps to SE
            Location.SOUTH: QPointF(331.9, 618.1),  # Maps to SW
            Location.WEST: QPointF(331.9, 331.9),  # Maps to NW
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
        arrow_location = self._calculate_arrow_location(motion, pictograph_data)

        # Step 2: Compute initial position
        initial_position = self._compute_initial_position(motion, arrow_location)

        # Step 3: Calculate rotation
        rotation = self._calculate_arrow_rotation(motion, arrow_location)

        # Step 4: Get adjustment
        adjustment = self._calculate_adjustment(arrow_data, pictograph_data)

        # Step 5: Apply final positioning formula
        final_x = initial_position.x() + adjustment.x()
        final_y = initial_position.y() + adjustment.y()

        # Publish arrow positioned event
        if self.event_bus and ArrowPositionedEvent:
            self.event_bus.publish(
                ArrowPositionedEvent(
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source="ArrowManagementService",
                    arrow_color=arrow_data.color,
                    position_data={
                        "x": final_x,
                        "y": final_y,
                        "rotation": rotation,
                        "motion_type": motion.motion_type.value,
                        "arrow_location": arrow_location.value,
                    },
                )
            )

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

    def cleanup(self):
        """Clean up event subscriptions when service is destroyed."""
        if self.event_bus:
            for sub_id in self._subscription_ids:
                self.event_bus.unsubscribe(sub_id)
            self._subscription_ids.clear()

    def _calculate_arrow_location(
        self, motion: MotionData, pictograph_data: Optional[PictographData] = None
    ) -> Location:
        """Calculate arrow location using location calculation algorithms."""
        if motion.motion_type == MotionType.STATIC:
            return motion.start_loc
        elif motion.motion_type in [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT]:
            return self._calculate_shift_arrow_location(
                motion.start_loc, motion.end_loc
            )
        elif motion.motion_type == MotionType.DASH:
            return self._calculate_dash_arrow_location(motion, pictograph_data)
        else:
            return motion.start_loc

    def _calculate_shift_arrow_location(
        self, start_loc: Location, end_loc: Location
    ) -> Location:
        """Calculate location for shift arrows (PRO/ANTI/FLOAT) based on start/end pair."""
        # Direction pairs mapping from shift location calculator
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

    def _calculate_dash_arrow_location(
        self, motion: MotionData, pictograph_data: Optional[PictographData] = None
    ) -> Location:
        """Calculate location for dash arrows using complete validated logic."""

        # Extract required parameters for calculation
        letter_type = None
        color = "blue"  # Default color
        other_motion = None
        grid_mode = "diamond"  # Default for TKA

        if pictograph_data:
            # Get letter type if available
            if hasattr(pictograph_data, "letter") and pictograph_data.letter:
                letter_type = LetterTypeClassifier.get_letter_type(
                    pictograph_data.letter
                )

            # Get grid mode from pictograph data
            if hasattr(pictograph_data, "grid_data") and pictograph_data.grid_data:
                grid_mode = pictograph_data.grid_data.grid_mode.value.lower()

            # Get other motion for special cases
            other_motion = self._get_other_motion(motion, pictograph_data)

            # Get arrow color if available
            for arrow_color, arrow_data in pictograph_data.arrows.items():
                if arrow_data.motion_data == motion:
                    color = arrow_color
                    break

        # Use the comprehensive dash location service
        return self.dash_location_service.calculate_dash_location(
            motion=motion,
        )

    def _compute_initial_position(
        self, motion: MotionData, arrow_location: Location
    ) -> Any:
        """Compute initial position using placement strategy."""
        if motion.motion_type in [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT]:
            return self._get_layer2_coords(arrow_location)
        elif motion.motion_type in [MotionType.STATIC, MotionType.DASH]:
            return self._get_hand_point_coords(arrow_location)
        else:
            return QPointF(self.CENTER_X, self.CENTER_Y)

    def _get_layer2_coords(self, location: Location) -> Any:
        """Get layer2 point coordinates for shift arrows."""
        return self.LAYER2_POINTS.get(location, QPointF(self.CENTER_X, self.CENTER_Y))

    def _get_hand_point_coords(self, location: Location) -> Any:
        """Get hand point coordinates for static/dash arrows."""
        return self.HAND_POINTS.get(location, QPointF(self.CENTER_X, self.CENTER_Y))

    def _calculate_arrow_rotation(
        self, motion: MotionData, arrow_location: Location
    ) -> float:
        """Calculate arrow rotation using validated rotation calculators."""
        if motion.motion_type == MotionType.STATIC:
            return self._calculate_static_rotation(arrow_location)
        elif motion.motion_type == MotionType.PRO:
            return self._calculate_pro_rotation(motion, arrow_location)
        elif motion.motion_type == MotionType.ANTI:
            return self._calculate_anti_rotation(motion, arrow_location)
        elif motion.motion_type == MotionType.DASH:
            return self._calculate_dash_rotation(motion, arrow_location)
        elif motion.motion_type == MotionType.FLOAT:
            return self._calculate_float_rotation(motion, arrow_location)
        else:
            return 0.0

    def _calculate_static_rotation(self, location: Location) -> float:
        """Calculate rotation for static arrows."""
        # Static arrows point inward by default
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

    def _calculate_pro_rotation(self, motion: MotionData, location: Location) -> float:
        """Calculate rotation for pro arrows."""
        # Pro rotation based on prop rotation direction and location
        if motion.prop_rot_dir == RotationDirection.CLOCKWISE:
            direction_map = {
                Location.NORTH: 315,
                Location.EAST: 45,
                Location.SOUTH: 135,
                Location.WEST: 225,
                Location.NORTHEAST: 0,
                Location.SOUTHEAST: 90,
                Location.SOUTHWEST: 180,
                Location.NORTHWEST: 270,
            }
        else:  # COUNTER_CLOCKWISE
            direction_map = {
                Location.NORTH: 315,
                Location.EAST: 225,
                Location.SOUTH: 135,
                Location.WEST: 45,
                Location.NORTHEAST: 270,
                Location.SOUTHEAST: 180,
                Location.SOUTHWEST: 90,
                Location.NORTHWEST: 0,
            }
        return direction_map.get(location, 0.0)

    def _calculate_anti_rotation(self, motion: MotionData, location: Location) -> float:
        """Calculate rotation for anti arrows using exact rotation logic."""
        # Anti rotation maps from AntiRotAngleCalculator - radial orientation (IN/OUT)
        if motion.prop_rot_dir == RotationDirection.CLOCKWISE:
            direction_map = {
                Location.NORTH: 315,
                Location.EAST: 225,
                Location.SOUTH: 135,
                Location.WEST: 45,
                Location.NORTHEAST: 270,
                Location.SOUTHEAST: 180,
                Location.SOUTHWEST: 90,
                Location.NORTHWEST: 0,
            }
        else:  # COUNTER_CLOCKWISE
            direction_map = {
                Location.NORTH: 315,
                Location.EAST: 45,
                Location.SOUTH: 135,
                Location.WEST: 225,
                Location.NORTHEAST: 0,
                Location.SOUTHEAST: 90,
                Location.SOUTHWEST: 180,
                Location.NORTHWEST: 270,
            }
        return direction_map.get(location, 0.0)

    def _calculate_dash_rotation(self, motion: MotionData, location: Location) -> float:
        """Calculate rotation for dash arrows using exact rotation logic."""
        # Handle NO_ROTATION case first (most common for dash)
        if motion.prop_rot_dir == RotationDirection.NO_ROTATION:
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
            return no_rotation_map.get((motion.start_loc, motion.end_loc), 0)

        # Handle rotation-based dash arrows
        if motion.prop_rot_dir == RotationDirection.CLOCKWISE:
            direction_map = {
                Location.NORTH: 270,
                Location.EAST: 0,
                Location.SOUTH: 90,
                Location.WEST: 180,
                Location.NORTHEAST: 315,
                Location.SOUTHEAST: 45,
                Location.SOUTHWEST: 135,
                Location.NORTHWEST: 225,
            }
        else:  # COUNTER_CLOCKWISE
            direction_map = {
                Location.NORTH: 270,
                Location.EAST: 180,
                Location.SOUTH: 90,
                Location.WEST: 0,
                Location.NORTHEAST: 225,
                Location.SOUTHEAST: 135,
                Location.SOUTHWEST: 45,
                Location.NORTHWEST: 315,
            }
        return direction_map.get(location, 0.0)

    def _calculate_float_rotation(
        self, motion: MotionData, location: Location
    ) -> float:
        """Calculate rotation for float arrows."""
        # Float rotation similar to pro/anti
        return self._calculate_pro_rotation(motion, location)

    def _calculate_adjustment(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> Any:
        """
        Calculate adjustment using complete validated adjustment system.

        This implements the complete adjustment pipeline:
        1. Default adjustments based on motion type and placement key
        2. Special adjustments for specific letters and configurations
        3. Quadrant-based directional adjustments"""
        motion = arrow_data.motion_data
        if not motion:
            return QPointF(0, 0)

        # Step 1: Get default adjustment using proper service integration
        default_adjustment = self._get_default_adjustment(arrow_data)

        # Step 2: Check for special adjustments (letter-specific overrides)
        special_adjustment = self._get_special_adjustment(arrow_data, pictograph_data)
        if special_adjustment is not None:
            # Special adjustment overrides default
            adjustment = special_adjustment
        else:
            # Use default adjustment
            adjustment = default_adjustment

        # Step 3: Apply quadrant-based directional adjustments
        final_adjustment = self._apply_quadrant_adjustments(
            arrow_data, adjustment, pictograph_data
        )

        return final_adjustment

    def _get_default_adjustment(self, arrow_data: ArrowData) -> Any:
        """Get default adjustment using data-driven placement system."""
        motion = arrow_data.motion_data
        if not motion:
            return QPointF(0, 0)

        # Generate placement key using the key service
        placement_key = self.placement_key_service.generate_placement_key(
            motion
        )  # Get adjustment from default placement service
        adjustment = self.default_placement_service.get_default_adjustment(
            motion, grid_mode="diamond", placement_key=placement_key
        )

        return adjustment

    def _get_special_adjustment(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> Union[Any, None]:
        """Get special adjustment for specific letters and configurations."""
        # CRITICAL FIX: Use cached service instance to avoid reloading JSON files on every call

        try:
            # Use cached service instance to avoid expensive JSON reloading
            if self._special_placement_service is None:
                from .special_placement_service import SpecialPlacementService

                self._special_placement_service = SpecialPlacementService()

            result = self._special_placement_service.get_special_adjustment(
                arrow_data, pictograph_data
            )

            return result
        except Exception:
            import traceback

            traceback.print_exc()
            return None

    def _apply_quadrant_adjustments(
        self,
        arrow_data: ArrowData,
        base_adjustment: PointType,
        pictograph_data: Optional[PictographData] = None,
    ) -> PointType:
        """Apply quadrant-based directional adjustments using positioning logic."""
        motion = arrow_data.motion_data
        if not motion:
            return base_adjustment

        # Step 1: Generate directional tuples for all 4 quadrants
        directional_tuples = self._generate_directional_tuples(
            motion, int(base_adjustment.x()), int(base_adjustment.y())
        )

        # Step 2: Get quadrant index for this arrow
        quadrant_index = self._get_quadrant_index(motion, pictograph_data)

        # Step 3: Apply the quadrant-specific adjustment
        if directional_tuples and 0 <= quadrant_index < len(directional_tuples):
            adjusted_x, adjusted_y = directional_tuples[quadrant_index]
            return QPointF(adjusted_x, adjusted_y)

        return base_adjustment

    def _generate_directional_tuples(
        self, motion: MotionData, x: int, y: int
    ) -> list[tuple[int, int]]:
        """Generate directional tuples for all 4 quadrants using positioning logic."""
        motion_type = motion.motion_type
        prop_rot_dir = motion.prop_rot_dir

        # Determine grid mode (simplified for now - always diamond)
        grid_mode = "diamond"

        if motion_type == MotionType.PRO:
            return self._get_pro_directional_tuples(grid_mode, prop_rot_dir, x, y)
        elif motion_type == MotionType.ANTI:
            return self._get_anti_directional_tuples(grid_mode, prop_rot_dir, x, y)
        elif motion_type == MotionType.STATIC:
            return self._get_static_directional_tuples(grid_mode, prop_rot_dir, x, y)
        elif motion_type == MotionType.DASH:
            return self._get_dash_directional_tuples(grid_mode, prop_rot_dir, x, y)
        elif motion_type == MotionType.FLOAT:
            return self._get_float_directional_tuples(motion, x, y)
        else:
            return [(x, y)] * 4

    def _get_pro_directional_tuples(
        self, grid_mode: str, prop_rot_dir: RotationDirection, x: int, y: int
    ) -> list[tuple[int, int]]:
        """Get PRO directional tuples using positioning mapping."""
        if grid_mode == "diamond":
            if prop_rot_dir == RotationDirection.CLOCKWISE:
                return [(x, y), (-y, x), (-x, -y), (y, -x)]
            else:  # COUNTER_CLOCKWISE
                return [(-y, -x), (x, -y), (y, x), (-x, y)]
        else:  # box mode
            if prop_rot_dir == RotationDirection.CLOCKWISE:
                return [(-x, y), (-y, -x), (x, -y), (y, x)]
            else:  # COUNTER_CLOCKWISE
                return [(x, y), (-y, x), (-x, -y), (y, -x)]

    def _get_anti_directional_tuples(
        self, grid_mode: str, prop_rot_dir: RotationDirection, x: int, y: int
    ) -> list[tuple[int, int]]:
        """Get ANTI directional tuples using positioning mapping."""
        if grid_mode == "diamond":
            if prop_rot_dir == RotationDirection.CLOCKWISE:
                return [(-y, -x), (x, -y), (y, x), (-x, y)]
            else:  # COUNTER_CLOCKWISE
                return [(x, y), (-y, x), (-x, -y), (y, -x)]
        else:  # box mode
            if prop_rot_dir == RotationDirection.CLOCKWISE:
                return [(-x, y), (-y, -x), (x, -y), (y, x)]
            else:  # COUNTER_CLOCKWISE
                return [(x, y), (-y, x), (-x, -y), (y, -x)]

    def _get_static_directional_tuples(
        self, grid_mode: str, prop_rot_dir: RotationDirection, x: int, y: int
    ) -> list[tuple[int, int]]:
        """Get STATIC directional tuples using positioning mapping."""
        if prop_rot_dir == RotationDirection.NO_ROTATION:
            return [(x, y), (-x, -y), (-y, x), (y, -x)]

        if grid_mode == "diamond":
            if prop_rot_dir == RotationDirection.CLOCKWISE:
                return [(x, -y), (y, x), (-x, y), (-y, -x)]
            else:  # COUNTER_CLOCKWISE
                return [(-x, -y), (y, -x), (x, y), (-y, x)]
        else:  # box mode
            if prop_rot_dir == RotationDirection.CLOCKWISE:
                return [(x, y), (-y, x), (-x, -y), (y, -x)]
            else:  # COUNTER_CLOCKWISE
                return [(-y, -x), (x, -y), (y, x), (-x, y)]

    def _get_dash_directional_tuples(
        self, grid_mode: str, prop_rot_dir: RotationDirection, x: int, y: int
    ) -> list[tuple[int, int]]:
        """Get DASH directional tuples using positioning mapping."""
        if grid_mode == "diamond":
            if prop_rot_dir == RotationDirection.CLOCKWISE:
                return [(x, -y), (y, x), (-x, y), (-y, -x)]
            elif prop_rot_dir == RotationDirection.COUNTER_CLOCKWISE:
                return [(-x, -y), (y, -x), (x, y), (-y, x)]
            else:  # NO_ROTATION
                return [(x, y), (-y, -x), (x, -y), (y, -x)]
        else:  # box mode
            if prop_rot_dir == RotationDirection.CLOCKWISE:
                return [(-y, x), (-x, -y), (y, -x), (x, y)]
            elif prop_rot_dir == RotationDirection.COUNTER_CLOCKWISE:
                return [(-x, y), (-y, -x), (x, -y), (y, x)]
            else:  # NO_ROTATION
                return [(x, y), (-y, x), (-x, -y), (y, -x)]

    def _get_float_directional_tuples(
        self, motion: MotionData, x: int, y: int
    ) -> list[tuple[int, int]]:
        """Get FLOAT directional tuples using positioning mapping."""
        # For now, use simplified float logic (CW handpath)
        # TODO: Implement handpath calculation for proper float direction
        return [(x, y), (-y, x), (-x, -y), (y, -x)]

    def _get_quadrant_index(
        self, motion: MotionData, pictograph_data: Optional[PictographData] = None
    ) -> int:
        """Get quadrant index for arrow using positioning logic."""
        # For diamond grid (simplified - always diamond for now)
        arrow_location = self._calculate_arrow_location(motion, pictograph_data)

        if motion.motion_type in [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT]:
            # Shift arrows use layer2 quadrant mapping
            location_to_index = {
                Location.NORTHEAST: 0,
                Location.SOUTHEAST: 1,
                Location.SOUTHWEST: 2,
                Location.NORTHWEST: 3,
            }
        else:  # STATIC, DASH
            # Static/dash arrows use hand point quadrant mapping
            location_to_index = {
                Location.NORTH: 0,
                Location.EAST: 1,
                Location.SOUTH: 2,
                Location.WEST: 3,
            }

        return location_to_index.get(arrow_location, 0)

    def _get_other_motion(
        self, current_motion: MotionData, pictograph_data: PictographData
    ) -> Optional[MotionData]:
        """Get the other motion from pictograph data (for Type 3 scenarios)."""
        if not pictograph_data.arrows:
            return None

        for arrow in pictograph_data.arrows.values():
            if arrow.motion_data and arrow.motion_data != current_motion:
                return arrow.motion_data
        return None
