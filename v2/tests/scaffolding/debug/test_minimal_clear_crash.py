#!/usr/bin/env python3
"""
Minimal Clear Sequence Crash Test for TKA V2
============================================

This test isolates the exact crash point during clear sequence operations
by testing each component individually to find where the crash occurs.
"""

import sys
import traceback
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Add v2 to path
v2_path = Path(__file__).parent
if str(v2_path) not in sys.path:
    sys.path.insert(0, str(v2_path))

try:
    from src.core.dependency_injection.simple_container import SimpleContainer
    from src.core.interfaces.core_services import ILayoutService
    from src.application.services.simple_layout_service import SimpleLayoutService
    from src.presentation.tabs.construct_tab_widget import ConstructTabWidget
    from src.domain.models.core_models import SequenceData, BeatData
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def test_sequence_data_empty():
    """Test if SequenceData.empty() works correctly."""
    print("\n🧪 Testing SequenceData.empty()...")
    try:
        empty_seq = SequenceData.empty()
        print(f"✅ SequenceData.empty() works: {empty_seq.length} beats")
        return True
    except Exception as e:
        print(f"❌ SequenceData.empty() failed: {e}")
        traceback.print_exc()
        return False


def test_workbench_creation():
    """Test if workbench can be created."""
    print("\n🧪 Testing workbench creation...")
    try:
        container = SimpleContainer()
        container.register_singleton(ILayoutService, SimpleLayoutService)
        
        construct_tab = ConstructTabWidget(container)
        workbench = construct_tab.workbench
        
        if workbench:
            print("✅ Workbench created successfully")
            return workbench
        else:
            print("❌ Workbench is None")
            return None
    except Exception as e:
        print(f"❌ Workbench creation failed: {e}")
        traceback.print_exc()
        return None


def test_workbench_set_sequence(workbench):
    """Test if workbench.set_sequence works with empty sequence."""
    print("\n🧪 Testing workbench.set_sequence with empty sequence...")
    try:
        empty_seq = SequenceData.empty()
        workbench.set_sequence(empty_seq)
        print("✅ workbench.set_sequence(empty) works")
        return True
    except Exception as e:
        print(f"❌ workbench.set_sequence(empty) failed: {e}")
        traceback.print_exc()
        return False


def test_beat_frame_set_sequence(workbench):
    """Test if beat frame set_sequence works with empty sequence."""
    print("\n🧪 Testing beat frame set_sequence with empty sequence...")
    try:
        beat_frame = workbench._beat_frame
        if beat_frame:
            empty_seq = SequenceData.empty()
            beat_frame.set_sequence(empty_seq)
            print("✅ beat_frame.set_sequence(empty) works")
            return True
        else:
            print("❌ Beat frame is None")
            return False
    except Exception as e:
        print(f"❌ beat_frame.set_sequence(empty) failed: {e}")
        traceback.print_exc()
        return False


def test_beat_frame_set_sequence_none(workbench):
    """Test if beat frame set_sequence works with None."""
    print("\n🧪 Testing beat frame set_sequence with None...")
    try:
        beat_frame = workbench._beat_frame
        if beat_frame:
            beat_frame.set_sequence(None)
            print("✅ beat_frame.set_sequence(None) works")
            return True
        else:
            print("❌ Beat frame is None")
            return False
    except Exception as e:
        print(f"❌ beat_frame.set_sequence(None) failed: {e}")
        traceback.print_exc()
        return False


def test_graph_service_update(workbench):
    """Test if graph service update works with empty sequence."""
    print("\n🧪 Testing graph service update with empty sequence...")
    try:
        graph_service = workbench._graph_service
        if graph_service:
            empty_seq = SequenceData.empty()
            graph_service.update_graph_display(empty_seq)
            print("✅ graph_service.update_graph_display(empty) works")
            return True
        else:
            print("❌ Graph service is None")
            return False
    except Exception as e:
        print(f"❌ graph_service.update_graph_display(empty) failed: {e}")
        traceback.print_exc()
        return False


def test_graph_service_update_none(workbench):
    """Test if graph service update works with None."""
    print("\n🧪 Testing graph service update with None...")
    try:
        graph_service = workbench._graph_service
        if graph_service:
            graph_service.update_graph_display(None)
            print("✅ graph_service.update_graph_display(None) works")
            return True
        else:
            print("❌ Graph service is None")
            return False
    except Exception as e:
        print(f"❌ graph_service.update_graph_display(None) failed: {e}")
        traceback.print_exc()
        return False


