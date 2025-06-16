#!/usr/bin/env python3
"""
Debug script to test Modern special placement service implementation.

This script will:
1. Test loading of special placement JSON configuration data
2. Verify orientation key generation logic
3. Test special adjustment calculation for sample arrows
4. Compare with expected Legacy behavior
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))


def debug_special_placement_service():
    """Debug Modern special placement service implementation."""
    print("🔍 DEBUGGING Modern SPECIAL PLACEMENT SERVICE")
    print("=" * 60)

    try:
        # Import Modern special placement service
        from application.services.positioning.special_placement_service import (
            SpecialPlacementService,
        )

        # Initialize service
        special_service = SpecialPlacementService()

        print("✅ Special placement service initialized successfully")

        # Check if special placements were loaded
        print(f"\n📊 SPECIAL PLACEMENT DATA LOADED")
        print("-" * 40)

        for grid_mode, mode_data in special_service.special_placements.items():
            print(f"Grid Mode: {grid_mode}")
            for ori_key, ori_data in mode_data.items():
                letter_count = len(ori_data)
                print(f"  {ori_key}: {letter_count} letters")

                # Show sample letters for first orientation key
                if ori_key == "from_layer1" and letter_count > 0:
                    sample_letters = list(ori_data.keys())[:5]
                    print(f"    Sample letters: {sample_letters}")

                    # Show sample data for first letter
                    if sample_letters:
                        first_letter = sample_letters[0]
                        letter_data = ori_data[first_letter]
                        print(
                            f"    {first_letter} data keys: {list(letter_data.keys())}"
                        )

                        # Show sample turn data
                        if letter_data:
                            first_turn_key = list(letter_data.keys())[0]
                            turn_data = letter_data[first_turn_key]
                            print(
                                f"    {first_turn_key} motion types: {list(turn_data.keys())}"
                            )

        # Test special adjustment lookup
        print(f"\n🎯 TESTING SPECIAL ADJUSTMENT LOOKUP")
        print("-" * 40)

        # Create mock arrow and pictograph data for testing
        from domain.models.core_models import MotionData, MotionType, Location
        from domain.models.pictograph_models import ArrowData, PictographData

        # Test with letter "A" which should have special placement data
        from domain.models.core_models import RotationDirection

        mock_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
            turns=1.0,
        )

        mock_arrow = ArrowData(motion_data=mock_motion)

        # Create mock pictograph data with blue and red motions for turns tuple
        class MockPictographData:
            def __init__(self, letter, blue_turns=0, red_turns=1.5):
                self.letter = letter
                self.grid_mode = "diamond"

                # Mock motion objects with turns
                class MockMotion:
                    def __init__(self, turns):
                        self.turns = turns

                self.blue_motion = MockMotion(blue_turns)
                self.red_motion = MockMotion(red_turns)

        mock_pictograph = MockPictographData("A", blue_turns=0, red_turns=1.5)

        # Test special adjustment lookup
        adjustment = special_service.get_special_adjustment(mock_arrow, mock_pictograph)

        print(f"Test case: Letter A, turns (0, 1.5), motion type PRO")
        print(f"Special adjustment result: {adjustment}")

        if adjustment:
            print(f"✅ Special adjustment found: ({adjustment.x()}, {adjustment.y()})")
        else:
            print("❌ No special adjustment found")

        # Test orientation key generation
        ori_key = special_service._generate_orientation_key(
            mock_motion, mock_pictograph
        )
        print(f"Generated orientation key: {ori_key}")

        # Test turns tuple generation
        turns_tuple = special_service._generate_turns_tuple(mock_pictograph)
        print(f"Generated turns tuple: {turns_tuple}")

        # Test with different letters and configurations
        test_cases = [
            ("A", 0, 1.5, MotionType.PRO),
            ("A", 0, 1.5, MotionType.ANTI),
            ("V", 1, 0.5, MotionType.PRO),
            ("V", 1, 0.5, MotionType.ANTI),
        ]

        print(f"\n🧪 TESTING MULTIPLE CONFIGURATIONS")
        print("-" * 40)

        for letter, blue_turns, red_turns, motion_type in test_cases:
            test_motion = MotionData(
                motion_type=motion_type,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.EAST,
                turns=1.0,
            )

            test_arrow = ArrowData(motion_data=test_motion)
            test_pictograph = MockPictographData(letter, blue_turns, red_turns)

            adjustment = special_service.get_special_adjustment(
                test_arrow, test_pictograph
            )
            turns_tuple = special_service._generate_turns_tuple(test_pictograph)

            print(
                f"Letter {letter}, turns {turns_tuple}, {motion_type.value}: {adjustment}"
            )

        print(f"\n✅ Special placement service debugging complete!")

    except Exception as e:
        print(f"❌ Error during debugging: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    debug_special_placement_service()
