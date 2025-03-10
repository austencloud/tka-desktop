import os
import sys


# Configure Python's import path before any other imports
def configure_imports():
    if getattr(sys, "frozen", False):
        # Running in PyInstaller package
        base_dir = sys._MEIPASS
    else:
        # Running in development
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Add src directory to path for both development and packaged modes
    src_dir = os.path.join(base_dir, "src")
    if os.path.exists(src_dir) and src_dir not in sys.path:
        sys.path.insert(0, src_dir)
        print(f"Added {src_dir} to Python path")

    # Print debug info
    print("Python path:", sys.path)
    print(
        "Contents of src directory:",
        os.listdir(src_dir) if os.path.exists(src_dir) else "Not found",
    )

    # If in packaged mode, also check contents of the package
    if getattr(sys, "frozen", False):
        print("Contents of MEIPASS:", os.listdir(base_dir))


# Run the main application
def run_app():
    # Now we can safely import from the application modules
    from src.main import main_without_imports

    main_without_imports()


if __name__ == "__main__":
    configure_imports()
    run_app()
