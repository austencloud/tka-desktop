"""
Test module for the codex hybrid pictograph exporter.

This module tests the functionality of the hybrid pictograph exporter,
specifically focusing on the correct generation of both pro and anti versions
of hybrid pictographs.
"""

import os
import sys
import pytest
from unittest.mock import MagicMock, patch

# Add the src directory to the Python path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../src"))
)

from main_window.main_widget.settings_dialog.ui.codex_exporter.exporters.hybrid_exporter import (
    HybridExporter,
)
from data.constants import RED, BLUE


class MockPictograph:
    """Mock pictograph class for testing."""

    def __init__(self):
        self.elements = MagicMock()
        self.managers = MagicMock()
        self.state = MagicMock()
        self.state.pictograph_data = {}

        # Set up motion objects
        self.red_motion = MagicMock()
        self.blue_motion = MagicMock()
        self.elements.motion_set = {RED: self.red_motion, BLUE: self.blue_motion}

        # Set up arrows
        self.elements.arrows = {RED: MagicMock(), BLUE: MagicMock()}

    def update(self):
        """Mock update method."""


@pytest.fixture
def mock_data_manager():
    """Create a mock data manager."""
    data_manager = MagicMock()

    # Create two different pictograph data objects for testing
    pro_red_anti_blue = {
        "letter": "C",
        "start_pos": "alpha1",
        "end_pos": "alpha3",
        "red_attributes": {
            "motion_type": "pro",
            "turns": 0,
            "prop_rot_dir": "clockwise",
            "start_ori": "in",
            "start_loc": "n",
            "end_loc": "e",
        },
        "blue_attributes": {
            "motion_type": "anti",
            "turns": 0,
            "prop_rot_dir": "counter_clockwise",
            "start_ori": "in",
            "start_loc": "s",
            "end_loc": "w",
        },
    }

    pro_blue_anti_red = {
        "letter": "C",
        "start_pos": "alpha1",
        "end_pos": "alpha3",
        "red_attributes": {
            "motion_type": "anti",
            "turns": 0,
            "prop_rot_dir": "counter_clockwise",
            "start_ori": "in",
            "start_loc": "n",
            "end_loc": "e",
        },
        "blue_attributes": {
            "motion_type": "pro",
            "turns": 0,
            "prop_rot_dir": "clockwise",
            "start_ori": "in",
            "start_loc": "s",
            "end_loc": "w",
        },
    }

    # Set up the fetch_matching_pictographs method to return our test data
    data_manager.fetch_matching_pictographs.return_value = [
        pro_red_anti_blue,
        pro_blue_anti_red,
    ]

    return data_manager


@pytest.fixture
def mock_factory():
    """Create a mock pictograph factory."""
    factory = MagicMock()

    # Set up the create_pictograph_from_data method to return a mock pictograph
    def create_mock_pictograph(data, grid_mode):
        pictograph = MockPictograph()
        pictograph.state.pictograph_data = data.copy()
        return pictograph

    factory.create_pictograph_from_data.side_effect = create_mock_pictograph

    return factory


@pytest.fixture
def mock_renderer():
    """Create a mock pictograph renderer."""
    renderer = MagicMock()

    # Set up the create_pictograph_image method to return a mock image
    renderer.create_pictograph_image.return_value = MagicMock()

    return renderer


@pytest.fixture
def mock_turn_configuration():
    """Create a mock turn configuration."""
    turn_config = MagicMock()

    # Set up the get_letter_positions method to return positions for letter C
    turn_config.get_letter_positions.return_value = ("alpha1", "alpha3")

    # Set up the get_hybrid_filename method
    turn_config.get_hybrid_filename.side_effect = (
        lambda letter, red_turns, blue_turns, motion_type: f"{letter}_{motion_type}.png"
    )

    # Set up the get_non_hybrid_filename method
    turn_config.get_non_hybrid_filename.side_effect = lambda letter: f"{letter}.png"

    return turn_config


@pytest.fixture
def hybrid_exporter(
    mock_data_manager, mock_factory, mock_renderer, mock_turn_configuration
):
    """Create a hybrid exporter with mock dependencies."""
    return HybridExporter(
        mock_data_manager, mock_factory, mock_renderer, mock_turn_configuration
    )


