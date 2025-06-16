# Code Quality Improvement Migration Guide

This guide outlines the steps to migrate from the current architecture to the improved, modern design patterns.

## Overview of Changes

### 1. Global Singleton Elimination → Dependency Injection
- **Old**: `AppContext` global singleton
- **New**: `DependencyContainer` with proper dependency injection
- **Benefits**: Testable, loosely coupled, follows SOLID principles

### 2. God Class Decomposition → Single Responsibility Components
- **Old**: Monolithic `MainWidget` class
- **New**: `MainWidgetCoordinator` with focused managers
- **Benefits**: Easier to test, maintain, and extend

### 3. Type Safety Improvements
- **Old**: Missing type hints, wildcard imports
- **New**: Comprehensive type annotations and typed interfaces
- **Benefits**: Better IDE support, fewer runtime errors, clearer contracts

## Migration Steps

### Phase 1: Dependency Injection Setup (Week 1)

#### Step 1.1: Configure Dependencies
```python
# In main.py, replace AppContext initialization
from src.core.dependency_container import configure_dependencies
from src.core.application_context import create_application_context

def main():
    # ... existing code ...
    
    # Configure dependency injection
    container = configure_dependencies()
    
    # Register services
    container.register_singleton(ISettingsManager, SettingsManager)
    container.register_singleton(IJsonManager, JsonManager)
    
    # Create application context
    app_context = create_application_context(container)
    
    # Create main window with dependency injection
    main_window = MainWindow(profiler, splash_screen, app_context)
```

#### Step 1.2: Update MainWindow Constructor
```python
# In main_window.py
class MainWindow(QMainWindow):
    def __init__(
        self, 
        profiler: "Profiler", 
        splash_screen: "SplashScreen",
        app_context: ApplicationContext  # Add this parameter
    ) -> None:
        super().__init__()
        self.profiler = profiler
        self.app_context = app_context  # Store context
        
        # Use new MainWidgetCoordinator instead of MainWidget
        from main_window.main_widget.core.main_widget_coordinator import MainWidgetFactory
        self.main_widget = MainWidgetFactory.create(self, splash_screen, app_context)
```

### Phase 2: MainWidget Refactoring (Week 2)

#### Step 2.1: Replace MainWidget Usage
```python
# Old code (to be replaced gradually)
main_widget = MainWidget(main_window, splash_screen)
main_widget.construct_tab.do_something()

# New code
coordinator = MainWidgetCoordinator(main_window, splash_screen, app_context)
construct_tab = coordinator.get_tab_widget("construct")
if construct_tab:
    construct_tab.do_something()
```

#### Step 2.2: Update Component Access Patterns
```python
# Old pattern (global singleton access)
settings = AppContext.settings_manager()

# New pattern (dependency injection)
class SomeComponent:
    def __init__(self, app_context: ApplicationContext):
        self.app_context = app_context
    
    def some_method(self):
        settings = self.app_context.settings_manager
```

### Phase 3: Type Safety Implementation (Week 3)

#### Step 3.1: Add Type Hints to Existing Functions
```python
# Before
def my_function(data, callback):
    # ... implementation

# After
from typing import Dict, Any, Callable, Optional

def my_function(
    data: Dict[str, Any], 
    callback: Optional[Callable[[str], None]] = None
) -> bool:
    # ... implementation
```

#### Step 3.2: Replace Wildcard Imports
```python
# Before
from data.constants import *

# After
from data.constants import (
    BLUE_ATTRS, RED_ATTRS, MOTION_TYPE, 
    START_LOC, END_LOC, PROP_ROT_DIR
)
```

#### Step 3.3: Use Typed Utilities
```python
# Before
def calc_font_size(parent_height, factor=0.03, min_size=10):
    return max(int(parent_height * factor), min_size)

# After
from utils.typed_utils import calc_font_size

# Function is now properly typed and validated
font_size = calc_font_size(widget.height(), factor=0.04, min_size=12)
```

## Testing the Migration

### Unit Tests for New Components
```python
# tests/unit/core/test_dependency_container.py
import pytest
from src.core.dependency_container import DependencyContainer
from src.interfaces.settings_manager_interface import ISettingsManager

class MockSettingsManager:
    def get_setting(self, section: str, key: str, default=None):
        return default

def test_dependency_container():
    container = DependencyContainer()
    container.register_singleton(ISettingsManager, MockSettingsManager)
    
    settings = container.resolve(ISettingsManager)
    assert isinstance(settings, MockSettingsManager)
    
    # Test singleton behavior
    settings2 = container.resolve(ISettingsManager)
    assert settings is settings2
```

### Integration Tests
```python
# tests/integration/test_main_widget_coordinator.py
def test_main_widget_coordinator_initialization():
    app_context = create_test_application_context()
    coordinator = MainWidgetCoordinator(None, None, app_context)
    
    # Test that essential components are created
    assert coordinator.tab_manager is not None
    assert coordinator.widget_manager is not None
    assert coordinator.state_manager is not None
```

## Rollback Plan

If issues arise during migration:

1. **Phase 1 Rollback**: Revert to original AppContext singleton
2. **Phase 2 Rollback**: Keep using original MainWidget class
3. **Phase 3 Rollback**: Remove type hints (though this shouldn't be necessary)

## Benefits After Migration

### 1. Improved Testability
- Components can be tested in isolation
- Easy to mock dependencies
- Clear interfaces for testing

### 2. Better Maintainability
- Single Responsibility Principle followed
- Clear separation of concerns
- Easier to understand and modify

### 3. Enhanced Type Safety
- Fewer runtime errors
- Better IDE support and autocomplete
- Clear contracts between components

### 4. Easier Extension
- New features can be added without modifying existing code
- Plugin architecture becomes possible
- Better support for different configurations

## Performance Considerations

The new architecture may have slight overhead due to:
- Dependency resolution (minimal impact)
- Additional abstraction layers (negligible)

However, benefits far outweigh costs:
- Better memory management
- Reduced coupling leads to better optimization opportunities
- Cleaner code is easier to profile and optimize

## Timeline

- **Week 1**: Dependency injection setup and basic container
- **Week 2**: MainWidget refactoring and component separation
- **Week 3**: Type safety improvements and testing
- **Week 4**: Integration testing and documentation

## Success Metrics

- [ ] All tests pass with new architecture
- [ ] No regression in functionality
- [ ] Improved code coverage (target: >80%)
- [ ] Reduced cyclomatic complexity
- [ ] Successful mypy --strict validation
- [ ] Performance maintained or improved
