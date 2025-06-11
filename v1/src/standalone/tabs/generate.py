#!/usr/bin/env python3
"""
Standalone runner for the Generate Tab.

Usage:
    python -m standalone.tabs.generate

Or directly:
    python src/standalone/tabs/generate.py
"""

import sys
import os

# Add src directory to path
src_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from standalone.core.base_runner import create_standalone_runner


def main():
    """Main entry point for standalone Generate Tab."""
    # Import here to avoid circular dependencies
    from main_window.main_widget.generate_tab.generate_tab_factory import (
        GenerateTabFactory,
    )

    # Create and run the standalone runner
    runner = create_standalone_runner("generate", GenerateTabFactory)
    return runner.run()


if __name__ == "__main__":
    sys.exit(main())
