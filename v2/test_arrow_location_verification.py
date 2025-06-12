#!/usr/bin/env python3
"""
Test arrow location calculation to verify it matches the reference implementation.
"""

import sys
from pathlib import Path

# Add the project root to path for absolute imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.application.services.arrow_positioning_service import ArrowPositioningService
from src.domain.models.core_models import MotionData, MotionType, Location, RotationDirection


def test_arrow_location_verification():
    """Test arrow location calculation against reference implementation."""
    print("🔍 ARROW LOCATION CALCULATION VERIFICATION")
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
    
    print(f"\n🎯 MOTION ANALYSIS:")
    print("=" * 50)
    print(f"Motion Type: {motion.motion_type.value}")
    print(f"Start Location: {motion.start_loc.value}")
    print(f"End Location: {motion.end_loc.value}")
    print(f"Prop Rotation: {motion.prop_rot_dir.value}")
    print(f"Turns: {motion.turns}")
    
    # Step 1: Calculate arrow location
    arrow_location = positioning_service._calculate_arrow_location(motion)
    print(f"\n📍 ARROW LOCATION CALCULATION:")
    print("=" * 50)
    print(f"Calculated Arrow Location: {arrow_location.value}")
    
    # Step 2: Verify shift arrow location logic
    print(f"\n🔍 SHIFT ARROW LOCATION LOGIC:")
    print("=" * 50)
    
    # Manual calculation using our logic
    start_end_pair = frozenset({motion.start_loc, motion.end_loc})
    print(f"Start-End Pair: {{{motion.start_loc.value}, {motion.end_loc.value}}}")
    
    # Check our direction pairs mapping
    direction_pairs = {
        frozenset({Location.NORTH, Location.EAST}): Location.NORTHEAST,
        frozenset({Location.EAST, Location.SOUTH}): Location.SOUTHEAST,
        frozenset({Location.SOUTH, Location.WEST}): Location.SOUTHWEST,
        frozenset({Location.WEST, Location.NORTH}): Location.NORTHWEST,
        frozenset({Location.NORTHEAST, Location.NORTHWEST}): Location.NORTH,
        frozenset({Location.NORTHEAST, Location.SOUTHEAST}): Location.EAST,
        frozenset({Location.SOUTHWEST, Location.SOUTHEAST}): Location.SOUTH,
        frozenset({Location.NORTHWEST, Location.SOUTHWEST}): Location.WEST,
    }
    
    expected_location = direction_pairs.get(start_end_pair, motion.start_loc)
    print(f"Expected Location: {expected_location.value}")
    print(f"Match: {arrow_location == expected_location}")
    
    # Step 3: Check reference implementation logic
    print(f"\n📚 REFERENCE IMPLEMENTATION CHECK:")
    print("=" * 50)
    
    # From start_end_loc_map.py, for NORTHWEST + CLOCKWISE + PRO:
    # PRO: (WEST, NORTH) - this matches our motion!
    print("Reference start_end_loc_map.py for NORTHWEST + CLOCKWISE + PRO:")
    print("  PRO: (WEST, NORTH) ✅ Matches our motion")
    
    # The reference maps (WEST, NORTH) to NORTHWEST location
    print("Reference expectation: W→N should map to NORTHWEST")
    print(f"Our calculation: {arrow_location.value}")
    print(f"Reference match: {'✅' if arrow_location == Location.NORTHWEST else '❌'}")
    
    # Step 4: Investigate if the issue is elsewhere
    print(f"\n🤔 INVESTIGATION SUMMARY:")
    print("=" * 50)
    
    if arrow_location == Location.NORTHWEST:
        print("✅ Arrow location calculation is CORRECT")
        print("❓ Issue might be in:")
        print("   1. Directional tuple generation")
        print("   2. Quadrant index mapping")
        print("   3. Reference implementation differences")
        
        # Let's check what the reference implementation would expect
        print(f"\n🔍 REFERENCE EXPECTATION ANALYSIS:")
        print("=" * 50)
        
        # If our arrow is at NW (quadrant 3), and we're using Pro CW Diamond
        # The directional tuples should be: [(x, y), (-y, x), (-x, -y), (y, -x)]
        # For input (-35, -15): [(-35, -15), (15, -35), (35, 15), (-15, 35)]
        # Quadrant 3 (NW) selects: (-15, 35)
        
        print("Pro CW Diamond directional tuples for (-35, -15):")
        print("  Quadrant 0 (NE): (-35, -15)")
        print("  Quadrant 1 (SE): (15, -35)")  
        print("  Quadrant 2 (SW): (35, 15)")
        print("  Quadrant 3 (NW): (-15, 35) ← Current selection")
        
        print("\nBut our test showed quadrant 2 (SW) gives better positioning...")
        print("This suggests either:")
        print("  1. Our directional tuple generation is wrong")
        print("  2. The reference uses different logic")
        print("  3. There's a coordinate system difference")
        
    else:
        print("❌ Arrow location calculation is INCORRECT")
        print(f"Expected: {Location.NORTHWEST.value}")
        print(f"Got: {arrow_location.value}")
    
    return True


if __name__ == "__main__":
    test_arrow_location_verification()
