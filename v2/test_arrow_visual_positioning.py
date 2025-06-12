#!/usr/bin/env python3
"""
Test script to debug arrow visual positioning without GUI.
"""

import sys
from pathlib import Path

# Add the v2 src directory to path
v2_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(v2_src_path))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from src.presentation.components.pictograph_component import PictographScene
from src.domain.models.core_models import BeatData, MotionData, MotionType, RotationDirection, Location
from src.application.services.pictograph_data_service import PictographDataService


def test_arrow_visual_positioning():
    """Test arrow visual positioning without showing GUI."""
    print("Testing Arrow Visual Positioning")
    print("=" * 40)
    
    # Create QApplication (required for Qt graphics)
    app = QApplication([])
    
    # Create scene
    scene = PictographScene()
    
    # Get test data
    data_service = PictographDataService()
    test_pictographs = data_service.get_test_pictographs()
    pictograph_data = test_pictographs[0]  # Letter A
    
    # Convert to BeatData
    blue_motion_data = pictograph_data["blue_motion"]
    red_motion_data = pictograph_data["red_motion"]
    
    blue_motion = MotionData(
        motion_type=MotionType(blue_motion_data["motion_type"]),
        prop_rot_dir=RotationDirection(blue_motion_data["prop_rot_dir"]),
        start_loc=Location(blue_motion_data["start_loc"]),
        end_loc=Location(blue_motion_data["end_loc"]),
        turns=blue_motion_data.get("turns", 1.0),
    )
    
    red_motion = MotionData(
        motion_type=MotionType(red_motion_data["motion_type"]),
        prop_rot_dir=RotationDirection(red_motion_data["prop_rot_dir"]),
        start_loc=Location(red_motion_data["start_loc"]),
        end_loc=Location(red_motion_data["end_loc"]),
        turns=red_motion_data.get("turns", 1.0),
    )
    
    beat_data = BeatData(
        letter=pictograph_data["letter"],
        blue_motion=blue_motion,
        red_motion=red_motion,
    )
    
    print(f"Testing Pictograph {beat_data.letter}")
    print(f"Blue Motion: {blue_motion.motion_type.value} {blue_motion.start_loc.value}→{blue_motion.end_loc.value} {blue_motion.prop_rot_dir.value}")
    print(f"Red Motion: {red_motion.motion_type.value} {red_motion.start_loc.value}→{red_motion.end_loc.value} {red_motion.prop_rot_dir.value}")
    print()
    
    # Update scene with beat data (this will trigger arrow rendering and debug output)
    scene.update_beat(beat_data)
    
    print("\nTest completed!")
    
    # Don't show GUI, just exit
    app.quit()


if __name__ == "__main__":
    test_arrow_visual_positioning()
