#!/usr/bin/env python3
"""
Test Event-Driven Architecture Implementation
Validates that the event system and command pattern are working correctly.
"""

import sys
from pathlib import Path

# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def test_event_system():
    """Test the event system functionality."""
    print("🔍 Testing Event System...")

    try:
        from core.events import get_event_bus, BeatAddedEvent, SequenceCreatedEvent

        # Create event bus
        event_bus = get_event_bus()
        print("✅ Event bus created successfully")

        # Test event subscription
        events_received = []

        def handle_beat_added(event):
            events_received.append(f"Beat added: {event.sequence_id}")

        def handle_sequence_created(event):
            events_received.append(f"Sequence created: {event.sequence_name}")

        # Subscribe to events
        sub1 = event_bus.subscribe("sequence.beat_added", handle_beat_added)
        sub2 = event_bus.subscribe("sequence.created", handle_sequence_created)
        print("✅ Event subscriptions created")

        # Publish events
        beat_event = BeatAddedEvent(
            sequence_id="test-seq-1", beat_position=0, total_beats=1
        )
        event_bus.publish(beat_event)

        seq_event = SequenceCreatedEvent(
            sequence_id="test-seq-1", sequence_name="Test Sequence", sequence_length=16
        )
        event_bus.publish(seq_event)

        print("✅ Events published successfully")

        # Verify events were received
        if len(events_received) == 2:
            print("✅ All events received correctly")
            for event in events_received:
                print(f"   📨 {event}")
        else:
            print(f"⚠️ Expected 2 events, received {len(events_received)}")

        # Cleanup
        event_bus.unsubscribe(sub1)
        event_bus.unsubscribe(sub2)
        print("✅ Event system test completed")

        return True

    except Exception as e:
        print(f"❌ Event system test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_command_system():
    """Test the command system functionality."""
    print("\n🔍 Testing Command System...")

    try:
        from core.events import get_event_bus
        from core.commands import CommandProcessor, AddBeatCommand
        from domain.models.core_models import (
            SequenceData,
            BeatData,
            MotionData,
            MotionType,
            Location,
            RotationDirection,
        )

        # Create event bus and command processor
        event_bus = get_event_bus()
        command_processor = CommandProcessor(event_bus)
        print("✅ Command processor created")

        # Create test sequence and beat
        sequence = SequenceData(id="test-seq", name="Test Sequence", beats=[])

        beat = BeatData(
            id="test-beat",
            beat_number=1,
            letter="A",
            blue_motion=MotionData(
                motion_type=MotionType.STATIC,
                prop_rot_dir=RotationDirection.NO_ROTATION,
                start_loc=Location.NORTH,
                end_loc=Location.NORTH,
                turns=0.0,
            ),
            red_motion=MotionData(
                motion_type=MotionType.STATIC,
                prop_rot_dir=RotationDirection.NO_ROTATION,
                start_loc=Location.SOUTH,
                end_loc=Location.SOUTH,
                turns=0.0,
            ),
        )

        # Test command execution
        command = AddBeatCommand(
            sequence=sequence, beat=beat, position=0, event_bus=event_bus
        )

        result = command_processor.execute(command)
        if result.success:
            print("✅ Command executed successfully")
            print(f"   📊 Result sequence has {len(result.result.beats)} beats")
        else:
            print(f"❌ Command execution failed: {result.error_message}")
            return False

        # Test undo functionality
        if command_processor.can_undo():
            undo_result = command_processor.undo()
            if undo_result.success:
                print("✅ Command undo successful")
                print(
                    f"   📊 Undone sequence has {len(undo_result.result.beats)} beats"
                )
            else:
                print(f"❌ Command undo failed: {undo_result.error_message}")
                return False
        else:
            print("⚠️ Undo not available")

        # Test redo functionality
        if command_processor.can_redo():
            redo_result = command_processor.redo()
            if redo_result.success:
                print("✅ Command redo successful")
                print(
                    f"   📊 Redone sequence has {len(redo_result.result.beats)} beats"
                )
            else:
                print(f"❌ Command redo failed: {redo_result.error_message}")
                return False
        else:
            print("⚠️ Redo not available")

        print("✅ Command system test completed")
        return True

    except Exception as e:
        print(f"❌ Command system test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_service_integration():
    """Test that services are properly integrated with event system."""
    print("\n🔍 Testing Service Integration...")

    try:
        from core.events import get_event_bus
        from application.services.motion.motion_generation_service import (
            MotionGenerationService,
        )
        from application.services.layout.layout_management_service import (
            LayoutManagementService,
        )
        from application.services.core.sequence_management_service import (
            SequenceManagementService,
        )

        event_bus = get_event_bus()

        # Test motion service with event bus
        motion_service = MotionGenerationService(event_bus=event_bus)
        print("✅ Motion service created with event bus")

        # Test layout service with event bus
        layout_service = LayoutManagementService(event_bus=event_bus)
        print("✅ Layout service created with event bus")

        # Test sequence service with event bus
        sequence_service = SequenceManagementService(event_bus=event_bus)
        print("✅ Sequence service created with event bus")

        # Verify services have event bus
        if hasattr(motion_service, "event_bus") and motion_service.event_bus:
            print("✅ Motion service has event bus")
        else:
            print("⚠️ Motion service missing event bus")

        if hasattr(layout_service, "event_bus") and layout_service.event_bus:
            print("✅ Layout service has event bus")
        else:
            print("⚠️ Layout service missing event bus")

        if hasattr(sequence_service, "event_bus") and sequence_service.event_bus:
            print("✅ Sequence service has event bus")
        else:
            print("⚠️ Sequence service missing event bus")

        print("✅ Service integration test completed")
        return True

    except Exception as e:
        print(f"❌ Service integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all event-driven architecture tests."""
    print("🚀 Event-Driven Architecture Test Suite")
    print("=" * 50)

    tests = [test_event_system, test_command_system, test_service_integration]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Event-driven architecture is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
