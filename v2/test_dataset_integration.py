#!/usr/bin/env python3
"""
Test script to verify v2 dataset integration accuracy.

This script validates that the v2 start position picker is using
the actual v1 dataset values for pixel-perfect accuracy.
"""

import sys
from pathlib import Path

# Add v2 source to Python path
v2_src = Path(__file__).parent / "src"
sys.path.insert(0, str(v2_src))

from src.application.services.pictograph_dataset_service import PictographDatasetService


def test_dataset_integration():
    """Test that dataset integration provides accurate v1 data."""
    print("🧪 Testing V2 Dataset Integration")
    print("=" * 50)

    # Initialize dataset service
    dataset_service = PictographDatasetService()

    # Get dataset info
    info = dataset_service.get_dataset_info()
    print(f"📊 Dataset Info:")
    print(f"   Diamond loaded: {info['diamond_loaded']}")
    print(f"   Box loaded: {info['box_loaded']}")
    print(f"   Diamond entries: {info['diamond_entries']}")
    print(f"   Box entries: {info['box_entries']}")
    print(f"   Total entries: {info['total_entries']}")
    print()

    # Test diamond start positions
    print("💎 Testing Diamond Start Positions:")
    diamond_positions = dataset_service.get_diamond_start_positions()

    for position_key in diamond_positions:
        beat_data = dataset_service.get_start_position_pictograph(
            position_key, "diamond"
        )
        if beat_data:
            print(f"   ✅ {position_key}:")
            print(f"      Letter: '{beat_data.letter}'")
            print(
                f"      Blue: {beat_data.blue_motion.start_loc.value} → {beat_data.blue_motion.end_loc.value}"
            )
            print(
                f"      Red: {beat_data.red_motion.start_loc.value} → {beat_data.red_motion.end_loc.value}"
            )
            print(f"      Blue Motion: {beat_data.blue_motion.motion_type.value}")
            print(f"      Red Motion: {beat_data.red_motion.motion_type.value}")
            if beat_data.glyph_data:
                print(
                    f"      VTG Mode: {beat_data.glyph_data.vtg_mode.value if beat_data.glyph_data.vtg_mode else 'None'}"
                )
                print(
                    f"      Elemental: {beat_data.glyph_data.elemental_type.value if beat_data.glyph_data.elemental_type else 'None'}"
                )
        else:
            print(f"   ❌ {position_key}: Not found")
        print()

    # Test box start positions
    print("📦 Testing Box Start Positions:")
    box_positions = dataset_service.get_box_start_positions()

    for position_key in box_positions:
        beat_data = dataset_service.get_start_position_pictograph(position_key, "box")
        if beat_data:
            print(f"   ✅ {position_key}:")
            print(f"      Letter: '{beat_data.letter}'")
            print(
                f"      Blue: {beat_data.blue_motion.start_loc.value} → {beat_data.blue_motion.end_loc.value}"
            )
            print(
                f"      Red: {beat_data.red_motion.start_loc.value} → {beat_data.red_motion.end_loc.value}"
            )
            print(f"      Blue Motion: {beat_data.blue_motion.motion_type.value}")
            print(f"      Red Motion: {beat_data.red_motion.motion_type.value}")
            if beat_data.glyph_data:
                print(
                    f"      VTG Mode: {beat_data.glyph_data.vtg_mode.value if beat_data.glyph_data.vtg_mode else 'None'}"
                )
                print(
                    f"      Elemental: {beat_data.glyph_data.elemental_type.value if beat_data.glyph_data.elemental_type else 'None'}"
                )
        else:
            print(f"   ❌ {position_key}: Not found")
        print()

    # Verify expected values match v1 dataset
    print("🔍 Verification Against Expected V1 Values:")

    expected_diamond = {
        "alpha1_alpha1": {
            "letter": "α",
            "blue_start": "s",
            "blue_end": "s",
            "red_start": "n",
            "red_end": "n",
        },
        "beta5_beta5": {
            "letter": "β",
            "blue_start": "s",
            "blue_end": "s",
            "red_start": "s",
            "red_end": "s",
        },
        "gamma11_gamma11": {
            "letter": "Γ",
            "blue_start": "s",
            "blue_end": "s",
            "red_start": "e",
            "red_end": "e",
        },
    }

    expected_box = {
        "alpha2_alpha2": {
            "letter": "α",
            "blue_start": "sw",
            "blue_end": "sw",
            "red_start": "ne",
            "red_end": "ne",
        },
        "beta4_beta4": {
            "letter": "β",
            "blue_start": "se",
            "blue_end": "se",
            "red_start": "se",
            "red_end": "se",
        },
        "gamma12_gamma12": {
            "letter": "Γ",
            "blue_start": "sw",
            "blue_end": "sw",
            "red_start": "se",
            "red_end": "se",
        },
    }

    all_correct = True

    # Check diamond positions
    for position_key, expected in expected_diamond.items():
        beat_data = dataset_service.get_start_position_pictograph(
            position_key, "diamond"
        )
        if beat_data:
            actual = {
                "letter": beat_data.letter,
                "blue_start": beat_data.blue_motion.start_loc.value,
                "blue_end": beat_data.blue_motion.end_loc.value,
                "red_start": beat_data.red_motion.start_loc.value,
                "red_end": beat_data.red_motion.end_loc.value,
            }

            if actual == expected:
                print(f"   ✅ {position_key}: CORRECT")
            else:
                print(f"   ❌ {position_key}: MISMATCH")
                print(f"      Expected: {expected}")
                print(f"      Actual: {actual}")
                all_correct = False
        else:
            print(f"   ❌ {position_key}: NOT FOUND")
            all_correct = False

    # Check box positions
    for position_key, expected in expected_box.items():
        beat_data = dataset_service.get_start_position_pictograph(position_key, "box")
        if beat_data:
            actual = {
                "letter": beat_data.letter,
                "blue_start": beat_data.blue_motion.start_loc.value,
                "blue_end": beat_data.blue_motion.end_loc.value,
                "red_start": beat_data.red_motion.start_loc.value,
                "red_end": beat_data.red_motion.end_loc.value,
            }

            if actual == expected:
                print(f"   ✅ {position_key}: CORRECT")
            else:
                print(f"   ❌ {position_key}: MISMATCH")
                print(f"      Expected: {expected}")
                print(f"      Actual: {actual}")
                all_correct = False
        else:
            print(f"   ❌ {position_key}: NOT FOUND")
            all_correct = False

    print()
    if all_correct:
        print("🎉 ALL TESTS PASSED! V2 dataset integration is pixel-perfect!")
    else:
        print("❌ Some tests failed. Dataset integration needs fixes.")

    return all_correct


if __name__ == "__main__":
    test_dataset_integration()
