#!/usr/bin/env python3
"""
Quick Functionality Verification Test

Tests the three implemented V1 functionality gaps in isolation.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from core.dependency_injection.di_container import SimpleContainer
from src.presentation.tabs.construct_tab_widget import ConstructTabWidget
from src.application.services.simple_layout_service import SimpleLayoutService
from src.core.interfaces.core_services import ILayoutService


def test_functionality():
    """Test the three critical functionalities"""
    
    print("🎯 Quick Functionality Verification Test")
    print("=" * 50)
    
    # Create container and services
    container = SimpleContainer()
    container.register_singleton(ILayoutService, SimpleLayoutService)
    
    # Create construct tab
    construct_tab = ConstructTabWidget(container)
    
    print("\n1️⃣ Testing START Text Overlay...")
    # Check if start position view has START text
    beat_frame = construct_tab.workbench._beat_frame
    if beat_frame and beat_frame._start_position_view:
        start_view = beat_frame._start_position_view
        if hasattr(start_view, '_start_text_overlay'):
            print("   ✅ START text overlay component exists")
        else:
            print("   ❌ START text overlay component missing")
    else:
        print("   ❌ Start position view not found")
    
    print("\n2️⃣ Testing Clear Sequence Functionality...")
    # Test clear sequence preserves start position
    workbench = construct_tab.workbench
    
    # Set a start position first
    from src.domain.models.core_models import BeatData, MotionData, MotionType, RotationDirection, Location
    
    start_position = BeatData(
        beat_number=1,
        letter="α",
        duration=1.0,
        blue_motion=MotionData(
            motion_type=MotionType.STATIC,
            prop_rot_dir=RotationDirection.NO_ROTATION,
            start_loc=Location.SOUTH,
            end_loc=Location.SOUTH,
            turns=0.0,
            start_ori="in",
            end_ori="in"
        ),
        red_motion=MotionData(
            motion_type=MotionType.STATIC,
            prop_rot_dir=RotationDirection.NO_ROTATION,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            turns=0.0,
            start_ori="in",
            end_ori="in"
        )
    )
    
    workbench.set_start_position(start_position)
    print(f"   Start position set: {workbench.get_start_position().letter}")
    
    # Clear sequence
    workbench._handle_clear()
    
    # Check if start position is preserved
    start_after_clear = workbench.get_start_position()
    sequence_after_clear = workbench.get_sequence()
    
    if start_after_clear and start_after_clear.letter == "α":
        print("   ✅ Start position preserved after clear")
    else:
        print("   ❌ Start position not preserved after clear")
        
    if not sequence_after_clear or len(sequence_after_clear.beats) == 0:
        print("   ✅ Sequence beats cleared")
    else:
        print("   ❌ Sequence beats not cleared")
    
    print("\n3️⃣ Testing Start Position Integration...")
    # Test option picker population
    option_picker = construct_tab.option_picker
    
    # Simulate start position selection
    construct_tab._handle_start_position_selected("alpha1_alpha1")
    
    # Check if option picker has been populated
    if hasattr(option_picker, '_beat_options'):
        beat_options = option_picker._beat_options
        if len(beat_options) > 0:
            print(f"   ✅ Option picker populated with {len(beat_options)} combinations")
        else:
            print("   ❌ Option picker not populated")
    else:
        print("   ❌ Option picker beat options not found")
    
    print("\n🎯 Functionality Verification Complete!")
    print("=" * 50)
    
    return True


def main():
    """Run the functionality verification"""
    app = QApplication(sys.argv)
    
    # Run test after app is initialized
    QTimer.singleShot(100, test_functionality)
    QTimer.singleShot(2000, app.quit)  # Exit after 2 seconds
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
