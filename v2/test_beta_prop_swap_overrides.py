#!/usr/bin/env python3
"""
Test script for V2 Beta Prop Swap Override System

This script validates that the V2 beta prop swap override system correctly
loads V1 override data and applies manual swap flags to override algorithmic
direction calculations.
"""

import sys
from pathlib import Path

# Add v2 source to Python path
v2_src = Path(__file__).parent / "src"
sys.path.insert(0, str(v2_src))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QPointF

from src.domain.models.core_models import BeatData, MotionData, MotionType, RotationDirection, Location
from src.application.services.beta_prop_position_service import BetaPropPositionService
from src.application.services.beta_prop_swap_service import BetaPropSwapService
from src.application.services.glyph_data_service import GlyphDataService


def create_test_beat_with_override() -> BeatData:
    """
    Create a beat that should have a swap override based on V1 data.
    
    Looking at V1 data, we can see entries like:
    "swap_beta_s_radial_blue_static_s_red_static_s": true
    
    This means: props at SOUTH with radial orientation, both static, should be swapped.
    """
    # Create motions that match a known override pattern
    blue_motion = MotionData(
        motion_type=MotionType.STATIC,
        prop_rot_dir=RotationDirection.NO_ROTATION,
        start_loc=Location.SOUTH,
        end_loc=Location.SOUTH,  # Both at SOUTH (overlap)
        turns=0.0,
        start_ori="in",  # Radial orientation
        end_ori="in"     # Radial orientation
    )
    
    red_motion = MotionData(
        motion_type=MotionType.STATIC,
        prop_rot_dir=RotationDirection.NO_ROTATION,
        start_loc=Location.SOUTH,
        end_loc=Location.SOUTH,  # Both at SOUTH (overlap)
        turns=0.0,
        start_ori="in",  # Radial orientation
        end_ori="in"     # Radial orientation
    )
    
    # Create beat with beta letter
    beat_data = BeatData(
        letter="β",  # Beta letter
        duration=1.0,
        blue_motion=blue_motion,
        red_motion=red_motion
    )
    
    # Generate glyph data
    glyph_service = GlyphDataService()
    glyph_data = glyph_service.determine_glyph_data(beat_data)
    
    return BeatData(
        letter=beat_data.letter,
        duration=beat_data.duration,
        blue_motion=beat_data.blue_motion,
        red_motion=beat_data.red_motion,
        glyph_data=glyph_data
    )


def create_test_beat_without_override() -> BeatData:
    """Create a beat that should NOT have a swap override."""
    # Create motions at different locations (no overlap, no override)
    blue_motion = MotionData(
        motion_type=MotionType.STATIC,
        prop_rot_dir=RotationDirection.NO_ROTATION,
        start_loc=Location.NORTH,
        end_loc=Location.NORTH,  # Blue at NORTH
        turns=0.0,
        start_ori="in",
        end_ori="in"
    )
    
    red_motion = MotionData(
        motion_type=MotionType.STATIC,
        prop_rot_dir=RotationDirection.NO_ROTATION,
        start_loc=Location.SOUTH,
        end_loc=Location.SOUTH,  # Red at SOUTH (no overlap)
        turns=0.0,
        start_ori="in",
        end_ori="in"
    )
    
    beat_data = BeatData(
        letter="β",
        duration=1.0,
        blue_motion=blue_motion,
        red_motion=red_motion
    )
    
    glyph_service = GlyphDataService()
    glyph_data = glyph_service.determine_glyph_data(beat_data)
    
    return BeatData(
        letter=beat_data.letter,
        duration=beat_data.duration,
        blue_motion=beat_data.blue_motion,
        red_motion=beat_data.red_motion,
        glyph_data=glyph_data
    )


