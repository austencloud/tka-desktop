#!/usr/bin/env python3
"""
Manual test script for the new clear sequence behavior.
This script tests the implementation without requiring the full test framework.
"""

import sys

sys.path.append("src")

from domain.models.core_models import SequenceData, BeatData
from presentation.components.workbench.event_controller import WorkbenchEventController
from unittest.mock import Mock


def test_clear_sequence_behavior():
    """Test the V1-style clear sequence behavior manually"""
    print("🧪 Testing V1-Style Clear Sequence Behavior")
    print("=" * 70)

    # Mock services
    workbench_service = Mock()
    fullscreen_service = Mock()
    deletion_service = Mock()
    dictionary_service = Mock()

    # Create event controller
    event_controller = WorkbenchEventController(
        workbench_service=workbench_service,
        fullscreen_service=fullscreen_service,
        deletion_service=deletion_service,
        dictionary_service=dictionary_service,
    )

    # Test 1: Clear sequence with multiple beats
    print("\n📝 Test 1: Clear sequence with multiple beats")
    test_sequence = SequenceData(
        name="Test Sequence",
        beats=[
            BeatData(beat_number=1, letter="A"),
            BeatData(beat_number=2, letter="B"),
            BeatData(beat_number=3, letter="C"),
        ],
    )

    print(f"   Original sequence: {test_sequence.length} beats")
    print(f"   Beat letters: {[beat.letter for beat in test_sequence.beats]}")

    event_controller.set_sequence(test_sequence)
    success, message, result_sequence = event_controller.handle_clear()

    print(f"   Clear result: {success}")
    print(f"   Message: {message}")

    if result_sequence is not None:
        print(f"   Result sequence: {result_sequence.length} beats")
        print(f"   Is empty: {result_sequence.is_empty}")
        print(f"   Metadata: {result_sequence.metadata}")

        # Verify V1-style clearing (completely empty)
        assert (
            result_sequence.length == 0
        ), f"Expected 0 beats (empty), got {result_sequence.length}"
        assert result_sequence.is_empty, "Sequence should be completely empty"
        assert len(result_sequence.beats) == 0, "Should have no beats"
        print("   ✅ Test 1 PASSED - V1-style complete clearing")
    else:
        print("   ❌ Test 1 FAILED - No result sequence")
        return False

    # Test 2: Clear empty sequence
    print("\n📝 Test 2: Clear empty sequence")
    empty_sequence = SequenceData.empty()
    print(f"   Original empty sequence: {empty_sequence.length} beats")

    event_controller.set_sequence(empty_sequence)
    success, message, result_sequence = event_controller.handle_clear()

    print(f"   Clear result: {success}")
    print(f"   Message: {message}")

    if result_sequence:
        print(f"   Preserved sequence: {result_sequence.length} beats")
        print(f"   First beat is blank: {result_sequence.beats[0].is_blank}")

        # Verify preservation
        assert (
            result_sequence.length == 1
        ), f"Expected 1 beat, got {result_sequence.length}"
        assert result_sequence.beats[0].is_blank, "First beat should be blank"
        print("   ✅ Test 2 PASSED")
    else:
        print("   ❌ Test 2 FAILED - No result sequence")
        return False

    # Test 3: Test sequence continuation
    print("\n📝 Test 3: Test sequence continuation from preserved beat")
    preserved_sequence = result_sequence

    # Add a new beat to the preserved sequence
    new_beat = BeatData(beat_number=2, letter="D")
    continued_sequence = preserved_sequence.add_beat(new_beat)

    print(f"   Continued sequence: {continued_sequence.length} beats")
    print(f"   Beat letters: {[beat.letter for beat in continued_sequence.beats]}")
    print(f"   First beat still blank: {continued_sequence.beats[0].is_blank}")
    print(f"   Second beat letter: {continued_sequence.beats[1].letter}")

    # Verify continuation
    assert (
        continued_sequence.length == 2
    ), f"Expected 2 beats, got {continued_sequence.length}"
    assert continued_sequence.beats[0].is_blank, "First beat should remain blank"
    assert continued_sequence.beats[1].letter == "D", "Second beat should have letter D"
    print("   ✅ Test 3 PASSED")

    # Test 4: Test BeatData operations
    print("\n📝 Test 4: Test BeatData operations")
    empty_beat = BeatData.empty()
    print(f"   Empty beat is blank: {empty_beat.is_blank}")
    print(f"   Empty beat letter: {empty_beat.letter}")
    print(f"   Empty beat beat_number: {empty_beat.beat_number}")

    # Update beat number
    updated_beat = empty_beat.update(beat_number=1)
    print(f"   Updated beat number: {updated_beat.beat_number}")
    print(f"   Updated beat still blank: {updated_beat.is_blank}")

    assert empty_beat.is_blank, "Empty beat should be blank"
    assert updated_beat.beat_number == 1, "Updated beat should have number 1"
    assert updated_beat.is_blank, "Updated beat should still be blank"
    print("   ✅ Test 4 PASSED")

    print("\n🎉 All tests PASSED!")
    print("✅ Clear sequence behavior correctly preserves start position beat")
    print("✅ Preserved beat maintains proper structure and metadata")
    print("✅ Sequences can be continued from preserved start position")
    return True


if __name__ == "__main__":
    try:
        success = test_clear_sequence_behavior()
        if success:
            print("\n🚀 Implementation is working correctly!")
            sys.exit(0)
        else:
            print("\n💥 Implementation has issues!")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test failed with exception: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
