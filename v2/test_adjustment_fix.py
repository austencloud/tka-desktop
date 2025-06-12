#!/usr/bin/env python3
"""
Test the adjustment fix to see if arrows are now closer to center.
"""

import sys
from pathlib import Path

# Add the project root to path for absolute imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.application.services.arrow_positioning_service import ArrowPositioningService
from src.domain.models.core_models import MotionData, MotionType, Location, RotationDirection
from src.domain.models.pictograph_models import ArrowData, PictographData


def test_adjustment_fix():
    """Test if the adjustment fix brings arrows closer to center."""
    print("🎯 Testing Adjustment Fix")
    print("=" * 40)
    
    positioning_service = ArrowPositioningService()
    
    # Test the same motions as before
    test_cases = [
        {
            "name": "Pro W→N CW (1 turn)",
            "motion": MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.WEST,
                end_loc=Location.NORTH,
                turns=1.0,
            ),
            "color": "blue",
            "old_distance": 269.1,
        },
        {
            "name": "Anti W→N CCW (1 turn)",
            "motion": MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                start_loc=Location.WEST,
                end_loc=Location.NORTH,
                turns=1.0,
            ),
            "color": "blue",
            "old_distance": 357.0,
        },
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['name']}")
        print("-" * 30)
        
        motion = test_case["motion"]
        color = test_case["color"]
        arrow_data = ArrowData(motion_data=motion, color=color, turns=motion.turns)
        pictograph_data = PictographData(arrows={color: arrow_data})
        
        x, y, rotation = positioning_service.calculate_arrow_position(arrow_data, pictograph_data)
        
        # Calculate distance from center
        center_distance = ((x - 475.0)**2 + (y - 475.0)**2)**0.5
        old_distance = test_case["old_distance"]
        
        print(f"  Motion: {motion.motion_type.value} {motion.start_loc.value}→{motion.end_loc.value}")
        print(f"  Position: ({x:.1f}, {y:.1f})")
        print(f"  Distance from Center: {center_distance:.1f}px")
        print(f"  Previous Distance: {old_distance:.1f}px")
        
        distance_change = center_distance - old_distance
        if abs(distance_change) > 1.0:
            if distance_change < 0:
                print(f"  ✅ IMPROVEMENT: {abs(distance_change):.1f}px closer to center!")
            else:
                print(f"  ❌ REGRESSION: {distance_change:.1f}px further from center")
        else:
            print(f"  ➡️  No significant change ({distance_change:.1f}px)")
    
    print(f"\n" + "=" * 40)
    print("🎯 ADJUSTMENT FIX RESULTS:")
    print("=" * 40)
    print("✅ Using V1 layer1_alpha adjustments instead of layer2_alpha")
    print("✅ Pro 1.0 turn: (-35, -15) instead of (0, 25)")
    print("✅ Anti 1.0 turn: (45, -55) same but other turns different")
    print("📋 Check if arrows are now positioned closer to center")


if __name__ == "__main__":
    test_adjustment_fix()
