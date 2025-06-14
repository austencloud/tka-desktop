"""
Pictograph Service for Kinetic Constructor v2

This service handles all business logic for pictograph creation, manipulation,
and positioning calculations. It integrates with the existing v2 architecture
and provides clean separation between business logic and UI.

REPLACES:
- Scattered pictograph logic in UI components
- Direct manipulation of pictograph objects
- Complex manager classes with UI coupling

PROVIDES:
- Clean business logic for pictograph operations
- Arrow and prop positioning calculations
- Immutable data transformations
- Dependency injection support
"""

from typing import Dict, Optional, Tuple
from abc import ABC, abstractmethod

from ...core.interfaces.core_services import ILayoutService
from domain.models.pictograph_models import (
    PictographData,
    ArrowData,
    PropData,
    GridData,
    GridMode,
    ArrowType,
    PropType,
)
from domain.models.core_models import MotionData, BeatData


class IPictographService(ABC):
    """Interface for pictograph service operations."""

    @abstractmethod
    def create_pictograph(self, beat_data: Optional[BeatData] = None) -> PictographData:
        """Create a new pictograph from beat data."""
        pass

    @abstractmethod
    def update_pictograph_from_beat(
        self, pictograph: PictographData, beat_data: BeatData
    ) -> PictographData:
        """Update a pictograph with new beat data."""
        pass

    @abstractmethod
    def calculate_arrow_positions(self, pictograph: PictographData) -> PictographData:
        """Calculate and update arrow positions."""
        pass

    @abstractmethod
    def calculate_prop_positions(self, pictograph: PictographData) -> PictographData:
        """Calculate and update prop positions."""
        pass

    @abstractmethod
    def create_grid_data(
        self, grid_mode: GridMode, size: Tuple[float, float]
    ) -> GridData:
        """Create grid data for the specified mode and size."""
        pass


