#!/usr/bin/env python3
"""
Debug the AppContextAdapter initialization issue.
"""

import sys
import os
import traceback

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_appcontext_adapter_timing():
    """Test when AppContextAdapter becomes available."""
    print("🔍 Testing AppContextAdapter Timing")
    print("=" * 50)
    
    try:
        print("Step 1: Testing AppContextAdapter before initialization...")
        from src.core.migration_adapters import AppContextAdapter
        
        try:
            settings = AppContextAdapter.settings_manager()
            print("❌ ERROR: AppContextAdapter should NOT be available yet!")
            return False
        except RuntimeError as e:
            print(f"✅ Expected: AppContextAdapter not available: {e}")
        
        print("\nStep 2: Initialize dependency injection...")
        from src.main import initialize_dependency_injection
        
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        print("\nStep 3: Testing AppContextAdapter after initialization...")
        try:
            settings = AppContextAdapter.settings_manager()
            print(f"✅ AppContextAdapter is now available: {type(settings).__name__}")
        except RuntimeError as e:
            print(f"❌ ERROR: AppContextAdapter should be available now: {e}")
            return False
        
        print("\nStep 4: Testing SequencePropertiesManagerFactory...")
        from src.main_window.main_widget.sequence_properties_manager.sequence_properties_manager_factory import SequencePropertiesManagerFactory
        
        manager = SequencePropertiesManagerFactory.create_legacy()
        print(f"✅ SequencePropertiesManagerFactory.create_legacy() works: {type(manager).__name__}")
        
        print("\nStep 5: Testing JsonManager creation...")
        json_manager = app_context.json_manager
        print(f"✅ JsonManager created: {type(json_manager).__name__}")
        
        loader_saver = json_manager.loader_saver
        print(f"✅ SequenceDataLoaderSaver: {type(loader_saver).__name__}")
        
        props_manager = loader_saver.sequence_properties_manager
        print(f"✅ SequencePropertiesManager: {type(props_manager).__name__}")
        
        print("\n🎉 All timing tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Timing test failed: {e}")
        traceback.print_exc()
        return False

def test_sequence_properties_manager_creation():
    """Test SequencePropertiesManager creation directly."""
    print("\n🔍 Testing SequencePropertiesManager Creation")
    print("=" * 50)
    
    try:
        print("Step 1: Test creation without AppContextAdapter...")
        from src.main_window.main_widget.sequence_properties_manager.sequence_properties_manager import SequencePropertiesManager
        
        try:
            manager = SequencePropertiesManager()
            print("❌ ERROR: This should fail without AppContextAdapter!")
            return False
        except RuntimeError as e:
            print(f"✅ Expected failure: {e}")
        
        print("\nStep 2: Test creation with None app_context...")
        try:
            manager = SequencePropertiesManager(None)
            print(f"✅ Creation with None app_context works: {type(manager).__name__}")
        except Exception as e:
            print(f"❌ Creation with None failed: {e}")
            traceback.print_exc()
            return False
        
        print("\nStep 3: Initialize dependency injection and test again...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        
        try:
            manager = SequencePropertiesManager()
            print(f"✅ Creation after initialization works: {type(manager).__name__}")
        except Exception as e:
            print(f"❌ Creation after initialization failed: {e}")
            traceback.print_exc()
            return False
        
        print("\n🎉 SequencePropertiesManager creation tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ SequencePropertiesManager creation test failed: {e}")
        traceback.print_exc()
        return False

def test_exact_error_reproduction():
    """Try to reproduce the exact error from the stack trace."""
    print("\n🔍 Reproducing Exact Error")
    print("=" * 50)
    
    try:
        print("Following the exact error path...")
        
        # Step 1: Initialize dependency injection
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Step 2: Create MainWindow
        from src.main import create_main_window
        from src.splash_screen.splash_screen import SplashScreen
        from src.settings_manager.settings_manager import SettingsManager
        from src.profiler import Profiler
        
        settings = SettingsManager()
        splash_screen = SplashScreen(None, settings)
        profiler = Profiler()
        
        main_window = create_main_window(profiler, splash_screen, app_context)
        print("✅ MainWindow created")
        
        # Step 3: This is where the error occurs
        print("Calling main_window.initialize_widgets() - this should trigger the error...")
        main_window.initialize_widgets()
        print("✅ Widget initialization completed - ERROR NOT REPRODUCED!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reproduced: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all debug tests."""
    print("🐛 DEBUGGING APPCONTEXTADAPTER ISSUE")
    print("=" * 60)
    
    test1_passed = test_appcontext_adapter_timing()
    test2_passed = test_sequence_properties_manager_creation()
    test3_passed = test_exact_error_reproduction()
    
    print("\n" + "=" * 60)
    print("DEBUG RESULTS")
    print("=" * 60)
    
    if test1_passed:
        print("✅ AppContextAdapter Timing: PASSED")
    else:
        print("❌ AppContextAdapter Timing: FAILED")
    
    if test2_passed:
        print("✅ SequencePropertiesManager Creation: PASSED")
    else:
        print("❌ SequencePropertiesManager Creation: FAILED")
    
    if test3_passed:
        print("✅ Exact Error Reproduction: PASSED (Error not reproduced)")
    else:
        print("❌ Exact Error Reproduction: FAILED (Error reproduced)")
    
    if test1_passed and test2_passed and test3_passed:
        print("\n🎉 ALL TESTS PASSED! The issue appears to be fixed.")
    else:
        print("\n⚠️ SOME TESTS FAILED! The issue still exists.")
    
    return 0 if (test1_passed and test2_passed and test3_passed) else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
