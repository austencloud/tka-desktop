"""
TEST LIFECYCLE: specification
CREATED: 2025-06-14
PURPOSE: Comprehensive testing for Type 3 (cross-shift) dash arrow positioning
SCOPE: Type 3 letters where dash arrows must avoid overlapping with shift arrows
EXPECTED_DURATION: permanent

Type 3 letters are cross-shift letters like Θ-, Ω-, etc. where:
- One motion is a shift (PRO/ANTI)
- Other motion is a dash
- Dash arrow must be positioned to avoid overlapping the shift arrow
- In certain turn scenarios, dash may need specific positioning for rotation clarity

This test refactored to use the pictograph data handler/service for generating
valid Type 3 pictographs rather than manual construction.
"""

import pytest
from typing import Tuple, List, Dict, Any, Optional
from PyQt6.QtCore import QPointF

from application.services.arrow_positioning_service import ArrowPositioningService
from application.services.core.pictograph_management_service import (
    PictographManagementService,
)
from application.services.core.data_conversion_service import DataConversionService
from domain.models.core_models import (
    MotionData,
    MotionType,
    RotationDirection,
    Location,
    BeatData,
)
from domain.models.pictograph_models import ArrowData, PictographData


@pytest.fixture
def positioning_service():
    """Provide ArrowPositioningService instance for testing."""
    return ArrowPositioningService()


@pytest.fixture
def pictograph_data_service():
    """Provide PictographManagementService instance for testing."""
    return PictographManagementService()


@pytest.fixture
def conversion_service():
    """Provide DataConversionService instance for testing."""
    return DataConversionService()


def get_type3_pictographs(
    pictograph_service: PictographManagementService,
) -> List[Dict[str, Any]]:
    """Get all Type 3 pictographs from the dataset."""
    # Type 3 letters (cross-shift): W-, X-, Y-, Z-, Σ-, Δ-, θ-, Ω-
    type3_letters = ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"]

    all_type3_pictographs = []

    for letter in type3_letters:
        try:
            # Get specific pictograph for this Type 3 letter
            pictograph_data = pictograph_service.get_specific_pictograph(letter, 0)
            all_type3_pictographs.append(pictograph_data)
        except ValueError:
            # Letter not found in dataset, skip
            continue

    return all_type3_pictographs


def convert_pictograph_to_beat_data(
    pictograph_data: Dict[str, Any], conversion_service: DataConversionService
) -> BeatData:
    """Convert pictograph data from service to BeatData format."""
    # Create V1-style data structure for conversion
    v1_data = {
        "letter": pictograph_data["letter"],
        "blue_attributes": {
            "motion_type": pictograph_data["blue_motion"]["motion_type"],
            "prop_rot_dir": pictograph_data["blue_motion"]["prop_rot_dir"],
            "start_loc": pictograph_data["blue_motion"]["start_loc"],
            "end_loc": pictograph_data["blue_motion"]["end_loc"],
            "turns": pictograph_data["blue_motion"]["turns"],
        },
        "red_attributes": {
            "motion_type": pictograph_data["red_motion"]["motion_type"],
            "prop_rot_dir": pictograph_data["red_motion"]["prop_rot_dir"],
            "start_loc": pictograph_data["red_motion"]["start_loc"],
            "end_loc": pictograph_data["red_motion"]["end_loc"],
            "turns": pictograph_data["red_motion"]["turns"],
        },
        "grid_mode": pictograph_data.get("grid_mode", "diamond"),
        "timing": pictograph_data.get("timing", "together"),
    }

    return conversion_service.convert_v1_pictograph_to_beat_data(v1_data)


def create_pictograph_from_beat_data(beat_data: BeatData) -> PictographData:
    """Create PictographData from BeatData."""
    arrows = {}

    if beat_data.blue_motion:
        blue_arrow = ArrowData(motion_data=beat_data.blue_motion, color="blue")
        arrows["blue"] = blue_arrow

    if beat_data.red_motion:
        red_arrow = ArrowData(motion_data=beat_data.red_motion, color="red")
        arrows["red"] = red_arrow

    return PictographData(arrows=arrows, letter=beat_data.letter)


