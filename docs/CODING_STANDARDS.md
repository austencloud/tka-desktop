# Modern Coding Standards & Best Practices

## 📋 **Core Principles**

### 1. **No Dummy Data - Use Real Pictograph Data**

- **NEVER** create fake/dummy BeatData objects for testing or initialization
- **ALWAYS** use the `PictographDatasetService` to load real pictograph data
- When pool initialization or testing requires beats, load from actual dataset

```python
# ❌ WRONG - Creating dummy beats
dummy_beat = BeatData(letter="A", blue_motion=MotionData(...))

# ✅ CORRECT - Using real data from dataset
dataset_service = PictographDatasetService()
real_beat = dataset_service.get_start_position_pictograph("alpha1_alpha1", "diamond")
```

### 2. **Class Size & Responsibility**

- **Maximum 200 lines** per class (excluding imports/docstrings)
- **Single Responsibility Principle** - each class should have one clear purpose
- **Split large classes** into smaller, focused components
- Use **composition over inheritance** where possible

### 3. **File Organization**

- **One primary class per file**
- File name should **match the class name** (no prefixes like "Modern")
- Group related utilities in separate modules
- Use `__init__.py` only for public API exports

### 4. **Dependency Injection**

- **ALL** external dependencies must be injected via constructor
- **NO** global state access or singleton patterns (except container)
- Services should be **interface-based** for testability

### 5. **Error Handling**

- **Graceful degradation** - system should work even if components fail
- **Specific exception types** - avoid generic Exception catches
- **Meaningful error messages** with context

## 🏗️ **Architecture Patterns**

### Component Structure

```
src/presentation/components/[component_name]/
├── __init__.py          # Public API only
├── [component_name].py  # Main component class
├── [component_name]_section.py
├── [component_name]_filter.py
└── [component_name]_widget.py
```

### Service Layer

```python
class SomeService:
    def __init__(self, dependency: IDependency):
        self._dependency = dependency

    def do_work(self) -> Result:
        # Implementation using injected dependencies
        pass
```

## 📊 **Data Standards**

### Real Data Loading Pattern

```python
class DataRequiringComponent:
    def __init__(self, dataset_service: PictographDatasetService):
        self._dataset_service = dataset_service

    def _load_real_beats(self, count: int = 6) -> List[BeatData]:
        positions = ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]
        beats = []

        for i in range(count):
            position_key = positions[i % len(positions)]
            beat = self._dataset_service.get_start_position_pictograph(
                position_key, "diamond"
            )
            if beat:
                beats.append(beat)

        return beats
```

### Object Pooling (Legacy Compatibility)

```python
class PooledComponent:
    MAX_OBJECTS = 36  # Legacy compatibility

    def __init__(self):
        self._pool: List[PoolObject] = []
        self._initialize_pool()

    def _initialize_pool(self):
        for i in range(self.MAX_OBJECTS):
            real_data = self._get_real_data_for_pool(i)
            obj = PoolObject(real_data)
            self._pool.append(obj)
```

## 🎯 **Component Splitting Guidelines**

### When to Split a Class

- **More than 200 lines**
- **Multiple responsibilities** (violates SRP)
- **Hard to test** due to complexity
- **Mixed concerns** (UI + business logic)

### Split Strategy

```python
# Before: Massive OptionPicker class
class MassiveOptionPicker:
    # 500+ lines handling everything

# After: Split into focused components
class OptionPicker:           # Main coordinator (50-100 lines)
class OptionPickerPool:       # Object pool management
class OptionPickerSections:   # Section management
class OptionPickerDisplay:    # Display update logic
class OptionPickerEvents:     # Event handling
```

## 🧪 **Testing Standards**

### Unit Test Structure

```python
class TestComponent:
    def setup_method(self):
        self.mock_service = Mock(spec=IService)
        self.component = Component(self.mock_service)

    def test_behavior_with_real_data(self):
        # Use real data, not mocks when testing data flow
        real_beat = load_real_beat_for_testing()
        result = self.component.process(real_beat)
        assert result.is_valid()
```

## 📝 **Documentation Standards**

### Code Comments

- **Minimal comments** - code should be self-documenting
- Comment **WHY, not WHAT**
- Document **complex algorithms** or **Legacy compatibility notes**

### Method Documentation

```python
def complex_method(self, param: ComplexType) -> Result:
    """Brief description of what this does.

    Args:
        param: What this parameter represents

    Returns:
        What the result contains

    Raises:
        SpecificException: When this specific error occurs
    """
```

## 🔄 **Migration Standards**

### Legacy Compatibility

- Maintain **object pooling patterns** for Qt stability
- Preserve **signal/slot architecture**
- Keep **layout algorithms** that work
- Document **Legacy behavioral equivalence**

### Progressive Enhancement

- **Gradual replacement** over big-bang rewrites
- **Feature flags** for new/old component switching
- **Backward compatibility** during transition
- **Performance benchmarking** before/after changes

## 🚨 **Code Review Checklist**

### Before Submitting

- [ ] No dummy/fake data - all data from services
- [ ] Classes under 200 lines
- [ ] Single responsibility per class
- [ ] Dependencies properly injected
- [ ] Real data used in tests
- [ ] Error handling implemented
- [ ] Performance impact considered

### During Review

- [ ] Architecture follows standards
- [ ] Code is testable
- [ ] No global state access
- [ ] Proper error handling
- [ ] Component boundaries clear
- [ ] Documentation adequate

## 📈 **Performance Standards**

### UI Responsiveness

- **No blocking operations** on main thread
- **Progressive loading** with callbacks
- **Object reuse** over recreation (Legacy pattern)
- **Lazy initialization** where appropriate

### Memory Management

- **Proper Qt parent/child relationships**
- **Object pooling** for frequently created objects
- **Explicit cleanup** in destructors
- **Avoid circular references**

## 🎨 **Style Guidelines**

### Naming Conventions

```python
# Classes: PascalCase
class OptionPickerSection:

# Methods/Variables: snake_case
def load_beat_options(self):
    beat_count = 0

# Constants: UPPER_SNAKE_CASE
MAX_PICTOGRAPHS = 36

# Private members: leading underscore
def _internal_method(self):
    self._private_data = []
```

### Import Organization

```python
# Standard library
import sys
from typing import List, Optional

# Third party
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal

# Local imports
from ..core.services import IService
from ..domain.models import BeatData
```

---

## 🎯 **Implementation Priority**

1. **Immediate**: Fix dummy data usage across codebase
2. **Short term**: Split large classes (starting with OptionPicker)
3. **Medium term**: Standardize dependency injection patterns
4. **Long term**: Complete Legacy compatibility verification

This document is **living** - update as patterns emerge and standards evolve.
