#!/usr/bin/env python3
"""
Test the JsonManager factory fix.
"""

import sys
import os
import traceback

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_json_manager_creation():
    """Test JsonManager creation with the new factory."""
    print("🔍 Testing JsonManager Factory Fix")
    print("=" * 50)
    
    try:
        print("Step 1: Initialize dependency injection...")
        from src.main import initialize_dependency_injection
        
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        print("Step 2: Test AppContextAdapter availability...")
        from src.core.migration_adapters import AppContextAdapter
        
        try:
            settings = AppContextAdapter.settings_manager()
            print("✅ AppContextAdapter is available")
        except RuntimeError as e:
            print(f"❌ AppContextAdapter not available: {e}")
            return False
        
        print("Step 3: Test JsonManager creation...")
        try:
            json_manager = app_context.json_manager
            print(f"✅ JsonManager created: {type(json_manager).__name__}")
            
            # Check if it has app_context
            loader_saver = json_manager.loader_saver
            print(f"✅ SequenceDataLoaderSaver accessible: {type(loader_saver).__name__}")
            
            props_manager = loader_saver.sequence_properties_manager
            print(f"✅ SequencePropertiesManager accessible: {type(props_manager).__name__}")
            
            # Test method calls
            sequence = loader_saver.load_current_sequence()
            print(f"✅ load_current_sequence() works: {len(sequence)} items")
            
            word = props_manager.calculate_word(None)
            print(f"✅ calculate_word() works: '{word}'")
            
            print("🎉 JsonManager factory fix successful!")
            return True
            
        except Exception as e:
            print(f"❌ JsonManager creation failed: {e}")
            traceback.print_exc()
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        traceback.print_exc()
        return False

def test_widget_initialization():
    """Test the full widget initialization that was causing the error."""
    print("\n🔍 Testing Full Widget Initialization")
    print("=" * 50)
    
    try:
        print("Step 1: Initialize dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        print("Step 2: Create MainWindow...")
        from src.main import create_main_window
        from src.splash_screen.splash_screen import SplashScreen
        from src.settings_manager.settings_manager import SettingsManager
        from src.profiler import Profiler
        
        settings = SettingsManager()
        splash_screen = SplashScreen(None, settings)
        profiler = Profiler()
        
        main_window = create_main_window(profiler, splash_screen, app_context)
        print("✅ MainWindow created")
        
        print("Step 3: Initialize widgets (this was failing)...")
        main_window.initialize_widgets()
        print("✅ Widget initialization completed successfully!")
        
        print("🎉 Full widget initialization test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Widget initialization test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run the tests."""
    print("🧪 Testing JsonManager Factory Fix")
    print("=" * 60)
    
    test1_passed = test_json_manager_creation()
    test2_passed = test_widget_initialization()
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    
    if test1_passed:
        print("✅ JsonManager Factory Test: PASSED")
    else:
        print("❌ JsonManager Factory Test: FAILED")
    
    if test2_passed:
        print("✅ Widget Initialization Test: PASSED")
    else:
        print("❌ Widget Initialization Test: FAILED")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED! The fix appears to work.")
        print("Now testing the actual application...")
        
        # Test the actual application
        print("\n🚀 Testing Actual Application Startup...")
        try:
            import subprocess
            result = subprocess.run([sys.executable, "src/main.py"], 
                                  cwd="/f/CODE/the-kinetic-constructor-desktop",
                                  timeout=10, 
                                  capture_output=True, 
                                  text=True)
            
            if result.returncode == 0:
                print("✅ Application started successfully!")
            else:
                print(f"❌ Application failed with return code {result.returncode}")
                print(f"STDERR: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("✅ Application started (timed out after 10s, which is expected)")
        except Exception as e:
            print(f"❌ Application test failed: {e}")
            return False
            
    else:
        print("\n⚠️ SOME TESTS FAILED! The fix needs more work.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
