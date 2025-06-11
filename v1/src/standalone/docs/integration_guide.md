# Standalone Integration Guide

This guide explains how to integrate the standalone tab system with the main application and how to extend it with new functionality.

## 🔗 Main Application Integration

### Enhanced Tab Switcher

The main application can integrate with standalone tabs through an enhanced tab switcher:

```python
from main_window.main_widget.enhanced_tab_switcher import EnhancedTabSwitcher

class MainWidget(QWidget):
    def __init__(self, app_context):
        super().__init__()
        self.app_context = app_context
        
        # Create enhanced tab switcher
        self.tab_switcher = EnhancedTabSwitcher(self, app_context)
        
        # Connect signals
        self.tab_switcher.external_tab_launched.connect(self.on_external_tab_launched)
        self.tab_switcher.external_tab_closed.connect(self.on_external_tab_closed)
        
    def setup_tab_context_menus(self):
        """Set up context menus for tab buttons."""
        for tab_name, button in self.tab_buttons.items():
            button.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            button.customContextMenuRequested.connect(
                lambda pos, name=tab_name: self.show_tab_context_menu(name, pos)
            )
    
    def show_tab_context_menu(self, tab_name: str, position):
        """Show context menu for tab button."""
        menu = QMenu(self)
        
        # Switch to tab (internal)
        switch_action = menu.addAction("Switch to Tab")
        switch_action.triggered.connect(lambda: self.switch_to_tab(tab_name))
        
        # Open in new window (external)
        external_action = menu.addAction("Open in New Window")
        external_action.triggered.connect(lambda: self.launch_external_tab(tab_name))
        
        # Close external tab (if running)
        if self.tab_switcher.is_external_tab_running(tab_name):
            close_action = menu.addAction("Close External Tab")
            close_action.triggered.connect(lambda: self.close_external_tab(tab_name))
        
        menu.exec(self.mapToGlobal(position))
    
    def launch_external_tab(self, tab_name: str):
        """Launch a tab as external standalone application."""
        self.tab_switcher.launch_external_tab(tab_name)
    
    def on_external_tab_launched(self, tab_name: str, process_id: int):
        """Handle external tab launch."""
        print(f"External {tab_name} tab launched with PID {process_id}")
        
    def on_external_tab_closed(self, tab_name: str):
        """Handle external tab closure."""
        print(f"External {tab_name} tab closed")
```

### Process Management

Track and manage external tab processes:

```python
class ExternalTabManager:
    def __init__(self):
        self.running_tabs = {}  # tab_name -> process
        
    def launch_tab(self, tab_name: str) -> int:
        """Launch external tab and return process ID."""
        import subprocess
        import sys
        
        launcher_path = "src/standalone/core/launcher.py"
        process = subprocess.Popen([
            sys.executable, launcher_path, tab_name
        ])
        
        self.running_tabs[tab_name] = process
        return process.pid
        
    def close_tab(self, tab_name: str) -> bool:
        """Close external tab."""
        if tab_name in self.running_tabs:
            process = self.running_tabs[tab_name]
            process.terminate()
            del self.running_tabs[tab_name]
            return True
        return False
        
    def is_running(self, tab_name: str) -> bool:
        """Check if external tab is running."""
        if tab_name not in self.running_tabs:
            return False
        
        process = self.running_tabs[tab_name]
        return process.poll() is None
```

## 🔧 Adding New Standalone Tabs

### Step 1: Create Tab Factory

Ensure your tab has a proper factory class:

```python
# my_tab/my_tab_factory.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

if TYPE_CHECKING:
    from core.application_context import ApplicationContext

class MyTabFactory:
    @staticmethod
    def create(parent: QWidget, app_context: "ApplicationContext") -> QWidget:
        """Create the tab widget."""
        from my_tab.my_tab import MyTab
        return MyTab(parent, app_context)
```

### Step 2: Add to Launcher Configuration

