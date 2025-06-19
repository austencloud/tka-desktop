#!/usr/bin/env python3
"""
Universal Test Runner for TKA Desktop
=====================================

This script can run any test file from anywhere in the project with proper path setup.

Usage Examples:
    python run_test.py test_clear_button_fix.py
    python run_test.py modern/test_start_position_clear.py
    python run_test.py modern/tests/test_some_feature.py
    python run_test.py --pytest test_clear_button_fix.py
    python run_test.py --validate-only

The script automatically:
- Sets up all Python import paths
- Validates the environment
- Runs the test with proper error handling
- Provides detailed debugging info on failure
"""

import sys
import subprocess
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Universal test runner for TKA Desktop"
    )
    parser.add_argument("test_file", nargs="?", help="Test file to run")
    parser.add_argument(
        "--pytest",
        action="store_true",
        help="Run with pytest instead of direct execution",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate setup, don't run tests",
    )
    parser.add_argument("--debug", action="store_true", help="Show debug information")
    parser.add_argument(
        "--setup-only", action="store_true", help="Only setup paths and exit"
    )

    args = parser.parse_args()

    # Setup project environment
    try:
        from project_root import (
            ensure_project_setup,
            validate_imports,
            print_debug_info,
            PROJECT_ROOT,
        )
    except ImportError as e:
        print(f"ERROR: Cannot import project_root module: {e}")
        print("Make sure project_root.py exists in the project root directory.")
        return 1

    # Ensure paths are set up
    if not ensure_project_setup():
        print("ERROR: Failed to setup project environment")
        return 1

    if args.debug:
        print_debug_info()

    if args.setup_only:
        print("✅ Project setup completed successfully")
        return 0

    # Validate imports
    if not validate_imports():
        print("ERROR: Import validation failed")
        if not args.debug:
            print("Run with --debug for more information")
        return 1

    if args.validate_only:
        print("✅ All validations passed")
        return 0

    if not args.test_file:
        print("ERROR: No test file specified")
        parser.print_help()
        return 1

    # Find the test file
    test_path = Path(args.test_file)

    # If not absolute, try relative to project root
    if not test_path.is_absolute():
        test_path = PROJECT_ROOT / test_path

    if not test_path.exists():
        print(f"ERROR: Test file not found: {test_path}")
        return 1

    print(f"Running test: {test_path}")

    # Run the test
    try:
        if args.pytest:
            # Run with pytest
            cmd = [sys.executable, "-m", "pytest", str(test_path), "-v"]
        else:
            # Run directly
            cmd = [sys.executable, str(test_path)]

        result = subprocess.run(cmd, cwd=PROJECT_ROOT)
        return result.returncode

    except Exception as e:
        print(f"ERROR: Failed to run test: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
