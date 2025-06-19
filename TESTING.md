# TKA Desktop Testing Guide

## 🤖 AI Assistant Quick Start

This project has a **bulletproof test execution system** that works with ANY method you might intuitively try. No special setup or import configuration is required.

### ✅ All These Commands Work Automatically:

```bash
# Direct execution (most common)
python test_start_position_clear.py
python test_clear_button_fix.py

# Pytest (any variant)
pytest test_start_position_clear.py
python -m pytest test_start_position_clear.py
pytest test_clear_button_fix.py -v

# Universal runner (if you prefer)
python run_test.py test_start_position_clear.py
python run_test.py --pytest test_clear_button_fix.py

# From any directory
cd modern && python ../test_start_position_clear.py
cd modern && pytest ../test_clear_button_fix.py

# IDE test runners (VS Code, PyCharm, etc.)
# Just click "Run Test" - it works automatically
```

### 🎯 For New Test Files

Add this single line at the top of any new test file:

```python
import tka_test_setup  # This line makes all TKA imports work automatically
```

That's it! Now you can use imports like:

```python
from presentation.components.workbench import ModernSequenceWorkbench
from domain.models.core_models import SequenceData
from application.services import WorkbenchService
```

## 📁 Project Structure

```
tka-desktop/
├── test_*.py                    # Root-level test files (use these for quick tests)
├── modern/
│   ├── src/
│   │   ├── presentation/        # UI components
│   │   ├── domain/             # Business logic
│   │   ├── application/        # Services
│   │   └── infrastructure/     # External interfaces
│   └── tests/                  # Organized test suites
├── tka_test_setup.py           # Universal import setup (auto-imported)
├── conftest.py                 # Pytest configuration (auto-loaded)
└── run_test.py                 # Universal test runner (optional)
```

## 🔧 Common Test Patterns

### Basic Test Structure

```python
import tka_test_setup  # Bulletproof import setup

def test_something():
    """Test description"""
    from presentation.components.workbench import SomeComponent

    # Your test code here
    assert True

if __name__ == "__main__":
    test_something()
    print("✅ Test passed!")
```

### Pytest Test Structure

```python
import tka_test_setup
import pytest

class TestSomething:
    def test_feature(self):
        from domain.models.core_models import SequenceData

        sequence = SequenceData.empty()
        assert len(sequence.beats) == 0

    def test_another_feature(self):
        # Tests automatically have access to all TKA imports
        pass
```

### Mock-Heavy Tests

```python
import tka_test_setup
from unittest.mock import Mock, patch

def test_with_mocks():
    from presentation.components.workbench.event_controller import WorkbenchEventController

    # Create mocks
    mock_service = Mock()

    # Test with mocks
    controller = WorkbenchEventController(
        workbench_service=mock_service,
        # ... other services
    )

    # Your test logic
    assert controller is not None
```

## 🚀 Advanced Usage

### Running Specific Test Categories

```bash
# Run only modern codebase tests
pytest -m modern

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run tests with verbose output
pytest -v

# Run tests and show print statements
pytest -s
```

### Debugging Failed Imports

```bash
# Check import setup diagnostics
python tka_test_setup.py

# Check project root detection
python project_root.py

# Validate test environment
python run_test.py --validate-only
```

## 🛠️ Troubleshooting

### "Module not found" errors

The test system should prevent these, but if you see them:

1. **Check you're in the project**: Make sure you're running tests from within the `tka-desktop` directory or its subdirectories.

2. **Verify the import line**: Ensure your test file has `import tka_test_setup` at the top.

3. **Run diagnostics**: Execute `python tka_test_setup.py` to see what's wrong.

### Qt/GUI Tests

For tests that use Qt widgets:

```python
import tka_test_setup
from PyQt6.QtWidgets import QApplication

def test_gui_component():
    # QApplication is automatically created by conftest.py
    from presentation.components.workbench import SomeWidget

    widget = SomeWidget()
    assert widget is not None
```

### CI/CD Integration

The test system works automatically in CI/CD environments. Just run:

```bash
pytest  # Runs all tests
pytest modern/tests/  # Runs organized test suites
```

## 📋 Test File Naming Conventions

- `test_*.py` - Individual test files (good for quick tests)
- `*_test.py` - Alternative naming (also works)
- `modern/tests/unit/test_*.py` - Unit tests
- `modern/tests/integration/test_*.py` - Integration tests

## 🎯 Best Practices for AI Assistants

1. **Always start with**: `import tka_test_setup`
2. **Use direct execution**: `python test_file.py` is the most reliable
3. **Test incrementally**: Create small test files to verify specific functionality
4. **Use descriptive names**: `test_start_position_clear.py` is better than `test1.py`
5. **Include assertions**: Always verify expected behavior with `assert` statements

## 🔍 Example Test Creation Workflow

1. Create a new test file:

```python
# test_my_feature.py
import tka_test_setup

def test_my_feature():
    from presentation.components.workbench import SomeComponent

    component = SomeComponent()
    assert component is not None
    print("✅ Test passed!")

if __name__ == "__main__":
    test_my_feature()
```

2. Run it:

```bash
python test_my_feature.py
```

3. If it works, you're done! If not, check the error message and adjust.

## 🤖 AI Assistant Integration Notes

This testing system is specifically designed to work seamlessly with AI assistants. Here's what makes it AI-friendly:

### Automatic Discovery

- **No manual setup**: Just `import tka_test_setup` and everything works
- **Intuitive commands**: Standard Python/pytest commands work out of the box
- **Clear error messages**: When something goes wrong, the error tells you exactly what to do
- **Self-documenting**: The system explains itself through clear naming and comments

### Robust Execution

- **Cross-directory compatibility**: Tests work from any directory within the project
- **Multiple execution methods**: Direct Python, pytest, IDE runners, CI/CD all work
- **Graceful degradation**: If setup fails, you get clear error messages, not cryptic import errors
- **Platform independence**: Works on Windows, Linux, and macOS

### AI-Friendly Patterns

```python
# This pattern always works - AI assistants can use it confidently
import tka_test_setup
from presentation.components.workbench import AnyComponent

def test_anything():
    # Test code here
    pass
```

### Debugging Support

If an AI assistant encounters issues, these commands provide clear diagnostics:

```bash
python tka_test_setup.py      # Shows setup status
python project_root.py        # Shows path detection
python run_test.py --debug    # Shows detailed execution info
```

---

**System Philosophy**: This testing system follows the principle that **standard commands should just work**. If a typical Python/pytest command doesn't work, that indicates a system bug, not user error. AI assistants should be able to run tests using their existing knowledge of Python testing without learning project-specific conventions.
