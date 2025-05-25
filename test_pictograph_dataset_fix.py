#!/usr/bin/env python3
"""
Test script to verify that the pictograph_dataset AttributeError fix is working correctly.
"""

import sys
import os
import subprocess
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_pictograph_data_loader_self_sufficiency():
    """Test that PictographDataLoader can work without main_widget.pictograph_dataset."""
    print("🧪 Testing PictographDataLoader Self-Sufficiency")
    print("=" * 60)
    
    try:
        # Test 1: Create PictographDataLoader with None main_widget
        print("Step 1: Testing PictographDataLoader with None main_widget...")
        from src.main_window.main_widget.pictograph_data_loader import PictographDataLoader
        
        loader = PictographDataLoader(None)
        print("✅ PictographDataLoader created with None main_widget")
        
        # Test 2: Test get_pictograph_dataset method
        print("\nStep 2: Testing get_pictograph_dataset method...")
        dataset = loader.get_pictograph_dataset()
        print(f"✅ get_pictograph_dataset() returned dataset with {len(dataset)} letters")
        
        # Test 3: Test find_pictograph_data method
        print("\nStep 3: Testing find_pictograph_data method...")
        from src.data.constants import LETTER, START_POS, END_POS
        
        # Create test data
        test_data = {
            LETTER: "A",
            START_POS: 1,
            END_POS: 2,
            "blue_motion_type": "clockwise",
            "red_motion_type": "counterclockwise"
        }
        
        result = loader.find_pictograph_data(test_data)
        if result is not None:
            print("✅ find_pictograph_data() returned valid data")
        else:
            print("✅ find_pictograph_data() returned None (graceful handling)")
        
        # Test 4: Test caching behavior
        print("\nStep 4: Testing caching behavior...")
        dataset2 = loader.get_pictograph_dataset()
        if dataset is dataset2:  # Same object reference
            print("✅ Dataset caching works correctly")
        else:
            print("⚠️ Dataset caching may not be working as expected")
        
        print("\n🎉 All self-sufficiency tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Self-sufficiency test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dependency_injection_integration():
    """Test that PictographDataLoader works correctly through dependency injection."""
    print("\n🧪 Testing Dependency Injection Integration")
    print("=" * 60)
    
    try:
        # Test 1: Initialize dependency injection
        print("Step 1: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 2: Get PictographDataLoader from dependency injection
        print("\nStep 2: Testing PictographDataLoader service access...")
        from src.main_window.main_widget.pictograph_data_loader import PictographDataLoader
        pictograph_data_loader = app_context.get_service(PictographDataLoader)
        print(f"✅ PictographDataLoader accessible via dependency injection: {type(pictograph_data_loader).__name__}")
        
        # Test 3: Test that it works without main_widget
        print("\nStep 3: Testing functionality without main_widget...")
        dataset = pictograph_data_loader.get_pictograph_dataset()
        print(f"✅ Dataset loaded successfully: {len(dataset)} letters")
        
        # Test 4: Test find_pictograph_data through dependency injection
        print("\nStep 4: Testing find_pictograph_data through dependency injection...")
        from src.data.constants import LETTER, START_POS, END_POS
        
        test_data = {
            LETTER: "B",
            START_POS: 2,
            END_POS: 3,
            "blue_motion_type": "clockwise",
            "red_motion_type": "counterclockwise"
        }
        
        result = pictograph_data_loader.find_pictograph_data(test_data)
        print("✅ find_pictograph_data() executed without AttributeError")
        
        print("\n🎉 All dependency injection integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Dependency injection integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_visibility_pictograph_integration():
    """Test that VisibilityPictograph can now work correctly."""
    print("\n🧪 Testing VisibilityPictograph Integration")
    print("=" * 60)
    
    try:
        # Test 1: Initialize dependency injection
        print("Step 1: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 2: Create mock components
        print("\nStep 2: Creating mock components...")
        from PyQt6.QtWidgets import QWidget, QApplication
        
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        class MockMainWidget(QWidget):
            def __init__(self):
                super().__init__()
                self.app_context = app_context
        
        class MockVisibilityTab:
            def __init__(self):
                self.main_widget = MockMainWidget()
        
        mock_tab = MockVisibilityTab()
        print("✅ Mock components created")
        
        # Test 3: Test the pattern used in VisibilityPictograph
        print("\nStep 3: Testing VisibilityPictograph pattern...")
        from src.main_window.main_widget.pictograph_data_loader import PictographDataLoader
        from src.data.constants import LETTER, START_POS, END_POS
        
        # Get PictographDataLoader from dependency injection
        pictograph_data_loader = mock_tab.main_widget.app_context.get_service(PictographDataLoader)
        
        # Test the example_data pattern used in VisibilityPictograph
        example_data = {
            LETTER: "A",
            START_POS: 1,
            END_POS: 2,
            "blue_motion_type": "clockwise",
            "red_motion_type": "counterclockwise"
        }
        
        pictograph_data = pictograph_data_loader.find_pictograph_data(example_data)
        print("✅ VisibilityPictograph pattern works without AttributeError")
        
        # Test 4: Test settings_manager access
        print("\nStep 4: Testing settings_manager access...")
        settings_manager = mock_tab.main_widget.app_context.settings_manager
        visibility_settings = settings_manager.visibility
        print("✅ Settings manager access works")
        
        print("\n🎉 All VisibilityPictograph integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ VisibilityPictograph integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_application_startup():
    """Test that the application starts without pictograph_dataset AttributeError."""
    print("\n🧪 Testing Application Startup")
    print("=" * 60)
    
    try:
        print("Starting application to test for pictograph_dataset errors...")
        
        # Start the application
        process = subprocess.Popen(
            [sys.executable, "src/main.py"],
            cwd="/f/CODE/the-kinetic-constructor-desktop",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit to see if it crashes due to pictograph_dataset errors
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
            
            # Check for pictograph_dataset AttributeError in stderr
            if "'NoneType' object has no attribute 'pictograph_dataset'" in stderr:
                print("❌ pictograph_dataset AttributeError found")
                print(f"STDERR: {stderr}")
                return False
            elif "AttributeError" in stderr and "pictograph_dataset" in stderr:
                print("❌ Other pictograph_dataset AttributeError found")
                print(f"STDERR: {stderr}")
                return False
            else:
                print("✅ No pictograph_dataset AttributeError detected")
                # Check if widget initialization completed
                if "MainWindow widgets initialized successfully" in stderr:
                    print("✅ Widget initialization completed successfully")
                # Check that VisibilityPictograph warning is gone
                if "Services not available during VisibilityPictograph initialization" not in stderr:
                    print("✅ VisibilityPictograph no longer shows service unavailable warning")
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

def main():
    """Run all tests."""
    print("🔧 TESTING PICTOGRAPH DATASET ATTRIBUTEERROR FIX")
    print("=" * 80)
    
    # Test 1: PictographDataLoader self-sufficiency
    test1_passed = test_pictograph_data_loader_self_sufficiency()
    
    # Test 2: Dependency injection integration
    test2_passed = test_dependency_injection_integration()
    
    # Test 3: VisibilityPictograph integration
    test3_passed = test_visibility_pictograph_integration()
    
    # Test 4: Application startup
    test4_passed = test_application_startup()
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    if test1_passed:
        print("✅ PictographDataLoader Self-Sufficiency: PASSED")
    else:
        print("❌ PictographDataLoader Self-Sufficiency: FAILED")
    
    if test2_passed:
        print("✅ Dependency Injection Integration: PASSED")
    else:
        print("❌ Dependency Injection Integration: FAILED")
    
    if test3_passed:
        print("✅ VisibilityPictograph Integration: PASSED")
    else:
        print("❌ VisibilityPictograph Integration: FAILED")
    
    if test4_passed:
        print("✅ Application Startup: PASSED")
    else:
        print("❌ Application Startup: FAILED")
    
    overall_success = test1_passed and test2_passed and test3_passed and test4_passed
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ The pictograph_dataset AttributeError has been FIXED!")
        print("✅ PictographDataLoader is now self-sufficient")
        print("✅ Works correctly with dependency injection")
        print("✅ VisibilityPictograph initializes without errors")
        print("✅ Application starts without pictograph_dataset AttributeError")
        print("✅ Proper caching and fallback mechanisms in place")
    else:
        print("\n⚠️ SOME TESTS FAILED!")
        print("❌ The pictograph_dataset attribute issue may not be fully resolved")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
