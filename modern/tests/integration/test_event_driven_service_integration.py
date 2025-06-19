"""
Integration tests for event-driven service integration.

Tests the complete event flow from service actions to event publishing,
verifying that the event-driven architecture works end-to-end.
"""

import pytest
from unittest.mock import Mock, MagicMock
import uuid
from datetime import datetime

from core.events import (
    TypeSafeEventBus,
    SequenceCreatedEvent,
    BeatAddedEvent,
    BeatRemovedEvent,
)
from application.services.core.sequence_management_service import (
    SequenceManagementService,
)
from domain.models.core_models import SequenceData, BeatData


@pytest.fixture
def event_bus():
    """Create event bus for testing."""
    return TypeSafeEventBus()


@pytest.fixture
def sequence_service(event_bus):
    """Create sequence management service with event bus."""
    return SequenceManagementService(event_bus=event_bus)


class TestEventDrivenServiceIntegration:
    """Test event-driven service integration."""

    def test_sequence_creation_publishes_event(self, sequence_service, event_bus):
        """Test that creating a sequence publishes SequenceCreatedEvent."""
        # Setup: Track published events
        published_events = []

        def track_event(event):
            published_events.append(event)

        event_bus.subscribe("sequence.created", track_event)

        # Action: Create sequence using service
        sequence = sequence_service.create_sequence("Test Sequence", 4)

        # Verify: Sequence was created
        assert sequence.name == "Test Sequence"
        assert sequence.length == 4

        # Verify: Event was published
        assert len(published_events) == 1
        event = published_events[0]
        assert isinstance(event, SequenceCreatedEvent)
        assert event.sequence_name == "Test Sequence"
        assert event.sequence_length == 4

    def test_beat_addition_publishes_event(self, sequence_service, event_bus):
        """Test that adding beats publishes BeatAddedEvent."""
        # Setup: Track published events
        published_events = []

        def track_event(event):
            published_events.append(event)

        event_bus.subscribe("sequence.beat_added", track_event)

        # Setup: Create initial sequence
        sequence = sequence_service.create_sequence("Test Sequence", 2)

        # Action: Add beat to sequence
        new_beat = BeatData(beat_number=3, letter="A", duration=1.0)
        updated_sequence = sequence_service.add_beat(sequence, new_beat, 2)

        # Verify: Beat was added
        assert updated_sequence.length == 3
        assert len(updated_sequence.beats) == 3

        # Verify: Event was published
        assert len(published_events) == 1
        event = published_events[0]
        assert isinstance(event, BeatAddedEvent)
        assert event.sequence_id == sequence.id
        assert event.total_beats == 3

    def test_beat_removal_publishes_event(self, sequence_service, event_bus):
        """Test that removing beats publishes BeatRemovedEvent."""
        # Setup: Track published events
        published_events = []

        def track_event(event):
            published_events.append(event)

        event_bus.subscribe("sequence.beat_removed", track_event)

        # Setup: Create sequence with beats
        sequence = sequence_service.create_sequence("Test Sequence", 3)

        # Action: Remove beat from sequence
        updated_sequence = sequence_service.remove_beat(sequence, 1)

        # Verify: Beat was removed
        assert updated_sequence.length == 2
        assert len(updated_sequence.beats) == 2

        # Verify: Event was published
        assert len(published_events) == 1
        event = published_events[0]
        assert isinstance(event, BeatRemovedEvent)
        assert event.sequence_id == sequence.id
        assert event.remaining_beats == 2

    def test_event_bus_handles_multiple_subscribers(self, sequence_service, event_bus):
        """Test that event bus delivers events to multiple subscribers."""
        # Setup: Track events from multiple subscribers
        subscriber1_events = []
        subscriber2_events = []

        def track_subscriber1(event):
            subscriber1_events.append(event)

        def track_subscriber2(event):
            subscriber2_events.append(event)

        event_bus.subscribe("sequence.created", track_subscriber1)
        event_bus.subscribe("sequence.created", track_subscriber2)

        # Action: Create sequence
        sequence = sequence_service.create_sequence("Multi-Subscriber Test", 5)

        # Verify: Both subscribers received the event
        assert len(subscriber1_events) == 1
        assert len(subscriber2_events) == 1
        assert subscriber1_events[0].sequence_name == "Multi-Subscriber Test"
        assert subscriber2_events[0].sequence_name == "Multi-Subscriber Test"

    def test_service_integration_with_event_bus(self, sequence_service, event_bus):
        """Test complete service integration with event bus."""
        # Setup: Track all sequence-related events
        all_events = []

        def track_all_events(event):
            all_events.append(event)

        event_bus.subscribe("sequence.created", track_all_events)
        event_bus.subscribe("sequence.beat_added", track_all_events)
        event_bus.subscribe("sequence.beat_removed", track_all_events)

        # Action: Perform sequence operations
        sequence = sequence_service.create_sequence("Integration Test", 2)

        new_beat = BeatData(beat_number=3, letter="B", duration=1.0)
        sequence = sequence_service.add_beat(sequence, new_beat, 2)

        sequence = sequence_service.remove_beat(sequence, 0)

        # Verify: All events were published in correct order
        assert len(all_events) == 3
        assert isinstance(all_events[0], SequenceCreatedEvent)
        assert isinstance(all_events[1], BeatAddedEvent)
        assert isinstance(all_events[2], BeatRemovedEvent)

        # Verify: Event data is consistent
        assert all_events[0].sequence_name == "Integration Test"
        assert all_events[1].total_beats == 3
        assert all_events[2].remaining_beats == 2
