import os
import sys
import subprocess
import shutil

# Print debug information
print("Python executable:", sys.executable)
print("Current working directory:", os.getcwd())

# If running as frozen application (packaged by PyInstaller)
if getattr(sys, 'frozen', False):
    # Get the directory where the executable is located
    base_dir = sys._MEIPASS
    print("MEIPASS directory:", base_dir)
    
    # List contents of the MEIPASS directory
    print("Contents of MEIPASS:", os.listdir(base_dir))
    
    # Check if src directory exists
    src_dir = os.path.join(base_dir, "src")
    if os.path.exists(src_dir):
        print("Contents of src directory:", os.listdir(src_dir))
        
        # Check if main_window directory exists in src
        main_window_dir = os.path.join(src_dir, "main_window")
        if os.path.exists(main_window_dir):
            print("main_window directory exists!")
            
            # Create a symbolic link to make main_window available directly
            if "main_window" not in os.listdir(base_dir):
                try:
                    # On Windows, try directory junction
                    if os.name == 'nt':
                        subprocess.run(['mklink', '/J', os.path.join(base_dir, 'main_window'), main_window_dir], shell=True)
                    else:
                        # On Unix, try symlink
                        os.symlink(main_window_dir, os.path.join(base_dir, 'main_window'))
                    print("Created symlink to main_window")
                except Exception as e:
                    print(f"Symlink creation failed: {e}")
                    
                    # Fallback: copy the directory
                    try:
                        shutil.copytree(main_window_dir, os.path.join(base_dir, 'main_window'))
                        print("Copied main_window directory")
                    except Exception as copy_e:
                        print(f"Copy failed: {copy_e}")
        else:
            print("ERROR: main_window directory NOT found in src!")
    else:
        print("ERROR: src directory NOT found in MEIPASS!")

    # Do the same for other critical modules
    for module in ['utils', 'settings_manager', 'splash_screen', 'profiler']:
        module_dir = os.path.join(src_dir, module)
        if os.path.exists(module_dir) and module not in os.listdir(base_dir):
            try:
                shutil.copytree(module_dir, os.path.join(base_dir, module))
                print(f"Copied {module} directory")
            except Exception as e:
                print(f"Copy of {module} failed: {e}")
    
    # Now adjust sys.path
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)
        print(f"Added {base_dir} to sys.path")

# Now we can safely import and run the main module
from src.main import main
main()