Update the launcher configuration:

```python
# standalone/core/launcher.py
TAB_FACTORIES = {
    # ... existing tabs ...
    "my_tab": ("my_tab.my_tab_factory", "MyTabFactory"),
}
```

### Step 3: Create Standalone Script

Create a standalone script for your tab:

```python
# standalone/tabs/my_tab.py
#!/usr/bin/env python3
"""
Standalone runner for My Tab.
"""

import sys
import os

# Add src directory to path
src_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from standalone.core.base_runner import create_standalone_runner

def main():
    """Main entry point for standalone My Tab."""
    from my_tab.my_tab_factory import MyTabFactory
    
    runner = create_standalone_runner("my_tab", MyTabFactory)
    return runner.run()

if __name__ == "__main__":
    sys.exit(main())
```

### Step 4: Add Tests

Create tests for your standalone tab:

```python
# standalone/tests/unit/test_my_tab.py
import unittest
from standalone.core.base_runner import create_standalone_runner
from my_tab.my_tab_factory import MyTabFactory

class TestMyTabStandalone(unittest.TestCase):
    def test_tab_creation(self):
        """Test that the tab can be created standalone."""
        runner = create_standalone_runner("my_tab", MyTabFactory)
        
        # Test setup
        runner.configure_import_paths()
        runner.initialize_logging()
        
        # Test dependency injection
        app_context = runner.initialize_dependency_injection()
        self.assertIsNotNone(app_context)
        
        # Test coordinator creation
        coordinator = runner.create_minimal_coordinator()
        self.assertIsNotNone(coordinator)
        
        # Test tab creation
        tab_widget = runner.create_tab_with_coordinator(coordinator)
        self.assertIsNotNone(tab_widget)

if __name__ == "__main__":
    unittest.main()
```

## 🎨 Custom Services

### Creating Custom Services

Add custom services to the standalone environment:

```python
# standalone/services/my_service/my_service.py
class MyStandaloneService:
    """Custom service for standalone environment."""
    
    def __init__(self):
        self.initialized = False
        
    def initialize(self):
        """Initialize the service."""
        # Custom initialization logic
        self.initialized = True
        
    def process_data(self, data):
        """Process data in standalone context."""
        if not self.initialized:
            self.initialize()
        
        # Custom processing logic
        return processed_data
```

### Integrating Services

Integrate custom services with the base runner:

```python
# Extend BaseStandaloneRunner
class CustomStandaloneRunner(BaseStandaloneRunner):
    def create_minimal_coordinator(self):
        """Create coordinator with custom services."""
        coordinator = super().create_minimal_coordinator()
        
        # Add custom service
        from standalone.services.my_service.my_service import MyStandaloneService
        coordinator.my_service = MyStandaloneService()
        
        return coordinator
```

## 🧪 Testing Framework

### Integration Testing

Create comprehensive integration tests:

```python
# standalone/tests/integration/test_my_integration.py
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

def test_my_integration():
    """Test complete integration of my functionality."""
    
    app = QApplication(sys.argv)
    
    try:
        # Create runner
        from standalone.core.base_runner import create_standalone_runner
        from my_tab.my_tab_factory import MyTabFactory
        
        runner = create_standalone_runner("my_tab", MyTabFactory)
        
        # Initialize
        runner.configure_import_paths()
        runner.initialize_logging()
        runner.app_context = runner.initialize_dependency_injection()
        
        # Create tab
        coordinator = runner.create_minimal_coordinator()
        tab_widget = runner.create_tab_with_coordinator(coordinator)
        
        # Test specific functionality
        assert hasattr(tab_widget, 'expected_method')
        result = tab_widget.expected_method()
        assert result is not None
        
        print("✅ Integration test passed")
        return 0
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return 1
    finally:
        app.quit()

if __name__ == "__main__":
    sys.exit(test_my_integration())
```

### Performance Testing

Monitor performance of standalone tabs:

