#!/usr/bin/env python3
"""
Development Environment Setup and Validation
===========================================

This script validates the entire TKA Desktop development environment
and provides detailed diagnostics for import issues.

Usage:
    python dev_setup.py                    # Full validation
    python dev_setup.py --fix-missing      # Create missing __init__.py files
    python dev_setup.py --test-imports     # Test specific imports
    python dev_setup.py --reset-cache      # Clear Python cache files
"""

import sys
import os
import shutil
import argparse
from pathlib import Path
from typing import List, Tuple

def create_missing_init_files() -> List[Path]:
    """
    Create __init__.py files in directories that should be Python packages.
    
    Returns:
        List[Path]: Paths of created files
    """
    from project_root import PROJECT_ROOT, MODERN_SRC
    
    directories_needing_init = [
        MODERN_SRC,
        MODERN_SRC / "presentation",
        MODERN_SRC / "presentation" / "components",
        MODERN_SRC / "presentation" / "components" / "workbench",
        MODERN_SRC / "presentation" / "components" / "workbench" / "sequence_beat_frame",
        MODERN_SRC / "domain",
        MODERN_SRC / "domain" / "models",
        MODERN_SRC / "application",
        MODERN_SRC / "application" / "services",
        MODERN_SRC / "infrastructure",
    ]
    
    created_files = []
    
    for directory in directories_needing_init:
        if directory.exists() and directory.is_dir():
            init_file = directory / "__init__.py"
            if not init_file.exists():
                init_file.write_text("# Auto-generated __init__.py\n")
                created_files.append(init_file)
                print(f"Created: {init_file}")
    
    return created_files

def test_critical_imports() -> List[Tuple[str, bool, str]]:
    """
    Test imports that are critical for the application.
    
    Returns:
        List[Tuple[str, bool, str]]: (import_name, success, error_message)
    """
    critical_imports = [
        "presentation",
        "presentation.components",
        "presentation.components.workbench",
        "presentation.components.workbench.sequence_beat_frame",
        "domain.models.core_models",
        "application.services",
        "infrastructure",
    ]
    
    results = []
    
    for import_name in critical_imports:
        try:
            __import__(import_name)
            results.append((import_name, True, ""))
            print(f"✅ {import_name}")
        except ImportError as e:
            results.append((import_name, False, str(e)))
            print(f"❌ {import_name}: {e}")
        except Exception as e:
            results.append((import_name, False, f"Unexpected error: {e}"))
            print(f"⚠️  {import_name}: Unexpected error: {e}")
    
    return results

def clear_python_cache() -> int:
    """
    Clear all Python cache files (__pycache__ directories and .pyc files).
    
    Returns:
        int: Number of cache directories/files removed
    """
    from project_root import PROJECT_ROOT
    
    removed_count = 0
    
    # Remove __pycache__ directories
    for pycache_dir in PROJECT_ROOT.rglob("__pycache__"):
        if pycache_dir.is_dir():
            shutil.rmtree(pycache_dir)
            removed_count += 1
            print(f"Removed cache: {pycache_dir}")
    
    # Remove .pyc files
    for pyc_file in PROJECT_ROOT.rglob("*.pyc"):
        pyc_file.unlink()
        removed_count += 1
        print(f"Removed: {pyc_file}")
    
    return removed_count

def validate_project_structure() -> bool:
    """
    Validate that the project structure is correct.
    
    Returns:
        bool: True if structure is valid
    """
    from project_root import PROJECT_ROOT, MODERN_SRC
    
    required_paths = [
        PROJECT_ROOT / "modern",
        MODERN_SRC,
        MODERN_SRC / "presentation",
        MODERN_SRC / "domain", 
        MODERN_SRC / "application",
        MODERN_SRC / "infrastructure",
    ]
    
    all_valid = True
    
    print("Validating project structure...")
    for path in required_paths:
        if path.exists():
            print(f"✅ {path}")
        else:
            print(f"❌ Missing: {path}")
            all_valid = False
    
    return all_valid

def main():
    parser = argparse.ArgumentParser(description='TKA Desktop development environment setup')
    parser.add_argument('--fix-missing', action='store_true', help='Create missing __init__.py files')
    parser.add_argument('--test-imports', action='store_true', help='Test critical imports')
    parser.add_argument('--reset-cache', action='store_true', help='Clear Python cache files')
    parser.add_argument('--validate-structure', action='store_true', help='Validate project structure')
    
    args = parser.parse_args()
    
    # Setup project
    try:
        from project_root import ensure_project_setup, print_debug_info
        ensure_project_setup()
    except ImportError:
        print("ERROR: Cannot import project_root. Make sure project_root.py exists.")
        return 1
    
    if not any([args.fix_missing, args.test_imports, args.reset_cache, args.validate_structure]):
        # Run all validations by default
        args.fix_missing = True
        args.test_imports = True
        args.validate_structure = True
    
    print("=== TKA DESKTOP DEVELOPMENT SETUP ===\n")
    
    overall_success = True
    
    if args.validate_structure:
        print("1. Validating project structure...")
        if not validate_project_structure():
            overall_success = False
        print()
    
    if args.reset_cache:
        print("2. Clearing Python cache...")
        removed = clear_python_cache()
        print(f"Cleared {removed} cache files/directories\n")
    
    if args.fix_missing:
        print("3. Creating missing __init__.py files...")
        created = create_missing_init_files()
        if created:
            print(f"Created {len(created)} __init__.py files")
        else:
            print("All __init__.py files already exist")
        print()
    
    if args.test_imports:
        print("4. Testing critical imports...")
        results = test_critical_imports()
        failed_imports = [r for r in results if not r[1]]
        if failed_imports:
            overall_success = False
            print(f"\n❌ {len(failed_imports)} imports failed")
        else:
            print(f"\n✅ All {len(results)} imports successful")
        print()
    
    print("=== SETUP COMPLETE ===")
    if overall_success:
        print("✅ Development environment is ready!")
        return 0
    else:
        print("❌ Some issues found. Please fix the errors above.")
        print("\nFor debugging, run: python project_root.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())
