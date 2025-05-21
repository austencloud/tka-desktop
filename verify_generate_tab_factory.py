"""
Simple script to verify the GenerateTabFactory implementation.
"""

import sys
import os
import traceback
import importlib.util

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from interfaces.settings_manager_interface import ISettingsManager
from interfaces.json_manager_interface import IJsonManager
from PyQt6.QtWidgets import QApplication


class MockSettingsManager(ISettingsManager):
    """Mock implementation of ISettingsManager for testing."""
    
    def __init__(self):
        pass
    
    def get_setting(self, section, key, default_value=None):
        return default_value
    
    def set_setting(self, section, key, value):
        pass
    
    def get_global_settings(self):
        return None
    
    def get_construct_tab_settings(self):
        return None
        
    def get_generate_tab_settings(self):
        return None


class MockJsonManager(IJsonManager):
    """Mock implementation of IJsonManager for testing."""
    
    def __init__(self):
        self.ori_calculator = None
        self.ori_validation_engine = None
    
    def save_sequence(self, sequence_data):
        return True
    
    def load_sequence(self, file_path=None):
        return []
    
    def get_updater(self):
        return None


def main():
    """Main function to verify the GenerateTabFactory implementation."""
    app = QApplication(sys.argv)
    
    # Create mock dependencies
    mock_settings_manager = MockSettingsManager()
    mock_json_manager = MockJsonManager()
    
    # Verify that the dependencies are properly defined
    assert isinstance(mock_settings_manager, ISettingsManager), "mock_settings_manager should implement ISettingsManager"
    assert isinstance(mock_json_manager, IJsonManager), "mock_json_manager should implement IJsonManager"
    
    # Verify that the GenerateTabFactory exists and has the create method
    try:
        # Import the factory directly to avoid circular imports
        spec = importlib.util.spec_from_file_location(
            "generate_tab_factory", 
            os.path.join(os.path.dirname(__file__), "src/main_window/main_widget/generate_tab/generate_tab_factory.py")
        )
        generate_tab_factory_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generate_tab_factory_module)
        
        # Check if the factory has the create method
        assert hasattr(generate_tab_factory_module.GenerateTabFactory, "create"), "GenerateTabFactory should have a create method"
        
        # Check the signature of the create method
        create_method = generate_tab_factory_module.GenerateTabFactory.create
        import inspect
        signature = inspect.signature(create_method)
        parameters = list(signature.parameters.keys())
        
        assert "main_widget" in parameters, "create method should have a main_widget parameter"
        assert "settings_manager" in parameters, "create method should have a settings_manager parameter"
        assert "json_manager" in parameters, "create method should have a json_manager parameter"
        
        print("GenerateTabFactory verification successful!")
        return 0
    except Exception as e:
        print(f"Verification failed: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
