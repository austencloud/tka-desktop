#!/usr/bin/env python3
"""
Demo script to show the standalone construct tab for 10 seconds.
This demonstrates that the standalone construct tab is working correctly.
"""

import sys
import os

# Add src directory to path
src_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)


def demo_construct_tab():
    """Demo the standalone construct tab."""

    try:
        from standalone.core.base_runner import create_standalone_runner
        from main_window.main_widget.construct_tab.construct_tab_factory import (
            ConstructTabFactory,
        )

        print("🚀 Starting Standalone Construct Tab Demo")
        print("=" * 50)

        print("1. Creating construct tab runner...")
        runner = create_standalone_runner("construct", ConstructTabFactory)

        print("2. Setting up runner...")
        runner.configure_import_paths()
        runner.initialize_logging()

        # Initialize Qt application
        from PyQt6.QtWidgets import QApplication

        app = QApplication(sys.argv)
        runner.app = app
        print("3. Qt application created")

        # Initialize dependency injection
        print("4. Initializing dependencies...")
        runner.app_context = runner.initialize_dependency_injection()
        print("5. Dependencies initialized ✅")

        # Create coordinator and tab
        print("6. Creating coordinator...")
        coordinator = runner.create_minimal_coordinator()
        print("7. Creating construct tab...")
        tab_widget = runner.create_tab_with_coordinator(coordinator)
        print("8. Construct tab created successfully! ✅")

        # Create window
        print("9. Creating window...")
        from standalone.core.base_runner import StandaloneTabWindow

        window = StandaloneTabWindow(tab_widget, "construct", coordinator)
        print("10. Window created! ✅")

        # Show window
        print("11. Showing window...")
        window.show()
        print("12. Window shown! ✅")

        print("\n🎉 SUCCESS! The standalone construct tab is now running!")
        print("\nThe window contains:")
        print("  - Sequence Workbench (left side)")
        print("  - Start Position Picker (right side)")
        print("  - Advanced Start Position Picker")
        print("  - Option Picker")
        print("  - Stack switching functionality")

        print(f"\n🎉 Demo is now running indefinitely!")
        print("You should see the construct tab window with all its components!")
        print("Close the window manually when you're done testing.")

        return app.exec()

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    result = demo_construct_tab()
    print(f"\nDemo completed with exit code: {result}")
    if result == 0:
        print("✅ Standalone construct tab is working perfectly!")
    else:
        print("❌ Demo failed")
    sys.exit(result)
