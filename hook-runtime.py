# hook-runtime.py
import os
import sys

# This function runs when the packaged app starts
def adjust_paths():
    # Debug output
    print("Python executable:", sys.executable)
    print("Current working directory:", os.getcwd())
    print("sys.path BEFORE:", sys.path)
    
    # If running as frozen application (packaged by PyInstaller)
    if getattr(sys, 'frozen', False):
        # Get the base directory (where the executable is)
        base_dir = sys._MEIPASS
        print("MEIPASS directory:", base_dir)
        
        # Add the src directory to the Python path
        src_dir = os.path.join(base_dir, "src")
        if os.path.exists(src_dir):
            # Add src directory at the BEGINNING of sys.path
            # This is crucial - it must be first so Python looks here before anywhere else
            sys.path.insert(0, src_dir)
            print(f"Added src directory to path: {src_dir}")
            print("Contents of src directory:", os.listdir(src_dir))
            
            # Check if main_window exists in src
            main_window_dir = os.path.join(src_dir, "main_window")
            if os.path.exists(main_window_dir):
                print(f"main_window directory exists at: {main_window_dir}")
                print("Contents of main_window:", os.listdir(main_window_dir))
            else:
                print(f"ERROR: main_window directory NOT FOUND at expected location: {main_window_dir}")
        else:
            print(f"ERROR: src directory NOT FOUND at expected location: {src_dir}")
            print("Contents of MEIPASS:", os.listdir(base_dir))
    
    print("sys.path AFTER:", sys.path)

# Run the function when this hook is loaded
adjust_paths()