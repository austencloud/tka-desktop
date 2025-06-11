#!/usr/bin/env python3
"""
Main entry point for The Kinetic Constructor Desktop application.
"""

import sys
import os


def main():
    """Launch the custom launcher."""
    launcher_path = os.path.join(os.path.dirname(__file__), "launcher")

    if launcher_path not in sys.path:
        sys.path.insert(0, launcher_path)

    try:
        from launcher.core.application import LauncherApplication

        app = LauncherApplication(sys.argv)
        return app.run()
    except ImportError as e:
        print(f"Error importing launcher: {e}")
        print("Falling back to V1 main application...")

        v1_src_path = os.path.join(os.path.dirname(__file__), "v1", "src")
        if v1_src_path not in sys.path:
            sys.path.insert(0, v1_src_path)

        try:
            from main import main as v1_main

            return v1_main()
        except ImportError as v1_error:
            print(f"Error importing V1 main: {v1_error}")
            print("Please ensure the application is properly set up.")
            return 1


if __name__ == "__main__":
    sys.exit(main())