def test_export_hybrid_pair_creates_both_versions(hybrid_exporter, tmp_path):
    """Test that _export_hybrid_pair creates both pro and anti versions."""
    # Mock the _save_pictograph method to track calls
    hybrid_exporter._save_pictograph = MagicMock()

    # Call the method with different turns for red and blue
    red_turns = 2
    blue_turns = 1
    letter = "C"
    directory = str(tmp_path)

    # Get the matching pictographs
    start_pos, end_pos = hybrid_exporter.turn_configuration.get_letter_positions(letter)
    matching_pictographs = hybrid_exporter.data_manager.fetch_matching_pictographs(
        letter, start_pos, end_pos
    )

    # Patch os.path.join to avoid file system operations
    with patch("os.path.join", return_value="mocked/path"), patch("os.makedirs"):
        # Call the method
        exported_count = hybrid_exporter._export_hybrid_pair(
            letter, directory, red_turns, blue_turns, matching_pictographs
        )

    # Verify that two pictographs were exported
    assert exported_count == 2
    assert hybrid_exporter._save_pictograph.call_count == 2

    # Get the calls to _save_pictograph
    calls = hybrid_exporter._save_pictograph.call_args_list

    # Verify the first call (pro_turns version)
    first_call_pictograph = calls[0][0][0]

    # Verify the second call (anti_turns version)
    second_call_pictograph = calls[1][0][0]

    # Since we mocked os.path.join, we can't check the filepath directly
    # Instead, check that the pictographs have different turn values

    # Check that the red and blue turns are different between the two calls
    red_turns_first = first_call_pictograph.elements.motion_set[RED].state.turns
    blue_turns_first = first_call_pictograph.elements.motion_set[BLUE].state.turns

    red_turns_second = second_call_pictograph.elements.motion_set[RED].state.turns
    blue_turns_second = second_call_pictograph.elements.motion_set[BLUE].state.turns

    # Either red turns or blue turns should be different between the two pictographs
    assert (red_turns_first != red_turns_second) or (
        blue_turns_first != blue_turns_second
    )


def test_export_pictograph_with_different_turns(hybrid_exporter, tmp_path):
    """Test that export_pictograph correctly handles different turns for red and blue."""
    # Mock the _export_hybrid_pair method to verify it's called
    hybrid_exporter._export_hybrid_pair = MagicMock(return_value=2)

    # Call the method with different turns for red and blue
    red_turns = 2
    blue_turns = 1
    letter = "C"
    directory = str(tmp_path)

    # Patch os.path.join to avoid file system operations
    with patch("os.path.join", return_value="mocked/path"), patch("os.makedirs"):
        # Call the method
        exported_count = hybrid_exporter.export_pictograph(
            letter, directory, red_turns, blue_turns
        )

    # Verify that _export_hybrid_pair was called with the correct arguments
    hybrid_exporter._export_hybrid_pair.assert_called_once()
    args = hybrid_exporter._export_hybrid_pair.call_args[0]
    assert args[0] == letter
    assert args[1] == directory
    assert args[2] == red_turns
    assert args[3] == blue_turns

    # Verify that the correct number of pictographs was exported
    assert exported_count == 2


def test_export_pictograph_with_same_turns(hybrid_exporter, tmp_path):
    """Test that export_pictograph correctly handles same turns for red and blue."""
    # Mock the _export_non_hybrid method to verify it's called
    hybrid_exporter._export_non_hybrid = MagicMock(return_value=1)

    # Call the method with same turns for red and blue
    turns = 2
    letter = "C"
    directory = str(tmp_path)

    # Patch os.path.join to avoid file system operations
    with patch("os.path.join", return_value="mocked/path"), patch("os.makedirs"):
        # Call the method
        exported_count = hybrid_exporter.export_pictograph(
            letter, directory, turns, turns
        )

    # Verify that _export_non_hybrid was called with the correct arguments
    hybrid_exporter._export_non_hybrid.assert_called_once()
    args = hybrid_exporter._export_non_hybrid.call_args[0]
    assert args[0] == letter
    assert args[1] == directory
    assert args[2] == turns

    # Verify that the correct number of pictographs was exported
    assert exported_count == 1


@patch(
    "main_window.main_widget.settings_dialog.ui.codex_exporter.turn_applier.TurnApplier.apply_turns_to_pictograph"
)
def test_turn_applier_called_correctly(mock_apply_turns, hybrid_exporter, tmp_path):
    """Test that TurnApplier.apply_turns_to_pictograph is called with correct arguments."""
    # Set up the mock
    mock_apply_turns.return_value = None

    # Mock the _save_pictograph method to avoid actual file operations
    hybrid_exporter._save_pictograph = MagicMock()

    # Create test data
    letter = "C"
    directory = str(tmp_path)
    red_turns = 2
    blue_turns = 1

    # Create a mock pictograph data with red=pro and blue=anti
    pro_red_anti_blue = {
        "letter": "C",
        "start_pos": "alpha1",
        "end_pos": "alpha3",
        "red_attributes": {
            "motion_type": "pro",
            "turns": 0,
            "prop_rot_dir": "clockwise",
        },
        "blue_attributes": {
            "motion_type": "anti",
            "turns": 0,
            "prop_rot_dir": "counter_clockwise",
        },
    }

    # Call the method
    hybrid_exporter._export_hybrid_pair(
        letter, directory, red_turns, blue_turns, [pro_red_anti_blue]
    )

    # Verify that apply_turns_to_pictograph was called twice with correct arguments
    assert mock_apply_turns.call_count == 2

    # First call should be for pro_red (red=pro with turns, blue=anti with turns)
    first_call_args = mock_apply_turns.call_args_list[0][1]
    assert first_call_args["red_turns"] == red_turns
    assert first_call_args["blue_turns"] == blue_turns

    # Second call should be for pro_blue (red=anti with turns, blue=pro with turns)
    second_call_args = mock_apply_turns.call_args_list[1][1]
    assert second_call_args["red_turns"] == red_turns
    assert second_call_args["blue_turns"] == blue_turns


if __name__ == "__main__":
    pytest.main(["-v", __file__])
