#!/usr/bin/env python3
"""
Test script for V2 Beta Prop Positioning System

This script validates that the V2 beta prop position handler correctly
detects overlapping props and applies appropriate separation offsets
to maintain visual clarity.
"""

import sys
from pathlib import Path

# Add v2 source to Python path
v2_src = Path(__file__).parent / "src"
sys.path.insert(0, str(v2_src))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QPointF

from src.domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
)
from src.application.services.beta_prop_position_service import BetaPropPositionService
from src.application.services.glyph_data_service import GlyphDataService


def create_overlapping_props_beat() -> BeatData:
    """Create a beat with overlapping props (both at same location)."""
    # Create motions that end at the same location (overlap scenario)
    blue_motion = MotionData(
        motion_type=MotionType.STATIC,
        prop_rot_dir=RotationDirection.NO_ROTATION,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,  # Both props end at SOUTH
        turns=0.0,
        start_ori="in",
        end_ori="in",
    )

    red_motion = MotionData(
        motion_type=MotionType.STATIC,
        prop_rot_dir=RotationDirection.NO_ROTATION,
        start_loc=Location.EAST,
        end_loc=Location.SOUTH,  # Both props end at SOUTH (overlap!)
        turns=0.0,
        start_ori="in",
        end_ori="in",
    )

    # Create beat with beta letter to trigger beta positioning
    beat_data = BeatData(
        letter="β",  # Beta letter should trigger beta positioning
        duration=1.0,
        blue_motion=blue_motion,
        red_motion=red_motion,
    )

    # Generate glyph data
    glyph_service = GlyphDataService()
    glyph_data = glyph_service.determine_glyph_data(beat_data)

    return BeatData(
        letter=beat_data.letter,
        duration=beat_data.duration,
        blue_motion=beat_data.blue_motion,
        red_motion=beat_data.red_motion,
        glyph_data=glyph_data,
    )


def create_non_overlapping_props_beat() -> BeatData:
    """Create a beat with non-overlapping props (different locations)."""
    blue_motion = MotionData(
        motion_type=MotionType.STATIC,
        prop_rot_dir=RotationDirection.NO_ROTATION,
        start_loc=Location.NORTH,
        end_loc=Location.NORTH,  # Blue at NORTH
        turns=0.0,
        start_ori="in",
        end_ori="in",
    )

    red_motion = MotionData(
        motion_type=MotionType.STATIC,
        prop_rot_dir=RotationDirection.NO_ROTATION,
        start_loc=Location.SOUTH,
        end_loc=Location.SOUTH,  # Red at SOUTH (no overlap)
        turns=0.0,
        start_ori="in",
        end_ori="in",
    )

    beat_data = BeatData(
        letter="β",  # Beta letter
        duration=1.0,
        blue_motion=blue_motion,
        red_motion=red_motion,
    )

    glyph_service = GlyphDataService()
    glyph_data = glyph_service.determine_glyph_data(beat_data)

    return BeatData(
        letter=beat_data.letter,
        duration=beat_data.duration,
        blue_motion=beat_data.blue_motion,
        red_motion=beat_data.red_motion,
        glyph_data=glyph_data,
    )


