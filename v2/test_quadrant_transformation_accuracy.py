#!/usr/bin/env python3
"""
Test quadrant transformation accuracy to verify mathematical correctness.
"""

import sys
from pathlib import Path

# Add the project root to path for absolute imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.application.services.arrow_positioning_service import ArrowPositioningService
from src.domain.models.core_models import MotionData, MotionType, Location, RotationDirection
from src.domain.models.pictograph_models import ArrowData, PictographData


def test_quadrant_transformation_accuracy():
    """Test the mathematical accuracy of quadrant transformations."""
    print("🔍 QUADRANT TRANSFORMATION ACCURACY TEST")
    print("=" * 50)
    
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
    
    print("\n🎯 DETAILED QUADRANT TRANSFORMATION ANALYSIS:")
    print("=" * 50)
    
    # Step 1: Get default adjustment from JSON
    default_adjustment = positioning_service._get_default_adjustment(arrow_data)
    print(f"1. Default Adjustment from JSON: ({default_adjustment.x():.0f}, {default_adjustment.y():.0f})")
    
    # Step 2: Get quadrant index
    quadrant_index = positioning_service._get_quadrant_index(motion)
    print(f"2. Quadrant Index: {quadrant_index}")
    
    # Step 3: Generate directional tuples
    directional_tuples = positioning_service._generate_directional_tuples(
        motion, int(default_adjustment.x()), int(default_adjustment.y())
    )
    print(f"3. Directional Tuples: {directional_tuples}")
    
    # Step 4: Apply quadrant transformation
    if directional_tuples and 0 <= quadrant_index < len(directional_tuples):
        adjusted_x, adjusted_y = directional_tuples[quadrant_index]
        print(f"4. Selected Tuple (index {quadrant_index}): ({adjusted_x}, {adjusted_y})")
    
    # Step 5: Verify transformation logic
    print(f"\n🔍 TRANSFORMATION LOGIC VERIFICATION:")
    print("=" * 50)
    
    x, y = int(default_adjustment.x()), int(default_adjustment.y())
    print(f"Input: x={x}, y={y}")
    print(f"Motion: {motion.motion_type.value} {motion.prop_rot_dir.value}")
    print(f"Grid Mode: diamond")
    
    # Manual calculation for Pro CW Diamond
    if motion.motion_type == MotionType.PRO and motion.prop_rot_dir == RotationDirection.CLOCKWISE:
        expected_tuples = [(x, y), (-y, x), (-x, -y), (y, -x)]
        print(f"Expected Pro CW Diamond tuples: {expected_tuples}")
        print(f"Actual tuples: {directional_tuples}")
        print(f"Match: {expected_tuples == directional_tuples}")
    
    # Step 6: Compare with reference implementation expectations
    print(f"\n📊 REFERENCE COMPARISON:")
    print("=" * 50)
    
    # Calculate what the final position should be
    arrow_location = positioning_service._calculate_arrow_location(motion)
    initial_position = positioning_service._compute_initial_position(motion, arrow_location)
    
    print(f"Arrow Location: {arrow_location.value}")
    print(f"Initial Position: ({initial_position.x():.1f}, {initial_position.y():.1f})")
    print(f"Final Adjustment: ({adjusted_x}, {adjusted_y})")
    
    final_x = initial_position.x() + adjusted_x
    final_y = initial_position.y() + adjusted_y
    distance = ((final_x - 475.0)**2 + (final_y - 475.0)**2)**0.5
    
    print(f"Final Position: ({final_x:.1f}, {final_y:.1f})")
    print(f"Distance from Center: {distance:.1f}px")
    
    # Step 7: Test different quadrant indices to see the pattern
    print(f"\n🔄 ALL QUADRANT TRANSFORMATIONS:")
    print("=" * 50)
    
    for i, (adj_x, adj_y) in enumerate(directional_tuples):
        test_final_x = initial_position.x() + adj_x
        test_final_y = initial_position.y() + adj_y
        test_distance = ((test_final_x - 475.0)**2 + (test_final_y - 475.0)**2)**0.5
        
        marker = "👉" if i == quadrant_index else "  "
        print(f"{marker} Quadrant {i}: ({adj_x:3}, {adj_y:3}) → ({test_final_x:5.1f}, {test_final_y:5.1f}) → {test_distance:5.1f}px")
    
    # Step 8: Investigate if there's a closer quadrant
    min_distance = min(
        ((initial_position.x() + adj_x - 475.0)**2 + (initial_position.y() + adj_y - 475.0)**2)**0.5
        for adj_x, adj_y in directional_tuples
    )
    
    print(f"\n🎯 OPTIMIZATION ANALYSIS:")
    print("=" * 50)
    print(f"Current Distance: {distance:.1f}px")
    print(f"Minimum Possible Distance: {min_distance:.1f}px")
    print(f"Potential Improvement: {distance - min_distance:.1f}px")
    
    if distance - min_distance > 5.0:
        print("⚠️  Significant improvement possible with different quadrant!")
        # Find the optimal quadrant
        for i, (adj_x, adj_y) in enumerate(directional_tuples):
            test_distance = ((initial_position.x() + adj_x - 475.0)**2 + (initial_position.y() + adj_y - 475.0)**2)**0.5
            if abs(test_distance - min_distance) < 1.0:
                print(f"🎯 Optimal quadrant would be: {i}")
    else:
        print("✅ Current quadrant selection appears optimal")
    
    return True


if __name__ == "__main__":
    test_quadrant_transformation_accuracy()
