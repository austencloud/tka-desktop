"""
Test for Type 3 dash arrow positioning (avoiding shift arrows)
"""

import sys
from pathlib import Path

# Add modern to path for imports
modern_path = Path(__file__).parent / "src"
if str(modern_path) not in sys.path:
    sys.path.insert(0, str(modern_path))

from domain.models.core_models import (
    MotionData,
    MotionType,
    RotationDirection,
    Location,
)
from application.services.arrow_positioning_service import ArrowPositioningService
from domain.models.pictograph_models import ArrowData, PictographData


def test_type3_dash_arrow_positioning():
    """Test Type 3 dash arrow positioning where dash must avoid shift arrow."""
    print("🧪 Testing Type 3 dash arrow positioning (avoiding shift arrows)...")

    # Create arrow positioning service
    positioning_service = ArrowPositioningService()

    # Type 3 scenario: One motion is shift (PRO), other is dash
    # Example: Theta dash (θ-) - one arrow does a shift, other does a dash

    print("\n📍 Test: Type 3 scenario - Shift from NORTH to EAST, Dash avoids")

    # Shift motion (PRO): NORTH → EAST (will be positioned at NORTHEAST)
    shift_motion = MotionData(
        motion_type=MotionType.PRO,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        start_loc=Location.NORTH,
        end_loc=Location.EAST,
        turns=1.0,
    )

    # Dash motion (DASH): NORTH → SOUTH (zero turns, should avoid shift location)
    dash_motion = MotionData(
        motion_type=MotionType.DASH,
        prop_rot_dir=RotationDirection.NO_ROTATION,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        turns=0.0,
    )

    # Create arrows
    shift_arrow = ArrowData(
        motion_data=shift_motion,
        color="blue",
    )

    dash_arrow = ArrowData(
        motion_data=dash_motion,
        color="red",
    )

    # Create pictograph with both arrows (Type 3 scenario)
    pictograph_data = PictographData(arrows={"blue": shift_arrow, "red": dash_arrow})

    # Calculate shift arrow position (should be at NORTHEAST)
    shift_x, shift_y, shift_rotation = positioning_service.calculate_arrow_position(
        shift_arrow, pictograph_data
    )

    shift_location = positioning_service._calculate_arrow_location(shift_motion)
    print(
        f"   Shift motion: {shift_motion.start_loc.value} → {shift_motion.end_loc.value}"
    )
    print(f"   Shift arrow location: {shift_location.value}")
    print(f"   Shift position: ({shift_x:.1f}, {shift_y:.1f})")

    # Calculate dash arrow position (should avoid shift location)
    dash_x, dash_y, dash_rotation = positioning_service.calculate_arrow_position(
        dash_arrow, pictograph_data
    )

    dash_location = positioning_service._calculate_arrow_location(dash_motion)
    print(
        f"   Dash motion: {dash_motion.start_loc.value} → {dash_motion.end_loc.value}"
    )
    print(f"   Dash arrow location: {dash_location.value}")
    print(f"   Dash position: ({dash_x:.1f}, {dash_y:.1f})")

    # Verify Type 3 detection
    is_type3 = positioning_service._is_type3_scenario(dash_motion, pictograph_data)
    print(f"   Type 3 detected: {is_type3}")

    # Test normal dash arrow (without Type 3 scenario) for comparison
    print("\n📍 Comparison: Normal dash arrow (no shift to avoid)")

    normal_pictograph = PictographData(arrows={"red": dash_arrow})

    normal_dash_x, normal_dash_y, normal_dash_rotation = (
        positioning_service.calculate_arrow_position(dash_arrow, normal_pictograph)
    )

    normal_dash_location = positioning_service._calculate_arrow_location(dash_motion)
    print(f"   Normal dash location: {normal_dash_location.value}")
    print(f"   Normal dash position: ({normal_dash_x:.1f}, {normal_dash_y:.1f})")

    # Verify different positioning
    if dash_location != normal_dash_location:
        print("✅ Type 3 logic successfully places dash away from shift!")
    else:
        print("⚠️  Type 3 logic may need refinement - same location as normal dash")

    print("\n✅ Type 3 dash arrow positioning test completed!")


if __name__ == "__main__":
    test_type3_dash_arrow_positioning()
