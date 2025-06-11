# Standalone Tab Usage Guide

Complete guide for using the standalone tab system effectively.

## 🚀 Getting Started

### Quick Launch

The fastest way to launch any tab:

```bash
# Launch construct tab
python src/standalone/core/launcher.py construct

# Launch with debug output
python src/standalone/core/launcher.py --debug construct
```

### Available Commands

```bash
# Show help and available tabs
python src/standalone/core/launcher.py --help

# Launch specific tabs
python src/standalone/core/launcher.py construct    # Build sequences
python src/standalone/core/launcher.py generate    # Generate sequences  
python src/standalone/core/launcher.py browse      # Browse sequences
python src/standalone/core/launcher.py learn       # Learn mode
python src/standalone/core/launcher.py sequence_card  # Sequence cards
```

## 🎯 Tab-Specific Usage

### Construct Tab

The construct tab allows you to build sequences step by step:

**Features:**
- Start position picker (right panel)
- Advanced start position picker
- Option picker for next moves
- Sequence workbench (left panel)
- Full screen preview button (👁️)

**Workflow:**
1. Select a start position from the right panel
2. Choose options to build your sequence
3. Use the full screen button to preview your sequence
4. Continue adding beats to complete your sequence

**Full Screen Functionality:**
- Click the eye icon (👁️) in the sequence workbench
- Full screen overlay appears with your sequence image
- Click anywhere on the overlay to close it
- Works correctly on dual screen setups

### Generate Tab

Generate sequences automatically based on parameters:

**Features:**
- Sequence generation parameters
- Batch generation capabilities
- Preview generated sequences
- Export generated sequences

### Browse Tab

Browse and manage existing sequences:

**Features:**
- Sequence library browser
- Search and filter functionality
- Sequence preview
- Metadata editing

### Learn Tab

Educational content and tutorials:

**Features:**
- Interactive lessons
- Progress tracking
- Practice exercises
- Reference materials

### Sequence Card Tab

View and edit individual sequence cards:

**Features:**
- Card editing interface
- Metadata management
- Visual preview
- Export options

## 🔧 Advanced Usage

### Module Syntax

Use Python module syntax for cleaner imports:

```bash
# Launch via module
python -m standalone.core.launcher construct
python -m standalone.tabs.construct

# From project root
cd /path/to/kinetic-constructor
python -m src.standalone.core.launcher construct
```

### Individual Scripts

Each tab has its own standalone script:

```bash
# Direct script execution
python src/standalone/tabs/construct.py
python src/standalone/tabs/generate.py
python src/standalone/tabs/browse.py
python src/standalone/tabs/learn.py
python src/standalone/tabs/sequence_card.py
```

### Debug Mode

Enable detailed logging and debugging:

```bash
# Debug mode shows:
# - Dependency injection details
# - Widget creation progress  
# - Error handling information
# - Performance metrics
python src/standalone/core/launcher.py --debug construct
```

## 🖥️ Window Management

### Window Layout

Each standalone tab creates a properly sized window:

- **Default size**: 1400x900 pixels
- **Construct tab**: Special left/right layout
  - Left: Sequence workbench (2/3 width)
  - Right: Stacked widget with pickers (1/3 width)
- **Other tabs**: Standard central widget layout

### Multi-Screen Support

The standalone system works correctly with multiple monitors:

- Windows appear on the primary screen by default
- Full screen overlays respect the current window's screen
- Proper geometry handling for dual screen setups
- Z-index management ensures overlays appear on top

### Window Controls

Standard window controls are available:

- Minimize, maximize, close buttons
- Resizable windows (where appropriate)
- Proper window titles indicating the tab name
- System tray integration (if enabled)

## 🎨 Customization

### Command Line Options

```bash
# Available options
python src/standalone/core/launcher.py --help

# Debug mode
python src/standalone/core/launcher.py --debug construct

# Future options (planned)
python src/standalone/core/launcher.py --config myconfig.json construct
python src/standalone/core/launcher.py --theme dark construct
python src/standalone/core/launcher.py --size 1600x1000 construct
```

### Environment Variables

Control behavior via environment variables:

```bash
# Enable debug logging
export STANDALONE_DEBUG=1
python src/standalone/core/launcher.py construct

# Set custom config path
export STANDALONE_CONFIG=/path/to/config.json
python src/standalone/core/launcher.py construct

# Disable auto-close timer
export STANDALONE_NO_TIMEOUT=1
python src/standalone/core/launcher.py construct
```

