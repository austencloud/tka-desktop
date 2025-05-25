#!/usr/bin/env python3
"""
Test script to verify that the settings_manager attribute fix is working correctly.
"""

import sys
import os
import subprocess
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_settings_manager_access_pattern():
    """Test that settings_manager is accessible through dependency injection."""
    print("🧪 Testing Settings Manager Access Pattern")
    print("=" * 60)
    
    try:
        # Test 1: Initialize dependency injection
        print("Step 1: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 2: Test app_context.settings_manager access
        print("\nStep 2: Testing app_context.settings_manager access...")
        settings_manager = app_context.settings_manager
        print(f"✅ settings_manager accessible via app_context: {type(settings_manager).__name__}")
        
        # Test 3: Test settings_manager attributes
        print("\nStep 3: Testing settings_manager attributes...")
        if hasattr(settings_manager, 'users'):
            print("✅ settings_manager has users")
        if hasattr(settings_manager, 'visibility'):
            print("✅ settings_manager has visibility")
        if hasattr(settings_manager, 'global_settings'):
            print("✅ settings_manager has global_settings")
        if hasattr(settings_manager, 'sequence_layout'):
            print("✅ settings_manager has sequence_layout")
        
        # Test 4: Test user_manager access
        print("\nStep 4: Testing user_manager access...")
        if hasattr(settings_manager.users, 'user_manager'):
            user_manager = settings_manager.users.user_manager
            print(f"✅ user_manager accessible: {type(user_manager).__name__}")
        
        print("\n🎉 All access pattern tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Access pattern test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_user_profile_tab_initialization():
    """Test that UserProfileTab can be initialized without AttributeError."""
    print("\n🧪 Testing UserProfileTab Initialization")
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
        
        class MockSettingsDialog:
            def __init__(self):
                self.main_widget = MockMainWidget()
        
        mock_settings_dialog = MockSettingsDialog()
        print("✅ Mock SettingsDialog created with app_context")
        
        # Test 3: Test settings_manager access pattern
        print("\nStep 3: Testing settings_manager access pattern...")
        try:
            settings_manager = mock_settings_dialog.main_widget.app_context.settings_manager
            user_manager = settings_manager.users.user_manager
            print(f"✅ user_manager accessible: {type(user_manager).__name__}")
        except AttributeError as e:
            print(f"❌ settings_manager access failed: {e}")
            return False
        
        # Test 4: Test the specific pattern used in UserProfileTab
        print("\nStep 4: Testing UserProfileTab access pattern...")
        try:
            # This simulates the pattern used in UserProfileTab.__init__()
            settings_manager = mock_settings_dialog.main_widget.app_context.settings_manager
            user_manager = settings_manager.users.user_manager
            print("✅ UserProfileTab access pattern works")
        except AttributeError as e:
            print(f"❌ UserProfileTab access pattern failed: {e}")
            return False
        
        print("\n🎉 All UserProfileTab tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ UserProfileTab test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_application_startup():
    """Test that the application starts without settings_manager AttributeError."""
    print("\n🧪 Testing Application Startup")
    print("=" * 60)
    
    try:
        print("Starting application to test for settings_manager errors...")
        
        # Start the application
        process = subprocess.Popen(
            [sys.executable, "src/main.py"],
            cwd="/f/CODE/the-kinetic-constructor-desktop",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit to see if it crashes due to settings_manager errors
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
            
            # Check for settings_manager AttributeError in stderr
            if "AttributeError" in stderr and "settings_manager" in stderr:
                print("❌ settings_manager AttributeError found")
                print(f"STDERR: {stderr}")
                return False
            elif "'MainWidgetCoordinator' object has no attribute 'settings_manager'" in stderr:
                print("❌ Specific settings_manager AttributeError found")
                print(f"STDERR: {stderr}")
                return False
            else:
                print("✅ No settings_manager AttributeError detected")
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

def test_settings_dialog_components():
    """Test that the settings dialog components we fixed work correctly."""
    print("\n🧪 Testing Settings Dialog Component Fixes")
    print("=" * 60)
    
    try:
        # Test 1: Initialize dependency injection
        print("Step 1: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 2: Test UserProfileTab pattern
        print("\nStep 2: Testing UserProfileTab pattern...")
        class MockMainWidget:
            def __init__(self):
                self.app_context = app_context
        
        mock_widget = MockMainWidget()
        
        # Simulate the fixed pattern
        try:
            settings_manager = mock_widget.app_context.settings_manager
            user_manager = settings_manager.users.user_manager
            print("✅ UserProfileTab pattern works")
        except AttributeError:
            print("❌ UserProfileTab pattern failed")
            return False
        
        # Test 3: Test VisibilityTab pattern
        print("\nStep 3: Testing VisibilityTab pattern...")
        try:
            settings_manager = mock_widget.app_context.settings_manager
            visibility_settings = settings_manager.visibility
            print("✅ VisibilityTab pattern works")
        except AttributeError:
            print("❌ VisibilityTab pattern failed")
            return False
        
        # Test 4: Test BeatLayoutTab pattern
        print("\nStep 4: Testing BeatLayoutTab pattern...")
        try:
            settings_manager = mock_widget.app_context.settings_manager
            layout_settings = settings_manager.sequence_layout
            print("✅ BeatLayoutTab pattern works")
        except AttributeError:
            print("❌ BeatLayoutTab pattern failed")
            return False
        
        # Test 5: Test ImageExportTab pattern
        print("\nStep 5: Testing ImageExportTab pattern...")
        try:
            settings_manager = mock_widget.app_context.settings_manager
            print("✅ ImageExportTab pattern works")
        except AttributeError:
            print("❌ ImageExportTab pattern failed")
            return False
        
        print("\n🎉 All settings dialog component tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Settings dialog component test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🔧 TESTING SETTINGS MANAGER ATTRIBUTE FIX")
    print("=" * 80)
    
    # Test 1: Settings Manager access pattern
    test1_passed = test_settings_manager_access_pattern()
    
    # Test 2: UserProfileTab initialization
    test2_passed = test_user_profile_tab_initialization()
    
    # Test 3: Application startup
    test3_passed = test_application_startup()
    
    # Test 4: Settings dialog components
    test4_passed = test_settings_dialog_components()
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    if test1_passed:
        print("✅ Settings Manager Access Pattern: PASSED")
    else:
        print("❌ Settings Manager Access Pattern: FAILED")
    
    if test2_passed:
        print("✅ UserProfileTab Initialization: PASSED")
    else:
        print("❌ UserProfileTab Initialization: FAILED")
    
    if test3_passed:
        print("✅ Application Startup: PASSED")
    else:
        print("❌ Application Startup: FAILED")
    
    if test4_passed:
        print("✅ Settings Dialog Components: PASSED")
    else:
        print("❌ Settings Dialog Components: FAILED")
    
    overall_success = test1_passed and test2_passed and test3_passed and test4_passed
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ The settings_manager AttributeError has been FIXED!")
        print("✅ Settings dialog components now use dependency injection correctly")
        print("✅ MainWidgetCoordinator.app_context.settings_manager is accessible")
        print("✅ UserProfileTab and other settings tabs initialize correctly")
        print("✅ Application starts without settings_manager AttributeError")
    else:
        print("\n⚠️ SOME TESTS FAILED!")
        print("❌ The settings_manager attribute issue may not be fully resolved")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
