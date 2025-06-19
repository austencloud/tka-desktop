#!/usr/bin/env python3
"""
Demo Event-Driven Workflow
Demonstrates the complete event-driven architecture in action.
"""

import sys
from pathlib import Path

# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def demo_event_driven_workflow():
    """Demonstrate the complete event-driven workflow."""
    print("🚀 Event-Driven Architecture Demo")
    print("=" * 50)

    # Import components
    from core.events import get_event_bus, reset_event_bus
    from application.services.core.sequence_management_service import (
        SequenceManagementService,
    )
    from application.services.layout.layout_management_service import (
        LayoutManagementService,
    )
    from domain.models.core_models import (
        BeatData,
        MotionData,
        MotionType,
        Location,
        RotationDirection,
    )

    # Reset and create fresh event bus
    reset_event_bus()
    event_bus = get_event_bus()
    print("✅ Event bus initialized")

    # Create services with event integration
    sequence_service = SequenceManagementService(event_bus=event_bus)
    layout_service = LayoutManagementService(event_bus=event_bus)
    print("✅ Services created with event integration")

    # Track events for demonstration
    events_log = []

    def log_event(event):
        events_log.append(f"{event.event_type}: {event.source}")

    # Subscribe to all events
    event_types = [
        "sequence.created",
        "sequence.beat_added",
        "sequence.beat_removed",
        "sequence.beat_updated",
        "layout.recalculated",
    ]

    subscriptions = []
    for event_type in event_types:
        sub_id = event_bus.subscribe(event_type, log_event)
        subscriptions.append(sub_id)

    print("✅ Event logging subscriptions created")

    # Demo 1: Create sequence with events
    print("\n🔍 Demo 1: Creating sequence with events")
    sequence = sequence_service.create_sequence_with_events("Demo Sequence", 16)
    print(f"   📊 Created sequence: {sequence.name} (ID: {sequence.id[:8]}...)")

    # Demo 2: Add beats with undo capability
    print("\n🔍 Demo 2: Adding beats with undo capability")

    # Create test beats
    beat1 = BeatData(
        id="beat-1",
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

    beat2 = BeatData(
        id="beat-2",
        beat_number=2,
        letter="B",
        blue_motion=MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
            turns=0.25,
        ),
        red_motion=MotionData(
            motion_type=MotionType.DASH,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.SOUTH,
            end_loc=Location.WEST,
            turns=0.25,
        ),
    )

    # Add beats using event-driven methods
    updated_sequence = sequence_service.add_beat_with_undo(beat1, 0)
    print(f"   📊 Added beat 1: {updated_sequence.length} beats total")

    updated_sequence = sequence_service.add_beat_with_undo(beat2, 1)
    print(f"   📊 Added beat 2: {updated_sequence.length} beats total")

    # Demo 3: Undo/Redo operations
    print("\n🔍 Demo 3: Undo/Redo operations")

    if sequence_service.can_undo():
        undo_desc = sequence_service.get_undo_description()
        print(f"   🔄 Undoing: {undo_desc}")
        undone_sequence = sequence_service.undo_last_operation()
        print(f"   📊 After undo: {undone_sequence.length} beats")

    if sequence_service.can_redo():
        redo_desc = sequence_service.get_redo_description()
        print(f"   🔄 Redoing: {redo_desc}")
        redone_sequence = sequence_service.redo_last_operation()
        print(f"   📊 After redo: {redone_sequence.length} beats")

    # Demo 4: Update beat with events
    print("\n🔍 Demo 4: Updating beat with events")
    updated_sequence = sequence_service.update_beat_with_undo(1, "letter", "X")
    print(f"   📊 Updated beat 1 letter to 'X'")

    # Demo 5: Show event log
    print("\n🔍 Demo 5: Event log summary")
    print(f"   📨 Total events captured: {len(events_log)}")
    for i, event in enumerate(events_log, 1):
        print(f"   {i:2d}. {event}")

    # Cleanup
    for sub_id in subscriptions:
        event_bus.unsubscribe(sub_id)

    print("\n✅ Demo completed successfully!")
    print("🎉 Event-driven architecture is working perfectly!")

    return True


def main():
    """Run the event-driven workflow demo."""
    try:
        demo_event_driven_workflow()
        return 0
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
