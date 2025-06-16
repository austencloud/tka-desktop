"""
Test for the enhanced dash arrow location calculation
"""

import sys
from pathlib import Path

# Add modern to path for imports
v2_path = Path(__file__).parent / "src"
if str(v2_path) not in sys.path:
    sys.path.insert(0, str(v2_path))

from domain.models.core_models import (
    MotionData,
    MotionType,
    RotationDirection,
    Location,
    BeatData,
)
from application.services.arrow_positioning_service import ArrowPositioningService
from domain.models.pictograph_models import ArrowData, PictographData


def test_dash_arrow_positioning():
    """Test that dash arrows use the enhanced Legacy logic for positioning."""
    print("🧪 Testing enhanced dash arrow positioning logic...")

    # Create arrow positioning service
    positioning_service = ArrowPositioningService()

    # Test case 1: Zero turns dash arrow (should use default mapping)
    print("\n📍 Test 1: Zero turns dash arrow")
    zero_turns_motion = MotionData(
        motion_type=MotionType.DASH,
        prop_rot_dir=RotationDirection.NO_ROTATION,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        turns=0.0,
        start_ori="in",
        end_ori="in",
    )

    arrow_data = ArrowData(
        motion_data=zero_turns_motion,
        color="blue",
        turns=0.0,
    )

    pictograph_data = PictographData(arrows={"blue": arrow_data})

    # Calculate position using the enhanced service
    pos_x, pos_y, rotation = positioning_service.calculate_arrow_position(
        arrow_data, pictograph_data
    )

    print(
        f"   Motion: {zero_turns_motion.start_loc.value} → {zero_turns_motion.end_loc.value}"
    )
    print(
        f"   Calculated arrow location: {positioning_service._calculate_arrow_location(zero_turns_motion).value}"
    )
    print(f"   Position: ({pos_x:.1f}, {pos_y:.1f})")
    print(f"   Rotation: {rotation:.1f}°")

    # Test case 2: Non-zero turns clockwise dash arrow
    print("\n📍 Test 2: Non-zero turns clockwise dash arrow")
    cw_turns_motion = MotionData(
        motion_type=MotionType.DASH,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        turns=1.0,
        start_ori="in",
        end_ori="out",
    )

    arrow_data_cw = ArrowData(
        motion_data=cw_turns_motion,
        color="red",
        turns=1.0,
    )

    pictograph_data_cw = PictographData(arrows={"red": arrow_data_cw})

    pos_x_cw, pos_y_cw, rotation_cw = positioning_service.calculate_arrow_position(
        arrow_data_cw, pictograph_data_cw
    )

    print(
        f"   Motion: {cw_turns_motion.start_loc.value} → {cw_turns_motion.end_loc.value} (CW)"
    )
    print(
        f"   Calculated arrow location: {positioning_service._calculate_arrow_location(cw_turns_motion).value}"
    )
    print(f"   Position: ({pos_x_cw:.1f}, {pos_y_cw:.1f})")
    print(f"   Rotation: {rotation_cw:.1f}°")

    # Test case 3: Non-zero turns counter-clockwise dash arrow
    print("\n📍 Test 3: Non-zero turns counter-clockwise dash arrow")
    ccw_turns_motion = MotionData(
        motion_type=MotionType.DASH,
        prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
        start_loc=Location.EAST,
        end_loc=Location.WEST,
        turns=1.0,
        start_ori="in",
        end_ori="out",
    )

    arrow_data_ccw = ArrowData(
        motion_data=ccw_turns_motion,
        color="blue",
        turns=1.0,
    )

    pictograph_data_ccw = PictographData(arrows={"blue": arrow_data_ccw})

    pos_x_ccw, pos_y_ccw, rotation_ccw = positioning_service.calculate_arrow_position(
        arrow_data_ccw, pictograph_data_ccw
    )

    print(
        f"   Motion: {ccw_turns_motion.start_loc.value} → {ccw_turns_motion.end_loc.value} (CCW)"
    )
    print(
        f"   Calculated arrow location: {positioning_service._calculate_arrow_location(ccw_turns_motion).value}"
    )
    print(f"   Position: ({pos_x_ccw:.1f}, {pos_y_ccw:.1f})")
    print(f"   Rotation: {rotation_ccw:.1f}°")

    print("\n✅ Enhanced dash arrow positioning test completed!")

    # Verify that different cases produce different locations
    location_1 = positioning_service._calculate_arrow_location(zero_turns_motion)
    location_2 = positioning_service._calculate_arrow_location(cw_turns_motion)
    location_3 = positioning_service._calculate_arrow_location(ccw_turns_motion)

    print(f"\n🔍 Verification:")
    print(f"   Zero turns location: {location_1.value}")
    print(f"   CW turns location: {location_2.value}")
    print(f"   CCW turns location: {location_3.value}")

    # They should be different locations (complex logic should make a difference)
    if location_1 != location_2 or location_2 != location_3:
        print("✅ Enhanced logic is producing different locations for different cases!")
    else:
        print(
            "⚠️  All cases produced the same location - may need more complex scenarios"
        )


if __name__ == "__main__":
    test_dash_arrow_positioning()
