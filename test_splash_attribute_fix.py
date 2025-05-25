#!/usr/bin/env python3
"""
Test script to verify that the splash attribute fix is working correctly.
"""

import sys
import os
import subprocess
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_splash_attribute_access():
    """Test that splash_screen attribute is accessible in MainWidgetCoordinator."""
    print("🧪 Testing Splash Attribute Access")
    print("=" * 60)
    
    try:
        # Test 1: Initialize dependency injection
        print("Step 1: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 2: Create MainWindow
        print("\nStep 2: Testing MainWindow creation...")
        from src.main import create_main_window
        from src.splash_screen.splash_screen import SplashScreen
        from src.settings_manager.settings_manager import SettingsManager
        from src.profiler import Profiler
        from PyQt6.QtWidgets import QApplication
        
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        settings = SettingsManager()
        splash_screen = SplashScreen(None, settings)
        profiler = Profiler()
        
        main_window = create_main_window(profiler, splash_screen, app_context)
        print("✅ MainWindow created")
        
        # Test 3: Check splash_screen attribute
        print("\nStep 3: Testing splash_screen attribute access...")
        main_widget = main_window.main_widget
        
        if main_widget is None:
            print("⚠️ MainWidget not created yet, initializing widgets...")
            main_window.initialize_widgets()
            main_widget = main_window.main_widget
        
        # Test that splash_screen attribute exists
        if hasattr(main_widget, 'splash_screen'):
            splash_screen_attr = main_widget.splash_screen
            print(f"✅ splash_screen attribute exists: {type(splash_screen_attr).__name__}")
        else:
            print("❌ splash_screen attribute missing")
            return False
        
        # Test that splash_screen has updater
        if hasattr(splash_screen_attr, 'updater'):
            updater = splash_screen_attr.updater
            print(f"✅ splash_screen.updater exists: {type(updater).__name__}")
        else:
            print("❌ splash_screen.updater missing")
            return False
        
        # Test that updater has update_progress method
        if hasattr(updater, 'update_progress'):
            print("✅ splash_screen.updater.update_progress method exists")
        else:
            print("❌ splash_screen.updater.update_progress method missing")
            return False
        
        # Test calling update_progress
        try:
            updater.update_progress("TestWidget")
            print("✅ splash_screen.updater.update_progress() call successful")
        except Exception as e:
            print(f"❌ splash_screen.updater.update_progress() call failed: {e}")
            return False
        
        print("\n🎉 All splash attribute tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Splash attribute test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_widget_initialization():
    """Test that widgets can be initialized without AttributeError."""
    print("\n🧪 Testing Widget Initialization")
    print("=" * 60)
    
    try:
        # Test 1: Initialize dependency injection
        print("Step 1: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 2: Create MainWindow
        print("\nStep 2: Testing MainWindow creation...")
        from src.main import create_main_window
        from src.splash_screen.splash_screen import SplashScreen
        from src.settings_manager.settings_manager import SettingsManager
        from src.profiler import Profiler
        from PyQt6.QtWidgets import QApplication
        
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        settings = SettingsManager()
        splash_screen = SplashScreen(None, settings)
        profiler = Profiler()
        
        main_window = create_main_window(profiler, splash_screen, app_context)
        print("✅ MainWindow created")
        
        # Test 3: Initialize widgets (this was failing before)
        print("\nStep 3: Testing widget initialization...")
        main_window.initialize_widgets()
        print("✅ Widget initialization completed without AttributeError")
        
        # Test 4: Check that main_widget exists
        print("\nStep 4: Testing main_widget existence...")
        if main_window.main_widget:
            print(f"✅ main_widget exists: {type(main_window.main_widget).__name__}")
        else:
            print("❌ main_widget is None")
            return False
        
        print("\n🎉 All widget initialization tests passed!")
        return True
        
    except AttributeError as e:
        if "splash" in str(e):
            print(f"❌ AttributeError related to splash: {e}")
            return False
        else:
            print(f"❌ Other AttributeError: {e}")
            return False
    except Exception as e:
        print(f"❌ Widget initialization test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_application_startup():
    """Test that the application starts without AttributeError."""
    print("\n🧪 Testing Application Startup")
    print("=" * 60)
    
    try:
        print("Starting application...")
        
        # Start the application
        process = subprocess.Popen(
            [sys.executable, "src/main.py"],
            cwd="/f/CODE/the-kinetic-constructor-desktop",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit to see if it crashes
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Application started successfully")
            
            # Let it run a bit more
            time.sleep(2)
            
            # Terminate the process
            process.terminate()
            try:
                stdout, stderr = process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
            
            # Check for AttributeError related to splash
            if "AttributeError" in stderr and "splash" in stderr:
                print("❌ AttributeError related to splash found")
                print(f"STDERR: {stderr}")
                return False
            elif "AttributeError" in stderr and "MainWidgetCoordinator" in stderr:
                print("❌ AttributeError related to MainWidgetCoordinator found")
                print(f"STDERR: {stderr}")
                return False
            else:
                print("✅ No splash-related AttributeError found")
                if stderr.strip():
                    print(f"Note: Some other output in stderr: {stderr[:200]}...")
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
    print("🔧 TESTING SPLASH ATTRIBUTE FIX")
    print("=" * 80)
    
    # Test 1: Splash attribute access
    test1_passed = test_splash_attribute_access()
    
    # Test 2: Widget initialization
    test2_passed = test_widget_initialization()
    
    # Test 3: Application startup
    test3_passed = test_application_startup()
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    if test1_passed:
        print("✅ Splash Attribute Access: PASSED")
    else:
        print("❌ Splash Attribute Access: FAILED")
    
    if test2_passed:
        print("✅ Widget Initialization: PASSED")
    else:
        print("❌ Widget Initialization: FAILED")
    
    if test3_passed:
        print("✅ Application Startup: PASSED")
    else:
        print("❌ Application Startup: FAILED")
    
    overall_success = test1_passed and test2_passed and test3_passed
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ The splash attribute AttributeError has been FIXED!")
        print("✅ MainWidgetCoordinator.splash_screen is accessible")
        print("✅ Widget initialization works correctly")
        print("✅ Splash screen progress updates work")
        print("✅ Application starts without AttributeError")
    else:
        print("\n⚠️ SOME TESTS FAILED!")
        print("❌ The splash attribute issue may not be fully resolved")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
