# tests/main_widget/construct_tab/test_add_to_sequence_manager.py
import pytest
from unittest.mock import MagicMock, patch

from main_window.main_widget.construct_tab.add_to_sequence_manager.add_to_sequence_manager import AddToSequenceManager

def test_create_new_beat_basic_flow():
    # Create full mock environment
    mock_json = MagicMock()
    mock_beat_frame = MagicMock()
    mock_pictograph = MagicMock()
    mock_beat_class = MagicMock()
    
    # CORRECTED PATCH PATH
    with patch(
        'main_window.main_widget.sequence_workbench.sequence_beat_frame.beat.Beat',
        new=mock_beat_class
    ):
        # Configure mocks
        mock_json.loader_saver.load_current_sequence.return_value = [
            {"existing": "beat1"},
            {"existing": "beat2", "is_placeholder": True},
            {"existing": "beat3"}
        ]
        
        mock_pictograph.managers.get.pictograph_data.return_value = {
            "start_pos": "alpha1",
            "end_pos": "beta2"
        }
        
        # Instantiate manager
        manager = AddToSequenceManager(
            json_manager=mock_json,
            beat_frame=mock_beat_frame,
            last_beat=None
        )
        
        # Execute
        result = manager.create_new_beat(mock_pictograph)
        
        # Verify
        mock_beat_class.assert_called_once_with(mock_beat_frame)
        assert manager.last_beat == mock_beat_class.return_value
        assert "duration" in mock_pictograph.managers.get.pictograph_data.return_value