def test_beta_prop_positioning():
    """Test the beta prop positioning service."""
    print("🧪 Testing V2 Beta Prop Positioning System")
    print("=" * 50)

    # Initialize service
    beta_service = BetaPropPositionService()

    # Test 1: Overlapping props with beta letter
    print("📍 Test 1: Overlapping Props with Beta Letter")
    overlapping_beat = create_overlapping_props_beat()

    should_apply = beta_service.should_apply_beta_positioning(overlapping_beat)
    print(f"   Should apply beta positioning: {should_apply}")

    if should_apply:
        blue_offset, red_offset = beta_service.calculate_separation_offsets(
            overlapping_beat
        )
        print(f"   Blue offset: {blue_offset}")
        print(f"   Red offset: {red_offset}")
        print(f"   ✅ Separation offsets calculated successfully")
    else:
        print(f"   ⚠️ Beta positioning not triggered")

    print()

    # Test 2: Non-overlapping props with beta letter
    print("📍 Test 2: Non-Overlapping Props with Beta Letter")
    non_overlapping_beat = create_non_overlapping_props_beat()

    should_apply = beta_service.should_apply_beta_positioning(non_overlapping_beat)
    print(f"   Should apply beta positioning: {should_apply}")

    if should_apply:
        print(f"   ❌ Beta positioning incorrectly triggered for non-overlapping props")
    else:
        print(f"   ✅ Beta positioning correctly skipped for non-overlapping props")

    print()

    # Test 3: Overlapping props with non-beta letter
    print("📍 Test 3: Overlapping Props with Non-Beta Letter")
    # Create new beat with alpha letter
    alpha_beat = BeatData(
        letter="α",  # Alpha letter (non-beta)
        duration=1.0,
        blue_motion=overlapping_beat.blue_motion,
        red_motion=overlapping_beat.red_motion,
        glyph_data=overlapping_beat.glyph_data,
    )

    should_apply = beta_service.should_apply_beta_positioning(alpha_beat)
    print(f"   Should apply beta positioning: {should_apply}")

    if should_apply:
        print(f"   ❌ Beta positioning incorrectly triggered for non-beta letter")
    else:
        print(f"   ✅ Beta positioning correctly skipped for non-beta letter")

    print()

    # Test 4: Offset calculation accuracy
    print("📍 Test 4: Offset Calculation Accuracy")
    # Use original overlapping beat with beta letter

    blue_offset, red_offset = beta_service.calculate_separation_offsets(
        overlapping_beat
    )

    # Verify offsets are non-zero and opposite
    blue_magnitude = (blue_offset.x() ** 2 + blue_offset.y() ** 2) ** 0.5
    red_magnitude = (red_offset.x() ** 2 + red_offset.y() ** 2) ** 0.5

    print(f"   Blue offset magnitude: {blue_magnitude:.2f}px")
    print(f"   Red offset magnitude: {red_magnitude:.2f}px")

    if blue_magnitude > 0 and red_magnitude > 0:
        print(f"   ✅ Both offsets have non-zero magnitude")
    else:
        print(f"   ❌ One or both offsets are zero")

    # Check if offsets are in opposite directions (for separation)
    dot_product = blue_offset.x() * red_offset.x() + blue_offset.y() * red_offset.y()
    if dot_product <= 0:
        print(f"   ✅ Offsets are in opposite/perpendicular directions (separation)")
    else:
        print(f"   ⚠️ Offsets are in same direction (may not separate properly)")

    print()

    # Test 5: Direction calculation
    print("📍 Test 5: Direction Calculation Logic")

    # Test different locations and colors
    test_cases = [
        (Location.NORTH, "blue", "Should move DOWN"),
        (Location.NORTH, "red", "Should move UP"),
        (Location.SOUTH, "blue", "Should move DOWN"),
        (Location.SOUTH, "red", "Should move UP"),
        (Location.EAST, "blue", "Should move LEFT"),
        (Location.EAST, "red", "Should move RIGHT"),
        (Location.WEST, "blue", "Should move LEFT"),
        (Location.WEST, "red", "Should move RIGHT"),
    ]

    for location, color, expected in test_cases:
        # Create test motion
        test_motion = MotionData(
            motion_type=MotionType.STATIC,
            prop_rot_dir=RotationDirection.NO_ROTATION,
            start_loc=location,
            end_loc=location,
            turns=0.0,
            start_ori="in",
            end_ori="in",
        )

        direction = beta_service._get_separation_direction(test_motion, color)
        print(f"   {location.value} + {color} → {direction.value} ({expected})")

    print()
    print("🎉 Beta Prop Positioning Tests Complete!")


if __name__ == "__main__":
    # Create QApplication for Qt components
    app = QApplication(sys.argv)

    try:
        test_beta_prop_positioning()
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        app.quit()
