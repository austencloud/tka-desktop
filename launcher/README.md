# TKA Launcher

A simple launcher application for the Kinetic Constructor project.

## Structure

```
launcher/
├── __init__.py                 # Package exports
├── accessibility.py           # Accessibility helper
├── apps.py                     # App definitions and data
└── launcher.py                 # Main launcher UI and application
```

## Usage

Run the launcher from the project root directory:

```bash
python main.py
```

The root `main.py` imports `LauncherApplication` from this launcher package.

## Features

- Simple, focused structure
- Accessibility support
- Keyboard shortcuts (Ctrl+Q to quit, F5 to refresh)
- Multi-screen positioning support
- Clean, minimal UI design
