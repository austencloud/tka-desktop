#!/usr/bin/env python3
"""
Test script to verify start position view behavior when sequence is cleared.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modern'))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from src.presentation.components.workbench.workbench import Workbench
from src.application.services.injection.container import ModernServiceContainer
from src.domain.models.core_models import SequenceData, BeatData

def test_start_position_clear():
    """Test that start position view remains visible when sequence is cleared."""
    app = QApplication([])
    
    # Create container and services
    container = ModernServiceContainer()
    
    # Create workbench
    workbench = Workbench(
        layout_service=container.get_layout_service(),
        graph_service=container.get_graph_service(),
        workbench_service=container.get_workbench_service(),
        fullscreen_service=container.get_fullscreen_service(),
        deletion_service=container.get_deletion_service(),
        dictionary_service=container.get_dictionary_service()
    )
    
    # Set a test start position
    test_start_position = BeatData.empty()
    test_start_position.positioning.positions["blue"]["pos"] = "alpha1"
    test_start_position.positioning.positions["red"]["pos"] = "alpha3"
    
    # Set start position
    workbench.set_start_position(test_start_position)
    
    # Create a sequence with some beats
    test_sequence = SequenceData.empty()
    test_beat = BeatData.empty()
    test_beat.positioning.positions["blue"]["pos"] = "beta1"
    test_beat.positioning.positions["red"]["pos"] = "beta3"
    test_sequence.beats.append(test_beat)
    
    # Set sequence
    workbench.set_sequence(test_sequence)
    
    print("Initial state:")
    print(f"- Sequence length: {len(test_sequence.beats)}")
    print(f"- Start position set: {workbench.get_start_position() is not None}")
    
    # Check start position view visibility
    beat_frame = workbench._beat_frame_section._beat_frame
    start_pos_view = beat_frame._start_position_view
    print(f"- Start position view visible: {start_pos_view.isVisible()}")
    print(f"- Start position view position data: {start_pos_view.get_position_data() is not None}")
    
    # Clear the sequence
    empty_sequence = SequenceData.empty()
    workbench.set_sequence(empty_sequence)
    
    print("\nAfter clearing sequence:")
    print(f"- Sequence length: {len(empty_sequence.beats)}")
    print(f"- Start position set: {workbench.get_start_position() is not None}")
    print(f"- Start position view visible: {start_pos_view.isVisible()}")
    print(f"- Start position view position data: {start_pos_view.get_position_data() is not None}")
    
    # The start position view should STILL be visible, even with empty sequence
    # AND the start position data should still be preserved (like legacy)
    expected_visible = True
    expected_has_data = True  # Start position should persist across sequence clears
    
    if start_pos_view.isVisible() == expected_visible:
        print("✓ Start position view visibility is correct")
    else:
        print("✗ Start position view visibility is incorrect")
        
    if (start_pos_view.get_position_data() is not None) == expected_has_data:
        print("✓ Start position data persistence is correct")
    else:
        print("✗ Start position data persistence is incorrect")
        print("  Expected start position to persist when sequence is cleared (like legacy)")

if __name__ == "__main__":
    test_start_position_clear()
