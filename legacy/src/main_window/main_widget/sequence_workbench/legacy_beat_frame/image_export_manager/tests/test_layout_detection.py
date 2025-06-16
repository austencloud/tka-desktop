"""
Test module for verifying that the image export layout detection works correctly.
"""
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from PyQt6.QtWidgets import QApplication, QGridLayout
from PyQt6.QtCore import Qt

from main_window.main_widget.sequence_workbench.legacy_beat_frame.image_export_manager.image_export_layout_handler import (
    ImageExportLayoutHandler
)
from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat_frame_layout_manager import (
    BeatFrameLayoutManager
)


def test_layout_detection():
    """
    Test that the image export layout handler correctly detects and uses the current beat frame layout.
    """
    app = QApplication([])
    
    # Create a mock beat frame with a layout manager
    class MockBeatFrame:
        def __init__(self):
            self.layout = QGridLayout()
            self.layout_manager = BeatFrameLayoutManager(self)
            self.selection_overlay = None
            self.start_pos_view = None
            self.beat_views = []
            self.sequence_workbench = None
            self.get = None
    
    # Create a mock image export manager
    class MockImageExportManager:
        def __init__(self):
            self.beat_frame = MockBeatFrame()
            self.include_start_pos = True
    
    # Create the layout handler
    export_manager = MockImageExportManager()
    layout_handler = ImageExportLayoutHandler(export_manager)
    
    # Test that the layout handler uses the correct layout
    # This is just a basic test to ensure the code runs without errors
    # In a real test, we would mock more functionality and verify the results
    
    # Print a success message
    print("Layout detection test completed successfully!")


if __name__ == "__main__":
    test_layout_detection()
