"""
Simple script to verify the LearnTabFactory implementation.
"""

import sys
import os
import traceback
import re

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))


def main():
    """Main function to verify the LearnTabFactory implementation."""
    
    # Read the LearnTabFactory file
    learn_tab_factory_path = os.path.join(
        os.path.dirname(__file__), 
        "src/main_window/main_widget/learn_tab/learn_tab_factory.py"
    )
    
    # Read the LearnTab file
    learn_tab_path = os.path.join(
        os.path.dirname(__file__), 
        "src/main_window/main_widget/learn_tab/learn_tab.py"
    )
    
    # Read the MainWidgetUI file
    main_widget_ui_path = os.path.join(
        os.path.dirname(__file__), 
        "src/main_window/main_widget/main_widget_ui.py"
    )
    
    try:
        # Verify LearnTabFactory
        with open(learn_tab_factory_path, 'r') as f:
            factory_content = f.read()
        
        assert "from interfaces.settings_manager_interface import ISettingsManager" in factory_content, \
            "LearnTabFactory should import ISettingsManager"
        assert "from interfaces.json_manager_interface import IJsonManager" in factory_content, \
            "LearnTabFactory should import IJsonManager"
        assert "def create(" in factory_content, \
            "LearnTabFactory should have a create method"
        assert "settings_manager: ISettingsManager" in factory_content, \
            "create method should accept settings_manager parameter"
        assert "json_manager: IJsonManager" in factory_content, \
            "create method should accept json_manager parameter"
        
        # Verify LearnTab
        with open(learn_tab_path, 'r') as f:
            learn_tab_content = f.read()
        
        assert "from interfaces.settings_manager_interface import ISettingsManager" in learn_tab_content, \
            "LearnTab should import ISettingsManager"
        assert "from interfaces.json_manager_interface import IJsonManager" in learn_tab_content, \
            "LearnTab should import IJsonManager"
        assert "settings_manager: ISettingsManager" in learn_tab_content, \
            "LearnTab constructor should accept settings_manager parameter"
        assert "json_manager: IJsonManager" in learn_tab_content, \
            "LearnTab constructor should accept json_manager parameter"
        assert "self.settings_manager = settings_manager" in learn_tab_content, \
            "LearnTab should store settings_manager as an instance variable"
        assert "self.json_manager = json_manager" in learn_tab_content, \
            "LearnTab should store json_manager as an instance variable"
        
        # Verify MainWidgetUI
        with open(main_widget_ui_path, 'r') as f:
            main_widget_ui_content = f.read()
        
        assert "from .learn_tab.learn_tab_factory import LearnTabFactory" in main_widget_ui_content, \
            "MainWidgetUI should import LearnTabFactory"
        assert re.search(r"mw\.learn_tab\s*=\s*LearnTabFactory\.create\(", main_widget_ui_content), \
            "MainWidgetUI should use LearnTabFactory.create to create LearnTab"
        assert re.search(r"LearnTabFactory\.create\([^)]*settings_manager\s*=\s*settings_manager", main_widget_ui_content), \
            "MainWidgetUI should pass settings_manager to LearnTabFactory.create"
        assert re.search(r"LearnTabFactory\.create\([^)]*json_manager\s*=\s*json_manager", main_widget_ui_content), \
            "MainWidgetUI should pass json_manager to LearnTabFactory.create"
        
        print("LearnTab dependency injection verification successful!")
        return 0
    except Exception as e:
        print(f"Verification failed: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
