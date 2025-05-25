#!/usr/bin/env python3
"""
Debug script to reproduce and fix the circular dependency error.
"""

import sys
import os
import traceback

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_step_by_step():
    """Test each step to find where the circular dependency occurs."""
    print("🔍 Debugging Circular Dependency Step by Step")
    print("=" * 60)
    
    try:
        print("Step 1: Testing dependency injection initialization...")
        from src.main import initialize_dependency_injection
        
        app_context = initialize_dependency_injection()
        print("✅ Step 1 passed: Dependency injection initialized")
        
        print("\nStep 2: Testing AppContextAdapter availability...")
        from src.core.migration_adapters import AppContextAdapter
        
        try:
            settings = AppContextAdapter.settings_manager()
            print("✅ Step 2 passed: AppContextAdapter is available")
        except RuntimeError as e:
            print(f"❌ Step 2 failed: {e}")
            return False
        
        print("\nStep 3: Testing direct JsonManager access...")
        try:
            json_manager = app_context.json_manager
            print(f"✅ Step 3 passed: JsonManager accessible: {type(json_manager).__name__}")
        except Exception as e:
            print(f"❌ Step 3 failed: {e}")
            traceback.print_exc()
            return False
        
        print("\nStep 4: Testing MainWindow creation...")
        try:
            from src.main import create_main_window
            from src.splash_screen.splash_screen import SplashScreen
            from src.settings_manager.settings_manager import SettingsManager
            from src.profiler import Profiler
            
            settings = SettingsManager()
            splash_screen = SplashScreen(None, settings)
            profiler = Profiler()
            
            main_window = create_main_window(profiler, splash_screen, app_context)
            print("✅ Step 4 passed: MainWindow created")
        except Exception as e:
            print(f"❌ Step 4 failed: {e}")
            traceback.print_exc()
            return False
        
        print("\nStep 5: Testing widget initialization...")
        try:
            main_window.initialize_widgets()
            print("✅ Step 5 passed: Widget initialization completed")
        except Exception as e:
            print(f"❌ Step 5 failed: {e}")
            traceback.print_exc()
            return False
        
        print("\n🎉 All steps passed! No circular dependency detected.")
        return True
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        traceback.print_exc()
        return False

def test_problematic_chain():
    """Test the specific chain that was causing the circular dependency."""
    print("\n🔍 Testing Problematic Component Chain")
    print("=" * 60)
    
    try:
        print("Initializing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        
        print("Testing JsonManager creation...")
        json_manager = app_context.json_manager
        print(f"JsonManager: {type(json_manager).__name__}")
        
        print("Testing SequenceDataLoaderSaver access...")
        loader_saver = json_manager.loader_saver
        print(f"SequenceDataLoaderSaver: {type(loader_saver).__name__}")
        
        print("Testing SequencePropertiesManager access...")
        props_manager = loader_saver.sequence_properties_manager
        print(f"SequencePropertiesManager: {type(props_manager).__name__}")
        
        print("Testing method calls...")
        sequence = loader_saver.load_current_sequence()
        print(f"load_current_sequence(): {len(sequence)} items")
        
        word = props_manager.calculate_word(None)
        print(f"calculate_word(): '{word}'")
        
        print("✅ Problematic chain test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Problematic chain test failed: {e}")
        traceback.print_exc()
        return False

def test_sequence_properties_manager_factory():
    """Test the SequencePropertiesManagerFactory specifically."""
    print("\n🔍 Testing SequencePropertiesManagerFactory")
    print("=" * 60)
    
    try:
        print("Testing create_legacy() without AppContextAdapter...")
        from src.main_window.main_widget.sequence_properties_manager.sequence_properties_manager_factory import SequencePropertiesManagerFactory
        
        # This should fail if AppContextAdapter is not available
        manager = SequencePropertiesManagerFactory.create_legacy()
        print(f"create_legacy() result: {type(manager).__name__}")
        
        print("Testing create_legacy() with AppContextAdapter...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        
        manager2 = SequencePropertiesManagerFactory.create_legacy()
        print(f"create_legacy() with AppContextAdapter: {type(manager2).__name__}")
        
        print("✅ SequencePropertiesManagerFactory test passed!")
        return True
        
    except Exception as e:
        print(f"❌ SequencePropertiesManagerFactory test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all debug tests."""
    print("🐛 DEBUGGING CIRCULAR DEPENDENCY ISSUE")
    print("=" * 60)
    
    # Test 1: Step by step
    test1_passed = test_step_by_step()
    
    # Test 2: Problematic chain
    test2_passed = test_problematic_chain()
    
    # Test 3: Factory
    test3_passed = test_sequence_properties_manager_factory()
    
    print("\n" + "=" * 60)
    print("DEBUG RESULTS SUMMARY")
    print("=" * 60)
    
    if test1_passed:
        print("✅ Step by Step Test: PASSED")
    else:
        print("❌ Step by Step Test: FAILED")
    
    if test2_passed:
        print("✅ Problematic Chain Test: PASSED")
    else:
        print("❌ Problematic Chain Test: FAILED")
    
    if test3_passed:
        print("✅ Factory Test: PASSED")
    else:
        print("❌ Factory Test: FAILED")
    
    if test1_passed and test2_passed and test3_passed:
        print("\n🎉 ALL TESTS PASSED! The issue appears to be fixed.")
    else:
        print("\n⚠️ SOME TESTS FAILED! The circular dependency issue still exists.")
    
    return 0 if (test1_passed and test2_passed and test3_passed) else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
