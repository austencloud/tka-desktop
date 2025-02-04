import os
import shutil
import ctypes
import sys

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def delete_empty_directories(directory):
    """Recursively delete all empty directories."""
    for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
        # If the directory is empty (no files and no subdirectories)
        if not dirnames and not filenames:
            try:
                print(f"Deleting empty directory: {dirpath}")
                shutil.rmtree(dirpath)
            except OSError as e:
                print(f"Error deleting {dirpath}: {e}")

if __name__ == "__main__":
    # If not admin, request admin privileges
    if not is_admin():
        print("Script is not running as admin, requesting privileges...")
        # Re-run the script with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    else:
        # Root directory where the dictionary is located
        root_dir = r"F:\CODE\tka-sequence-constructor\dictionary"
        delete_empty_directories(root_dir)