```python
# standalone/tests/performance/test_performance.py
import time
import psutil
import os

def test_tab_performance():
    """Test performance metrics of standalone tab."""
    
    # Measure startup time
    start_time = time.time()
    
    # Launch tab
    process = subprocess.Popen([
        sys.executable, "src/standalone/core/launcher.py", "construct"
    ])
    
    # Wait for window to appear (implementation specific)
    time.sleep(2)
    
    startup_time = time.time() - start_time
    
    # Measure memory usage
    process_info = psutil.Process(process.pid)
    memory_mb = process_info.memory_info().rss / 1024 / 1024
    
    # Cleanup
    process.terminate()
    
    print(f"Startup time: {startup_time:.2f}s")
    print(f"Memory usage: {memory_mb:.1f}MB")
    
    # Assert performance requirements
    assert startup_time < 5.0, "Startup too slow"
    assert memory_mb < 500, "Memory usage too high"
```

## 📊 Configuration System

### Tab Configuration

Configure tab-specific settings:

```python
# standalone/core/config.py
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

class LaunchMode(Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"
    BOTH = "both"

@dataclass
class TabConfig:
    display_name: str
    description: str
    can_run_standalone: bool = True
    launch_mode: LaunchMode = LaunchMode.BOTH
    icon_path: Optional[str] = None
    keyboard_shortcut: Optional[str] = None

@dataclass
class StandaloneConfig:
    tabs: Dict[str, TabConfig]
    default_launch_mode: LaunchMode = LaunchMode.INTERNAL
    enable_context_menus: bool = True
    auto_close_timeout: int = 0  # 0 = no timeout

def get_standalone_config() -> StandaloneConfig:
    """Get the standalone configuration."""
    return StandaloneConfig(
        tabs={
            "construct": TabConfig(
                display_name="Construct",
                description="Build sequences with start positions and options",
                keyboard_shortcut="Ctrl+1"
            ),
            "generate": TabConfig(
                display_name="Generate", 
                description="Generate new sequences automatically",
                keyboard_shortcut="Ctrl+2"
            ),
            # ... other tabs
        }
    )
```

## 🔄 State Synchronization

### Data Sharing

Share data between main app and standalone tabs:

```python
# standalone/core/state_manager.py
import json
import os
from typing import Any, Dict

class StateManager:
    """Manage shared state between main app and standalone tabs."""
    
    def __init__(self, state_file: str = "shared_state.json"):
        self.state_file = state_file
        self.state = self.load_state()
        
    def load_state(self) -> Dict[str, Any]:
        """Load state from file."""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {}
        
    def save_state(self):
        """Save state to file."""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
            
    def get(self, key: str, default: Any = None) -> Any:
        """Get state value."""
        return self.state.get(key, default)
        
    def set(self, key: str, value: Any):
        """Set state value."""
        self.state[key] = value
        self.save_state()
        
    def update(self, updates: Dict[str, Any]):
        """Update multiple state values."""
        self.state.update(updates)
        self.save_state()
```

## 🚀 Advanced Features

### Plugin System

Support for custom plugins:

```python
# standalone/core/plugin_manager.py
import importlib
from typing import List, Type

class PluginManager:
    """Manage standalone tab plugins."""
    
    def __init__(self):
        self.plugins = []
        
    def load_plugin(self, plugin_module: str):
        """Load a plugin module."""
        try:
            module = importlib.import_module(plugin_module)
            if hasattr(module, 'StandalonePlugin'):
                plugin = module.StandalonePlugin()
                self.plugins.append(plugin)
                return plugin
        except ImportError as e:
            print(f"Failed to load plugin {plugin_module}: {e}")
            
    def apply_plugins(self, runner):
        """Apply all loaded plugins to a runner."""
        for plugin in self.plugins:
            plugin.configure_runner(runner)
```

This integration guide provides the foundation for extending and integrating the standalone tab system with your application's specific needs.
