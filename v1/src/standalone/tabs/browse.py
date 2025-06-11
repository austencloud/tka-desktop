#!/usr/bin/env python3
"""
Standalone runner for the Browse Tab.

Usage:
    python -m standalone.tabs.browse

Or directly:
    python src/standalone/tabs/browse.py
"""

import sys
import os

# Add src directory to path
src_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from standalone.core.base_runner import create_standalone_runner


def main():
    """Main entry point for standalone Browse Tab."""
    # Import here to avoid circular dependencies
    from browse_tab.integration.browse_tab_factory import BrowseTabFactory

    # Create and run the standalone runner
    runner = create_standalone_runner("browse", BrowseTabFactory)
    return runner.run()


if __name__ == "__main__":
    sys.exit(main())
