"""
TEST LIFECYCLE: specification
CREATED: 2025-06-14
PURPOSE: Contract testing for ArrowManagementService consolidation
SCOPE: Unified arrow operations, positioning, mirroring, beta positioning
EXPECTED_DURATION: permanent
"""

import pytest
from typing import Tuple
from PyQt6.QtCore import QPointF

from application.services.positioning.arrow_management_service import (
    ArrowManagementService,
    IArrowManagementService,
)
from domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
    Orientation,
)
from domain.models.pictograph_models import (
    ArrowData,
    PictographData,
    GridData,
    GridMode,
)


@pytest.fixture
def arrow_service():
    """Provide ArrowManagementService instance for testing."""
    return ArrowManagementService()


@pytest.fixture
def sample_motion_data():
    """Provide sample motion data for testing."""
    return MotionData(
        motion_type=MotionType.PRO,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        turns=1.0,
    )


@pytest.fixture
def sample_arrow_data(sample_motion_data):
    """Provide sample arrow data for testing."""
    return ArrowData(
        color="blue",
        motion_data=sample_motion_data,
        is_visible=True,
        position_x=200,
        position_y=200,
        rotation_angle=0,
    )


@pytest.fixture
def sample_pictograph_data():
    """Provide sample pictograph data for testing."""
    grid_data = GridData(
        grid_mode=GridMode.DIAMOND,
        center_x=200.0,
        center_y=200.0,
        radius=100.0,
    )

    return PictographData(
        grid_data=grid_data,
        arrows={},
        props={},
        is_blank=False,
    )


class TestArrowManagementServiceInterface:
    """Test that ArrowManagementService implements the interface correctly."""

    def test_implements_interface(self, arrow_service):
        """Test that service implements IArrowManagementService."""
        assert isinstance(arrow_service, IArrowManagementService)

    def test_has_all_interface_methods(self, arrow_service):
        """Test that service has all required interface methods."""
        required_methods = [
            "calculate_arrow_position",
            "should_mirror_arrow",
            "calculate_all_arrow_positions",
        ]

        for method_name in required_methods:
            assert hasattr(arrow_service, method_name)
            assert callable(getattr(arrow_service, method_name))