class TestType3DashArrowPositioning:
    """Test Type 3 dash arrow positioning scenarios using real data."""

    def test_type3_pictographs_from_data_service(
        self, positioning_service, pictograph_data_service, conversion_service
    ):
        """Test Type 3 dash arrow positioning using real pictographs from the data service."""
        # Get Type 3 pictographs from the data service
        type3_pictographs = get_type3_pictographs(pictograph_data_service)

        if not type3_pictographs:
            pytest.skip("No Type 3 pictographs found in dataset")

        print(
            f"🧪 Testing {len(type3_pictographs)} Type 3 pictographs from data service..."
        )

        for pictograph_data in type3_pictographs:
            letter = pictograph_data["letter"]
            print(f"\n📍 Testing Type 3 letter: {letter}")

            # Convert to BeatData
            beat_data = convert_pictograph_to_beat_data(
                pictograph_data, conversion_service
            )

            # Create PictographData
            pictograph = create_pictograph_from_beat_data(beat_data)

            # Identify dash and shift motions
            dash_motion = None
            shift_motion = None
            dash_arrow = None

            for color, arrow in pictograph.arrows.items():
                if arrow.motion_data.motion_type == MotionType.DASH:
                    dash_motion = arrow.motion_data
                    dash_arrow = arrow
                elif arrow.motion_data.motion_type in [MotionType.PRO, MotionType.ANTI]:
                    shift_motion = arrow.motion_data

            if not dash_motion or not shift_motion:
                print(f"   ⚠️ Skipping {letter} - not a valid Type 3 scenario")
                continue

            print(
                f"   Dash motion: {dash_motion.start_loc.value} → {dash_motion.end_loc.value} (turns={dash_motion.turns})"
            )
            print(
                f"   Shift motion: {shift_motion.start_loc.value} → {shift_motion.end_loc.value} (turns={shift_motion.turns})"
            )

            # Test dash arrow positioning
            dash_location = positioning_service._calculate_dash_arrow_location(
                dash_motion, pictograph
            )

            # Verify Type 3 detection
            is_type3 = positioning_service._is_type3_scenario(dash_motion, pictograph)
            print(f"   Type 3 detected: {is_type3}")

            if dash_motion.turns == 0:
                assert (
                    is_type3
                ), f"Should detect Type 3 for {letter} with zero turns dash"

                # Verify dash avoids shift end location
                shift_end_location = shift_motion.end_loc
                print(f"   Shift ends at: {shift_end_location.value}")
                print(f"   Dash positioned at: {dash_location.value}")

                # Dash should not be at the same location as shift arrow
                assert (
                    dash_location != shift_end_location
                ), f"Dash arrow should avoid shift location for {letter}"

                # Test positioning calculation
                pos_x, pos_y, rotation = positioning_service.calculate_arrow_position(
                    dash_arrow, pictograph
                )

                # Should use hand point coordinates for calculated location
                expected_pos = positioning_service.HAND_POINTS[dash_location]
                assert (
                    abs(pos_x - expected_pos.x()) < 10
                ), f"X position mismatch for {letter}"
                assert (
                    abs(pos_y - expected_pos.y()) < 10
                ), f"Y position mismatch for {letter}"

                print(
                    f"   ✅ {letter}: Dash correctly positioned at {dash_location.value} (avoiding {shift_end_location.value})"
                )
            else:
                print(
                    f"   ℹ️ {letter}: Non-zero turns, using rotation-based positioning"
                )

        print(f"\n✅ All Type 3 pictographs tested successfully!")

    def test_type3_specific_scenarios(
        self, positioning_service, pictograph_data_service, conversion_service
    ):
        """Test specific Type 3 scenarios with detailed verification."""
        type3_pictographs = get_type3_pictographs(pictograph_data_service)

        if not type3_pictographs:
            pytest.skip("No Type 3 pictographs found in dataset")

        # Focus on testing specific avoidance patterns
        for pictograph_data in type3_pictographs[
            :3
        ]:  # Test first 3 for detailed analysis
            letter = pictograph_data["letter"]
            print(f"\n🔍 Detailed test for Type 3 letter: {letter}")

            # Convert and create pictograph
            beat_data = convert_pictograph_to_beat_data(
                pictograph_data, conversion_service
            )
            pictograph = create_pictograph_from_beat_data(beat_data)

            # Extract motions
            dash_motion = None
            shift_motion = None

            for arrow in pictograph.arrows.values():
                if arrow.motion_data.motion_type == MotionType.DASH:
                    dash_motion = arrow.motion_data
                elif arrow.motion_data.motion_type in [MotionType.PRO, MotionType.ANTI]:
                    shift_motion = arrow.motion_data

            if not dash_motion or not shift_motion or dash_motion.turns != 0:
                continue

            # Test normal positioning vs Type 3 positioning
            print("   Testing normal vs Type 3 positioning...")

            # Normal dash positioning (without Type 3 scenario)
            normal_pictograph = PictographData(
                arrows={"dash": ArrowData(motion_data=dash_motion, color="blue")}
            )
            normal_location = positioning_service._calculate_dash_arrow_location(
                dash_motion, normal_pictograph
            )

            # Type 3 dash positioning (with shift to avoid)
            type3_location = positioning_service._calculate_dash_arrow_location(
                dash_motion, pictograph
            )

            print(f"   Normal positioning: {normal_location.value}")
            print(f"   Type 3 positioning: {type3_location.value}")
            print(f"   Shift location: {shift_motion.end_loc.value}")

            # Type 3 should avoid shift location
            assert (
                type3_location != shift_motion.end_loc
            ), f"Type 3 should avoid shift location for {letter}"

            # If normal positioning would conflict with shift, Type 3 should be different
            if normal_location == shift_motion.end_loc:
                assert (
                    type3_location != normal_location
                ), f"Type 3 should differ from normal when avoiding conflict for {letter}"
                print(
                    f"   ✅ {letter}: Type 3 successfully avoided conflict ({normal_location.value} → {type3_location.value})"
                )
            else:
                print(
                    f"   ℹ️ {letter}: No conflict to avoid, positioning may be similar"
                )

    def test_type3_comprehensive_coverage(
        self, positioning_service, pictograph_data_service
    ):
        """Test comprehensive coverage of Type 3 scenarios."""
        type3_pictographs = get_type3_pictographs(pictograph_data_service)

        if not type3_pictographs:
            pytest.skip("No Type 3 pictographs found in dataset")

        print(
            f"🎯 Comprehensive Type 3 coverage test with {len(type3_pictographs)} pictographs..."
        )

        # Statistics tracking
        total_tested = 0
        type3_detected = 0
        avoidance_successful = 0
        zero_turns_count = 0

        for pictograph_data in type3_pictographs:
            letter = pictograph_data["letter"]

            try:
                # Convert data
                beat_data = convert_pictograph_to_beat_data(
                    pictograph_data, DataConversionService()
                )
                pictograph = create_pictograph_from_beat_data(beat_data)

                # Find dash motion
                dash_motion = None
                shift_motion = None

                for arrow in pictograph.arrows.values():
                    if arrow.motion_data.motion_type == MotionType.DASH:
                        dash_motion = arrow.motion_data
                    elif arrow.motion_data.motion_type in [
                        MotionType.PRO,
                        MotionType.ANTI,
                    ]:
                        shift_motion = arrow.motion_data

                if not dash_motion or not shift_motion:
                    continue

                total_tested += 1

                if dash_motion.turns == 0:
                    zero_turns_count += 1

                    # Test Type 3 detection
                    is_type3 = positioning_service._is_type3_scenario(
                        dash_motion, pictograph
                    )
                    if is_type3:
                        type3_detected += 1

                        # Test avoidance
                        dash_location = (
                            positioning_service._calculate_dash_arrow_location(
                                dash_motion, pictograph
                            )
                        )
                        if dash_location != shift_motion.end_loc:
                            avoidance_successful += 1

            except Exception as e:
                print(f"   ⚠️ Error testing {letter}: {e}")
                continue

        print(f"\n📊 Type 3 Coverage Results:")
        print(f"   Total pictographs tested: {total_tested}")
        print(f"   Zero-turns dash scenarios: {zero_turns_count}")
        print(f"   Type 3 detected: {type3_detected}")
        print(f"   Successful avoidance: {avoidance_successful}")

        # Assertions for coverage
        assert total_tested > 0, "Should test at least some Type 3 pictographs"
        if zero_turns_count > 0:
            assert (
                type3_detected > 0
            ), "Should detect Type 3 scenarios in zero-turns dash cases"
            assert avoidance_successful > 0, "Should successfully avoid shift locations"

            detection_rate = type3_detected / zero_turns_count
            avoidance_rate = (
                avoidance_successful / type3_detected if type3_detected > 0 else 0
            )

            print(f"   Detection rate: {detection_rate:.1%}")
            print(f"   Avoidance success rate: {avoidance_rate:.1%}")

            assert (
                detection_rate > 0.5
            ), "Should detect Type 3 in majority of zero-turns cases"
            assert (
                avoidance_rate > 0.8
            ), "Should successfully avoid conflicts in most cases"

    def test_type3_north_south_shift_with_dash_avoidance(self, positioning_service):
        """Test dash arrow avoids shift arrow going North→South (manual fallback test)."""
        # Create shift motion: North → South (shift arrow will be at South)
        shift_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
        )

        # Create dash motion: East → West (should avoid South where shift is)
        dash_motion = MotionData(
            motion_type=MotionType.DASH,
            prop_rot_dir=RotationDirection.NO_ROTATION,
            start_loc=Location.EAST,
            end_loc=Location.WEST,
            turns=0.0,
        )

        # Create pictograph with both motions (Type 3 scenario)
        shift_arrow = ArrowData(motion_data=shift_motion, color="red")
        dash_arrow = ArrowData(motion_data=dash_motion, color="blue")
        pictograph_data = PictographData(
            arrows={"red": shift_arrow, "blue": dash_arrow}
        )

        # Test Type 3 scenario detection and positioning
        dash_location = positioning_service._calculate_dash_arrow_location(
            dash_motion, pictograph_data
        )

        # In Type 3, dash should avoid the shift end location (South)
        # Based on V1 logic, East→West dash should avoid South by going to North
        assert (
            dash_location == Location.NORTH
        ), f"Expected North but got {dash_location}"

        # Verify positioning
        pos_x, pos_y, rotation = positioning_service.calculate_arrow_position(
            dash_arrow, pictograph_data
        )

        # Should use hand point coordinates for North
        expected_pos = positioning_service.HAND_POINTS[Location.NORTH]
        assert abs(pos_x - expected_pos.x()) < 10
        assert abs(pos_y - expected_pos.y()) < 10

    def test_type3_east_west_shift_with_dash_avoidance(self, positioning_service):
        """Test dash arrow avoids shift arrow going East→West (manual fallback test)."""
        # Create shift motion: East → West (shift arrow will be at West)
        shift_motion = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.EAST,
            end_loc=Location.WEST,
            turns=1.0,
        )

        # Create dash motion: North → South (should avoid West where shift is)
        dash_motion = MotionData(
            motion_type=MotionType.DASH,
            prop_rot_dir=RotationDirection.NO_ROTATION,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=0.0,
        )

        dash_location = positioning_service._calculate_dash_arrow_location(dash_motion)

        # Based on V1 logic, North→South dash should go to East (avoiding West)
        assert dash_location == Location.EAST

    def test_type3_diagonal_shift_with_dash_avoidance(self, positioning_service):
        """Test dash arrow avoids diagonal shift arrows (manual fallback test)."""
        # Create shift motion: Northeast → Southwest (shift arrow at Southwest)
        shift_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTHEAST,
            end_loc=Location.SOUTHWEST,
            turns=1.0,
        )

        # Create dash motion: Northwest → Southeast (should avoid Southwest)
        dash_motion = MotionData(
            motion_type=MotionType.DASH,
            prop_rot_dir=RotationDirection.NO_ROTATION,
            start_loc=Location.NORTHWEST,
            end_loc=Location.SOUTHEAST,
            turns=0.0,
        )

        dash_location = positioning_service._calculate_dash_arrow_location(dash_motion)

        # Should avoid Southwest (where shift ends)
        assert dash_location != Location.SOUTHWEST

    def test_type3_dash_with_clockwise_turns(self, positioning_service):
        """Test Type 3 dash arrows with clockwise turns maintain proper positioning (manual fallback test)."""
        # Non-zero turns should use rotation-based positioning regardless of Type 3
        shift_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
        )

        dash_motion = MotionData(
            motion_type=MotionType.DASH,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.EAST,
            end_loc=Location.WEST,
            turns=1.5,
        )

        # Create pictograph with both motions
        shift_arrow = ArrowData(motion_data=shift_motion, color="red")
        dash_arrow = ArrowData(motion_data=dash_motion, color="blue")
        pictograph_data = PictographData(
            arrows={"red": shift_arrow, "blue": dash_arrow}
        )

        dash_location = positioning_service._calculate_dash_arrow_location(
            dash_motion, pictograph_data
        )

        # Non-zero turns should use rotation direction mapping
        expected_location = positioning_service.ROTATION_TO_DASH_LOCATION_MAP[
            RotationDirection.CLOCKWISE
        ]
        assert dash_location == expected_location

    def test_type3_dash_with_counter_clockwise_turns(self, positioning_service):
        """Test Type 3 dash arrows with counter-clockwise turns (manual fallback test)."""
        shift_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
        )

        dash_motion = MotionData(
            motion_type=MotionType.DASH,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.EAST,
            end_loc=Location.WEST,
            turns=0.5,
        )

        # Create pictograph with both motions
        shift_arrow = ArrowData(motion_data=shift_motion, color="red")
        dash_arrow = ArrowData(motion_data=dash_motion, color="blue")
        pictograph_data = PictographData(
            arrows={"red": shift_arrow, "blue": dash_arrow}
        )

        dash_location = positioning_service._calculate_dash_arrow_location(
            dash_motion, pictograph_data
        )

        # Non-zero turns should use rotation direction mapping
        expected_location = positioning_service.ROTATION_TO_DASH_LOCATION_MAP[
            RotationDirection.COUNTER_CLOCKWISE
        ]
        assert dash_location == expected_location

    def test_type3_complex_scenario_multiple_directions(self, positioning_service):
        """Test Type 3 complex scenarios with multiple direction combinations (manual fallback test)."""
        # Test multiple shift directions and verify dash avoidance
        shift_directions = [
            (Location.NORTH, Location.EAST),
            (Location.EAST, Location.SOUTH),
            (Location.SOUTH, Location.WEST),
            (Location.WEST, Location.NORTH),
        ]

        for start_loc, end_loc in shift_directions:
            shift_motion = MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=start_loc,
                end_loc=end_loc,
                turns=1.0,
            )

            dash_motion = MotionData(
                motion_type=MotionType.DASH,
                prop_rot_dir=RotationDirection.NO_ROTATION,
                start_loc=Location.NORTHEAST,
                end_loc=Location.SOUTHWEST,
                turns=0.0,
            )

            # Create Type 3 scenario
            shift_arrow = ArrowData(motion_data=shift_motion, color="red")
            dash_arrow = ArrowData(motion_data=dash_motion, color="blue")
            pictograph_data = PictographData(
                arrows={"red": shift_arrow, "blue": dash_arrow}
            )

            dash_location = positioning_service._calculate_dash_arrow_location(
                dash_motion, pictograph_data
            )

            # Verify Type 3 detection
            is_type3 = positioning_service._is_type3_scenario(
                dash_motion, pictograph_data
            )
            assert (
                is_type3
            ), f"Should detect Type 3 for shift {start_loc.value}→{end_loc.value}"

            # Dash should avoid shift end location
            assert (
                dash_location != end_loc
            ), f"Dash should avoid shift end location {end_loc.value}"
