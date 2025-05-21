"""
Simple script to verify the MainWidgetUI implementation.
"""

import sys
import os
import traceback
import re

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))


def main():
    """Main function to verify the MainWidgetUI implementation."""
    
    # Read the MainWidgetUI file
    main_widget_ui_path = os.path.join(
        os.path.dirname(__file__), 
        "src/main_window/main_widget/main_widget_ui.py"
    )
    
    try:
        with open(main_widget_ui_path, 'r') as f:
            content = f.read()
        
        # Check if GenerateTabFactory is imported
        assert "from .generate_tab.generate_tab_factory import GenerateTabFactory" in content, \
            "GenerateTabFactory should be imported in MainWidgetUI"
        
        # Check if GenerateTabFactory.create is used
        assert re.search(r"mw\.generate_tab\s*=\s*GenerateTabFactory\.create\(", content), \
            "GenerateTabFactory.create should be used to create the GenerateTab"
        
        # Check if settings_manager and json_manager are passed to GenerateTabFactory.create
        assert re.search(r"GenerateTabFactory\.create\([^)]*settings_manager\s*=\s*settings_manager", content), \
            "settings_manager should be passed to GenerateTabFactory.create"
        assert re.search(r"GenerateTabFactory\.create\([^)]*json_manager\s*=\s*json_manager", content), \
            "json_manager should be passed to GenerateTabFactory.create"
        
        print("MainWidgetUI verification successful!")
        return 0
    except Exception as e:
        print(f"Verification failed: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
