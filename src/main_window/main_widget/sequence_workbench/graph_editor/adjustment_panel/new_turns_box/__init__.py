from pathlib import Path
import sys

def create_directories_and_files():
    try:
        base_dir = Path('F:/CODE/the-kinetic-constructor-desktop/src/main_window/main_widget/sequence_workbench/graph_editor/adjustment_panel/new_turns_box')
        
        # Check if path exists or can be created
        print(f"Checking path: {base_dir}")
        if not base_dir.exists():
            print("Base directory doesn't exist, trying to create it")
            base_dir.mkdir(parents=True, exist_ok=True)
        dirs = [
            'domain',
            'ui',
            'ui/buttons',
            'managers',
            'services'
        ]

        files = [
            'domain/__init__.py',
            'ui/__init__.py',
            'ui/buttons/__init__.py',
            'managers/__init__.py',
            'services/__init__.py'
        ]

        for directory in dirs:
            dir_path = base_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {dir_path}")

        for file in files:
            file_path = base_dir / file
            file_path.touch()
            print(f"Created file: {file_path}")

    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Script is running...")
    create_directories_and_files()
    print("Script completed.")