## 🧪 Testing and Validation

### Run Demos

Test functionality with demo scripts:

```bash
# Basic functionality demo
python src/standalone/demos/demo.py

# Construct tab specific demo
python src/standalone/demos/demo_construct.py

# Comprehensive final demo
python src/standalone/demos/final_demo.py
```

### Integration Tests

Validate complete functionality:

```bash
# Full screen integration test
python src/standalone/tests/integration/test_fullscreen_integration.py

# Manual verification test
python src/standalone/tests/manual/test_final.py
```

### Unit Tests

Test individual components:

```bash
# Image creator tests
python src/standalone/tests/unit/test_image_creator.py

# Tab creation tests
python src/standalone/tests/unit/test_tabs.py
```

## 🔍 Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Ensure you're in the project root
cd /path/to/kinetic-constructor

# Or use absolute paths
python /full/path/to/src/standalone/core/launcher.py construct
```

**Qt Application Errors:**
```bash
# Only one QApplication per process
# If you get Qt errors, restart your terminal/IDE

# Check display settings
export DISPLAY=:0  # Linux
# Or check Windows display scaling
```

**Missing Dependencies:**
```bash
# Install required packages
pip install PyQt6
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

**Window Display Issues:**
```bash
# Debug window creation
python src/standalone/core/launcher.py --debug construct

# Check screen configuration
python -c "from PyQt6.QtWidgets import QApplication; app = QApplication([]); print([s.geometry() for s in app.screens()])"
```

### Debug Information

Enable comprehensive debugging:

```bash
# Full debug output
export STANDALONE_DEBUG=1
export STANDALONE_VERBOSE=1
python src/standalone/core/launcher.py construct
```

### Log Files

Check log files for detailed information:

```bash
# Default log location (if file logging enabled)
tail -f logs/standalone.log

# Or check console output with timestamps
python src/standalone/core/launcher.py --debug construct 2>&1 | ts
```

## 📊 Performance

### Startup Performance

Typical startup times:

- **Construct tab**: 2-3 seconds
- **Generate tab**: 1-2 seconds  
- **Browse tab**: 3-4 seconds (loads sequence data)
- **Learn tab**: 1-2 seconds
- **Sequence card tab**: 2-3 seconds

### Memory Usage

Typical memory usage:

- **Base overhead**: ~100-150 MB
- **Construct tab**: ~200-300 MB
- **Browse tab**: ~300-500 MB (with sequence cache)
- **Generate tab**: ~150-250 MB

### Optimization Tips

1. **Close unused tabs**: Each standalone tab uses memory
2. **Use debug mode sparingly**: Debug output impacts performance
3. **Monitor system resources**: Check Task Manager/Activity Monitor
4. **Restart periodically**: Long-running tabs may accumulate memory

## 🔄 Integration with Main App

### Context Menus

When integrated with the main application:

1. Right-click any tab button
2. Choose "Open in New Window"
3. Standalone tab launches automatically
4. Choose "Close External Tab" to close it

### Process Management

The main application can track standalone tabs:

- View running external tabs
- Close external tabs remotely
- Monitor resource usage
- Sync data between instances

### Data Synchronization

Standalone tabs can share data with the main application:

- Sequence data synchronization
- Settings synchronization
- User preferences
- Recent files and history

## 🚀 Best Practices

### Development

1. **Test standalone mode early**: Don't wait until the end
2. **Use the debug mode**: Helps identify issues quickly
3. **Check all tabs**: Ensure each tab works standalone
4. **Monitor performance**: Watch startup time and memory usage

### Deployment

1. **Include all dependencies**: Ensure standalone tabs work in production
2. **Test on target systems**: Verify compatibility
3. **Document usage**: Provide clear instructions for users
4. **Monitor usage**: Track which tabs are used standalone

### User Experience

1. **Consistent interface**: Maintain UI consistency across tabs
2. **Clear documentation**: Provide usage instructions
3. **Error handling**: Graceful error messages and recovery
4. **Performance**: Keep startup times reasonable

This usage guide covers all aspects of using the standalone tab system effectively. For technical implementation details, see the [Integration Guide](integration_guide.md).
