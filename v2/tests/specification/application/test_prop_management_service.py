"""
Tests for PropManagementService.

Tests the prop management functionality including beta positioning,
prop separation, and overlap detection.
"""

import pytest
import pandas as pd
import random
from pathlib import Path
from PyQt6.QtCore import QPointF

from application.services.positioning.prop_management_service import (
    PropManagementService,
    IPropManagementService,
)
from domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    Location,
    RotationDirection,
    Orientation,
)

from domain.models.pictograph_models import PropType


def load_beta_ending_pictographs():
    """Load all pictographs that end at beta positions from the dataframe."""
    data_path = (
        Path(__file__).parent.parent.parent.parent.parent
        / "data"
        / "DiamondPictographDataframe.csv"
    )
    df = pd.read_csv(data_path)

    # Filter for pictographs that end at beta positions
    beta_ending = df[df["end_pos"].str.contains("beta", na=False)]
    return beta_ending


def create_beat_data_from_row(row):
    """Convert a dataframe row to BeatData object."""  # Map string values to enums
    motion_type_map = {
        "pro": MotionType.PRO,
        "anti": MotionType.ANTI,
        "static": MotionType.STATIC,
        "dash": MotionType.DASH,
    }
    rotation_map = {
        "cw": RotationDirection.CLOCKWISE,
        "ccw": RotationDirection.COUNTER_CLOCKWISE,
    }
    location_map = {
        "n": Location.NORTH,
        "e": Location.EAST,
        "s": Location.SOUTH,
        "w": Location.WEST,
        "ne": Location.NORTHEAST,
        "se": Location.SOUTHEAST,
        "sw": Location.SOUTHWEST,
        "nw": Location.NORTHWEST,
    }

    blue_motion = MotionData(
        motion_type=motion_type_map[row["blue_motion_type"]],
        prop_rot_dir=rotation_map[row["blue_prop_rot_dir"]],
        start_loc=location_map[row["blue_start_loc"]],
        end_loc=location_map[row["blue_end_loc"]],
    )

    red_motion = MotionData(
        motion_type=motion_type_map[row["red_motion_type"]],
        prop_rot_dir=rotation_map[row["red_prop_rot_dir"]],
        start_loc=location_map[row["red_start_loc"]],
        end_loc=location_map[row["red_end_loc"]],
    )

    return BeatData(
        beat_number=1,
        letter=row["letter"],
        blue_motion=blue_motion,
        red_motion=red_motion,
    )


@pytest.fixture
def prop_service():
    """Provide PropManagementService instance for testing."""
    return PropManagementService()


@pytest.fixture
def sample_beta_beat_data():
    """Provide sample beat data for beta positioning tests."""
    # Just use one of the known beta-ending letters
    return BeatData(
        beat_number=1,
        letter="H",  # H is a beta-ending letter
    )


@pytest.fixture
def sample_non_beta_beat_data():
    """Provide sample beat data without beta positioning."""
    return BeatData(
        beat_number=1,
        letter="A",  # A is not a beta-ending letter
    )


class TestPropManagementServiceInterface:
    """Test that PropManagementService implements the interface correctly."""

    def test_implements_interface(self, prop_service):
        """Test that service implements IPropManagementService."""
        assert isinstance(prop_service, IPropManagementService)

    def test_has_all_interface_methods(self, prop_service):
        """Test that service has all required interface methods."""
        required_methods = [
            "should_apply_beta_positioning",
            "apply_beta_positioning",
            "calculate_separation_offsets",
            "detect_prop_overlap",
        ]

        for method_name in required_methods:
            assert hasattr(prop_service, method_name)
            assert callable(getattr(prop_service, method_name))


