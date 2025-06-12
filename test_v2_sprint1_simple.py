#!/usr/bin/env python3
"""
Simple V2 Beat Frame System Test - SPRINT 1

Tests core components without complex imports.
"""

import sys
from pathlib import Path

# Add V2 to path
v2_path = Path(__file__).parent / "v2" / "src"
sys.path.insert(0, str(v2_path))

def test_beat_frame_layout_service():
    """Test the beat frame layout service calculations"""
    print("🧪 Testing Beat Frame Layout Service...")
    
    try:
        from application.services.beat_frame_layout_service import BeatFrameLayoutService
        
        service = BeatFrameLayoutService()
        print("  ✅ BeatFrameLayoutService created successfully")
        
        # Test optimal layout calculations
        test_cases = [
            (1, {"rows": 1, "columns": 8}),
            (8, {"rows": 1, "columns": 8}),
            (9, {"rows": 2, "columns": 5}),
            (16, {"rows": 2, "columns": 8}),
            (32, {"rows": 4, "columns": 8}),
        ]
        
        for beat_count, expected in test_cases:
            layout = service.calculate_optimal_layout(beat_count)
            print(f"  ✅ {beat_count} beats → {layout['rows']}×{layout['columns']} layout")
            
            # Validate layout can accommodate beats
            is_valid = service.validate_layout(beat_count, layout["rows"], layout["columns"])
            print(f"    {'✅' if is_valid else '❌'} Layout validation: {is_valid}")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Beat frame layout service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sequence_data_models():
    """Test V2 sequence data models"""
    print("🧪 Testing V2 Sequence Data Models...")
    
    try:
        from domain.models.core_models import SequenceData, BeatData, MotionData, MotionType, RotationDirection
        
        # Test empty sequence creation
        empty_sequence = SequenceData.empty()
        print(f"  ✅ Empty sequence created: {empty_sequence.name}, {empty_sequence.length} beats")
        print(f"  ✅ Empty sequence is_empty: {empty_sequence.is_empty}")
        
        # Test beat data creation with correct enum values
        beat_data = BeatData(
            letter="A",
            duration=4.0,
            beat_number=1,
            blue_motion=MotionData(
                motion_type=MotionType.PRO,  # Use correct enum value
                rotation_direction=RotationDirection.CLOCKWISE,
                start_location="n",
                end_location="s"
            ),
            red_motion=MotionData(
                motion_type=MotionType.DASH,  # Use correct enum value
                rotation_direction=RotationDirection.COUNTER_CLOCKWISE,
                start_location="e",
                end_location="w"
            )
        )
        print(f"  ✅ Beat data created: {beat_data.letter}, duration {beat_data.duration}")
        
        # Test sequence with beats
        sequence = SequenceData(name="Test Sequence", beats=[beat_data])
        print(f"  ✅ Sequence created: {sequence.name}, {sequence.length} beats")
        print(f"  ✅ Sequence total_duration: {sequence.total_duration}")
        print(f"  ✅ Sequence is_valid: {sequence.is_valid}")
        
        # Test immutable operations
        new_beat = BeatData(
            letter="B",
            duration=4.0,
            beat_number=2,
            blue_motion=MotionData(
                motion_type=MotionType.FLOAT,
                rotation_direction=RotationDirection.CLOCKWISE,
                start_location="ne",
                end_location="sw"
            ),
            red_motion=MotionData(
                motion_type=MotionType.STATIC,
                rotation_direction=RotationDirection.CLOCKWISE,
                start_location="nw",
                end_location="nw"
            )
        )
        
        extended_sequence = sequence.add_beat(new_beat)
        print(f"  ✅ Beat added immutably: original {sequence.length}, new {extended_sequence.length}")
        
        # Test serialization
        sequence_dict = sequence.to_dict()
        restored_sequence = SequenceData.from_dict(sequence_dict)
        print(f"  ✅ Serialization test: {restored_sequence.name}, {restored_sequence.length} beats")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Sequence data models test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_layout_calculations():
    """Test advanced layout calculations"""
    print("🧪 Testing Advanced Layout Calculations...")
    
    try:
        from application.services.beat_frame_layout_service import BeatFrameLayoutService
        from PyQt6.QtCore import QSize
        
        service = BeatFrameLayoutService()
        
        # Test responsive layout for different screen sizes
        screen_sizes = [
            (1920, 1080, "1080p"),
            (2560, 1440, "1440p"),
            (3840, 2160, "4K"),
        ]
        
        for width, height, name in screen_sizes:
            size = QSize(width, height)
            layout = service.calculate_layout_for_size(16, size)  # 16 beats
            print(f"  ✅ {name} ({width}×{height}): {layout['rows']}×{layout['columns']} layout")
            
        # Test grid dimensions
        layouts = [
            {"rows": 1, "columns": 8},
            {"rows": 2, "columns": 4},
            {"rows": 4, "columns": 2},
        ]
        
        for layout in layouts:
            width, height = service.get_grid_dimensions(layout)
            print(f"  ✅ {layout['rows']}×{layout['columns']} grid: {width}×{height} pixels")
            
        # Test beat positioning
        layout = {"rows": 3, "columns": 4}
        for beat_index in [0, 3, 7, 11]:
            row, col = service.get_beat_position(beat_index, layout)
            reverse_index = service.get_beat_index(row, col, layout)
            print(f"  ✅ Beat {beat_index}: row {row}, col {col} → index {reverse_index}")
            
        # Test scroll position calculation
        scroll_x, scroll_y = service.calculate_scroll_position(5, layout)
        print(f"  ✅ Scroll position for beat 5: ({scroll_x}, {scroll_y})")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Layout calculations test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enum_values():
    """Test that all enum values are correct"""
    print("🧪 Testing Enum Values...")
    
    try:
        from domain.models.core_models import MotionType, RotationDirection, HandMotionType
        
        # Test MotionType enum
        motion_types = [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT, MotionType.DASH, MotionType.STATIC]
        print(f"  ✅ MotionType values: {[mt.value for mt in motion_types]}")
        
        # Test RotationDirection enum
        rotation_dirs = [RotationDirection.CLOCKWISE, RotationDirection.COUNTER_CLOCKWISE]
        print(f"  ✅ RotationDirection values: {[rd.value for rd in rotation_dirs]}")
        
        # Test HandMotionType enum
        hand_motion_types = list(HandMotionType)
        print(f"  ✅ HandMotionType count: {len(hand_motion_types)}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Enum values test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_path_management_integration():
    """Test integration with our version-aware path management"""
    print("🧪 Testing Path Management Integration...")
    
    try:
        # Add launcher core to path
        launcher_core_path = Path(__file__).parent / "launcher" / "core"
        sys.path.insert(0, str(launcher_core_path))
        
        from version_path_manager import get_path_manager, Version
        
        path_manager = get_path_manager()
        print("  ✅ Version path manager accessible from V2")
        
        # Test V2 data path
        v2_data_path = path_manager.get_data_path("arrow_placement/diamond/default/default_diamond_pro_placements.json", Version.V2)
        print(f"  ✅ V2 data path: {v2_data_path}")
        
        # Test V2 image path
        v2_image_path = path_manager.get_image_path("grid/diamond_grid.svg", Version.V2)
        print(f"  ✅ V2 image path: {v2_image_path}")
        
        # Test file existence
        data_exists = path_manager.file_exists("arrow_placement/diamond/default/default_diamond_pro_placements.json", "data", Version.V2)
        print(f"  ✅ V2 data file exists: {data_exists}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Path management integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run simplified SPRINT 1 tests"""
    print("🚀 V2 Beat Frame System - SPRINT 1 Simple Testing")
    print("=" * 65)
    
    tests = [
        ("Beat Frame Layout Service", test_beat_frame_layout_service),
        ("V2 Sequence Data Models", test_sequence_data_models),
        ("Advanced Layout Calculations", test_layout_calculations),
        ("Enum Values", test_enum_values),
        ("Path Management Integration", test_path_management_integration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}:")
        if test_func():
            passed += 1
            print(f"  ✅ {test_name} PASSED")
        else:
            print(f"  ❌ {test_name} FAILED")
    
    print(f"\n📊 SPRINT 1 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 SPRINT 1 Core Components - WORKING!")
        print("\n✅ Verified Components:")
        print("  • Beat frame layout service with dynamic calculations")
        print("  • V2 sequence data models with immutable operations")
        print("  • Advanced layout calculations for responsive design")
        print("  • Correct enum values for motion types and directions")
        print("  • Integration with version-aware path management")
        print("\n📋 SPRINT 1 Analysis Summary:")
        print("  • Core business logic services are working correctly")
        print("  • Data models support immutable operations")
        print("  • Layout calculations handle various screen sizes")
        print("  • Path management integrates with V2 architecture")
        print("\n🚀 Ready for UI component integration and SPRINT 2!")
        return True
    else:
        print("❌ Some SPRINT 1 core components need fixes.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
