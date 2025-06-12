#!/usr/bin/env python3
"""
Simple test of arrow positioning without Qt.
"""

import sys
from pathlib import Path

# Add the v2 src directory to path
v2_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(v2_src_path))

print("Starting simple positioning test...")

try:
    from application.services.pictograph_data_service import PictographDataService
    print("✓ Imported PictographDataService")
    
    from application.services.arrow_positioning_service import ArrowPositioningService
    print("✓ Imported ArrowPositioningService")
    
    from domain.models.core_models import MotionData, MotionType, Location, RotationDirection
    print("✓ Imported core models")
    
    from domain.models.pictograph_models import ArrowData, PictographData
    print("✓ Imported pictograph models")
    
    print("\nCreating services...")
    data_service = PictographDataService()
    positioning_service = ArrowPositioningService()
    print("✓ Services created")
    
    print("\nGetting test data...")
    test_pictographs = data_service.get_test_pictographs()
    pictograph_data = test_pictographs[0]
    print("✓ Test data retrieved")
    
    print("\nCreating motion data...")
    blue_motion_data = pictograph_data["blue_motion"]
    blue_motion = MotionData(
        motion_type=MotionType(blue_motion_data["motion_type"]),
        prop_rot_dir=RotationDirection(blue_motion_data["prop_rot_dir"]),
        start_loc=Location(blue_motion_data["start_loc"]),
        end_loc=Location(blue_motion_data["end_loc"]),
        turns=blue_motion_data.get("turns", 1.0),
    )
    print("✓ Motion data created")
    
    print("\nCreating arrow data...")
    blue_arrow_data = ArrowData(
        motion_data=blue_motion,
        color="blue",
        turns=blue_motion.turns,
    )
    print("✓ Arrow data created")
    
    print("\nCreating pictograph data...")
    pictograph_data_obj = PictographData(arrows={"blue": blue_arrow_data})
    print("✓ Pictograph data created")
    
    print("\nCalling positioning service...")
    result = positioning_service.calculate_arrow_position(
        blue_arrow_data, pictograph_data_obj
    )
    print(f"✓ Positioning service returned: {result}")
    
    print("\n🎉 SUCCESS: All tests passed!")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
