"""
Script to verify the dependency injection implementation across multiple components.
"""

import sys
import os
import traceback
import re

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))


def check_file_content(file_path, checks):
    """Check if a file contains specific patterns."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            
        for check_name, pattern in checks.items():
            if isinstance(pattern, str):
                assert pattern in content, f"Check '{check_name}' failed: '{pattern}' not found in {file_path}"
            else:  # Assume it's a regex pattern
                assert pattern.search(content), f"Check '{check_name}' failed: regex pattern not matched in {file_path}"
        
        return True
    except Exception as e:
        print(f"Error checking {file_path}: {e}")
        return False


def main():
    """Main function to verify the dependency injection implementation."""
    src_dir = os.path.join(os.path.dirname(__file__), "src")
    
    # Define the files to check and the patterns to look for
    files_to_check = {
        # Interfaces
        os.path.join(src_dir, "interfaces/settings_manager_interface.py"): {
            "is_protocol": "class ISettingsManager(Protocol)",
            "has_browse_settings": "@property\n    def browse_settings",
            "has_get_generate_tab_settings": "def get_generate_tab_settings",
            "has_get_construct_tab_settings": "def get_construct_tab_settings",
            "has_get_global_settings": "def get_global_settings",
        },
        
        os.path.join(src_dir, "interfaces/json_manager_interface.py"): {
            "is_protocol": "class IJsonManager(Protocol)",
            "has_save_sequence": "def save_sequence",
            "has_load_sequence": "def load_sequence",
            "has_get_updater": "def get_updater",
        },
        
        # Factories
        os.path.join(src_dir, "main_window/main_widget/construct_tab/construct_tab_factory.py"): {
            "has_create_method": "def create",
            "accepts_settings_manager": "settings_manager: ISettingsManager",
            "accepts_json_manager": "json_manager: IJsonManager",
        },
        
        os.path.join(src_dir, "main_window/main_widget/generate_tab/generate_tab_factory.py"): {
            "has_create_method": "def create",
            "accepts_settings_manager": "settings_manager: ISettingsManager",
            "accepts_json_manager": "json_manager: IJsonManager",
        },
        
        os.path.join(src_dir, "main_window/main_widget/learn_tab/learn_tab_factory.py"): {
            "has_create_method": "def create",
            "accepts_settings_manager": "settings_manager: ISettingsManager",
            "accepts_json_manager": "json_manager: IJsonManager",
        },
        
        os.path.join(src_dir, "main_window/main_widget/browse_tab/browse_tab_factory.py"): {
            "has_create_method": "def create",
            "accepts_settings_manager": "settings_manager: ISettingsManager",
            "accepts_json_manager": "json_manager: IJsonManager",
        },
        
        os.path.join(src_dir, "main_window/main_widget/sequence_card_tab/sequence_card_tab_factory.py"): {
            "has_create_method": "def create",
            "accepts_settings_manager": "settings_manager: ISettingsManager",
            "accepts_json_manager": "json_manager: IJsonManager",
        },
        
        os.path.join(src_dir, "main_window/main_widget/main_background_widget/main_background_widget_factory.py"): {
            "has_create_method": "def create",
            "accepts_settings_manager": "settings_manager: ISettingsManager",
        },
        
        # Components
        os.path.join(src_dir, "main_window/main_widget/main_widget_ui.py"): {
            "uses_construct_tab_factory": re.compile(r"mw\.construct_tab\s*=\s*ConstructTabFactory\.create\("),
            "uses_generate_tab_factory": re.compile(r"mw\.generate_tab\s*=\s*GenerateTabFactory\.create\("),
            "uses_learn_tab_factory": re.compile(r"mw\.learn_tab\s*=\s*LearnTabFactory\.create\("),
            "uses_browse_tab_factory": re.compile(r"mw\.browse_tab\s*=\s*BrowseTabFactory\.create\("),
            "uses_sequence_card_tab_factory": re.compile(r"mw\.sequence_card_tab\s*=\s*SequenceCardTabFactory\.create\("),
            "uses_main_background_widget_factory": re.compile(r"mw\.background_widget\s*=\s*MainBackgroundWidgetFactory\.create\("),
            "passes_settings_manager": re.compile(r"settings_manager=settings_manager"),
            "passes_json_manager": re.compile(r"json_manager=json_manager"),
        },
    }
    
    # Check each file
    all_checks_passed = True
    for file_path, checks in files_to_check.items():
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            all_checks_passed = False
            continue
            
        if not check_file_content(file_path, checks):
            all_checks_passed = False
    
    if all_checks_passed:
        print("All dependency injection checks passed!")
        return 0
    else:
        print("Some dependency injection checks failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
