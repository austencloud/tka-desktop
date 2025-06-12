#!/usr/bin/env python3
"""
Comprehensive test to identify positioning discrepancies between our implementation
and the reference implementation.
"""

import sys
from pathlib import Path

# Add the project root to path for absolute imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.application.services.arrow_positioning_service import ArrowPositioningService
from src.domain.models.core_models import MotionData, MotionType, Location, RotationDirection
from src.domain.models.pictograph_models import ArrowData, PictographData


def test_positioning_discrepancies():
    """Test to identify specific positioning discrepancies."""
    print("🔍 COMPREHENSIVE POSITIONING DISCREPANCY ANALYSIS")
    print("=" * 60)
    
    positioning_service = ArrowPositioningService()
    
    # Test case: Pro W→N CW (1 turn)
    motion = MotionData(
        motion_type=MotionType.PRO,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        start_loc=Location.WEST,
        end_loc=Location.NORTH,
        turns=1.0,
    )
    
    arrow_data = ArrowData(motion_data=motion, color="blue", turns=motion.turns)
    pictograph_data = PictographData(arrows={"blue": arrow_data})
    
    print("\n🎯 STEP-BY-STEP POSITIONING ANALYSIS:")
    print("=" * 60)
    
    # Step 1: Arrow location calculation
    arrow_location = positioning_service._calculate_arrow_location(motion)
    print(f"1. Arrow Location: {arrow_location.value}")
    
    # Step 2: Initial position calculation
    initial_position = positioning_service._compute_initial_position(motion, arrow_location)
    print(f"2. Initial Position: ({initial_position.x():.1f}, {initial_position.y():.1f})")
    
    # Step 3: Default adjustment lookup
    default_adjustment = positioning_service._get_default_adjustment(arrow_data)
    print(f"3. Default Adjustment: ({default_adjustment.x():.0f}, {default_adjustment.y():.0f})")
    
    # Step 4: Quadrant adjustments
    quadrant_adjustment = positioning_service._apply_quadrant_adjustments(arrow_data, default_adjustment)
    print(f"4. Quadrant Adjustment: ({quadrant_adjustment.x():.0f}, {quadrant_adjustment.y():.0f})")
    
    # Step 5: Final position calculation
    final_x = initial_position.x() + quadrant_adjustment.x()
    final_y = initial_position.y() + quadrant_adjustment.y()
    print(f"5. Final Position: ({final_x:.1f}, {final_y:.1f})")
    
    # Calculate distance from center
    center_distance = ((final_x - 475.0)**2 + (final_y - 475.0)**2)**0.5
    print(f"6. Distance from Center: {center_distance:.1f}px")
    
    print(f"\n🔍 COORDINATE SYSTEM ANALYSIS:")
    print("=" * 60)
    
    # Check our layer2 points vs reference
    print("Our LAYER2_POINTS (currently using BOX coordinates):")
    for loc, point in positioning_service.LAYER2_POINTS.items():
        print(f"  {loc.value}: ({point.x():.1f}, {point.y():.1f})")
    
    print("\nReference DIAMOND layer2_points from circle_coords.json:")
    diamond_layer2_reference = {
        "ne": (618.1, 331.9),
        "se": (618.1, 618.1),
        "sw": (331.9, 618.1),
        "nw": (331.9, 331.9),
    }
    for loc, coords in diamond_layer2_reference.items():
        print(f"  {loc}: {coords}")
    
    print("\nReference BOX layer2_points from circle_coords.json:")
    box_layer2_reference = {
        "n": (475, 272.6),
        "e": (677.4, 475),
        "s": (475, 677.4),
        "w": (272.6, 475),
    }
    for loc, coords in box_layer2_reference.items():
        print(f"  {loc}: {coords}")
    
    print(f"\n🚨 IDENTIFIED DISCREPANCIES:")
    print("=" * 60)
    
    print("1. LAYER2 COORDINATE MISMATCH:")
    print("   ❌ We're using BOX layer2 points for DIAMOND grid")
    print("   ❌ Pro W→N should use NW diamond point (331.9, 331.9)")
    print(f"   ❌ We're using W box point ({positioning_service.LAYER2_POINTS[Location.WEST].x():.1f}, {positioning_service.LAYER2_POINTS[Location.WEST].y():.1f})")
    
    print("\n2. BOUNDING RECT CENTER MISSING:")
    print("   ❌ Reference subtracts arrow.boundingRect().center()")
    print("   ❌ We don't account for bounding rect offset")
    
    print("\n3. COORDINATE SYSTEM ORIENTATION:")
    print("   ❓ Need to verify if adjustment signs are correct")
    print("   ❓ Need to verify quadrant transformation accuracy")
    
    print(f"\n🎯 EXPECTED FIXES:")
    print("=" * 60)
    print("1. Use correct DIAMOND layer2 points instead of BOX points")
    print("2. Subtract bounding rect center in final positioning formula")
    print("3. Verify adjustment application signs and coordinate system")
    print("4. Test quadrant transformation mathematical accuracy")
    
    # Calculate what the position SHOULD be with correct diamond coordinates
    correct_nw_point = (331.9, 331.9)  # Correct diamond NW layer2 point
    corrected_distance = ((correct_nw_point[0] + quadrant_adjustment.x() - 475.0)**2 + 
                         (correct_nw_point[1] + quadrant_adjustment.y() - 475.0)**2)**0.5
    
    print(f"\n📊 CORRECTED CALCULATION PREVIEW:")
    print("=" * 60)
    print(f"With correct diamond NW point {correct_nw_point}:")
    print(f"  Corrected Position: ({correct_nw_point[0] + quadrant_adjustment.x():.1f}, {correct_nw_point[1] + quadrant_adjustment.y():.1f})")
    print(f"  Corrected Distance: {corrected_distance:.1f}px")
    print(f"  Distance Improvement: {center_distance - corrected_distance:.1f}px closer to center")
    
    return True


if __name__ == "__main__":
    test_positioning_discrepancies()
