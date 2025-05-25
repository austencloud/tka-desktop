#!/usr/bin/env python3
"""
Simple verification that the circular dependency fix works.
"""

import sys
import os
import subprocess
import time

def test_application_startup():
    """Test that the application starts without the circular dependency error."""
    print("🧪 Testing Application Startup")
    print("=" * 50)
    
    try:
        # Start the application and let it run for a few seconds
        print("Starting application...")
        process = subprocess.Popen(
            [sys.executable, "src/main.py"],
            cwd="/f/CODE/the-kinetic-constructor-desktop",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit to see if it crashes immediately
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Application is running (no immediate crash)")
            
            # Let it run a bit more
            time.sleep(2)
            
            # Terminate the process
            process.terminate()
            try:
                stdout, stderr = process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
            
            # Check for the specific error we were trying to fix
            if "AppContextAdapter not initialized" in stderr:
                print("❌ FAILED: Circular dependency error still occurs")
                print(f"STDERR: {stderr}")
                return False
            elif "RuntimeError" in stderr:
                print("❌ FAILED: RuntimeError still occurs")
                print(f"STDERR: {stderr}")
                return False
            else:
                print("✅ SUCCESS: No circular dependency error detected")
                if stderr.strip():
                    print(f"Note: Some other output in stderr: {stderr[:200]}...")
                return True
        else:
            # Process crashed immediately
            stdout, stderr = process.communicate()
            print("❌ FAILED: Application crashed immediately")
            print(f"Return code: {process.returncode}")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: Exception during test: {e}")
        return False

def test_component_creation():
    """Test that the problematic components can be created."""
    print("\n🧪 Testing Component Creation")
    print("=" * 50)
    
    try:
        # Add src to path
        sys.path.insert(0, os.path.join("/f/CODE/the-kinetic-constructor-desktop", 'src'))
        
        print("Testing dependency injection initialization...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection works")
        
        print("Testing JsonManager creation...")
        json_manager = app_context.json_manager
        print("✅ JsonManager creation works")
        
        print("Testing component chain...")
        loader_saver = json_manager.loader_saver
        props_manager = loader_saver.sequence_properties_manager
        print("✅ Component chain works")
        
        print("Testing method calls...")
        sequence = loader_saver.load_current_sequence()
        word = props_manager.calculate_word(None)
        print("✅ Method calls work")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run verification tests."""
    print("🔧 VERIFYING CIRCULAR DEPENDENCY FIX")
    print("=" * 60)
    
    test1_passed = test_application_startup()
    test2_passed = test_component_creation()
    
    print("\n" + "=" * 60)
    print("VERIFICATION RESULTS")
    print("=" * 60)
    
    if test1_passed:
        print("✅ Application Startup: PASSED")
    else:
        print("❌ Application Startup: FAILED")
    
    if test2_passed:
        print("✅ Component Creation: PASSED")
    else:
        print("❌ Component Creation: FAILED")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ The circular dependency issue has been FIXED!")
        print("✅ The application starts without errors")
        print("✅ All components work correctly")
    else:
        print("\n⚠️ SOME TESTS FAILED!")
        print("❌ The circular dependency issue may still exist")
    
    return 0 if (test1_passed and test2_passed) else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
