#!/usr/bin/env python3
"""
Main entry point for The Kinetic Constructor Desktop application.
"""

import os
import sys


def main():
    try:
        from launcher import LauncherApplication

        app = LauncherApplication(sys.argv)
        return app.run()
    except ImportError as e:
        print(f"Error importing launcher: {e}")
        print("Falling back to Legacy main application...")

        legacy_src_path = os.path.join(os.path.dirname(__file__), "legacy", "src")
        if legacy_src_path not in sys.path:
            sys.path.insert(0, legacy_src_path)

        try:
            from main import main as legacy_main

            return legacy_main()
        except ImportError as legacy_error:
            print(f"Error importing Legacy main: {legacy_error}")
            print("Please ensure the application is properly set up.")
            return 1


if __name__ == "__main__":
    sys.exit(main())