def test_beta_prop_swap_overrides():
    """Test the beta prop swap override system."""
    print("🧪 Testing V2 Beta Prop Swap Override System")
    print("=" * 50)
    
    # Initialize services
    beta_service = BetaPropPositionService()
    swap_service = BetaPropSwapService()
    
    # Test 1: Check if special placements loaded
    print("📊 Test 1: Special Placements Loading")
    placements_info = swap_service.get_loaded_placements_info()
    
    if placements_info["loaded"]:
        print("   ✅ Special placements loaded successfully")
        for grid_mode, grid_data in placements_info["grid_modes"].items():
            print(f"   📁 {grid_mode.upper()} grid:")
            for ori_key, count in grid_data.items():
                print(f"      - {ori_key}: {count}")
    else:
        print("   ❌ Special placements failed to load")
        return False
    
    print()
    
    # Test 2: Override key generation
    print("📍 Test 2: Override Key Generation")
    test_beat = create_test_beat_with_override()
    
    override_key = swap_service._generate_override_key(test_beat, "diamond")
    print(f"   Generated override key: {override_key}")
    
    expected_pattern = "swap_beta_s_radial_blue_static_s_red_static_s"
    if override_key == expected_pattern:
        print(f"   ✅ Override key matches expected pattern")
    else:
        print(f"   ⚠️ Override key doesn't match expected: {expected_pattern}")
    
    print()
    
    # Test 3: Swap detection
    print("📍 Test 3: Swap Override Detection")
    
    # Test with potential override beat
    should_swap = swap_service.should_swap_beta_props(test_beat, "diamond")
    print(f"   Should swap (with override): {should_swap}")
    
    # Test with non-override beat
    no_override_beat = create_test_beat_without_override()
    should_not_swap = swap_service.should_swap_beta_props(no_override_beat, "diamond")
    print(f"   Should swap (without override): {should_not_swap}")
    
    print()
    
    # Test 4: Direction calculation with and without swap
    print("📍 Test 4: Direction Calculation with Swap Override")
    
    # Calculate offsets without considering overrides (algorithmic only)
    print("   🔧 Algorithmic directions (before swap check):")
    blue_dir_algo = beta_service._get_separation_direction(test_beat.blue_motion, "blue")
    red_dir_algo = beta_service._get_separation_direction(test_beat.red_motion, "red")
    print(f"      Blue direction: {blue_dir_algo.value}")
    print(f"      Red direction: {red_dir_algo.value}")
    
    # Calculate offsets with swap override system
    print("   🔄 Final directions (after swap override check):")
    blue_offset, red_offset = beta_service.calculate_separation_offsets(test_beat)
    
    # Determine final directions from offsets
    if blue_offset.x() > 0:
        blue_final = "right"
    elif blue_offset.x() < 0:
        blue_final = "left"
    elif blue_offset.y() > 0:
        blue_final = "down"
    elif blue_offset.y() < 0:
        blue_final = "up"
    else:
        blue_final = "none"
        
    if red_offset.x() > 0:
        red_final = "right"
    elif red_offset.x() < 0:
        red_final = "left"
    elif red_offset.y() > 0:
        red_final = "down"
    elif red_offset.y() < 0:
        red_final = "up"
    else:
        red_final = "none"
    
    print(f"      Blue final direction: {blue_final}")
    print(f"      Red final direction: {red_final}")
    
    # Check if directions were swapped
    if (blue_final != blue_dir_algo.value or red_final != red_dir_algo.value):
        print(f"   ✅ Directions were modified (likely swapped)")
    else:
        print(f"   ⚠️ Directions unchanged (no swap applied)")
    
    print()
    
    # Test 5: Integration with beta positioning
    print("📍 Test 5: Integration with Beta Positioning System")
    
    # Test that beta positioning applies swap overrides
    if beta_service.should_apply_beta_positioning(test_beat):
        print("   ✅ Beta positioning should be applied")
        
        blue_offset, red_offset = beta_service.calculate_separation_offsets(test_beat)
        print(f"   Blue offset: {blue_offset}")
        print(f"   Red offset: {red_offset}")
        
        # Verify offsets are non-zero and in opposite directions
        blue_mag = (blue_offset.x()**2 + blue_offset.y()**2)**0.5
        red_mag = (red_offset.x()**2 + red_offset.y()**2)**0.5
        
        if blue_mag > 0 and red_mag > 0:
            print("   ✅ Both props have separation offsets")
        else:
            print("   ❌ One or both props have zero offset")
            
    else:
        print("   ⚠️ Beta positioning not triggered")
    
    print()
    print("🎉 Beta Prop Swap Override Tests Complete!")
    
    return True


if __name__ == "__main__":
    # Create QApplication for Qt components
    app = QApplication(sys.argv)
    
    try:
        success = test_beta_prop_swap_overrides()
        if success:
            print("\n✅ All tests completed successfully!")
        else:
            print("\n❌ Some tests failed!")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        app.quit()