class TestBetaPositioning:
    """Test beta prop positioning functionality."""

    def test_should_apply_beta_positioning_beta_letter(
        self, prop_service, sample_beta_beat_data
    ):
        """Test beta positioning detection for beta-ending letter."""
        should_apply = prop_service.should_apply_beta_positioning(sample_beta_beat_data)
        assert should_apply is True

    def test_should_apply_beta_positioning_non_beta_letter(
        self, prop_service, sample_non_beta_beat_data
    ):
        """Test beta positioning detection for non-beta letter."""
        should_apply = prop_service.should_apply_beta_positioning(
            sample_non_beta_beat_data
        )
        assert should_apply is False

    def test_should_apply_beta_positioning_no_overlap(self, prop_service):
        """Test beta positioning when props don't overlap."""
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
        )
        red_motion = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,  # Different end location = no overlap
        )

        beat_data = BeatData(
            beat_number=1,
            letter="Aβ",
            blue_motion=blue_motion,
            red_motion=red_motion,
        )

        should_apply = prop_service.should_apply_beta_positioning(beat_data)
        assert should_apply is False

    def test_should_apply_beta_positioning_no_letter(self, prop_service):
        """Test beta positioning with no letter."""
        beat_data = BeatData(beat_number=1, letter=None)

        should_apply = prop_service.should_apply_beta_positioning(beat_data)
        assert should_apply is False

    def test_should_apply_beta_positioning_no_motions(self, prop_service):
        """Test beta positioning with missing motions."""
        beat_data = BeatData(
            beat_number=1,
            letter="Aβ",
            blue_motion=None,
            red_motion=None,
        )

        should_apply = prop_service.should_apply_beta_positioning(beat_data)
        assert should_apply is False

    def test_apply_beta_positioning_returns_beat_data(
        self, prop_service, sample_beta_beat_data
    ):
        """Test that apply_beta_positioning returns BeatData."""
        result = prop_service.apply_beta_positioning(sample_beta_beat_data)
        assert isinstance(result, BeatData)

    def test_apply_beta_positioning_non_beta_returns_original(
        self, prop_service, sample_non_beta_beat_data
    ):
        """Test that non-beta letters return original data."""
        result = prop_service.apply_beta_positioning(sample_non_beta_beat_data)
        assert result == sample_non_beta_beat_data


class TestPropOverlapDetection:
    """Test prop overlap detection logic."""

    def test_detect_prop_overlap_same_location_same_orientation(self, prop_service):
        """Test overlap detection when props end at same location with same orientation."""
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=0,  # Even turns = same orientation
        )
        red_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=0,  # Even turns = same orientation
        )

        beat_data = BeatData(
            beat_number=1,
            blue_motion=blue_motion,
            red_motion=red_motion,
        )

        overlaps = prop_service.detect_prop_overlap(beat_data)
        assert overlaps is True

    def test_detect_prop_overlap_different_locations(self, prop_service):
        """Test overlap detection when props end at different locations."""
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
        )
        red_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,  # Different end location
        )

        beat_data = BeatData(
            beat_number=1,
            blue_motion=blue_motion,
            red_motion=red_motion,
        )

        overlaps = prop_service.detect_prop_overlap(beat_data)
        assert overlaps is False

    def test_detect_prop_overlap_no_motions(self, prop_service):
        """Test overlap detection with missing motions."""
        beat_data = BeatData(
            beat_number=1,
            blue_motion=None,
            red_motion=None,
        )

        overlaps = prop_service.detect_prop_overlap(beat_data)
        assert overlaps is False


class TestSeparationOffsets:
    """Test calculation of prop separation offsets."""

    def test_calculate_separation_offsets_returns_tuple(
        self, prop_service, sample_beta_beat_data
    ):
        """Test that calculate_separation_offsets returns tuple of QPointF."""
        blue_offset, red_offset = prop_service.calculate_separation_offsets(
            sample_beta_beat_data
        )

        assert isinstance(blue_offset, QPointF)
        assert isinstance(red_offset, QPointF)

    def test_calculate_separation_offsets_no_motions(self, prop_service):
        """Test separation offsets with missing motions."""
        beat_data = BeatData(
            beat_number=1,
            blue_motion=None,
            red_motion=None,
        )

        blue_offset, red_offset = prop_service.calculate_separation_offsets(beat_data)

        assert blue_offset == QPointF(0, 0)
        assert red_offset == QPointF(0, 0)

    def test_calculate_separation_offsets_blue_left_red_right(
        self, prop_service, sample_beta_beat_data
    ):
        """Test that blue prop typically moves left and red prop moves right."""
        blue_offset, red_offset = prop_service.calculate_separation_offsets(
            sample_beta_beat_data
        )

        # Blue should generally move left (negative x), red should move right (positive x)
        # The exact values depend on the direction calculation, but this tests the general pattern
        assert blue_offset.x() <= 0  # Blue moves left or diagonally left
        assert red_offset.x() >= 0  # Red moves right or diagonally right


