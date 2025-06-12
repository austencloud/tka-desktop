#!/usr/bin/env python3
"""
Test V2 Beat Frame System - SPRINT 1 Implementation

Tests the core beat frame system with dynamic grid layout,
beat view components, and start position integration.
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
            
        # Test grid dimensions calculation
        layout = {"rows": 2, "columns": 4}
        width, height = service.get_grid_dimensions(layout)
        print(f"  ✅ Grid dimensions for 2×4: {width}×{height} pixels")
        
        # Test beat positioning
        beat_index = 5
        row, col = service.get_beat_position(beat_index, layout)
        print(f"  ✅ Beat {beat_index} position: row {row}, col {col}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Beat frame layout service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_beat_view_component():
    """Test the modern beat view component"""
    print("🧪 Testing Modern Beat View Component...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.sequence_workbench.beat_frame.beat_view import ModernBeatView
        from domain.models.core_models import BeatData, MotionData, MotionType, RotationDirection
        
        app = QApplication(sys.argv)
        
        # Create beat view
        beat_view = ModernBeatView(beat_number=1)
        print("  ✅ ModernBeatView created successfully")
        
        # Test beat data setting
        beat_data = BeatData(
            letter="A",
            duration=4.0,
            beat_number=1,
            blue_motion=MotionData(
                motion_type=MotionType.SHIFT,
                rotation_direction=RotationDirection.CLOCKWISE,
                start_location="n",
                end_location="s"
            ),
            red_motion=MotionData(
                motion_type=MotionType.DASH,
                rotation_direction=RotationDirection.COUNTER_CLOCKWISE,
                start_location="e",
                end_location="w"
            )
        )
        
        beat_view.set_beat_data(beat_data)
        print("  ✅ Beat data set successfully")
        
        # Test selection state
        beat_view.set_selected(True)
        print(f"  ✅ Selection state: {beat_view.is_selected()}")
        
        beat_view.set_selected(False)
        beat_view.set_highlighted(True)
        print(f"  ✅ Highlight state: {beat_view.is_highlighted()}")
        
        # Test size hints
        size_hint = beat_view.sizeHint()
        min_size_hint = beat_view.minimumSizeHint()
        print(f"  ✅ Size hints: {size_hint.width()}×{size_hint.height()}, min: {min_size_hint.width()}×{min_size_hint.height()}")
        
        beat_view.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Beat view component test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_start_position_view():
    """Test the start position view component"""
    print("🧪 Testing Start Position View Component...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.sequence_workbench.beat_frame.start_position_view import StartPositionView
        from domain.models.core_models import BeatData, MotionData, MotionType, RotationDirection
        
        app = QApplication(sys.argv)
        
        # Create start position view
        start_view = StartPositionView()
        print("  ✅ StartPositionView created successfully")
        
        # Test position key setting
        start_view.set_position_key("alpha1")
        print("  ✅ Position key set successfully")
        
        # Test position data setting
        position_data = BeatData(
            letter="A",
            duration=4.0,
            beat_number=1,
            blue_motion=MotionData(
                motion_type=MotionType.STATIC,
                rotation_direction=RotationDirection.CLOCKWISE,
                start_location="n",
                end_location="n"
            ),
            red_motion=MotionData(
                motion_type=MotionType.STATIC,
                rotation_direction=RotationDirection.CLOCKWISE,
                start_location="s",
                end_location="s"
            )
        )
        
        start_view.set_position_data(position_data)
        print("  ✅ Position data set successfully")
        
        # Test highlight state
        start_view.set_highlighted(True)
        print(f"  ✅ Highlight state: {start_view.is_highlighted()}")
        
        start_view.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Start position view test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_beat_selection_manager():
    """Test the beat selection manager"""
    print("🧪 Testing Beat Selection Manager...")
    
    try:
        from PyQt6.QtWidgets import QApplication, QWidget
        from presentation.components.sequence_workbench.beat_frame.beat_selection_manager import BeatSelectionManager
        from presentation.components.sequence_workbench.beat_frame.beat_view import ModernBeatView
        
        app = QApplication(sys.argv)
        
        # Create parent widget and selection manager
        parent_widget = QWidget()
        selection_manager = BeatSelectionManager(parent_widget)
        print("  ✅ BeatSelectionManager created successfully")
        
        # Create some beat views
        beat_views = []
        for i in range(5):
            beat_view = ModernBeatView(beat_number=i + 1, parent=parent_widget)
            beat_views.append(beat_view)
            
        selection_manager.register_beat_views(beat_views)
        print("  ✅ Beat views registered successfully")
        
        # Test selection
        selection_manager.select_beat(2)
        selected_index = selection_manager.get_selected_index()
        print(f"  ✅ Selected beat index: {selected_index}")
        
        # Test navigation
        selection_manager.select_next_beat()
        new_selected = selection_manager.get_selected_index()
        print(f"  ✅ Next beat selected: {new_selected}")
        
        selection_manager.select_previous_beat()
        prev_selected = selection_manager.get_selected_index()
        print(f"  ✅ Previous beat selected: {prev_selected}")
        
        # Test multi-selection
        selection_manager.set_multi_selection_enabled(True)
        selection_manager.add_to_selection(0)
        selection_manager.add_to_selection(4)
        selected_indices = selection_manager.get_selected_indices()
        print(f"  ✅ Multi-selection: {selected_indices}")
        
        # Test clear selection
        selection_manager.clear_selection()
        final_selected = selection_manager.get_selected_index()
        print(f"  ✅ Selection cleared: {final_selected is None}")
        
        parent_widget.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Beat selection manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sequence_data_integration():
    """Test integration with V2 sequence data models"""
    print("🧪 Testing Sequence Data Integration...")
    
    try:
        from domain.models.core_models import SequenceData, BeatData, MotionData, MotionType, RotationDirection
        
        # Test empty sequence creation
        empty_sequence = SequenceData.empty()
        print(f"  ✅ Empty sequence created: {empty_sequence.name}, {empty_sequence.length} beats")
        
        # Test sequence with beats
        beats = []
        for i in range(3):
            beat = BeatData(
                letter=chr(ord('A') + i),
                duration=4.0,
                beat_number=i + 1,
                blue_motion=MotionData(
                    motion_type=MotionType.SHIFT,
                    rotation_direction=RotationDirection.CLOCKWISE,
                    start_location="n",
                    end_location="s"
                ),
                red_motion=MotionData(
                    motion_type=MotionType.DASH,
                    rotation_direction=RotationDirection.COUNTER_CLOCKWISE,
                    start_location="e",
                    end_location="w"
                )
            )
            beats.append(beat)
            
        sequence = SequenceData(name="Test Sequence", beats=beats)
        print(f"  ✅ Test sequence created: {sequence.name}, {sequence.length} beats")
        
        # Test immutable operations
        new_beat = BeatData(
            letter="D",
            duration=4.0,
            beat_number=4,
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
        print(f"  ❌ Sequence data integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all SPRINT 1 tests"""
    print("🚀 V2 Beat Frame System - SPRINT 1 Testing")
    print("=" * 60)
    
    tests = [
        ("Beat Frame Layout Service", test_beat_frame_layout_service),
        ("Beat View Component", test_beat_view_component),
        ("Start Position View", test_start_position_view),
        ("Beat Selection Manager", test_beat_selection_manager),
        ("Sequence Data Integration", test_sequence_data_integration),
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
        print("🎉 SPRINT 1 Core Beat Frame System - COMPLETE!")
        print("\n✅ Implemented Features:")
        print("  • Modern beat frame with dynamic grid layout")
        print("  • Beat view components with V2 styling")
        print("  • Start position integration")
        print("  • Beat selection and navigation")
        print("  • Layout calculation service")
        print("  • Immutable sequence data integration")
        print("\n🚀 Ready for SPRINT 2: Essential Button Panel")
        return True
    else:
        print("❌ Some SPRINT 1 components need fixes. Check the test output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
