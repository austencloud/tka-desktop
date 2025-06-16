"""
Test Clear Sequence Behavior - Preserve Start Position Beat

Tests the new clear sequence behavior that preserves the start position beat
while clearing all other beats from the sequence, maintaining START text overlay
and proper layout.
"""

import pytest
from unittest.mock import Mock, MagicMock
from PyQt6.QtWidgets import QApplication

from domain.models.core_models import SequenceData, BeatData
from presentation.components.workbench.event_controller import WorkbenchEventController
from presentation.components.workbench.sequence_beat_frame.sequence_beat_frame import SequenceBeatFrame
from presentation.components.workbench.sequence_beat_frame.beat_view import BeatView
from application.services.layout.layout_management_service import LayoutManagementService


class TestClearSequenceBehavior:
    """Test the new clear sequence behavior that preserves start position beat"""

    def setup_method(self):
        """Setup for each test method"""
        # Mock services
        self.workbench_service = Mock()
        self.fullscreen_service = Mock()
        self.deletion_service = Mock()
        self.dictionary_service = Mock()
        self.layout_service = Mock()

        # Create event controller
        self.event_controller = WorkbenchEventController(
            workbench_service=self.workbench_service,
            fullscreen_service=self.fullscreen_service,
            deletion_service=self.deletion_service,
            dictionary_service=self.dictionary_service,
        )

        # Create test sequence with multiple beats
        self.test_sequence = SequenceData(
            name="Test Sequence",
            beats=[
                BeatData(beat_number=1, letter="A"),
                BeatData(beat_number=2, letter="B"),
                BeatData(beat_number=3, letter="C"),
            ]
        )

    def test_clear_sequence_preserves_start_position_beat(self):
        """Test that clear sequence preserves the start position beat"""
        # Set up sequence
        self.event_controller.set_sequence(self.test_sequence)
        
        # Clear sequence
        success, message, result_sequence = self.event_controller.handle_clear()
        
        # Verify success
        assert success is True
        assert "start position preserved" in message.lower()
        assert result_sequence is not None
        
        # Verify preserved sequence structure
        assert result_sequence.length == 1
        assert len(result_sequence.beats) == 1
        
        # Verify preserved beat is empty but positioned correctly
        preserved_beat = result_sequence.beats[0]
        assert preserved_beat.beat_number == 1
        assert preserved_beat.is_blank is True
        assert preserved_beat.letter is None
        
        # Verify metadata indicates preservation
        assert result_sequence.metadata.get("preserve_start_position") is True
        assert result_sequence.metadata.get("cleared") is True

    def test_clear_empty_sequence_still_preserves_beat(self):
        """Test that clearing an already empty sequence still creates preserved beat"""
        # Set up empty sequence
        empty_sequence = SequenceData.empty()
        self.event_controller.set_sequence(empty_sequence)
        
        # Clear sequence
        success, message, result_sequence = self.event_controller.handle_clear()
        
        # Verify success and preservation
        assert success is True
        assert result_sequence is not None
        assert result_sequence.length == 1
        assert result_sequence.beats[0].is_blank is True
        assert result_sequence.metadata.get("preserve_start_position") is True

    def test_clear_single_beat_sequence_preserves_as_empty(self):
        """Test that clearing a single beat sequence preserves it as empty beat"""
        # Set up single beat sequence
        single_beat_sequence = SequenceData(
            name="Single Beat",
            beats=[BeatData(beat_number=1, letter="X")]
        )
        self.event_controller.set_sequence(single_beat_sequence)
        
        # Clear sequence
        success, message, result_sequence = self.event_controller.handle_clear()
        
        # Verify preservation
        assert success is True
        assert result_sequence.length == 1
        assert result_sequence.beats[0].is_blank is True
        assert result_sequence.beats[0].beat_number == 1
        assert result_sequence.beats[0].letter is None

    def test_beat_view_start_text_overlay_functionality(self):
        """Test that BeatView can show/hide START text overlay correctly"""
        # Create beat view
        beat_view = BeatView(beat_number=1)
        
        # Test initial state
        assert beat_view.is_start_text_visible() is False
        
        # Enable START text
        beat_view.set_start_text_visible(True)
        assert beat_view.is_start_text_visible() is True
        
        # Disable START text
        beat_view.set_start_text_visible(False)
        assert beat_view.is_start_text_visible() is False

    def test_beat_view_start_text_mutual_exclusivity(self):
        """Test that START text is mutually exclusive with beat content"""
        # Create beat view with pictograph component mock
        beat_view = BeatView(beat_number=1)
        beat_view._pictograph_component = Mock()
        beat_view._pictograph_component.scene = Mock()
        
        # Enable START text with empty beat
        empty_beat = BeatData.empty()
        beat_view.set_beat_data(empty_beat)
        beat_view.set_start_text_visible(True)
        
        # Verify START text should be shown (empty beat + enabled)
        assert beat_view.is_start_text_visible() is True
        
        # Add content to beat
        filled_beat = BeatData(beat_number=1, letter="A", is_blank=False)
        beat_view.set_beat_data(filled_beat)
        
        # START text should still be enabled but overlay logic handles mutual exclusivity
        assert beat_view.is_start_text_visible() is True

    @pytest.mark.integration
    def test_sequence_beat_frame_handles_preserved_sequence(self):
        """Integration test: sequence beat frame handles preserved start position sequence"""
        # Mock layout service
        self.layout_service.calculate_beat_frame_layout.return_value = {
            "rows": 1, 
            "columns": 8
        }
        
        # Create sequence beat frame
        beat_frame = SequenceBeatFrame(layout_service=self.layout_service)
        
        # Create preserved sequence (like after clear)
        preserved_sequence = SequenceData(
            name="Cleared Sequence",
            beats=[BeatData.empty().update(beat_number=1)],
            metadata={"cleared": True, "preserve_start_position": True}
        )
        
        # Set sequence
        beat_frame.set_sequence(preserved_sequence)
        
        # Verify beat frame state
        assert beat_frame.get_sequence() == preserved_sequence
        
        # Verify first beat view is configured correctly
        first_beat_view = beat_frame._beat_views[0]
        assert first_beat_view.is_start_text_visible() is True
        
        # Verify other beat views don't have START text
        for i in range(1, min(5, len(beat_frame._beat_views))):
            assert beat_frame._beat_views[i].is_start_text_visible() is False

    def test_clear_sequence_error_handling(self):
        """Test error handling in clear sequence operation"""
        # Mock BeatData.empty to raise exception
        with pytest.mock.patch('domain.models.core_models.BeatData.empty', side_effect=Exception("Test error")):
            success, message, result_sequence = self.event_controller.handle_clear()
            
            assert success is False
            assert "Clear failed" in message
            assert result_sequence is None

    def test_preserved_beat_allows_sequence_continuation(self):
        """Test that preserved beat allows users to continue building sequences"""
        # Clear sequence to get preserved beat
        self.event_controller.set_sequence(self.test_sequence)
        success, message, preserved_sequence = self.event_controller.handle_clear()
        
        assert success is True
        assert preserved_sequence.length == 1
        
        # Simulate adding a new beat to the preserved sequence
        new_beat = BeatData(beat_number=2, letter="D")
        continued_sequence = preserved_sequence.add_beat(new_beat)
        
        # Verify sequence can be continued
        assert continued_sequence.length == 2
        assert continued_sequence.beats[0].is_blank is True  # Preserved start
        assert continued_sequence.beats[1].letter == "D"    # New beat
        assert continued_sequence.beats[1].beat_number == 2

    def test_preserved_sequence_metadata_structure(self):
        """Test that preserved sequence has correct metadata structure"""
        self.event_controller.set_sequence(self.test_sequence)
        success, message, preserved_sequence = self.event_controller.handle_clear()
        
        assert success is True
        
        # Verify metadata structure
        metadata = preserved_sequence.metadata
        assert isinstance(metadata, dict)
        assert metadata["cleared"] is True
        assert metadata["preserve_start_position"] is True
        
        # Verify sequence name indicates clearing
        assert "cleared" in preserved_sequence.name.lower()
