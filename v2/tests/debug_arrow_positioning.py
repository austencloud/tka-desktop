#!/usr/bin/env python3
"""
Debug script to test Modern arrow positioning with special placement logic.

This script will:
1. Test Modern's arrow positioning pipeline with special placement integration
2. Verify that special adjustments are being applied for specific letters
3. Compare default vs special placement adjustments
4. Validate that the special placement service is working in the actual positioning pipeline
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "v2", "src"))


def debug_arrow_positioning():
    """Debug Modern arrow positioning with special placement logic."""
    print("🔍 DEBUGGING Modern ARROW POSITIONING WITH SPECIAL PLACEMENT")
    print("=" * 70)

    try:
        # Import Modern services
        from application.services.positioning.arrow_management_service import (
            ArrowManagementService,
        )
        from application.services.positioning.special_placement_service import (
            SpecialPlacementService,
        )
        from domain.models.core_models import (
            MotionData,
            MotionType,
            Location,
            RotationDirection,
        )
        from domain.models.pictograph_models import ArrowData, PictographData

        # Initialize services
        arrow_service = ArrowManagementService()
        special_service = SpecialPlacementService()

        print("✅ Services initialized successfully")

        # Test special placement service directly
        print(f"\n🎯 TESTING SPECIAL PLACEMENT SERVICE DIRECTLY")
        print("-" * 50)

        # Create test data for letter V which should have special placements
        test_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
            turns=1.0,
        )

        test_arrow = ArrowData(motion_data=test_motion)

        # Create mock pictograph data with turns that should have special placement
        class MockPictographData:
            def __init__(self, letter, blue_turns=1, red_turns=0.5):
                self.letter = letter
                self.grid_mode = "diamond"

                class MockMotion:
                    def __init__(self, turns):
                        self.turns = turns

                self.blue_motion = MockMotion(blue_turns)
                self.red_motion = MockMotion(red_turns)

        test_pictograph = MockPictographData("V", blue_turns=1, red_turns=0.5)

        # Test special adjustment lookup
        special_adjustment = special_service.get_special_adjustment(
            test_arrow, test_pictograph
        )
        print(f"Letter V, turns (1, 0.5), PRO motion:")
        print(f"  Special adjustment: {special_adjustment}")

        if special_adjustment:
            print(
                f"  ✅ Special adjustment found: ({special_adjustment.x()}, {special_adjustment.y()})"
            )
        else:
            print(f"  ❌ No special adjustment found")

        # Test with different motion type
        test_motion_anti = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
            turns=1.0,
        )

        test_arrow_anti = ArrowData(motion_data=test_motion_anti)
        special_adjustment_anti = special_service.get_special_adjustment(
            test_arrow_anti, test_pictograph
        )

        print(f"Letter V, turns (1, 0.5), ANTI motion:")
        print(f"  Special adjustment: {special_adjustment_anti}")

        # Test complete arrow positioning pipeline
        print(f"\n🔧 TESTING COMPLETE ARROW POSITIONING PIPELINE")
        print("-" * 50)

        # Create full pictograph data for arrow positioning
        full_pictograph = PictographData(
            letter="V", metadata={"blue_turns": 1, "red_turns": 0.5}
        )

        # Test arrow positioning with special placement integration
        final_x, final_y, rotation = arrow_service.calculate_arrow_position(
            test_arrow, full_pictograph
        )

        print(f"Complete arrow positioning for Letter V:")
        print(f"  Final position: ({final_x}, {final_y})")
        print(f"  Rotation: {rotation}°")

        # Test with letter that shouldn't have special placement
        test_pictograph_no_special = MockPictographData(
            "A", blue_turns=0, red_turns=1.5
        )
        special_adjustment_none = special_service.get_special_adjustment(
            test_arrow, test_pictograph_no_special
        )

        print(f"\nLetter A, turns (0, 1.5), PRO motion:")
        print(f"  Special adjustment: {special_adjustment_none}")

        if special_adjustment_none:
            print(
                f"  ✅ Special adjustment found: ({special_adjustment_none.x()}, {special_adjustment_none.y()})"
            )
        else:
            print(f"  ❌ No special adjustment found (expected for this case)")

        # Test multiple letters with special placements
        print(f"\n🧪 TESTING MULTIPLE LETTERS WITH SPECIAL PLACEMENTS")
        print("-" * 50)

        test_cases = [
            ("V", 1, 0.5, MotionType.PRO),
            ("V", 1, 0.5, MotionType.ANTI),
            ("A", 0, 1.5, MotionType.PRO),
            ("B", 2, 2, MotionType.PRO),
            ("G", 0, 0, MotionType.PRO),
        ]

        for letter, blue_turns, red_turns, motion_type in test_cases:
            test_motion_case = MotionData(
                motion_type=motion_type,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.EAST,
                turns=1.0,
            )

            test_arrow_case = ArrowData(motion_data=test_motion_case)
            test_pictograph_case = MockPictographData(letter, blue_turns, red_turns)

            adjustment = special_service.get_special_adjustment(
                test_arrow_case, test_pictograph_case
            )
            turns_tuple = special_service._generate_turns_tuple(test_pictograph_case)

            status = "✅ FOUND" if adjustment else "❌ NONE"
            adjustment_str = (
                f"({adjustment.x()}, {adjustment.y()})" if adjustment else "None"
            )

            print(
                f"  {letter} {turns_tuple} {motion_type.value}: {status} {adjustment_str}"
            )

        print(f"\n✅ Arrow positioning with special placement debugging complete!")

    except Exception as e:
        print(f"❌ Error during debugging: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    debug_arrow_positioning()
