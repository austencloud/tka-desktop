#!/usr/bin/env python3
"""
Unified launcher for standalone tabs.

This provides a single entry point to launch any tab as a standalone application.

Usage:
    python src/standalone/core/launcher.py construct
    python src/standalone/core/launcher.py generate
    python src/standalone/core/launcher.py browse
    python src/standalone/core/launcher.py learn
    python src/standalone/core/launcher.py sequence_card

Or with module syntax:
    python -m standalone.core.launcher construct
"""

import sys
import os
import argparse

# Add src directory to path
src_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from standalone.core.base_runner import create_standalone_runner


# Tab factory mappings
TAB_FACTORIES = {
    "construct": (
        "main_window.main_widget.construct_tab.construct_tab_factory",
        "ConstructTabFactory",
    ),
    "generate": (
        "main_window.main_widget.generate_tab.generate_tab_factory",
        "GenerateTabFactory",
    ),
    "browse": ("browse_tab.integration.browse_tab_factory", "BrowseTabFactory"),
    "learn": ("main_window.main_widget.learn_tab.learn_tab_factory", "LearnTabFactory"),
    "sequence_card": (
        "main_window.main_widget.sequence_card_tab.utils.tab_factory",
        "SequenceCardTabFactory",
    ),
}


def get_factory_class(tab_name: str):
    """Dynamically import and return the factory class for a tab."""
    if tab_name not in TAB_FACTORIES:
        raise ValueError(
            f"Unknown tab: {tab_name}. Available tabs: {list(TAB_FACTORIES.keys())}"
        )

    module_path, class_name = TAB_FACTORIES[tab_name]

    # Dynamic import
    module = __import__(module_path, fromlist=[class_name])
    factory_class = getattr(module, class_name)

    return factory_class


def main():
    """Main entry point for the unified launcher."""
    parser = argparse.ArgumentParser(
        description="Launch individual tabs as standalone applications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Available tabs:
  {chr(10).join(f"  {name:<15} - {name.replace('_', ' ').title()} Tab" for name in TAB_FACTORIES.keys())}

Examples:
  python {sys.argv[0]} construct
  python {sys.argv[0]} browse
  python {sys.argv[0]} sequence_card
        """,
    )

    parser.add_argument(
        "tab", choices=list(TAB_FACTORIES.keys()), help="Name of the tab to launch"
    )

    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    try:
        # Get the factory class for the requested tab
        factory_class = get_factory_class(args.tab)

        # Create and run the standalone runner
        runner = create_standalone_runner(args.tab, factory_class)

        if args.debug:
            import logging

            logging.getLogger().setLevel(logging.DEBUG)
            print(f"Launching {args.tab} tab in standalone mode...")

        return runner.run()

    except Exception as e:
        print(f"Error launching {args.tab} tab: {e}")
        if args.debug:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
