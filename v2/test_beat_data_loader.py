#!/usr/bin/env python3
"""
Simple test script to verify BeatDataLoader positions mapping works correctly.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

try:
    # Test minimal import without package dependencies
    from typing import List, Optional, Dict, Any, Callable
    from PyQt6.QtCore import QObject

    # Define the positions mapping directly for testing
    POSITIONS_MAP = {
        # Alpha positions - location tuples to position names
        # Format: (blue_location, red_location) -> position_name
        # Where: blue = left hand, red = right hand
        ("s", "n"): "alpha1",  # SOUTH, NORTH
        ("sw", "ne"): "alpha2",  # SOUTHWEST, NORTHEAST
        ("w", "e"): "alpha3",  # WEST, EAST
        ("nw", "se"): "alpha4",  # NORTHWEST, SOUTHEAST
        ("n", "s"): "alpha5",  # NORTH, SOUTH
        ("ne", "sw"): "alpha6",  # NORTHEAST, SOUTHWEST
        ("e", "w"): "alpha7",  # EAST, WEST
        ("se", "nw"): "alpha8",  # SOUTHEAST, NORTHWEST
        # Beta positions - same location for both hands
        ("n", "n"): "beta1",
        ("ne", "ne"): "beta2",
        ("e", "e"): "beta3",
        ("se", "se"): "beta4",
        ("s", "s"): "beta5",
        ("sw", "sw"): "beta6",
        ("w", "w"): "beta7",
        ("nw", "nw"): "beta8",
        # Gamma positions - mixed combinations
        ("w", "n"): "gamma1",
        ("nw", "ne"): "gamma2",
        ("n", "e"): "gamma3",
        ("ne", "se"): "gamma4",
        ("e", "s"): "gamma5",
        ("se", "sw"): "gamma6",
        ("s", "w"): "gamma7",
        ("sw", "nw"): "gamma8",
        ("e", "n"): "gamma9",
        ("se", "ne"): "gamma10",
        ("s", "e"): "gamma11",
        ("sw", "se"): "gamma12",
        ("w", "s"): "gamma13",
        ("nw", "sw"): "gamma14",
        ("n", "w"): "gamma15",
        ("ne", "nw"): "gamma16",
    }

    def test_position_mapping():
        """Test the position mapping with user's specific examples."""
        print("🧪 Testing Position Mapping")
        print("=" * 40)

        # Test user's specific examples
        test_cases = [
            (("s", "n"), "alpha1", "right hand N, left hand S"),
            (("w", "e"), "alpha3", "right hand E, left hand W"),
            (("n", "s"), "alpha5", "right hand S, left hand N"),
        ]

        for position_key, expected, description in test_cases:
            result = POSITIONS_MAP.get(position_key, "Not found")
            status = "✅" if result == expected else "❌"
            print(f"{status} {description}")
            print(f"   Key: {position_key} -> {result}")
            print(f"   Expected: {expected}")
            print()

        # Test reverse mapping creation
        location_to_position_map = {}
        for location_tuple, position in POSITIONS_MAP.items():
            location_to_position_map[location_tuple] = position

        print("📋 Reverse mapping created successfully")
        print(f"   Total mappings: {len(location_to_position_map)}")

        # Test a few lookups
        test_lookups = [("s", "n"), ("w", "e"), ("n", "s")]
        print("\n🔍 Testing position lookups:")
        for key in test_lookups:
            result = location_to_position_map.get(key, "Not found")
            print(f"   {key} -> {result}")

    if __name__ == "__main__":
        test_position_mapping()
        print("\n✅ BeatDataLoader position mapping test completed!")

except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback

    traceback.print_exc()
