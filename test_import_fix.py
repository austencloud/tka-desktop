#!/usr/bin/env python3
"""
Test script to verify that the import issues in dependency_container.py are fixed.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_dependency_container_imports():
    """Test that the dependency container can be imported and configured without import errors."""
    print("🧪 Testing Dependency Container Import Fix")
    print("=" * 60)
    
    try:
        # Test 1: Import the dependency container module
        print("Step 1: Testing dependency container import...")
        from src.core.dependency_container import configure_dependencies
        print("✅ Dependency container imported successfully")
        
        # Test 2: Configure dependencies (this will test the JsonManager import)
        print("\nStep 2: Testing dependency configuration...")
        container = configure_dependencies()
        print("✅ Dependencies configured successfully")
        
        # Test 3: Check that JsonManager is registered
        print("\nStep 3: Testing JsonManager registration...")
        from src.interfaces.json_manager_interface import IJsonManager
        
        # Try to resolve JsonManager from container
        json_manager = container.resolve(IJsonManager)
        print(f"✅ JsonManager resolved successfully: {type(json_manager).__name__}")
        
        # Test 4: Test that JsonManager can be created
        print("\nStep 4: Testing JsonManager creation...")
        if json_manager:
            print(f"✅ JsonManager instance created: {type(json_manager).__name__}")
            
            # Check if it has expected attributes
            if hasattr(json_manager, 'loader_saver'):
                print("✅ JsonManager has loader_saver attribute")
            else:
                print("⚠️ JsonManager missing loader_saver attribute")
                
            if hasattr(json_manager, 'updater'):
                print("✅ JsonManager has updater attribute")
            else:
                print("⚠️ JsonManager missing updater attribute")
        else:
            print("❌ JsonManager instance is None")
            return False
        
        print("\n🎉 All import tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_json_manager_direct_import():
    """Test that JsonManager can be imported directly."""
    print("\n🧪 Testing Direct JsonManager Import")
    print("=" * 60)
    
    try:
        # Test direct import of JsonManager
        print("Testing direct JsonManager import...")
        from src.main_window.main_widget.json_manager.json_manager import JsonManager
        print("✅ JsonManager imported directly")
        
        # Test creating an instance
        print("Testing JsonManager instance creation...")
        json_manager = JsonManager(None)  # Pass None as app_context
        print(f"✅ JsonManager instance created: {type(json_manager).__name__}")
        
        # Test basic attributes
        if hasattr(json_manager, 'loader_saver'):
            print("✅ JsonManager has loader_saver")
        if hasattr(json_manager, 'updater'):
            print("✅ JsonManager has updater")
        if hasattr(json_manager, 'ori_calculator'):
            print("✅ JsonManager has ori_calculator")
        
        print("\n🎉 Direct import test passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Direct import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error in direct import: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_application_startup():
    """Test that the application starts without import errors."""
    print("\n🧪 Testing Application Startup")
    print("=" * 60)
    
    try:
        import subprocess
        import time
        
        print("Starting application to test for import errors...")
        
        # Start the application
        process = subprocess.Popen(
            [sys.executable, "src/main.py"],
            cwd="/f/CODE/the-kinetic-constructor-desktop",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit to see if it crashes due to import errors
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
            
            # Check for import errors in stderr
            if "ImportError" in stderr and "json_manager" in stderr:
                print("❌ Import errors related to json_manager found")
                print(f"STDERR: {stderr}")
                return False
            elif "could not be resolved" in stderr:
                print("❌ Import resolution errors found")
                print(f"STDERR: {stderr}")
                return False
            else:
                print("✅ No import errors detected")
                # Check if JSON Manager was registered successfully
                if "JSON Manager registered" in stderr:
                    print("✅ JSON Manager registered successfully")
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
    print("🔧 TESTING IMPORT FIX")
    print("=" * 80)
    
    # Test 1: Dependency container imports
    test1_passed = test_dependency_container_imports()
    
    # Test 2: Direct JsonManager import
    test2_passed = test_json_manager_direct_import()
    
    # Test 3: Application startup
    test3_passed = test_application_startup()
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    if test1_passed:
        print("✅ Dependency Container Imports: PASSED")
    else:
        print("❌ Dependency Container Imports: FAILED")
    
    if test2_passed:
        print("✅ Direct JsonManager Import: PASSED")
    else:
        print("❌ Direct JsonManager Import: FAILED")
    
    if test3_passed:
        print("✅ Application Startup: PASSED")
    else:
        print("❌ Application Startup: FAILED")
    
    overall_success = test1_passed and test2_passed and test3_passed
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ The import issues in dependency_container.py have been FIXED!")
        print("✅ JsonManager imports correctly")
        print("✅ No more 'could not be resolved' errors")
        print("✅ Dependency injection system works correctly")
        print("✅ Application starts without import errors")
    else:
        print("\n⚠️ SOME TESTS FAILED!")
        print("❌ Import issues may still exist")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
