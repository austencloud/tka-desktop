"""
Test module for the ConstructTab dependency injection implementation.
"""

import os
import sys
import pytest
from unittest.mock import MagicMock
from PyQt6.QtCore import QSize

# Add the src directory to the Python path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../src"))
)

from interfaces.settings_manager_interface import ISettingsManager
from interfaces.json_manager_interface import IJsonManager
from main_window.main_widget.construct_tab.construct_tab import ConstructTab
from main_window.main_widget.fade_manager.fade_manager import FadeManager


class MockSettingsManager(ISettingsManager):
    """Mock implementation of ISettingsManager for testing."""
    
    def get_setting(self, section, key, default_value=None):
        return default_value
    
    def set_setting(self, section, key, value):
        pass
    
    def get_global_settings(self):
        return MagicMock()
    
    def get_construct_tab_settings(self):
        return MagicMock()


class MockJsonManager(IJsonManager):
    """Mock implementation of IJsonManager for testing."""
    
    def save_sequence(self, sequence_data):
        return True
    
    def load_sequence(self, file_path=None):
        return []
    
    def get_updater(self):
        return MagicMock()


def test_construct_tab_with_di():
    """Test that ConstructTab can be instantiated with dependency injection."""
    # Create mock dependencies
    mock_settings_manager = MockSettingsManager()
    mock_json_manager = MockJsonManager()
    mock_beat_frame = MagicMock()
    mock_fade_manager = MagicMock()
    
    # Create the component with mock dependencies
    construct_tab = ConstructTab(
        beat_frame=mock_beat_frame,
        pictograph_dataset={},
        size_provider=lambda: QSize(800, 600),
        fade_to_stack_index=lambda index: None,
        fade_manager=mock_fade_manager,
        settings_manager=mock_settings_manager,
        json_manager=mock_json_manager
    )
    
    # Verify that the dependencies were properly injected
    assert construct_tab.settings_manager is mock_settings_manager
    assert construct_tab.json_manager is mock_json_manager
    
    # Verify that we can call methods that use the dependencies
    construct_tab.transition_to_option_picker()  # This uses fade_to_stack_index
    
    # This test passes if no exceptions are raised
