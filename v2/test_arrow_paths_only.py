#!/usr/bin/env python3
"""
Test script to verify arrow path resolution and SVG file access without Qt.
"""

import sys
import os
sys.path.append('src')

from src.domain.models.core_models import MotionData, MotionType, Location, RotationDirection


def test_arrow_path_resolution():
    """Test arrow path resolution without creating Qt objects."""
    print("=== Testing Arrow Path Resolution ===")
    
    from src.presentation.components.pictograph.asset_utils import get_image_path
    
    # Test motion data
    test_motions = [
        MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.WEST,
            end_loc=Location.NORTH,
            turns=1.0,
            start_ori='in',
            end_ori='out'
        ),
        MotionData(
            motion_type=MotionType.STATIC,
            prop_rot_dir=RotationDirection.NO_ROTATION,
            start_loc=Location.SOUTH,
            end_loc=Location.SOUTH,
            turns=0.0,
            start_ori='in',
            end_ori='in'
        ),
        MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.EAST,
            end_loc=Location.SOUTH,
            turns=1.5,
            start_ori='in',
            end_ori='out'
        ),
        MotionData(
            motion_type=MotionType.DASH,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.WEST,
            turns=2.0,
            start_ori='in',
            end_ori='out'
        ),
    ]
    
    # Simulate the ArrowRenderer._get_arrow_svg_file logic
    for i, motion_data in enumerate(test_motions):
        print(f"Motion {i+1}: {motion_data.motion_type.value}")
        
        # Replicate the path logic from ArrowRenderer
        turns_str = f"{motion_data.turns:.1f}"
        
        if motion_data.motion_type == MotionType.STATIC:
            svg_path = get_image_path(f"arrows/static/from_radial/static_{turns_str}.svg")
        elif motion_data.motion_type == MotionType.PRO:
            svg_path = get_image_path(f"arrows/pro/from_radial/pro_{turns_str}.svg")
        elif motion_data.motion_type == MotionType.ANTI:
            svg_path = get_image_path(f"arrows/anti/from_radial/anti_{turns_str}.svg")
        elif motion_data.motion_type == MotionType.DASH:
            svg_path = get_image_path(f"arrows/dash/from_radial/dash_{turns_str}.svg")
        elif motion_data.motion_type == MotionType.FLOAT:
            svg_path = get_image_path("arrows/float.svg")
        else:
            svg_path = get_image_path(f"arrows/static/from_radial/static_{turns_str}.svg")
        
        print(f"  SVG path: {svg_path}")
        print(f"  File exists: {os.path.exists(svg_path)}")
        
        if os.path.exists(svg_path):
            try:
                with open(svg_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"  SVG content length: {len(content)} characters")
                print(f"  Contains <svg>: {'<svg' in content}")
            except Exception as e:
                print(f"  Error reading SVG: {e}")
        print()


def test_static_svg_issue():
    """Test the specific static SVG issue."""
    print("=== Testing Static SVG Issue ===")
    
    from src.presentation.components.pictograph.asset_utils import get_image_path
    
    # Check static_0.0.svg specifically
    static_path = get_image_path("arrows/static/from_radial/static_0.0.svg")
    print(f"Static 0.0 path: {static_path}")
    print(f"File exists: {os.path.exists(static_path)}")
    
    if os.path.exists(static_path):
        try:
            with open(static_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"Content length: {len(content)}")
            print(f"First 200 characters:")
            print(content[:200])
            
            # Check if it's an empty or malformed SVG
            if len(content.strip()) == 0:
                print("WARNING: Static SVG file is empty!")
            elif '<svg' not in content:
                print("WARNING: Static SVG file doesn't contain <svg> tag!")
            else:
                print("Static SVG appears to have valid content")
                
        except Exception as e:
            print(f"Error reading static SVG: {e}")


if __name__ == "__main__":
    print("Arrow Path Resolution Test (No Qt)")
    print("=" * 40)
    
    test_arrow_path_resolution()
    test_static_svg_issue()
    
    print("Test completed.")
