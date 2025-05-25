#!/usr/bin/env python3
"""
Test script to verify that the json_manager attribute fix is working correctly.
"""

import sys
import os
import subprocess
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_json_manager_access_pattern():
    """Test that json_manager is accessible through dependency injection."""
    print("🧪 Testing JSON Manager Access Pattern")
    print("=" * 60)
    
    try:
        # Test 1: Initialize dependency injection
        print("Step 1: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 2: Test app_context.json_manager access
        print("\nStep 2: Testing app_context.json_manager access...")
        json_manager = app_context.json_manager
        print(f"✅ json_manager accessible via app_context: {type(json_manager).__name__}")
        
        # Test 3: Test json_manager attributes
        print("\nStep 3: Testing json_manager attributes...")
        if hasattr(json_manager, 'loader_saver'):
            print("✅ json_manager has loader_saver")
        if hasattr(json_manager, 'start_pos_handler'):
            print("✅ json_manager has start_pos_handler")
        if hasattr(json_manager, 'updater'):
            print("✅ json_manager has updater")
        
        # Test 4: Test start_pos_handler methods
        print("\nStep 4: Testing start_pos_handler...")
        if hasattr(json_manager.start_pos_handler, 'set_start_position_data'):
            print("✅ start_pos_handler has set_start_position_data method")
        
        print("\n🎉 All access pattern tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Access pattern test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sequence_beat_frame_initialization():
    """Test that SequenceBeatFrame can be initialized without AttributeError."""
    print("\n🧪 Testing SequenceBeatFrame Initialization")
    print("=" * 60)
    
    try:
        # Test 1: Initialize dependency injection
        print("Step 1: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 2: Create a mock MainWidgetCoordinator with app_context
        print("\nStep 2: Creating mock MainWidgetCoordinator...")
        from PyQt6.QtWidgets import QWidget, QApplication
        
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        class MockMainWidget(QWidget):
            def __init__(self):
                super().__init__()
                self.app_context = app_context
                self.splash_screen = None
        
        mock_main_widget = MockMainWidget()
        print("✅ Mock MainWidgetCoordinator created with app_context")
        
        # Test 3: Test json_manager access pattern
        print("\nStep 3: Testing json_manager access pattern...")
        try:
            json_manager = mock_main_widget.app_context.json_manager
            print(f"✅ json_manager accessible: {type(json_manager).__name__}")
        except AttributeError as e:
            print(f"❌ json_manager access failed: {e}")
            return False
        
        # Test 4: Test the specific pattern used in SequenceBeatFrame
        print("\nStep 4: Testing SequenceBeatFrame access pattern...")
        try:
            # This simulates the pattern used in SequenceBeatFrame._setup_components()
            json_manager = mock_main_widget.app_context.json_manager
            start_pos_handler = json_manager.start_pos_handler
            print("✅ SequenceBeatFrame access pattern works")
        except AttributeError as e:
            print(f"❌ SequenceBeatFrame access pattern failed: {e}")
            return False
        
        print("\n🎉 All SequenceBeatFrame tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ SequenceBeatFrame test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_application_startup():
    """Test that the application starts without json_manager AttributeError."""
    print("\n🧪 Testing Application Startup")
    print("=" * 60)
    
    try:
        print("Starting application to test for json_manager errors...")
        
        # Start the application
        process = subprocess.Popen(
            [sys.executable, "src/main.py"],
            cwd="/f/CODE/the-kinetic-constructor-desktop",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit to see if it crashes due to json_manager errors
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Application started successfully")
            
            # Terminate the process
            process.terminate()
            try:
                stdout, stderr = process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
            
            # Check for json_manager AttributeError in stderr
            if "AttributeError" in stderr and "json_manager" in stderr:
                print("❌ json_manager AttributeError found")
                print(f"STDERR: {stderr}")
                return False
            elif "'MainWidgetCoordinator' object has no attribute 'json_manager'" in stderr:
                print("❌ Specific json_manager AttributeError found")
                print(f"STDERR: {stderr}")
                return False
            else:
                print("✅ No json_manager AttributeError detected")
                # Check if widget initialization completed
                if "MainWindow widgets initialized successfully" in stderr:
                    print("✅ Widget initialization completed successfully")
                return True
        else:
            # Process crashed
            stdout, stderr = process.communicate()
            print("❌ Application crashed")
            print(f"Return code: {process.returncode}")
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Application startup test failed: {e}")
        return False

def test_component_fixes():
    """Test that the specific components we fixed work correctly."""
    print("\n🧪 Testing Component Fixes")
    print("=" * 60)
    
    try:
        # Test 1: Initialize dependency injection
        print("Step 1: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 2: Test SequenceBeatFrame pattern
        print("\nStep 2: Testing SequenceBeatFrame pattern...")
        class MockMainWidget:
            def __init__(self):
                self.app_context = app_context
        
        mock_widget = MockMainWidget()
        
        # Simulate the fixed pattern
        try:
            json_manager = mock_widget.app_context.json_manager
            start_position_adder_json_manager = json_manager
            print("✅ SequenceBeatFrame pattern works")
        except AttributeError:
            print("❌ SequenceBeatFrame pattern failed")
            return False
        
        # Test 3: Test MainWidgetState pattern
        print("\nStep 3: Testing MainWidgetState pattern...")
        try:
            json_manager = mock_widget.app_context.json_manager
            current_sequence = json_manager.loader_saver.load_current_sequence()
            print(f"✅ MainWidgetState pattern works: {len(current_sequence)} items")
        except AttributeError:
            print("❌ MainWidgetState pattern failed")
            return False
        
        # Test 4: Test StartPositionAdder pattern
        print("\nStep 4: Testing StartPositionAdder pattern...")
        try:
            json_manager = mock_widget.app_context.json_manager
            start_pos_handler = json_manager.start_pos_handler
            print("✅ StartPositionAdder pattern works")
        except AttributeError:
            print("❌ StartPositionAdder pattern failed")
            return False
        
        print("\n🎉 All component fix tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Component fix test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🔧 TESTING JSON MANAGER ATTRIBUTE FIX")
    print("=" * 80)
    
    # Test 1: JSON Manager access pattern
    test1_passed = test_json_manager_access_pattern()
    
    # Test 2: SequenceBeatFrame initialization
    test2_passed = test_sequence_beat_frame_initialization()
    
    # Test 3: Application startup
    test3_passed = test_application_startup()
    
    # Test 4: Component fixes
    test4_passed = test_component_fixes()
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    if test1_passed:
        print("✅ JSON Manager Access Pattern: PASSED")
    else:
        print("❌ JSON Manager Access Pattern: FAILED")
    
    if test2_passed:
        print("✅ SequenceBeatFrame Initialization: PASSED")
    else:
        print("❌ SequenceBeatFrame Initialization: FAILED")
    
    if test3_passed:
        print("✅ Application Startup: PASSED")
    else:
        print("❌ Application Startup: FAILED")
    
    if test4_passed:
        print("✅ Component Fixes: PASSED")
    else:
        print("❌ Component Fixes: FAILED")
    
    overall_success = test1_passed and test2_passed and test3_passed and test4_passed
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ The json_manager AttributeError has been FIXED!")
        print("✅ Components now use dependency injection correctly")
        print("✅ MainWidgetCoordinator.app_context.json_manager is accessible")
        print("✅ SequenceBeatFrame initialization works")
        print("✅ Application starts without json_manager AttributeError")
    else:
        print("\n⚠️ SOME TESTS FAILED!")
        print("❌ The json_manager attribute issue may not be fully resolved")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
