# Component Migration Examples

This document provides concrete examples of how to migrate existing components from the old AppContext singleton pattern to the new dependency injection system.

## Example 1: Migrating a Settings-Dependent Component

### Before (Old AppContext Pattern)
```python
# src/some_component/old_component.py
from settings_manager.global_settings.app_context import AppContext

class OldComponent:
    def __init__(self):
        # Component directly accesses global singleton
        self.settings = AppContext.settings_manager()
    
    def do_something(self):
        current_tab = self.settings.global_settings.current_tab
        # ... rest of the logic
```

### After (Dependency Injection Pattern)
```python
# src/some_component/new_component.py
from typing import TYPE_CHECKING
from core.application_context import ApplicationContext

if TYPE_CHECKING:
    from interfaces.settings_manager_interface import ISettingsManager

class NewComponent:
    def __init__(self, app_context: ApplicationContext):
        # Dependencies injected through constructor
        self.app_context = app_context
        self.settings = app_context.settings_manager
    
    def do_something(self):
        current_tab = self.settings.global_settings.current_tab
        # ... rest of the logic (unchanged)

# Factory for creating the component
class NewComponentFactory:
    @staticmethod
    def create(parent, app_context: ApplicationContext) -> NewComponent:
        return NewComponent(app_context)
```

### Migration Steps
1. Add `app_context` parameter to constructor
2. Get dependencies from `app_context` instead of global singleton
3. Create a factory class for consistent creation
4. Update all places that create this component to use the factory

## Example 2: Migrating a Complex Component with Multiple Dependencies

### Before
```python
# src/complex_component/old_complex_component.py
from settings_manager.global_settings.app_context import AppContext

class OldComplexComponent:
    def __init__(self, parent):
        self.parent = parent
        # Multiple global dependencies
        self.settings = AppContext.settings_manager()
        self.json_manager = AppContext.json_manager()
        self.selected_arrow = AppContext.selected_arrow()
    
    def save_data(self, data):
        # Uses multiple dependencies
        if self.settings.global_settings.auto_save:
            self.json_manager.save_sequence(data)
        
        if self.selected_arrow:
            # Do something with selected arrow
            pass
```

### After
```python
# src/complex_component/new_complex_component.py
from typing import TYPE_CHECKING, Optional
from core.application_context import ApplicationContext

if TYPE_CHECKING:
    from interfaces.settings_manager_interface import ISettingsManager
    from interfaces.json_manager_interface import IJsonManager
    from objects.arrow.arrow import Arrow

class NewComplexComponent:
    def __init__(self, parent, app_context: ApplicationContext):
        self.parent = parent
        self.app_context = app_context
        
        # Get dependencies from app context
        self.settings = app_context.settings_manager
        self.json_manager = app_context.json_manager
    
    @property
    def selected_arrow(self) -> Optional["Arrow"]:
        """Get selected arrow from app context."""
        return self.app_context.selected_arrow
    
    def save_data(self, data):
        # Logic unchanged, but dependencies come from DI
        if self.settings.global_settings.auto_save:
            self.json_manager.save_sequence(data)
        
        if self.selected_arrow:
            # Do something with selected arrow
            pass

# Factory with proper dependency injection
class NewComplexComponentFactory:
    @staticmethod
    def create(parent, app_context: ApplicationContext) -> NewComplexComponent:
        return NewComplexComponent(parent, app_context)
```

## Example 3: Gradual Migration Using Adapters

For components that are difficult to migrate immediately, use the adapter pattern:

### Gradual Migration Approach
```python
# src/legacy_component/partially_migrated_component.py
from core.migration_adapters import AppContextAdapter, ComponentMigrationHelper
from core.application_context import ApplicationContext

class PartiallyMigratedComponent:
    def __init__(self, parent, app_context: ApplicationContext = None):
        self.parent = parent
        
        if app_context:
            # New dependency injection path
            self.app_context = app_context
            self.settings = app_context.settings_manager
            self.json_manager = app_context.json_manager
        else:
            # Legacy path using adapter
            adapter = AppContextAdapter.settings_manager()
            self.settings = adapter
            self.json_manager = AppContextAdapter.json_manager()
    
    def migrate_to_di(self, app_context: ApplicationContext):
        """Method to migrate this component to dependency injection."""
        helper = ComponentMigrationHelper(app_context)
        helper.migrate_component(self, "PartiallyMigratedComponent")
```

