"""
Test Dynamic Option Picker Updates - Scaffolding Test
Expiration: 2025-01-15

Tests the dynamic option picker update functionality to ensure Legacy-compatible
continuous sequence building behavior in Modern.

This test validates:
1. Option picker refreshes after each pictograph selection
2. End position extraction from beat data
3. Next options are correctly loaded based on sequence state
4. Continuous sequence building workflow
"""

import sys
import os
from typing import Any, Generator
import pytest
from unittest.mock import Mock, patch, MagicMock
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QCoreApplication, QTimer

# Add modern src to path
from pathlib import Path

modern_src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

from domain.models.core_models import (
    BeatData,
    SequenceData,
    MotionData,
    Location,
    MotionType,
)
from presentation.components.option_picker.beat_data_loader import BeatDataLoader
from presentation.tabs.construct.construct_tab_widget import ConstructTabWidget


class TestDynamicOptionPickerUpdates:
    """Test dynamic option picker updates for continuous sequence building"""

    @pytest.fixture
    def app(self) -> Generator[QApplication | QCoreApplication | None, Any, None]:
        """Create QApplication for testing"""
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        yield app
        # Don't quit the app as it might be shared

    @pytest.fixture
    def mock_services(self):
        """Create mock services for testing"""
        position_service = Mock()
        conversion_service = Mock()

        # Mock position service methods
        position_service.get_next_options.return_value = [
            {
                "letter": "A",
                "end_pos": "alpha2",
                "blue_attributes": {
                    "start_loc": "n",
                    "end_loc": "e",
                    "motion_type": "pro",
                },
                "red_attributes": {
                    "start_loc": "n",
                    "end_loc": "e",
                    "motion_type": "anti",
                },
            },
            {
                "letter": "B",
                "end_pos": "alpha3",
                "blue_attributes": {
                    "start_loc": "n",
                    "end_loc": "s",
                    "motion_type": "pro",
                },
                "red_attributes": {
                    "start_loc": "n",
                    "end_loc": "s",
                    "motion_type": "anti",
                },
            },
        ]

        # Mock conversion service
        conversion_service.convert_legacy_pictograph_to_beat_data.side_effect = (
            lambda data: BeatData(
                letter=data["letter"],
                beat_number=1,
                duration=1.0,
                blue_motion=MotionData(
                    motion_type=MotionType.PRO,
                    start_loc=Location.NORTH,
                    end_loc=Location.EAST,
                ),
                red_motion=MotionData(
                    motion_type=MotionType.ANTI,
                    start_loc=Location.NORTH,
                    end_loc=Location.EAST,
                ),
            )
        )

        return position_service, conversion_service

    @pytest.fixture
    def beat_data_loader(self, mock_services):
        """Create BeatDataLoader with mock services"""
        position_service, conversion_service = mock_services
        loader = BeatDataLoader()
        loader.position_service = position_service
        loader.conversion_service = conversion_service
        return loader

    def test_end_position_extraction_from_legacy_format(self, beat_data_loader):
        """Test end position extraction from Legacy-format beat data"""
        # Test direct end_pos field
        beat_data = {"end_pos": "beta5", "letter": "A"}
        end_pos = beat_data_loader._extract_end_position(
            beat_data, beat_data_loader.position_service
        )
        assert end_pos == "beta5"

    def test_end_position_extraction_from_motion_data(self, beat_data_loader):
        """Test end position calculation from motion attributes"""
        beat_data = {
            "letter": "A",
            "blue_attributes": {"end_loc": "e"},
            "red_attributes": {"end_loc": "s"},
        }
        end_pos = beat_data_loader._extract_end_position(
            beat_data, beat_data_loader.position_service
        )
        assert end_pos == "alpha7"  # (e, s) maps to alpha7

    def test_refresh_options_from_sequence(self, beat_data_loader, mock_services):
        """Test option refresh based on sequence data"""
        position_service, conversion_service = mock_services

        # Create sequence with start position and one beat
        sequence_data = [
            {"metadata": "sequence_info"},
            {"beat": 0, "letter": "β", "end_pos": "beta5"},
            {"beat": 1, "letter": "A", "end_pos": "alpha2"},
        ]

        # Test refresh
        options = beat_data_loader.refresh_options_from_sequence(sequence_data)

        # Verify position service was called with last beat's end position
        position_service.get_next_options.assert_called_with("alpha2")

        # Verify options were converted
        assert len(options) == 2
        assert all(isinstance(opt, BeatData) for opt in options)

    def test_sequence_to_legacy_format_conversion(self, app):
        """Test conversion of Modern SequenceData to Legacy format"""
        # Create mock construct tab
        construct_tab = Mock(spec=ConstructTabWidget)

        # Create test sequence
        beat1 = BeatData(
            letter="A",
            beat_number=1,
            duration=1.0,
            blue_motion=MotionData(
                motion_type=MotionType.PRO,
                start_loc=Location.NORTH,
                end_loc=Location.EAST,
            ),
            red_motion=MotionData(
                motion_type=MotionType.ANTI,
                start_loc=Location.NORTH,
                end_loc=Location.SOUTH,
            ),
        )

        sequence = SequenceData(name="Test", beats=[beat1])

        # Test conversion method
        construct_tab._convert_sequence_to_legacy_format = (
            ConstructTabWidget._convert_sequence_to_legacy_format
        )
        legacy_format = construct_tab._convert_sequence_to_legacy_format(
            construct_tab, sequence
        )

        # Verify format
        assert len(legacy_format) == 2  # metadata + 1 beat
        assert legacy_format[0] == {"metadata": "sequence_info"}
        assert legacy_format[1]["letter"] == "A"
        assert legacy_format[1]["end_pos"] == "alpha3"  # (n->e, n->s) maps to alpha3

    @patch("presentation.components.option_picker.OptionPickerWidget")
    def test_option_picker_refresh_integration(
        self, mock_option_picker_class, app, mock_services
    ):
        """Test integration of option picker refresh with sequence updates"""
        position_service, conversion_service = mock_services

        # Create mock option picker instance
        mock_option_picker = Mock()
        mock_option_picker_class.return_value = mock_option_picker

        # Create construct tab with mocked dependencies
        with patch(
            "presentation.tabs.construct_tab_widget.ConstructTabWidget._create_workbench"
        ), patch(
            "presentation.tabs.construct_tab_widget.ConstructTabWidget._create_start_position_picker"
        ), patch(
            "presentation.tabs.construct_tab_widget.ConstructTabWidget._create_option_picker"
        ):

            construct_tab = ConstructTabWidget()
            construct_tab.option_picker = mock_option_picker

            # Create test sequence
            beat1 = BeatData(
                letter="A",
                beat_number=1,
                duration=1.0,
                blue_motion=MotionData(
                    motion_type=MotionType.PRO,
                    start_loc=Location.NORTH,
                    end_loc=Location.EAST,
                ),
                red_motion=MotionData(
                    motion_type=MotionType.ANTI,
                    start_loc=Location.NORTH,
                    end_loc=Location.SOUTH,
                ),
            )

            sequence = SequenceData(name="Test", beats=[beat1])

            # Test refresh method
            construct_tab._refresh_option_picker_from_sequence(sequence)

            # Verify option picker refresh was called
            mock_option_picker.refresh_options_from_sequence.assert_called_once()

            # Verify the sequence data passed to option picker
            call_args = mock_option_picker.refresh_options_from_sequence.call_args[0][0]
            assert len(call_args) == 2  # metadata + 1 beat
            assert call_args[1]["letter"] == "A"

    def test_circular_signal_protection(self, app):
        """Test that circular signal emissions are prevented"""
        with patch(
            "presentation.tabs.construct_tab_widget.ConstructTabWidget._create_workbench"
        ), patch(
            "presentation.tabs.construct_tab_widget.ConstructTabWidget._create_start_position_picker"
        ), patch(
            "presentation.tabs.construct_tab_widget.ConstructTabWidget._create_option_picker"
        ):

            construct_tab = ConstructTabWidget()
            construct_tab.option_picker = Mock()
            construct_tab._emitting_signal = True  # Simulate ongoing emission

            # Create test sequence
            sequence = SequenceData(name="Test", beats=[])

            # Test that refresh is skipped during signal emission
            construct_tab._on_workbench_modified(sequence)

            # Verify option picker refresh was not called due to circular protection
            construct_tab.option_picker.refresh_options_from_sequence.assert_not_called()


if __name__ == "__main__":
    # Run the test
    pytest.main([__file__, "-v"])
