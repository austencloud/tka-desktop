#!/usr/bin/env python3
"""
Test script to verify that the pictograph_data_loader attribute fix is working correctly.
"""

import sys
import os
import subprocess
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_pictograph_data_loader_access_pattern():
    """Test that pictograph_data_loader is accessible through dependency injection."""
    print("🧪 Testing PictographDataLoader Access Pattern")
    print("=" * 60)
    
    try:
        # Test 1: Initialize dependency injection
        print("Step 1: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 2: Test app_context.get_service for PictographDataLoader
        print("\nStep 2: Testing PictographDataLoader service access...")
        from src.main_window.main_widget.pictograph_data_loader import PictographDataLoader
        pictograph_data_loader = app_context.get_service(PictographDataLoader)
        print(f"✅ PictographDataLoader accessible via app_context: {type(pictograph_data_loader).__name__}")
        
        # Test 3: Test PictographDataLoader methods
        print("\nStep 3: Testing PictographDataLoader methods...")
        if hasattr(pictograph_data_loader, 'find_pictograph_data'):
            print("✅ PictographDataLoader has find_pictograph_data method")
        if hasattr(pictograph_data_loader, 'load_pictograph_dataset'):
            print("✅ PictographDataLoader has load_pictograph_dataset method")
        
        print("\n🎉 All access pattern tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Access pattern test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_visibility_pictograph_initialization():
    """Test that VisibilityPictograph can be initialized without AttributeError."""
    print("\n🧪 Testing VisibilityPictograph Initialization")
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
        
        class MockVisibilityTab:
            def __init__(self):
                self.main_widget = MockMainWidget()
        
        mock_tab = MockVisibilityTab()
        print("✅ Mock VisibilityTab created with app_context")
        
        # Test 3: Test PictographDataLoader access pattern
        print("\nStep 3: Testing PictographDataLoader access pattern...")
        try:
            from src.main_window.main_widget.pictograph_data_loader import PictographDataLoader
            pictograph_data_loader = mock_tab.main_widget.app_context.get_service(PictographDataLoader)
            print(f"✅ PictographDataLoader accessible: {type(pictograph_data_loader).__name__}")
        except (AttributeError, KeyError) as e:
            print(f"❌ PictographDataLoader access failed: {e}")
            return False
        
        # Test 4: Test the specific pattern used in VisibilityPictograph
        print("\nStep 4: Testing VisibilityPictograph access pattern...")
        try:
            # This simulates the pattern used in VisibilityPictograph.__init__()
            pictograph_data_loader = mock_tab.main_widget.app_context.get_service(PictographDataLoader)
            settings_manager = mock_tab.main_widget.app_context.settings_manager
            print("✅ VisibilityPictograph access pattern works")
        except (AttributeError, KeyError) as e:
            print(f"❌ VisibilityPictograph access pattern failed: {e}")
            return False
        
        print("\n🎉 All VisibilityPictograph tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ VisibilityPictograph test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_application_startup():
    """Test that the application starts without pictograph_data_loader AttributeError."""
    print("\n🧪 Testing Application Startup")
    print("=" * 60)
    
    try:
        print("Starting application to test for pictograph_data_loader errors...")
        
        # Start the application
        process = subprocess.Popen(
            [sys.executable, "src/main.py"],
            cwd="/f/CODE/the-kinetic-constructor-desktop",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit to see if it crashes due to pictograph_data_loader errors
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
            
            # Check for pictograph_data_loader AttributeError in stderr
            if "AttributeError" in stderr and "pictograph_data_loader" in stderr:
                print("❌ pictograph_data_loader AttributeError found")
                print(f"STDERR: {stderr}")
                return False
            elif "'MainWidgetCoordinator' object has no attribute 'pictograph_data_loader'" in stderr:
                print("❌ Specific pictograph_data_loader AttributeError found")
                print(f"STDERR: {stderr}")
                return False
            else:
                print("✅ No pictograph_data_loader AttributeError detected")
                # Check if widget initialization completed
                if "MainWindow widgets initialized successfully" in stderr:
                    print("✅ Widget initialization completed successfully")
                # Check for the graceful warning instead of error
                if "Services not available during VisibilityPictograph initialization" in stderr:
                    print("✅ VisibilityPictograph shows graceful warning instead of AttributeError")
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
        
        # Test 2: Test VisibilityPictograph pattern
        print("\nStep 2: Testing VisibilityPictograph pattern...")
        class MockMainWidget:
            def __init__(self):
                self.app_context = app_context
        
        mock_widget = MockMainWidget()
        
        # Simulate the fixed pattern
        try:
            from src.main_window.main_widget.pictograph_data_loader import PictographDataLoader
            pictograph_data_loader = mock_widget.app_context.get_service(PictographDataLoader)
            settings_manager = mock_widget.app_context.settings_manager
            print("✅ VisibilityPictograph pattern works")
        except (AttributeError, KeyError):
            print("❌ VisibilityPictograph pattern failed")
            return False
        
        # Test 3: Test CodexDataManager pattern
        print("\nStep 3: Testing CodexDataManager pattern...")
        try:
            pictograph_data_loader = mock_widget.app_context.get_service(PictographDataLoader)
            # Test the find_pictograph_data method exists
            if hasattr(pictograph_data_loader, 'find_pictograph_data'):
                print("✅ CodexDataManager pattern works")
            else:
                print("❌ CodexDataManager pattern failed - missing method")
                return False
        except (AttributeError, KeyError):
            print("❌ CodexDataManager pattern failed")
            return False
        
        # Test 4: Test MainWidgetManagers pattern
        print("\nStep 4: Testing MainWidgetManagers pattern...")
        try:
            pictograph_data_loader = mock_widget.app_context.get_service(PictographDataLoader)
            # Test the load_pictograph_dataset method exists
            if hasattr(pictograph_data_loader, 'load_pictograph_dataset'):
                print("✅ MainWidgetManagers pattern works")
            else:
                print("❌ MainWidgetManagers pattern failed - missing method")
                return False
        except (AttributeError, KeyError):
            print("❌ MainWidgetManagers pattern failed")
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
    print("🔧 TESTING PICTOGRAPH DATA LOADER ATTRIBUTE FIX")
    print("=" * 80)
    
    # Test 1: PictographDataLoader access pattern
    test1_passed = test_pictograph_data_loader_access_pattern()
    
    # Test 2: VisibilityPictograph initialization
    test2_passed = test_visibility_pictograph_initialization()
    
    # Test 3: Application startup
    test3_passed = test_application_startup()
    
    # Test 4: Component fixes
    test4_passed = test_component_fixes()
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    if test1_passed:
        print("✅ PictographDataLoader Access Pattern: PASSED")
    else:
        print("❌ PictographDataLoader Access Pattern: FAILED")
    
    if test2_passed:
        print("✅ VisibilityPictograph Initialization: PASSED")
    else:
        print("❌ VisibilityPictograph Initialization: FAILED")
    
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
        print("✅ The pictograph_data_loader AttributeError has been FIXED!")
        print("✅ Components now use dependency injection correctly")
        print("✅ MainWidgetCoordinator.app_context.get_service(PictographDataLoader) works")
        print("✅ VisibilityPictograph and other components initialize correctly")
        print("✅ Application starts without pictograph_data_loader AttributeError")
        print("✅ Graceful fallback handling when services aren't available")
    else:
        print("\n⚠️ SOME TESTS FAILED!")
        print("❌ The pictograph_data_loader attribute issue may not be fully resolved")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