## Example 4: Updating Factory Classes

### Before
```python
# src/some_tab/old_tab_factory.py
from .some_tab import SomeTab
from settings_manager.global_settings.app_context import AppContext

class OldTabFactory:
    @staticmethod
    def create(main_widget):
        # Dependencies accessed globally
        settings = AppContext.settings_manager()
        json_manager = AppContext.json_manager()
        
        return SomeTab(
            main_widget=main_widget,
            settings_manager=settings,
            json_manager=json_manager
        )
```

### After
```python
# src/some_tab/new_tab_factory.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
import logging

from core.application_context import ApplicationContext
from main_window.main_widget.core.widget_manager import WidgetFactory
from .some_tab import SomeTab

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

class NewTabFactory(WidgetFactory):
    @staticmethod
    def create(parent: QWidget, app_context: ApplicationContext) -> SomeTab:
        """Create SomeTab with proper dependency injection."""
        try:
            # Get dependencies from app context
            settings_manager = app_context.settings_manager
            json_manager = app_context.json_manager
            
            # Create tab with dependencies
            tab = SomeTab(
                main_widget=parent,  # parent is MainWidgetCoordinator
                settings_manager=settings_manager,
                json_manager=json_manager
            )
            
            # Store app context for future use
            tab.app_context = app_context
            
            logger.info("Created SomeTab with dependency injection")
            return tab
            
        except Exception as e:
            logger.error(f"Failed to create SomeTab: {e}")
            raise
```

## Example 5: Testing with Dependency Injection

### Before (Hard to Test)
```python
# tests/test_old_component.py
import unittest
from unittest.mock import patch
from src.some_component.old_component import OldComponent

class TestOldComponent(unittest.TestCase):
    @patch('settings_manager.global_settings.app_context.AppContext.settings_manager')
    def test_do_something(self, mock_settings):
        # Complex mocking required
        mock_settings.return_value.global_settings.current_tab = "test_tab"
        
        component = OldComponent()
        component.do_something()
        # ... assertions
```

### After (Easy to Test)
```python
# tests/test_new_component.py
import unittest
from unittest.mock import Mock
from src.some_component.new_component import NewComponent
from core.application_context import ApplicationContext

class TestNewComponent(unittest.TestCase):
    def setUp(self):
        # Create mock dependencies
        self.mock_settings = Mock()
        self.mock_settings.global_settings.current_tab = "test_tab"
        
        # Create mock app context
        self.mock_app_context = Mock(spec=ApplicationContext)
        self.mock_app_context.settings_manager = self.mock_settings
    
    def test_do_something(self):
        # Easy dependency injection for testing
        component = NewComponent(self.mock_app_context)
        component.do_something()
        # ... assertions
```

## Migration Checklist

For each component you migrate:

- [ ] Add `app_context: ApplicationContext` parameter to constructor
- [ ] Replace `AppContext.service_name()` calls with `app_context.service_name`
- [ ] Create a factory class that follows the `WidgetFactory` pattern
- [ ] Update all creation sites to use the factory
- [ ] Add proper type hints using `TYPE_CHECKING`
- [ ] Add error handling in the factory
- [ ] Write unit tests using dependency injection
- [ ] Update documentation

## Benefits After Migration

1. **Testability**: Easy to mock dependencies in unit tests
2. **Flexibility**: Can swap implementations for different environments
3. **Clarity**: Dependencies are explicit in constructor
4. **SOLID Principles**: Follows Dependency Inversion Principle
5. **Maintainability**: Easier to understand and modify code
6. **Performance**: No global state access overhead

## Common Pitfalls to Avoid

1. **Don't** create the app_context inside components - always inject it
2. **Don't** store global references to services - use the app_context
3. **Don't** forget to update factory classes when migrating components
4. **Don't** mix old and new patterns in the same component
5. **Do** use the migration adapters for gradual migration
6. **Do** add proper error handling in factories
7. **Do** write tests for migrated components
