"""
Simple script to verify the dependency injection implementation for GenerateTab.
"""

import sys
import os
import traceback
import importlib.util

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from interfaces.settings_manager_interface import ISettingsManager
from interfaces.json_manager_interface import IJsonManager
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication


class MockSettingsManager(ISettingsManager):
    """Mock implementation of ISettingsManager for testing."""

    def __init__(self):
        self.generate_tab_settings = MockGenerateTabSettings()

    def get_setting(self, section, key, default_value=None):
        return default_value

    def set_setting(self, section, key, value):
        pass

    def get_global_settings(self):
        return None

    def get_construct_tab_settings(self):
        return None

    def get_generate_tab_settings(self):
        return self.generate_tab_settings


class MockGenerateTabSettings:
    """Mock implementation of GenerateTabSettings for testing."""

    def get_setting(self, key, default_value=None):
        return default_value

    def set_setting(self, key, value):
        pass

    def get_CAP_type(self):
        return "strict_mirrored"


class MockJsonManager(IJsonManager):
    """Mock implementation of IJsonManager for testing."""

    def __init__(self):
        self.ori_calculator = MockOriCalculator()
        self.ori_validation_engine = MockOriValidationEngine()
        self.loader_saver = MockLoaderSaver()

    def save_sequence(self, sequence_data):
        return True

    def load_sequence(self, file_path=None):
        return []

    def get_updater(self):
        return None


class MockLoaderSaver:
    def load_current_sequence(self):
        # Return a minimal valid sequence with metadata and one beat
        return [
            {"word": "test", "author": "test", "level": 1},  # Metadata
            {
                "beat": 0,
                "letter": "α",
                "end_pos": "alpha3",
                "is_placeholder": False,
                "blue_attributes": {
                    "start_loc": "w",
                    "end_loc": "w",
                    "start_ori": "in",
                    "end_ori": "in",
                    "prop_rot_dir": "no_rot",
                    "turns": 0,
                    "motion_type": "static",
                },
                "red_attributes": {
                    "start_loc": "e",
                    "end_loc": "e",
                    "start_ori": "in",
                    "end_ori": "in",
                    "prop_rot_dir": "no_rot",
                    "turns": 0,
                    "motion_type": "static",
                },
            },
        ]


class MockOriCalculator:
    def calculate_end_ori(self, pictograph_data, color):
        return "in"


class MockOriValidationEngine:
    def validate_single_pictograph(self, pictograph_data, last_pictograph_data):
        pass


def main():
    """Main function to verify the dependency injection implementation."""
    app = QApplication(sys.argv)

    # Create mock dependencies
    mock_settings_manager = MockSettingsManager()
    mock_json_manager = MockJsonManager()

    # Verify that the dependencies are properly defined
    assert isinstance(
        mock_settings_manager, ISettingsManager
    ), "mock_settings_manager should implement ISettingsManager"
    assert isinstance(
        mock_json_manager, IJsonManager
    ), "mock_json_manager should implement IJsonManager"

    # Verify that the mock implementations have the required methods
    assert hasattr(
        mock_settings_manager, "get_generate_tab_settings"
    ), "settings_manager should have get_generate_tab_settings method"
    assert hasattr(
        mock_json_manager, "ori_calculator"
    ), "json_manager should have ori_calculator attribute"
    assert hasattr(
        mock_json_manager, "ori_validation_engine"
    ), "json_manager should have ori_validation_engine attribute"

    # Create a simple mock main widget
    class MockMainWidget:
        def __init__(self):
            self.splash = MockSplash()
            self.sequence_workbench = MockSequenceWorkbench()
            self.construct_tab = MockConstructTab()

        def size(self):
            return QSize(800, 600)

    class MockSplash:
        class MockUpdater:
            def update_progress(self, text):
                print(f"Updating progress: {text}")

        def __init__(self):
            self.updater = self.MockUpdater()

    class MockSequenceWorkbench:
        def __init__(self):
            self.beat_frame = MockBeatFrame()

    class MockBeatFrame:
        def __init__(self):
            self.sequence_workbench = MockSequenceWorkbench()
            self.beat_factory = MockBeatFactory()

        def emit_update_image_export_preview(self):
            pass

    class MockBeatFactory:
        def create_new_beat_and_add_to_sequence(
            self, data, override_grow_sequence=False, update_image_export_preview=True
        ):
            pass

    class MockConstructTab:
        class MockOptionPicker:
            class MockUpdater:
                def update_options(self):
                    pass

            class MockOptionGetter:
                def _load_all_next_option_dicts(self, sequence):
                    return []

            def __init__(self):
                self.updater = self.MockUpdater()
                self.option_getter = self.MockOptionGetter()

        def __init__(self):
            self.option_picker = self.MockOptionPicker()

    mock_main_widget = MockMainWidget()

    try:
        # Create the component with mock dependencies
        generate_tab = GenerateTab(
            main_widget=mock_main_widget,
            settings_manager=mock_settings_manager,
            json_manager=mock_json_manager,
        )

        # Verify that the dependencies were properly injected
        assert (
            generate_tab.settings_manager is mock_settings_manager
        ), "settings_manager not properly injected"
        assert (
            generate_tab.json_manager is mock_json_manager
        ), "json_manager not properly injected"

        # Verify that the builders have access to the json_manager
        assert (
            generate_tab.freeform_builder.json_manager is mock_json_manager
        ), "json_manager not properly passed to freeform_builder"
        assert (
            generate_tab.circular_builder.json_manager is mock_json_manager
        ), "json_manager not properly passed to circular_builder"

        print("GenerateTab dependency injection verification successful!")
        return 0
    except Exception as e:
        print(f"Verification failed: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
