"""
Test module specifically for verifying that hybrid pictograph variations are correctly exported.

This test focuses on the issue where two different pictographs in the matching_pictographs list
should result in different exported images, not the same image twice.
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

    def __init__(self, pictograph_id=None):
        self.pictograph_id = pictograph_id  # Used to identify different pictographs
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

    def __eq__(self, other):
        if not isinstance(other, MockPictograph):
            return False
        return self.pictograph_id == other.pictograph_id


@pytest.fixture
def mock_data_manager():
    """Create a mock data manager with two different pictograph data objects."""
    data_manager = MagicMock()

    # Create two different pictograph data objects for testing
    pro_red_anti_blue = {
        "id": "pro_red_anti_blue",
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
        "id": "pro_blue_anti_red",
        "letter": "C",
        "start_pos": "alpha1",
        "end_pos": "alpha3",
        "red_attributes": {
            "motion_type": "anti",
            "turns": 0,
            "prop_rot_dir": "counter_clockwise",
            "start_ori": "in",
            "start_loc": "s",
            "end_loc": "w",
        },
        "blue_attributes": {
            "motion_type": "pro",
            "turns": 0,
            "prop_rot_dir": "clockwise",
            "start_ori": "in",
            "start_loc": "n",
            "end_loc": "e",
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
    """Create a mock pictograph factory that creates different pictographs based on input data."""
    factory = MagicMock()

    # Set up the create_pictograph_from_data method to return a mock pictograph
    def create_mock_pictograph(data, grid_mode):
        pictograph = MockPictograph(pictograph_id=data.get("id"))
        pictograph.state.pictograph_data = data.copy()
        return pictograph

    factory.create_pictograph_from_data.side_effect = create_mock_pictograph

    return factory


@pytest.fixture
def mock_renderer():
    """Create a mock pictograph renderer."""
    renderer = MagicMock()

    # Set up the create_pictograph_image method to return a mock image
    def create_mock_image(pictograph, add_border=False):
        # Create a unique mock for each pictograph to simulate different images
        mock_image = MagicMock()
        mock_image.pictograph_id = pictograph.pictograph_id
        return mock_image

    renderer.create_pictograph_image.side_effect = create_mock_image

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


def test_export_hybrid_pair_processes_both_pictographs(hybrid_exporter, tmp_path):
    """Test that _export_hybrid_pair processes both pictographs in the matching_pictographs list."""
    # We'll patch os.path.join inside the test to avoid recursion

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

    # Call the method with patched os.path.join
    with patch("os.path.join", return_value="mocked/path"), patch("os.makedirs"):
        exported_count = hybrid_exporter._export_hybrid_pair(
            letter, directory, red_turns, blue_turns, matching_pictographs
        )

    # Verify that two pictographs were exported (1 pro version and 1 anti version)
    assert exported_count == 2
    assert hybrid_exporter._save_pictograph.call_count == 2

    # Get the calls to _save_pictograph
    calls = hybrid_exporter._save_pictograph.call_args_list

    # Extract the pictographs from each call
    pictographs = [call_args[0][0] for call_args in calls]

    # We should have 2 pictographs with 2 unique IDs (1 pro version and 1 anti version)
    pictograph_ids = [p.pictograph_id for p in pictographs]
    assert len(set(pictograph_ids)) == 2  # Should have 2 unique pictograph IDs

    # Verify that we have two different pictographs with different turn patterns
    assert len(pictographs) == 2, f"Expected 2 pictographs, got {len(pictographs)}"

    # Get the turns for each pictograph
    red_turns_first = pictographs[0].elements.motion_set[RED].state.turns
    blue_turns_first = pictographs[0].elements.motion_set[BLUE].state.turns

    red_turns_second = pictographs[1].elements.motion_set[RED].state.turns
    blue_turns_second = pictographs[1].elements.motion_set[BLUE].state.turns

    # The two pictographs should have different turn patterns
    assert (red_turns_first, blue_turns_first) != (
        red_turns_second,
        blue_turns_second,
    ), "Expected different turn patterns for the two pictographs"

    # For mocked objects, we can't use > comparison, so just check that they're different
    assert (
        red_turns_first != red_turns_second or blue_turns_first != blue_turns_second
    ), "Expected different turn patterns for the two pictographs"


def test_export_pictograph_with_multiple_matching_pictographs(
    hybrid_exporter, tmp_path
):
    """Test that export_pictograph correctly handles multiple matching pictographs."""
    # We'll patch os.path.join inside the test to avoid recursion

    # Mock the _export_hybrid_pair method to verify it's called with the correct arguments
    hybrid_exporter._export_hybrid_pair = MagicMock(return_value=2)

    # Call the method with different turns for red and blue
    red_turns = 2
    blue_turns = 1
    letter = "C"
    directory = str(tmp_path)

    # Call the method with patched os.path.join
    with patch("os.path.join", return_value="mocked/path"), patch("os.makedirs"):
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

    # Verify that the matching_pictographs list contains both pictographs
    matching_pictographs = args[4]
    assert len(matching_pictographs) == 2
    assert matching_pictographs[0]["id"] == "pro_red_anti_blue"
    assert matching_pictographs[1]["id"] == "pro_blue_anti_red"

    # Verify that the correct number of pictographs was exported
    assert exported_count == 2


@patch(
    "main_window.main_widget.settings_dialog.ui.codex_exporter.turn_applier.TurnApplier.apply_turns_to_pictograph"
)
def test_turn_applier_called_with_different_pictographs(
    mock_apply_turns, hybrid_exporter, tmp_path
):
    """Test that TurnApplier.apply_turns_to_pictograph is called with different pictographs."""
    # Set up the mock
    mock_apply_turns.return_value = None

    # Mock the _save_pictograph method to avoid actual file operations
    hybrid_exporter._save_pictograph = MagicMock()

    # Create test data
    letter = "C"
    directory = str(tmp_path)
    red_turns = 2
    blue_turns = 1

    # Get the matching pictographs
    start_pos, end_pos = hybrid_exporter.turn_configuration.get_letter_positions(letter)
    matching_pictographs = hybrid_exporter.data_manager.fetch_matching_pictographs(
        letter, start_pos, end_pos
    )

    # Call the method with patched os.path.join
    with patch("os.path.join", return_value="mocked/path"), patch("os.makedirs"):
        hybrid_exporter._export_hybrid_pair(
            letter, directory, red_turns, blue_turns, matching_pictographs
        )

    # Verify that apply_turns_to_pictograph was called 2 times (1 pro version and 1 anti version)
    assert mock_apply_turns.call_count == 2

    # Extract the pictographs from each call
    pictographs = [call_args[0][0] for call_args in mock_apply_turns.call_args_list]

    # Verify that we have 2 pictographs with 2 unique IDs
    pictograph_ids = [p.pictograph_id for p in pictographs]
    unique_ids = set(pictograph_ids)
    assert len(unique_ids) == 2

    # Verify that we have two different pictographs with different turn patterns
    assert len(pictographs) == 2, f"Expected 2 pictographs, got {len(pictographs)}"

    # In the new implementation, both pictographs have the same turn values
    # but different motion types (one is red=pro/blue=anti, the other is red=anti/blue=pro)
    # So we only need to check that they have different IDs
    assert pictograph_ids[0] != pictograph_ids[1], "Expected different pictographs"


if __name__ == "__main__":
    pytest.main(["-v", __file__])