def test_dictionary_service(workbench):
    """Test if dictionary service works with empty sequence."""
    print("\n🧪 Testing dictionary service with empty sequence...")
    try:
        dict_service = workbench._dictionary_service
        if dict_service:
            empty_seq = SequenceData.empty()
            difficulty = dict_service.calculate_difficulty(empty_seq)
            word = dict_service.get_word_for_sequence(empty_seq)
            print(f"✅ Dictionary service works: difficulty={difficulty}, word={word}")
            return True
        else:
            print("❌ Dictionary service is None")
            return False
    except Exception as e:
        print(f"❌ Dictionary service failed: {e}")
        traceback.print_exc()
        return False


def test_update_display_safe(workbench):
    """Test if _update_display_safe works."""
    print("\n🧪 Testing _update_display_safe...")
    try:
        workbench._current_sequence = SequenceData.empty()
        workbench._update_display_safe()
        print("✅ _update_display_safe works")
        return True
    except Exception as e:
        print(f"❌ _update_display_safe failed: {e}")
        traceback.print_exc()
        return False


def test_handle_clear_step_by_step(workbench):
    """Test _handle_clear step by step to isolate crash point."""
    print("\n🧪 Testing _handle_clear step by step...")
    
    try:
        print("   Step 1: Creating empty sequence...")
        empty_sequence = SequenceData.empty()
        workbench._current_sequence = empty_sequence
        print("   ✅ Step 1 completed")
        
        print("   Step 2: Updating beat frame...")
        if workbench._beat_frame:
            workbench._beat_frame.set_sequence(empty_sequence)
        print("   ✅ Step 2 completed")
        
        print("   Step 3: Updating display safely...")
        workbench._update_display_safe()
        print("   ✅ Step 3 completed")
        
        print("   Step 4: Emitting signal...")
        workbench.sequence_modified.emit(empty_sequence)
        print("   ✅ Step 4 completed")
        
        print("✅ All _handle_clear steps completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ _handle_clear step failed: {e}")
        traceback.print_exc()
        return False


def test_actual_handle_clear(workbench):
    """Test the actual _handle_clear method."""
    print("\n🧪 Testing actual _handle_clear method...")
    try:
        workbench._handle_clear()
        print("✅ _handle_clear completed successfully")
        return True
    except Exception as e:
        print(f"❌ _handle_clear failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Main test function."""
    print("🔍 MINIMAL CLEAR SEQUENCE CRASH TEST")
    print("=" * 50)
    
    app = QApplication(sys.argv)
    
    # Run tests in sequence
    tests = [
        ("SequenceData.empty()", test_sequence_data_empty),
        ("Workbench Creation", test_workbench_creation),
    ]
    
    workbench = None
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        if test_name == "Workbench Creation":
            workbench = test_func()
            if not workbench:
                print("❌ Cannot continue without workbench")
                return 1
        else:
            result = test_func()
            if not result:
                print(f"❌ Test failed: {test_name}")
                return 1
    
    # Continue with workbench-dependent tests
    workbench_tests = [
        ("Workbench set_sequence(empty)", lambda: test_workbench_set_sequence(workbench)),
        ("Beat frame set_sequence(empty)", lambda: test_beat_frame_set_sequence(workbench)),
        ("Beat frame set_sequence(None)", lambda: test_beat_frame_set_sequence_none(workbench)),
        ("Graph service update(empty)", lambda: test_graph_service_update(workbench)),
        ("Graph service update(None)", lambda: test_graph_service_update_none(workbench)),
        ("Dictionary service", lambda: test_dictionary_service(workbench)),
        ("Update display safe", lambda: test_update_display_safe(workbench)),
        ("Handle clear step by step", lambda: test_handle_clear_step_by_step(workbench)),
        ("Actual handle clear", lambda: test_actual_handle_clear(workbench)),
    ]
    
    for test_name, test_func in workbench_tests:
        print(f"\n🧪 Running: {test_name}")
        result = test_func()
        if not result:
            print(f"❌ CRASH POINT FOUND: {test_name}")
            return 1
    
    print("\n🎉 ALL TESTS PASSED - NO CRASH DETECTED")
    print("This suggests the crash might be in signal handling or timing-related")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
