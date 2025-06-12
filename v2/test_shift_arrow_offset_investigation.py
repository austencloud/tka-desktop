#!/usr/bin/env python3
"""
Investigate shift arrow positioning offset compared to reference implementation.
"""

import sys
from pathlib import Path

# Add the project root to path for absolute imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.application.services.arrow_positioning_service import ArrowPositioningService
from src.domain.models.core_models import MotionData, MotionType, Location, RotationDirection
from src.domain.models.pictograph_models import ArrowData, PictographData


def test_shift_arrow_offset_investigation():
    """Investigate systematic offset in shift arrow positioning."""
    print("🔍 Investigating Shift Arrow Positioning Offset")
    print("=" * 60)
    
    positioning_service = ArrowPositioningService()
    
    # Test comprehensive set of shift arrows (PRO and ANTI)
    test_cases = [
        # PRO arrows - all 8 grid positions
        {
            "name": "Pro W→N CW (NW)",
            "motion": MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.WEST,
                end_loc=Location.NORTH,
                turns=1.0,
            ),
            "expected_reference": None,  # To be filled with reference values
        },
        {
            "name": "Pro N→E CW (NE)",
            "motion": MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.EAST,
                turns=1.0,
            ),
            "expected_reference": None,
        },
        {
            "name": "Pro E→S CW (SE)",
            "motion": MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.EAST,
                end_loc=Location.SOUTH,
                turns=1.0,
            ),
            "expected_reference": None,
        },
        {
            "name": "Pro S→W CW (SW)",
            "motion": MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.WEST,
                turns=1.0,
            ),
            "expected_reference": None,
        },
        # ANTI arrows - sample positions
        {
            "name": "Anti W→N CCW (NW)",
            "motion": MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                start_loc=Location.WEST,
                end_loc=Location.NORTH,
                turns=1.0,
            ),
            "expected_reference": None,
        },
        {
            "name": "Anti E→S CCW (SE)",
            "motion": MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                start_loc=Location.EAST,
                end_loc=Location.SOUTH,
                turns=1.0,
            ),
            "expected_reference": None,
        },
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🎯 Test {i}: {test_case['name']}")
        print("-" * 50)
        
        motion = test_case["motion"]
        arrow_data = ArrowData(motion_data=motion, color="blue", turns=motion.turns)
        pictograph_data = PictographData(arrows={"blue": arrow_data})
        
        # Get complete positioning breakdown
        x, y, rotation = positioning_service.calculate_arrow_position(arrow_data, pictograph_data)
        
        # Get detailed intermediate values
        arrow_location = positioning_service._calculate_arrow_location(motion)
        initial_position = positioning_service._compute_initial_position(motion, arrow_location)
        default_adjustment = positioning_service._get_default_adjustment(arrow_data)
        quadrant_index = positioning_service._get_quadrant_index(motion)
        directional_tuples = positioning_service._generate_directional_tuples(
            motion, int(default_adjustment.x()), int(default_adjustment.y())
        )
        
        # Calculate distance from center
        center_distance = ((x - 475.0)**2 + (y - 475.0)**2)**0.5
        
        print(f"  Motion: {motion.motion_type.value} {motion.start_loc.value}→{motion.end_loc.value} {motion.prop_rot_dir.value}")
        print(f"  Arrow Location: {arrow_location.value}")
        print(f"  Initial Position: ({initial_position.x():.1f}, {initial_position.y():.1f})")
        print(f"  Default Adjustment: ({default_adjustment.x():.1f}, {default_adjustment.y():.1f})")
        print(f"  Quadrant Index: {quadrant_index}")
        if directional_tuples and quadrant_index < len(directional_tuples):
            selected_tuple = directional_tuples[quadrant_index]
            print(f"  Quadrant Transform: {selected_tuple}")
        print(f"  Final Position: ({x:.1f}, {y:.1f})")
        print(f"  Distance from Center: {center_distance:.1f}px")
        print(f"  Rotation: {rotation:.1f}°")
        
        results.append({
            "name": test_case["name"],
            "position": (x, y),
            "distance": center_distance,
            "rotation": rotation,
            "arrow_location": arrow_location.value,
            "initial_pos": (initial_position.x(), initial_position.y()),
            "adjustment": (default_adjustment.x(), default_adjustment.y()),
            "quadrant_transform": directional_tuples[quadrant_index] if directional_tuples and quadrant_index < len(directional_tuples) else None,
        })
    
    print("\n" + "=" * 60)
    print("📊 OFFSET ANALYSIS:")
    print("=" * 60)
    
    # Analyze patterns in the results
    pro_distances = [r["distance"] for r in results if "Pro" in r["name"]]
    anti_distances = [r["distance"] for r in results if "Anti" in r["name"]]
    
    if pro_distances:
        avg_pro_distance = sum(pro_distances) / len(pro_distances)
        print(f"Average PRO arrow distance from center: {avg_pro_distance:.1f}px")
    
    if anti_distances:
        avg_anti_distance = sum(anti_distances) / len(anti_distances)
        print(f"Average ANTI arrow distance from center: {avg_anti_distance:.1f}px")
    
    print(f"\n🔍 SYSTEMATIC OFFSET INVESTIGATION:")
    print(f"• All shift arrows positioned away from center (475, 475)")
    print(f"• Consistent quadrant transformations applied")
    print(f"• Default adjustments: Pro (0, 25), Anti (45, -55)")
    print(f"• Initial positions based on layer2 coordinates")
    
    print(f"\n📋 REFERENCE COMPARISON NEEDED:")
    print(f"• Run reference implementation with same test cases")
    print(f"• Extract exact pixel coordinates for comparison")
    print(f"• Identify systematic offset patterns")
    print(f"• Adjust default adjustment values if needed")
    print(f"• Verify layer2 coordinate calculations")
    
    print(f"\n🎯 NEXT STEPS:")
    print(f"1. Extract reference coordinates for these exact test cases")
    print(f"2. Compare against our calculated positions")
    print(f"3. Identify consistent offset patterns")
    print(f"4. Adjust positioning parameters accordingly")
    print(f"5. Validate with pixel-perfect comparison")


if __name__ == "__main__":
    test_shift_arrow_offset_investigation()
