# Standalone Tab System

A comprehensive system for running individual tabs as standalone applications, providing modular access to specific functionality without launching the full application.

## 🏗️ Architecture

The standalone system is organized into logical, forward-thinking directories:

```
src/standalone/
├── core/                           # Core infrastructure
│   ├── base_runner.py             # Base standalone runner
│   ├── launcher.py                # Main launcher entry point
│   └── patches/                   # System patches
│       └── full_screen_patch.py   # Full screen functionality patch
│
├── tabs/                          # Individual tab implementations
│   ├── browse.py                  # Browse tab standalone
│   ├── construct.py               # Construct tab standalone
│   ├── generate.py                # Generate tab standalone
│   ├── learn.py                   # Learn tab standalone
│   └── sequence_card.py           # Sequence card tab standalone
│
├── services/                      # Standalone services and utilities
│   └── image_creator/             # Image creation service
│       ├── image_creator.py       # Main image creator
│       ├── beat_factory.py        # Beat data processing
│       ├── beat_renderer.py       # Beat rendering
│       └── layout_calculator.py   # Layout calculations
│
├── tests/                         # All test files
│   ├── integration/               # Integration tests
│   ├── unit/                      # Unit tests
│   └── manual/                    # Manual testing utilities
│
├── demos/                         # Demo and example files
└── docs/                          # Documentation
```

## 🚀 Quick Start

### Launch Any Tab

```bash
# Using the unified launcher
python src/standalone/core/launcher.py construct
python src/standalone/core/launcher.py generate
python src/standalone/core/launcher.py browse
python src/standalone/core/launcher.py learn
python src/standalone/core/launcher.py sequence_card

# Using individual scripts
python src/standalone/tabs/construct.py
python src/standalone/tabs/generate.py

# Using module syntax
python -m standalone.core.launcher construct
python -m standalone.tabs.construct

# Debug mode
python src/standalone/core/launcher.py --debug construct
```

### Available Tabs

- **construct** - Build sequences with start positions and options
- **generate** - Generate new sequences automatically
- **browse** - Browse and manage existing sequences
- **learn** - Learn mode for educational content
- **sequence_card** - View and edit sequence cards

## 🎯 Key Features

### 1. **Self-Contained Architecture**

- Each tab runs independently with its own dependency injection
- No interference with the main application
- Complete isolation of resources and state

### 2. **Pixel-Perfect Image Creation**

- Standalone image creator produces identical output to main application
- Uses real BeatView components and rendering pipeline
- Supports full screen overlays with proper dual-screen positioning

### 3. **Full Screen Functionality**

- Working full screen button in standalone construct tab
- Proper z-index handling for dual screen setups
- Click-to-close overlay functionality
- Seamless integration with sequence building

### 4. **Perfect Layout Parity**

- Standalone construct tab maintains 1:1 ratio of workbench to picker
- Matches main application layout proportions exactly
- Equal width allocation (50% each) for optimal usability
- Verified pixel-perfect layout consistency

### 5. **Robust Error Handling**

- Graceful fallbacks when components aren't available
- Comprehensive logging and debugging support
- Automatic recovery from common issues

### 6. **Universal Compatibility**

- Works in both standalone and main application contexts
- Maintains complete visual and functional parity
- Supports all existing tab functionality

## 🔧 Technical Implementation

### Base Runner System

The `BaseStandaloneRunner` provides common infrastructure:

```python
from standalone.core.base_runner import create_standalone_runner
from main_window.main_widget.construct_tab.construct_tab_factory import ConstructTabFactory

# Create and run standalone tab
runner = create_standalone_runner("construct", ConstructTabFactory)
exit_code = runner.run()
```

### Dependency Injection

Each standalone tab gets its own dependency injection container:

- Settings Manager
- JSON Manager
- Dictionary Data Manager
- Motion and Arrow objects
- Pictograph Data Loader
- Letter Determiner
- Sequence Validator

### Widget Management

Minimal widget manager provides essential widgets on demand:

- Sequence Workbench
- Fade Manager
- Pictograph Collector
- Full Screen Overlay

## 🧪 Testing

### Run Tests

```bash
# Integration tests
python src/standalone/tests/integration/test_fullscreen_integration.py

# Manual tests
python src/standalone/tests/manual/test_final.py

# Unit tests
python src/standalone/tests/unit/test_image_creator.py
```

### Demo Scripts

```bash
# Basic demo
python src/standalone/demos/demo.py

# Construct tab demo
python src/standalone/demos/demo_construct.py

# Final comprehensive demo
python src/standalone/demos/final_demo.py
```

## 📋 Usage Examples

### Basic Usage

```python
# Simple standalone tab launch
from standalone.core.launcher import main
import sys

sys.argv = ['launcher.py', 'construct']
exit_code = main()
```

### Advanced Usage

```python
# Custom runner with specific configuration
from standalone.core.base_runner import BaseStandaloneRunner
from main_window.main_widget.construct_tab.construct_tab_factory import ConstructTabFactory

runner = BaseStandaloneRunner("construct", ConstructTabFactory)
runner.configure_import_paths()
runner.initialize_logging()

# Custom setup here...

exit_code = runner.run()
```

### Image Creation

```python
# Standalone image creation
from standalone.services.image_creator.image_creator import StandaloneImageCreator

creator = StandaloneImageCreator()
image = creator.create_sequence_image(
    sequence_data=sequence_dict,
    options={"include_start_position": True},
    user_name="User",
    export_date="12-25-2024"
)
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure src directory is in Python path
2. **Qt Application Conflicts**: Only one QApplication per process
3. **Missing Dependencies**: Check that all required modules are available
4. **Window Display Issues**: Verify Qt display settings and screen configuration

### Debug Mode

Enable debug logging for detailed information:

```bash
python src/standalone/core/launcher.py --debug construct
```

### Log Output

The system provides comprehensive logging:

- Dependency injection status
- Widget creation progress
- Error handling and fallbacks
- Performance metrics

## 🚀 Future Enhancements

### Planned Features

1. **Configuration System**: Customizable tab settings and preferences
2. **Plugin Architecture**: Support for custom tab extensions
3. **Inter-Tab Communication**: Message passing between standalone tabs
4. **Resource Sharing**: Shared caches and data between instances
5. **Performance Monitoring**: Built-in performance metrics and optimization

### Integration Opportunities

1. **Main Application Integration**: Enhanced tab switcher with context menus
2. **Process Management**: Track and manage external tab processes
3. **State Synchronization**: Sync data between main app and standalone tabs
4. **Workspace Management**: Save and restore tab layouts and configurations

## 📚 API Reference

See individual module documentation:

- [Base Runner API](integration_guide.md#base-runner)
- [Image Creator API](integration_guide.md#image-creator)
- [Tab Factory API](integration_guide.md#tab-factories)
- [Testing API](integration_guide.md#testing)

## 🤝 Contributing

When adding new standalone functionality:

1. Follow the established directory structure
2. Maintain compatibility with existing interfaces
3. Add comprehensive tests for new features
4. Update documentation and examples
5. Ensure proper error handling and logging

## 📄 License

This standalone system is part of the Kinetic Constructor project and follows the same licensing terms.