class TestDirectionalOffsets:
    """Test directional offset calculations."""

    def test_calculate_directional_offset_basic_directions(self, prop_service):
        """Test offset calculation for basic directions."""
        # Test with default prop type (Hand)
        prop_type = PropType.HAND if hasattr(PropType, "HAND") else list(PropType)[0]

        left_offset = prop_service._calculate_directional_offset(
            prop_service.LEFT, prop_type
        )
        right_offset = prop_service._calculate_directional_offset(
            prop_service.RIGHT, prop_type
        )
        up_offset = prop_service._calculate_directional_offset(
            prop_service.UP, prop_type
        )
        down_offset = prop_service._calculate_directional_offset(
            prop_service.DOWN, prop_type
        )

        # Left should be negative x
        assert left_offset.x() < 0
        assert left_offset.y() == 0

        # Right should be positive x
        assert right_offset.x() > 0
        assert right_offset.y() == 0

        # Up should be negative y
        assert up_offset.x() == 0
        assert up_offset.y() < 0

        # Down should be positive y
        assert down_offset.x() == 0
        assert down_offset.y() > 0

    def test_calculate_directional_offset_diagonal_directions(self, prop_service):
        """Test offset calculation for diagonal directions."""
        prop_type = PropType.HAND if hasattr(PropType, "HAND") else list(PropType)[0]

        upleft_offset = prop_service._calculate_directional_offset(
            prop_service.UPLEFT, prop_type
        )
        downright_offset = prop_service._calculate_directional_offset(
            prop_service.DOWNRIGHT, prop_type
        )

        # Up-left should be negative x and y
        assert upleft_offset.x() < 0
        assert upleft_offset.y() < 0

        # Down-right should be positive x and y
        assert downright_offset.x() > 0
        assert downright_offset.y() > 0


class TestOrientationCalculations:
    """Test orientation calculations for props."""

    def test_calculate_end_orientation_pro_even_turns(self, prop_service):
        """Test end orientation calculation for PRO motion with even turns."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=2,  # Even turns
        )

        end_orientation = prop_service._calculate_end_orientation(motion)

        # PRO with even turns should keep same orientation
        assert end_orientation == Orientation.IN

    def test_calculate_end_orientation_pro_odd_turns(self, prop_service):
        """Test end orientation calculation for PRO motion with odd turns."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1,  # Odd turns
        )

        end_orientation = prop_service._calculate_end_orientation(motion)

        # PRO with odd turns should switch orientation
        assert end_orientation == Orientation.OUT

    def test_calculate_end_orientation_anti_even_turns(self, prop_service):
        """Test end orientation calculation for ANTI motion with even turns."""
        motion = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=2,  # Even turns
        )

        end_orientation = prop_service._calculate_end_orientation(motion)

        # ANTI with even turns should switch orientation
        assert end_orientation == Orientation.OUT

    def test_calculate_end_orientation_anti_odd_turns(self, prop_service):
        """Test end orientation calculation for ANTI motion with odd turns."""
        motion = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1,  # Odd turns
        )

        end_orientation = prop_service._calculate_end_orientation(motion)

        # ANTI with odd turns should keep same orientation
        assert end_orientation == Orientation.IN


class TestPropClassification:
    """Test prop classification functionality."""

    def test_classify_props_by_size_returns_dict(self, prop_service):
        """Test that prop classification returns expected dictionary structure."""
        beat_data = BeatData(beat_number=1)

        classification = prop_service.classify_props_by_size(beat_data)

        assert isinstance(classification, dict)
        assert "big_props" in classification
        assert "small_props" in classification
        assert "hands" in classification
        assert all(isinstance(category, list) for category in classification.values())

    def test_get_repositioning_strategy_returns_string(self, prop_service):
        """Test that repositioning strategy returns valid strategy name."""
        beat_data = BeatData(beat_number=1, letter="A")
        classification = {"big_props": [], "small_props": [], "hands": []}

        strategy = prop_service.get_repositioning_strategy(beat_data, classification)

        assert isinstance(strategy, str)
        assert strategy in [
            "big_prop_repositioning",
            "small_prop_repositioning",
            "hand_repositioning",
            "default_repositioning",
        ]
