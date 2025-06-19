#!/usr/bin/env python3
"""
Import Validation Test Script
===========================

This script tests all the import scenarios to ensure the architecture works.
Run this after setting up the new import architecture.
"""

from project_root import ensure_project_setup, print_debug_info
ensure_project_setup()

import sys
import subprocess
import tempfile
from pathlib import Path

def test_direct_execution():
    """Test running scripts directly with python"""
    print("=== Testing Direct Execution ===")
    
    test_files = [
        "test_clear_button_fix.py",
        "test_start_position_clear.py"
    ]
    
    from project_root import PROJECT_ROOT
    
    for test_file in test_files:
        test_path = PROJECT_ROOT / test_file
        if test_path.exists():
            print(f"\nTesting: {test_file}")
            try:
                result = subprocess.run(
                    [sys.executable, str(test_path)], 
                    cwd=PROJECT_ROOT,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    print(f"  ✅ {test_file} - SUCCESS")
                else:
                    print(f"  ❌ {test_file} - FAILED")
                    print(f"     STDERR: {result.stderr}")
            except Exception as e:
                print(f"  ❌ {test_file} - ERROR: {e}")
        else:
            print(f"  ⚠️  {test_file} - NOT FOUND")

def test_pytest_execution():
    """Test running with pytest"""
    print("\n=== Testing Pytest Execution ===")
    
    try:
        from project_root import PROJECT_ROOT
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "-q"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("  ✅ Pytest collection - SUCCESS")
        else:
            print("  ❌ Pytest collection - FAILED")
            print(f"     STDERR: {result.stderr}")
    except Exception as e:
        print(f"  ❌ Pytest test - ERROR: {e}")

def test_universal_runner():
    """Test the universal test runner"""
    print("\n=== Testing Universal Runner ===")
    
    try:
        from project_root import PROJECT_ROOT
        
        # Test validation only
        result = subprocess.run(
            [sys.executable, "run_test.py", "--validate-only"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("  ✅ Universal runner validation - SUCCESS")
        else:
            print("  ❌ Universal runner validation - FAILED")
            print(f"     STDERR: {result.stderr}")
            
    except Exception as e:
        print(f"  ❌ Universal runner test - ERROR: {e}")

def test_manual_imports():
    """Test importing key modules manually"""
    print("\n=== Testing Manual Imports ===")
    
    imports_to_test = [
        ("presentation", "Main presentation module"),
        ("presentation.components.workbench", "Workbench components"),
        ("domain.models.core_models", "Core domain models"),
        ("application.services", "Application services"),
        ("infrastructure", "Infrastructure layer")
    ]
    
    for import_name, description in imports_to_test:
        try:
            __import__(import_name)
            print(f"  ✅ {import_name} - {description}")
        except ImportError as e:
            print(f"  ❌ {import_name} - FAILED: {e}")
        except Exception as e:
            print(f"  ⚠️  {import_name} - UNEXPECTED ERROR: {e}")

def main():
    print("TKA DESKTOP IMPORT ARCHITECTURE VALIDATION")
    print("=" * 50)
    
    # Show debug info
    print("\n=== Environment Info ===")
    print_debug_info()
    
    # Run all tests
    test_manual_imports()
    test_direct_execution()
    test_pytest_execution()
    test_universal_runner()
    
    print("\n" + "=" * 50)
    print("VALIDATION COMPLETE")
    print("If you see ❌ errors above, run: python dev_setup.py --fix-missing")

if __name__ == "__main__":
    main()