class PictographService(IPictographService):
    """
    Service for pictograph business logic.

    Handles all pictograph operations using dependency injection
    and immutable data structures.
    """

    def __init__(self, layout_service: ILayoutService):
        """Initialize with injected dependencies."""
        self.layout_service = layout_service

        # Import here to avoid circular imports
        from .arrow_positioning_service import ArrowPositioningService

        self.arrow_positioning_service = ArrowPositioningService()

    def create_pictograph(self, beat_data: Optional[BeatData] = None) -> PictographData:
        """
        Create a new pictograph from beat data.

        Args:
            beat_data: Optional beat data to initialize the pictograph

        Returns:
            New PictographData instance
        """
        # Create default grid data
        grid_data = self.create_grid_data(GridMode.DIAMOND, (400, 400))

        # Create base pictograph
        pictograph = PictographData(
            grid_data=grid_data, is_blank=beat_data is None or beat_data.is_blank
        )

        # Update with beat data if provided
        if beat_data and not beat_data.is_blank:
            pictograph = self.update_pictograph_from_beat(pictograph, beat_data)

        return pictograph

    def update_pictograph_from_beat(
        self, pictograph: PictographData, beat_data: BeatData
    ) -> PictographData:
        """
        Update a pictograph with new beat data.

        Args:
            pictograph: Current pictograph data
            beat_data: Beat data to apply

        Returns:
            Updated PictographData instance
        """
        # Update basic properties
        updated_pictograph = pictograph.update(
            letter=beat_data.letter, is_blank=beat_data.is_blank
        )

        # Update arrows with motion data
        if beat_data.blue_motion:
            blue_arrow = self._create_arrow_from_motion("blue", beat_data.blue_motion)
            arrow_dict = blue_arrow.to_dict()
            arrow_dict.pop("color", None)  # Remove color to avoid conflict
            updated_pictograph = updated_pictograph.update_arrow("blue", **arrow_dict)

        if beat_data.red_motion:
            red_arrow = self._create_arrow_from_motion("red", beat_data.red_motion)
            arrow_dict = red_arrow.to_dict()
            arrow_dict.pop("color", None)  # Remove color to avoid conflict
            updated_pictograph = updated_pictograph.update_arrow("red", **arrow_dict)

        # Update props with motion data
        if beat_data.blue_motion:
            blue_prop = self._create_prop_from_motion("blue", beat_data.blue_motion)
            prop_dict = blue_prop.to_dict()
            prop_dict.pop("color", None)  # Remove color to avoid conflict
            updated_pictograph = updated_pictograph.update_prop("blue", **prop_dict)

        if beat_data.red_motion:
            red_prop = self._create_prop_from_motion("red", beat_data.red_motion)
            prop_dict = red_prop.to_dict()
            prop_dict.pop("color", None)  # Remove color to avoid conflict
            updated_pictograph = updated_pictograph.update_prop("red", **prop_dict)

        # Calculate positions
        updated_pictograph = self.calculate_arrow_positions(updated_pictograph)
        updated_pictograph = self.calculate_prop_positions(updated_pictograph)

        return updated_pictograph

    def calculate_arrow_positions(self, pictograph: PictographData) -> PictographData:
        """
        Calculate and update arrow positions using v1 algorithms.

        Args:
            pictograph: Current pictograph data

        Returns:
            Updated PictographData with calculated arrow positions
        """
        # Use the v1-based arrow positioning service
        return self.arrow_positioning_service.calculate_all_arrow_positions(pictograph)

    def calculate_prop_positions(self, pictograph: PictographData) -> PictographData:
        """
        Calculate and update prop positions.

        Args:
            pictograph: Current pictograph data

        Returns:
            Updated PictographData with calculated prop positions
        """
        # TODO: Integrate the prop positioning system from v1
        # For now, use simplified positioning

        updated_pictograph = pictograph

        # Calculate blue prop position
        if "blue" in pictograph.props:
            blue_prop = pictograph.blue_prop
            if blue_prop.motion_data:
                position_x, position_y = self._calculate_simple_prop_position(
                    blue_prop, pictograph.grid_data, "blue"
                )
                updated_pictograph = updated_pictograph.update_prop(
                    "blue", position_x=position_x, position_y=position_y
                )

        # Calculate red prop position
        if "red" in pictograph.props:
            red_prop = pictograph.red_prop
            if red_prop.motion_data:
                position_x, position_y = self._calculate_simple_prop_position(
                    red_prop, pictograph.grid_data, "red"
                )
                updated_pictograph = updated_pictograph.update_prop(
                    "red", position_x=position_x, position_y=position_y
                )

        return updated_pictograph

    def create_grid_data(
        self, grid_mode: GridMode, size: Tuple[float, float]
    ) -> GridData:
        """
        Create grid data for the specified mode and size.

        Args:
            grid_mode: Grid mode (diamond or box)
            size: (width, height) of the grid area

        Returns:
            GridData instance with calculated grid points
        """
        width, height = size
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) / 3  # Use 1/3 of the smaller dimension

        # Calculate grid points based on mode
        grid_points = self._calculate_grid_points(grid_mode, center_x, center_y, radius)

        return GridData(
            grid_mode=grid_mode,
            center_x=center_x,
            center_y=center_y,
            radius=radius,
            grid_points=grid_points,
        )

    def _create_arrow_from_motion(
        self, color: str, motion_data: MotionData
    ) -> ArrowData:
        """Create arrow data from motion data."""
        arrow_type = ArrowType.BLUE if color == "blue" else ArrowType.RED

        return ArrowData(
            arrow_type=arrow_type,
            motion_data=motion_data,
            color=color,
            turns=motion_data.turns,
            is_visible=True,
        )

    def _create_prop_from_motion(self, color: str, motion_data: MotionData) -> PropData:
        """Create prop data from motion data."""
        return PropData(
            prop_type=PropType.STAFF,  # Default to staff for now
            motion_data=motion_data,
            color=color,
            rotation_direction=motion_data.prop_rot_dir.value,
            is_visible=True,
        )

    def _calculate_simple_arrow_position(
        self, arrow: ArrowData, grid: GridData, color: str
    ) -> Tuple[float, float]:
        """Simplified arrow positioning - will be replaced with full system."""
        # Basic positioning based on color
        offset = 20 if color == "blue" else -20
        return grid.center_x + offset, grid.center_y + offset

    def _calculate_simple_prop_position(
        self, prop: PropData, grid: GridData, color: str
    ) -> Tuple[float, float]:
        """Simplified prop positioning - will be replaced with full system."""
        # Basic positioning based on color
        offset = 30 if color == "blue" else -30
        return grid.center_x + offset, grid.center_y + offset

    def _calculate_grid_points(
        self, grid_mode: GridMode, center_x: float, center_y: float, radius: float
    ) -> Dict[str, Tuple[float, float]]:
        """Calculate grid points for the specified mode."""
        # Simplified grid calculation - will be replaced with full system
        points = {}

        if grid_mode == GridMode.DIAMOND:
            # Diamond grid points
            points["alpha1"] = (center_x, center_y - radius)
            points["alpha3"] = (center_x + radius, center_y)
            points["alpha5"] = (center_x, center_y + radius)
            points["alpha7"] = (center_x - radius, center_y)
        else:
            # Box grid points
            points["alpha2"] = (center_x + radius * 0.7, center_y - radius * 0.7)
            points["alpha4"] = (center_x + radius * 0.7, center_y + radius * 0.7)
            points["alpha6"] = (center_x - radius * 0.7, center_y + radius * 0.7)
            points["alpha8"] = (center_x - radius * 0.7, center_y - radius * 0.7)

        return points
