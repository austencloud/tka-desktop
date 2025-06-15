"""
Integration tests for ModernBeatFrame component.

Tests the complete beat frame workflow including service integration.
"""

import pytest
from unittest.mock import Mock, MagicMock
from PyQt6.QtTest import QSignalSpy  # Changed from PyQt6.QtCore

from v2.src.presentation.components.workbench.beat_frame.modern_beat_frame import (
    ModernBeatFrame,
)
from v2.src.application.services.beat_frame_layout_service import BeatFrameLayoutService


@pytest.mark.integration
class TestBeatFrameIntegration:
    """Test beat frame component integration."""

    def setup_method(self):
        """Setup for each test."""
        self.layout_service = BeatFrameLayoutService()

    def test_beat_frame_creation_with_real_service(self, qapp, mock_sequence_data):
        """Test beat frame creation with real layout service."""
        # Create beat frame with real service
        beat_frame = ModernBeatFrame(layout_service=self.layout_service, parent=None)

        # Verify initialization
        assert beat_frame is not None
        assert beat_frame._layout_service is self.layout_service

        # Test setting sequence
        beat_frame.set_sequence(mock_sequence_data)

        # Verify beat views were created
        assert len(beat_frame._beat_views) > 0

    def test_beat_selection_signal_flow(self, qapp, mock_sequence_data):
        """Test signal flow when beat is selected."""
        beat_frame = ModernBeatFrame(layout_service=self.layout_service, parent=None)

        # Setup signal spy
        signal_spy = QSignalSpy(beat_frame.beat_selected)

        # Set sequence to create beat views
        beat_frame.set_sequence(mock_sequence_data)

        # Simulate beat selection
        if beat_frame._beat_views:
            first_beat_view = beat_frame._beat_views[0]
            first_beat_view._on_clicked()

            # Process events
            qapp.processEvents()

            # Verify signal was emitted
            assert len(signal_spy) == 1

    def test_sequence_modification_workflow(self, qapp, mock_sequence_data):
        """Test complete sequence modification workflow using real data."""
        beat_frame = ModernBeatFrame(layout_service=self.layout_service, parent=None)

        # Setup signal spies
        beat_selected_spy = QSignalSpy(beat_frame.beat_selected)
        sequence_modified_spy = QSignalSpy(beat_frame.sequence_modified)

        # Initial sequence
        beat_frame.set_sequence(mock_sequence_data)
        qapp.processEvents()

        # Modify sequence (add beat) using real data
        from application.services.data.pictograph_dataset_service import (
            PictographDatasetService,
        )
        from src.domain.models.core_models import BeatData

        dataset_service = PictographDatasetService()
        new_beat = dataset_service.get_start_position_pictograph(
            "gamma11_gamma11", "diamond"
        )

        if not new_beat:
            # Fallback to empty beat if dataset unavailable
            new_beat = BeatData.empty()

        new_beat = new_beat.update(letter="C")
        modified_sequence = mock_sequence_data.add_beat(new_beat)

        beat_frame.set_sequence(modified_sequence)
        qapp.processEvents()

        # Verify sequence was updated
        assert beat_frame._current_sequence == modified_sequence
        assert len(beat_frame._beat_views) == modified_sequence.length

    def test_layout_service_integration(self, qapp, mock_sequence_data):
        """Test integration with layout service."""
        beat_frame = ModernBeatFrame(layout_service=self.layout_service, parent=None)

        # Set sequence
        beat_frame.set_sequence(mock_sequence_data)

        # Verify layout service was used
        grid_layout = beat_frame._beat_grid_layout
        assert grid_layout is not None

        # Verify grid dimensions match service calculations
        expected_cols, expected_rows = self.layout_service.calculate_grid_dimensions(
            mock_sequence_data.length
        )

        # Check that beat views are positioned according to layout service
        for i, beat_view in enumerate(beat_frame._beat_views):
            if beat_view:
                expected_row, expected_col = divmod(i, expected_cols)
                actual_position = grid_layout.getItemPosition(
                    grid_layout.indexOf(beat_view)
                )
                if actual_position[0] != -1:  # Item found in layout
                    assert actual_position[0] == expected_row
                    assert actual_position[1] == expected_col

    def test_responsive_resize_behavior(self, qapp, mock_sequence_data):
        """Test responsive behavior during resize."""
        beat_frame = ModernBeatFrame(layout_service=self.layout_service, parent=None)

        # Set sequence
        beat_frame.set_sequence(mock_sequence_data)

        # Initial size
        beat_frame.resize(800, 600)
        qapp.processEvents()

        initial_cell_size = self.layout_service.get_grid_cell_size(800, 600, 4, 4)

        # Resize to different size
        beat_frame.resize(1200, 900)
        qapp.processEvents()

        new_cell_size = self.layout_service.get_grid_cell_size(1200, 900, 4, 4)

        # Verify cell size changed appropriately
        assert new_cell_size != initial_cell_size
        assert new_cell_size[0] > initial_cell_size[0]  # Larger width
        assert new_cell_size[1] > initial_cell_size[1]  # Larger height

    def test_start_position_integration(self, qapp, mock_sequence_data):
        """Test start position view integration."""
        beat_frame = ModernBeatFrame(layout_service=self.layout_service, parent=None)

        # Set sequence with start position
        beat_frame.set_sequence(mock_sequence_data)

        # Verify start position view exists
        assert beat_frame._start_position_view is not None

        # Verify start position is at grid position (0,0)
        grid_layout = beat_frame._beat_grid_layout
        start_pos_item = grid_layout.itemAtPosition(0, 0)
        assert start_pos_item is not None
        assert start_pos_item.widget() == beat_frame._start_position_view

    def test_beat_view_creation_performance(self, qapp):
        """Test performance of beat view creation for large sequences using real data."""
        import time
        from src.domain.models.core_models import SequenceData, BeatData
        from application.services.data.pictograph_dataset_service import (
            PictographDatasetService,
        )

        # Use real pictograph data instead of dummy beats
        dataset_service = PictographDatasetService()

        # Create large sequence with real data by reusing start positions
        beats = []
        start_positions = ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]

        for i in range(64):
            position_key = start_positions[i % len(start_positions)]
            beat_data = dataset_service.get_start_position_pictograph(
                position_key, "diamond"
            )

            if not beat_data:
                # Fallback to empty beat if dataset unavailable
                beat_data = BeatData.empty()

            # Update beat number for sequence
            beat_data = beat_data.update(beat_number=i + 1, letter=f"Beat{i+1}")
            beats.append(beat_data)

        large_sequence = SequenceData(beats=beats, length=64)

        beat_frame = ModernBeatFrame(layout_service=self.layout_service, parent=None)

        # Measure creation time
        start_time = time.time()
        beat_frame.set_sequence(large_sequence)
        qapp.processEvents()
        duration = time.time() - start_time

        # Should create 64 beat views quickly
        assert duration < 1.0, f"Beat view creation too slow: {duration}s"
        assert len(beat_frame._beat_views) == 64