class TestArrowPositioning:
    """Test arrow positioning calculations."""

    def test_calculate_arrow_position_returns_tuple(
        self, arrow_service, sample_arrow_data, sample_pictograph_data
    ):
        """Test that calculate_arrow_position returns (x, y, rotation) tuple."""
        result = arrow_service.calculate_arrow_position(
            sample_arrow_data, sample_pictograph_data
        )

        assert isinstance(result, tuple)
        assert len(result) == 3

        x, y, rotation = result
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        assert isinstance(rotation, (int, float))

    def test_calculate_arrow_position_with_no_motion(
        self, arrow_service, sample_pictograph_data
    ):
        """Test positioning with arrow that has no motion data."""
        arrow_data = ArrowData(
            color="blue",
            motion_data=None,
            is_visible=True,
        )

        x, y, rotation = arrow_service.calculate_arrow_position(
            arrow_data, sample_pictograph_data
        )

        # Should return center position with no rotation
        assert x == arrow_service.CENTER_X
        assert y == arrow_service.CENTER_Y
        assert rotation == 0.0

    def test_calculate_arrow_position_pro_motion(
        self, arrow_service, sample_pictograph_data
    ):
        """Test positioning for PRO motion type."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
        )

        arrow_data = ArrowData(
            color="blue",
            motion_data=motion,
            is_visible=True,
        )

        x, y, rotation = arrow_service.calculate_arrow_position(
            arrow_data, sample_pictograph_data
        )

        # PRO motion should use layer2 coordinates for end location
        expected_pos = arrow_service.LAYER2_POINTS[Location.SOUTH]
        assert abs(x - expected_pos.x()) < 50  # Allow for adjustments
        assert abs(y - expected_pos.y()) < 50  # Allow for adjustments

    def test_calculate_arrow_position_static_motion(
        self, arrow_service, sample_pictograph_data
    ):
        """Test positioning for STATIC motion type."""
        motion = MotionData(
            motion_type=MotionType.STATIC,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.EAST,
            end_loc=Location.EAST,
            turns=0.0,
        )

        arrow_data = ArrowData(
            color="red",
            motion_data=motion,
            is_visible=True,
        )

        x, y, rotation = arrow_service.calculate_arrow_position(
            arrow_data, sample_pictograph_data
        )

        # STATIC motion should use hand point coordinates for start location
        expected_pos = arrow_service.HAND_POINTS[Location.EAST]
        assert abs(x - expected_pos.x()) < 50  # Allow for adjustments
        assert abs(y - expected_pos.y()) < 50  # Allow for adjustments


class TestArrowMirroring:
    """Test arrow mirroring logic."""

    def test_should_mirror_arrow_anti_clockwise(self, arrow_service):
        """Test mirroring for ANTI motion with clockwise rotation."""
        motion = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
        )

        arrow_data = ArrowData(color="blue", motion_data=motion)

        should_mirror = arrow_service.should_mirror_arrow(arrow_data)
        assert should_mirror is True

    def test_should_mirror_arrow_anti_counter_clockwise(self, arrow_service):
        """Test mirroring for ANTI motion with counter-clockwise rotation."""
        motion = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
        )

        arrow_data = ArrowData(color="blue", motion_data=motion)

        should_mirror = arrow_service.should_mirror_arrow(arrow_data)
        assert should_mirror is False

    def test_should_mirror_arrow_pro_clockwise(self, arrow_service):
        """Test mirroring for PRO motion with clockwise rotation."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
        )

        arrow_data = ArrowData(color="blue", motion_data=motion)

        should_mirror = arrow_service.should_mirror_arrow(arrow_data)
        assert should_mirror is False

    def test_should_mirror_arrow_no_motion(self, arrow_service):
        """Test mirroring with no motion data."""
        arrow_data = ArrowData(color="blue", motion_data=None)

        should_mirror = arrow_service.should_mirror_arrow(arrow_data)
        assert should_mirror is False


class TestCalculateAllArrowPositions:
    """Test calculation of all arrow positions in pictograph."""

    def test_calculate_all_arrow_positions_empty_pictograph(
        self, arrow_service, sample_pictograph_data
    ):
        """Test with pictograph that has default arrows but no motion data."""
        result = arrow_service.calculate_all_arrow_positions(sample_pictograph_data)

        assert isinstance(result, PictographData)
        # Pictographs always have blue and red arrows (legacy pattern)
        assert len(result.arrows) == 2
        assert "blue" in result.arrows
        assert "red" in result.arrows
        # But they should have no motion data
        assert result.arrows["blue"].motion_data is None
        assert result.arrows["red"].motion_data is None

    def test_calculate_all_arrow_positions_with_arrows(self, arrow_service):
        """Test with pictograph containing arrows."""
        # Create pictograph with arrows
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
        )

        blue_arrow = ArrowData(
            color="blue",
            motion_data=blue_motion,
            is_visible=True,
        )

        grid_data = GridData(
            grid_mode=GridMode.DIAMOND,
            center_x=200.0,
            center_y=200.0,
            radius=100.0,
        )

        pictograph = PictographData(
            grid_data=grid_data,
            arrows={"blue": blue_arrow},
            props={},
            is_blank=False,
        )

        result = arrow_service.calculate_all_arrow_positions(pictograph)

        assert isinstance(result, PictographData)
        assert "blue" in result.arrows

        # Arrow should have updated position
        updated_arrow = result.arrows["blue"]
        assert updated_arrow.position_x is not None
        assert updated_arrow.position_y is not None
        assert updated_arrow.rotation_angle is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
