#!/usr/bin/env python3
"""
Event-Driven Integration Verification Demo

This script demonstrates and verifies that the event-driven architecture
is working correctly by testing service event publishing and subscription.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.core.events import (
    TypeSafeEventBus,
    SequenceCreatedEvent,
    BeatAddedEvent,
    BeatRemovedEvent,
)
from src.application.services.core.sequence_management_service import (
    SequenceManagementService,
)
from src.domain.models.core_models import BeatData


def main():
    """Demonstrate event-driven integration."""
    print("🚀 Event-Driven Integration Verification")
    print("=" * 50)

    # Create event bus
    event_bus = TypeSafeEventBus()
    print("✅ Event bus created")

    # Track events
    events_received = []

    def log_event(event):
        events_received.append(event)
        event_type = event.event_type
        source = event.source
        print(f"📨 Event received: {event_type} from {source}")

        if hasattr(event, "sequence_name"):
            print(f"   📋 Sequence: {event.sequence_name}")
        if hasattr(event, "total_beats"):
            print(f"   🎵 Total beats: {event.total_beats}")
        if hasattr(event, "remaining_beats"):
            print(f"   🎵 Remaining beats: {event.remaining_beats}")

    # Subscribe to all sequence events
    print("\n🔗 Setting up event subscriptions...")
    event_bus.subscribe("sequence.created", log_event)
    event_bus.subscribe("sequence.beat_added", log_event)
    event_bus.subscribe("sequence.beat_removed", log_event)
    print("✅ Event subscriptions created")

    # Create sequence service with event bus
    sequence_service = SequenceManagementService(event_bus=event_bus)
    print("✅ Sequence service created with event bus")

    print("\n🎬 Demo: Event-driven sequence operations")
    print("-" * 40)

    # Demo 1: Create sequence
    print("\n1️⃣ Creating sequence...")
    sequence = sequence_service.create_sequence("Event Demo Sequence", 3)
    print(f"   ✅ Created: {sequence.name} (ID: {sequence.id[:8]}...)")

    # Demo 2: Add beat
    print("\n2️⃣ Adding beat...")
    new_beat = BeatData(
        beat_number=4, letter="A", duration=1.0, blue_motion=None, red_motion=None
    )
    sequence = sequence_service.add_beat(sequence, new_beat, 3)
    print(f"   ✅ Added beat, sequence now has {sequence.length} beats")

    # Demo 3: Remove beat
    print("\n3️⃣ Removing beat...")
    sequence = sequence_service.remove_beat(sequence, 1)
    print(f"   ✅ Removed beat, sequence now has {sequence.length} beats")

    # Verify events were published
    print("\n📊 Event Summary")
    print("-" * 20)
    print(f"Total events received: {len(events_received)}")

    expected_events = [
        ("sequence.created", SequenceCreatedEvent),
        ("sequence.beat_added", BeatAddedEvent),
        ("sequence.beat_removed", BeatRemovedEvent),
    ]

    success = True
    for i, (expected_type, expected_class) in enumerate(expected_events):
        if i < len(events_received):
            event = events_received[i]
            if event.event_type == expected_type and isinstance(event, expected_class):
                print(f"✅ Event {i+1}: {expected_type} - CORRECT")
            else:
                print(
                    f"❌ Event {i+1}: Expected {expected_type}, got {event.event_type}"
                )
                success = False
        else:
            print(f"❌ Event {i+1}: Missing {expected_type}")
            success = False

    print("\n🎯 Integration Test Result")
    print("=" * 30)
    if success and len(events_received) == 3:
        print("✅ SUCCESS: Event-driven integration is working correctly!")
        print("   - Services publish events when operations occur")
        print("   - Event bus delivers events to subscribers")
        print("   - Event data is correctly populated")
        return True
    else:
        print("❌ FAILURE: Event-driven integration has issues")
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 Error during demo: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
