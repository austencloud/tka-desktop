"""
TKA Desktop Universal Test Setup
===============================

This module provides bulletproof test setup that works with ANY test execution method.
Simply import this at the top of any test file to ensure all imports work correctly.

AI-Friendly Usage:
    # Add this line at the top of any test file:
    import tka_test_setup

    # That's it! Now all TKA Desktop imports will work regardless of how the test is run.

Supported Execution Methods:
    - python test_file.py
    - pytest test_file.py  
    - python -m pytest test_file.py
    - IDE test runners (VS Code, PyCharm, etc.)
    - CI/CD pipelines
    - Any other Python execution context

This module automatically:
    - Detects the TKA Desktop project root
    - Configures Python import paths
    - Enables imports like: from presentation.components.workbench import ...
    - Works from any directory within the project
    - Provides clear error messages if setup fails
"""

import sys
import os
from pathlib import Path
import warnings

# Global flag to prevent duplicate setup
_TKA_SETUP_COMPLETED = False


def find_tka_project_root(start_path=None):
    """
    Find the TKA Desktop project root by looking for characteristic files/directories.
    
    Args:
        start_path: Path to start searching from (defaults to current file location)
        
    Returns:
        Path: Project root directory
        
    Raises:
        RuntimeError: If project root cannot be found
    """
    if start_path is None:
        start_path = Path(__file__).parent
    else:
        start_path = Path(start_path)
    
    # Look for these files/directories to identify project root
    project_markers = [
        'modern/src/presentation',
        'modern/src/domain', 
        'modern/src/application',
        'project_root.py',
        'pytest.ini',
        'pyrightconfig.json'
    ]
    
    current = start_path.resolve()
    
    # Search up the directory tree
    for _ in range(10):  # Prevent infinite loops
        # Check if this directory looks like the project root
        marker_count = sum(1 for marker in project_markers if (current / marker).exists())
        
        if marker_count >= 3:  # Found enough markers
            return current
            
        # Move up one level
        parent = current.parent
        if parent == current:  # Reached filesystem root
            break
        current = parent
    
    # Fallback: try common project names in the path
    current = start_path.resolve()
    while current.parent != current:
        if current.name.lower() in ['tka-desktop', 'tka_desktop', 'the-kinetic-constructor']:
            return current
        current = current.parent
    
    raise RuntimeError(f"Could not find TKA Desktop project root starting from {start_path}")


def setup_tka_imports(verbose=False):
    """
    Set up Python import paths for TKA Desktop project.
    
    Args:
        verbose: If True, print setup information
        
    Returns:
        bool: True if setup successful, False otherwise
    """
    global _TKA_SETUP_COMPLETED
    
    if _TKA_SETUP_COMPLETED:
        return True
    
    try:
        # Find project root
        project_root = find_tka_project_root()
        
        # Define required paths
        required_paths = [
            project_root / "modern" / "src",  # For: from presentation.components...
            project_root / "modern",          # For: from src.presentation...
            project_root,                     # For: from project_root import...
        ]
        
        # Add paths to sys.path
        paths_added = []
        for path in required_paths:
            path_str = str(path)
            if path.exists() and path_str not in sys.path:
                sys.path.insert(0, path_str)
                paths_added.append(path_str)
        
        # Set PYTHONPATH for subprocess consistency
        if paths_added:
            current_pythonpath = os.environ.get('PYTHONPATH', '')
            pythonpath_parts = paths_added.copy()
            
            if current_pythonpath:
                existing_parts = current_pythonpath.split(os.pathsep)
                pythonpath_parts.extend([p for p in existing_parts if p not in pythonpath_parts])
            
            os.environ['PYTHONPATH'] = os.pathsep.join(pythonpath_parts)
        
        _TKA_SETUP_COMPLETED = True
        
        if verbose:
            print(f"✅ TKA Desktop test setup complete!")
            print(f"   Project root: {project_root}")
            print(f"   Added {len(paths_added)} paths to sys.path")
        
        return True
        
    except Exception as e:
        error_msg = f"TKA Desktop test setup failed: {e}"
        if verbose:
            print(f"❌ {error_msg}")
        else:
            warnings.warn(error_msg, UserWarning)
        return False


def validate_tka_imports():
    """
    Validate that key TKA Desktop imports work correctly.
    
    Returns:
        bool: True if validation successful
    """
    test_imports = [
        'presentation',
        'presentation.components',
        'domain.models',
        'application.services'
    ]
    
    failed_imports = []
    for import_name in test_imports:
        try:
            __import__(import_name)
        except ImportError:
            failed_imports.append(import_name)
    
    if failed_imports:
        warnings.warn(
            f"Some TKA Desktop imports failed: {failed_imports}. "
            f"This may indicate missing dependencies or incorrect project structure.",
            UserWarning
        )
        return False
    
    return True


def get_tka_diagnostic_info():
    """
    Get diagnostic information about the TKA Desktop test setup.
    
    Returns:
        dict: Diagnostic information
    """
    try:
        project_root = find_tka_project_root()
        modern_src = project_root / "modern" / "src"
        
        return {
            'setup_completed': _TKA_SETUP_COMPLETED,
            'project_root': str(project_root),
            'modern_src_exists': modern_src.exists(),
            'current_working_directory': os.getcwd(),
            'python_executable': sys.executable,
            'sys_path_entries': len(sys.path),
            'pythonpath_set': 'PYTHONPATH' in os.environ,
            'import_validation': validate_tka_imports() if _TKA_SETUP_COMPLETED else False
        }
    except Exception as e:
        return {
            'setup_completed': False,
            'error': str(e),
            'current_working_directory': os.getcwd(),
            'python_executable': sys.executable
        }


# AUTOMATIC SETUP: This runs when the module is imported
# This is the key feature that makes the system AI-friendly and bulletproof
try:
    setup_tka_imports(verbose=False)
except Exception:
    # Fail silently to avoid breaking imports in edge cases
    pass


# Convenience functions for explicit setup (optional)
def ensure_tka_setup(verbose=False):
    """
    Explicitly ensure TKA Desktop is set up for testing.
    
    This is optional - setup happens automatically on import.
    Use this if you want verbose output or explicit control.
    
    Args:
        verbose: If True, print setup information
        
    Returns:
        bool: True if setup successful
    """
    return setup_tka_imports(verbose=verbose)


def print_tka_diagnostics():
    """Print diagnostic information about TKA Desktop test setup."""
    print("TKA Desktop Test Setup Diagnostics")
    print("=" * 40)
    
    info = get_tka_diagnostic_info()
    for key, value in info.items():
        print(f"{key:25}: {value}")


# Export the main functions that users might need
__all__ = [
    'ensure_tka_setup',      # Explicit setup (optional)
    'validate_tka_imports',  # Validation function
    'print_tka_diagnostics', # Diagnostic information
    'get_tka_diagnostic_info' # Diagnostic data
]


if __name__ == "__main__":
    # When run directly, show diagnostics
    print_tka_diagnostics()
    print("\nTesting imports...")
    if validate_tka_imports():
        print("✅ All key imports work correctly!")
    else:
        print("❌ Some imports failed. Check the warnings above.")
