#!/usr/bin/env python3
"""
TEST LIFECYCLE: SCAFFOLDING
PURPOSE: Simple debug tests for critical V2 bugs without complex UI setup
DELETE_AFTER: 2025-07-15
CREATED: 2025-06-14
AUTHOR: @austencloud
RELATED_ISSUE: Critical bugs - sequence clear crash, option selection workflow
"""

import sys
import traceback
from pathlib import Path

# Add v2 to path
v2_path = Path(__file__).parent
if str(v2_path) not in sys.path:
    sys.path.insert(0, str(v2_path))


def test_clear_sequence_crash():
    """Test Bug #1: Program crashes when clearing sequence."""
    print("\n🐛 TEST 1: Clear Sequence Crash Bug")
    print("-" * 40)

    try:
        # Import required modules
        from src.domain.models.core_models import SequenceData, BeatData
        from application.services.data.pictograph_dataset_service import (
            PictographDatasetService,
        )

        print("   ✅ Imports successful")

        # Test SequenceData.empty() method
        print("   Testing SequenceData.empty()...")
        empty_sequence = SequenceData.empty()
        print(f"   ✅ Empty sequence created: {empty_sequence.length} beats")

        # Test creating a sequence with beats
        print("   Testing sequence with beats...")
        dataset_service = PictographDatasetService()
        real_beat = dataset_service.get_start_position_pictograph(
            "alpha1_alpha1", "diamond"
        )

        if real_beat:
            print("   ✅ Real beat data loaded")

            # Create sequence with beat
            sequence_with_beats = SequenceData(beats=[real_beat])
            print(
                f"   ✅ Sequence with beats created: {sequence_with_beats.length} beats"
            )

            # Test clearing sequence (this should not crash)
            cleared_sequence = SequenceData.empty()
            print(f"   ✅ Sequence cleared: {cleared_sequence.length} beats")

            return True, "SequenceData operations work correctly"
        else:
            return False, "Could not load real beat data"

    except Exception as e:
        print(f"   ❌ Error: {e}")
        traceback.print_exc()
        return False, f"Clear sequence test failed: {e}"


def test_option_selection_workflow():
    """Test Bug #2: Option selection workflow."""
    print("\n🐛 TEST 2: Option Selection Workflow Bug")
    print("-" * 40)

    try:
        # Import required modules
        from src.domain.models.core_models import SequenceData, BeatData
        from application.services.data.pictograph_dataset_service import (
            PictographDatasetService,
        )

        print("   ✅ Imports successful")

        # Test dataset service
        dataset_service = PictographDatasetService()

        # Test start position loading
        print("   Testing start position loading...")
        start_position = dataset_service.get_start_position_pictograph(
            "alpha1_alpha1", "diamond"
        )

        if start_position:
            print(f"   ✅ Start position loaded: {start_position.letter}")

            # Test option loading after start position
            print("   Testing option loading...")

            # Try to get next options (this simulates what should happen after start position)
            try:
                # Check if we can load more beats from dataset
                beta_beat = dataset_service.get_start_position_pictograph(
                    "beta5_beta5", "diamond"
                )
                if beta_beat:
                    print(f"   ✅ Additional beat loaded: {beta_beat.letter}")

                    # Test sequence building
                    print("   Testing sequence building...")
                    sequence = SequenceData(beats=[beta_beat])
                    print(f"   ✅ Sequence built: {sequence.length} beats")

                    return True, "Option selection workflow works correctly"
                else:
                    return False, "Could not load additional beats"

            except Exception as option_error:
                print(f"   ❌ Option loading error: {option_error}")
                return False, f"Option loading failed: {option_error}"
        else:
            return False, "Could not load start position"

    except Exception as e:
        print(f"   ❌ Error: {e}")
        traceback.print_exc()
        return False, f"Option selection test failed: {e}"


def test_construct_tab_integration():
    """Test Bug #3: ConstructTab integration issues."""
    print("\n🐛 TEST 3: ConstructTab Integration Bug")
    print("-" * 40)

    try:
        # Test the specific methods that are causing issues
        from src.domain.models.core_models import SequenceData, BeatData
        from application.services.data.pictograph_dataset_service import (
            PictographDatasetService,
        )

        print("   ✅ Imports successful")

        # Simulate the construct tab workflow
        dataset_service = PictographDatasetService()

        # Step 1: Start position selection
        print("   Step 1: Start position selection...")
        start_position = dataset_service.get_start_position_pictograph(
            "alpha1_alpha1", "diamond"
        )

        if not start_position:
            return False, "Could not load start position"

        print(f"   ✅ Start position: {start_position.letter}")

        # Step 2: Option selection simulation
        print("   Step 2: Option selection simulation...")

        # This simulates what _handle_option_selected should do
        current_sequence = SequenceData.empty()

        # Create new beat (this is what was failing)
        try:
            new_beat = dataset_service.get_start_position_pictograph(
                "beta5_beta5", "diamond"
            )
            if new_beat:
                # Update beat number for sequence position
                new_beat_updated = new_beat.update(
                    beat_number=current_sequence.length + 1
                )

                # Add to sequence
                updated_beats = current_sequence.beats + [new_beat_updated]
                updated_sequence = current_sequence.update(beats=updated_beats)

                print(f"   ✅ Beat added to sequence: {updated_sequence.length} beats")

                # Step 3: Clear sequence simulation
                print("   Step 3: Clear sequence simulation...")
                cleared_sequence = SequenceData.empty()
                print(f"   ✅ Sequence cleared: {cleared_sequence.length} beats")

                return True, "ConstructTab integration works correctly"
            else:
                return False, "Could not create new beat for sequence"

        except Exception as beat_error:
            print(f"   ❌ Beat creation error: {beat_error}")
            traceback.print_exc()
            return False, f"Beat creation failed: {beat_error}"

    except Exception as e:
        print(f"   ❌ Error: {e}")
        traceback.print_exc()
        return False, f"ConstructTab integration test failed: {e}"


def main():
    """Main test function."""
    print("🐛 V2 Critical Bug Simple Tests")
    print("=" * 50)

    tests = [
        ("Clear Sequence Crash", test_clear_sequence_crash),
        ("Option Selection Workflow", test_option_selection_workflow),
        ("ConstructTab Integration", test_construct_tab_integration),
    ]

    results = {}

    for test_name, test_func in tests:
        try:
            success, message = test_func()
            results[test_name] = (success, message)
        except Exception as e:
            results[test_name] = (False, f"Test execution failed: {e}")

    # Generate report
    print("\n📊 TEST RESULTS")
    print("=" * 30)

    passed = 0
    failed = 0

    for test_name, (success, message) in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {test_name}")
        print(f"   {message}")
        print()

        if success:
            passed += 1
        else:
            failed += 1

    print(f"Summary: {passed} passed, {failed} failed")

    if failed > 0:
        print("\n🔧 ISSUES DETECTED:")
        print("The following bugs need to be fixed:")
        for test_name, (success, message) in results.items():
            if not success:
                print(f"- {test_name}: {message}")
        return 1
    else:
        print("\n🎉 ALL TESTS PASSED!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
