"""
Simple script to verify the dependency injection implementation.
"""

import sys
import os
import traceback

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from interfaces.settings_manager_interface import ISettingsManager
from interfaces.json_manager_interface import IJsonManager
from main_window.main_widget.construct_tab.construct_tab import ConstructTab
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication


class MockConstructTabSettings:
    """Mock implementation of ConstructTabSettings for testing."""

    def get_filters(self):
        return "continuous"

    def set_filters(self, filter_name):
        pass


class MockSettingsManager(ISettingsManager):
    """Mock implementation of ISettingsManager for testing."""

    def __init__(self):
        self.construct_tab_settings = MockConstructTabSettings()

    def get_setting(self, section, key, default_value=None):
        return default_value

    def set_setting(self, section, key, value):
        pass

    def get_global_settings(self):
        return None

    def get_construct_tab_settings(self):
        return self.construct_tab_settings


class MockJsonManager(IJsonManager):
    """Mock implementation of IJsonManager for testing."""

    def __init__(self):
        self.ori_calculator = MockOriCalculator()
        self.ori_validation_engine = MockOriValidationEngine()
        self.start_pos_handler = MockStartPosHandler()
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


class MockStartPosHandler:
    def set_start_position_data(self, start_pos_beat):
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
        mock_settings_manager, "get_construct_tab_settings"
    ), "settings_manager should have get_construct_tab_settings method"
    assert hasattr(
        mock_json_manager, "loader_saver"
    ), "json_manager should have loader_saver attribute"

    # Verify that the AddToSequenceManager class accepts the dependencies
    try:
        from main_window.main_widget.construct_tab.add_to_sequence_manager.add_to_sequence_manager import (
            AddToSequenceManager,
        )

        # Create a simple mock beat frame and last beat
        class MockBeatFrame:
            pass

        class MockBeat:
            pass

        add_to_sequence_manager = AddToSequenceManager(
            json_manager=mock_json_manager,
            beat_frame=MockBeatFrame(),
            last_beat=lambda: None,
            settings_manager=mock_settings_manager,
        )

        # Verify that the dependencies were properly injected
        assert (
            add_to_sequence_manager.json_manager is mock_json_manager
        ), "json_manager not properly injected"
        assert (
            add_to_sequence_manager.settings_manager is mock_settings_manager
        ), "settings_manager not properly injected"

        print("Dependency injection verification successful!")
        return 0
    except Exception as e:
        print(f"Verification failed: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
