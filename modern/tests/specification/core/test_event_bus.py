"""
TEST LIFECYCLE: specification
CREATED: 2025-06-14
PURPOSE: Contract testing for TypeSafeEventBus implementation
SCOPE: Event publishing, subscription, async handling, type safety
EXPECTED_DURATION: permanent
"""

import pytest
import asyncio
from typing import List
from unittest.mock import Mock

from src.core.events.event_bus import (
    TypeSafeEventBus,
    SequenceEvent,
    ArrowEvent,
    MotionEvent,
    UIEvent,
    EventPriority,
    get_event_bus,
    reset_event_bus,
)


@pytest.fixture
def event_bus():
    """Provide fresh event bus for each test."""
    bus = TypeSafeEventBus()
    yield bus
    bus.shutdown()


@pytest.fixture
def sample_sequence_event():
    """Provide sample sequence event."""
    return SequenceEvent(
        sequence_id="test-seq-123",
        operation="created",
        data={"name": "Test Sequence", "length": 16},
        source="test",
    )


@pytest.fixture
def sample_arrow_event():
    """Provide sample arrow event."""
    return ArrowEvent(
        arrow_color="blue",
        operation="positioned",
        pictograph_id="test-pic-456",
        position_data={"x": 100, "y": 200, "rotation": 45},
        source="test",
    )


class TestEventBusBasics:
    """Test basic event bus functionality."""

    def test_event_bus_creation(self, event_bus):
        """Test event bus can be created."""
        assert event_bus is not None
        assert event_bus.get_subscription_count() == 0

    def test_subscribe_and_unsubscribe(self, event_bus):
        """Test basic subscription and unsubscription."""
        handler = Mock()

        # Subscribe
        sub_id = event_bus.subscribe("test.event", handler)
        assert isinstance(sub_id, str)
        assert event_bus.get_subscription_count("test.event") == 1

        # Unsubscribe
        result = event_bus.unsubscribe(sub_id)
        assert result is True
        assert event_bus.get_subscription_count("test.event") == 0

    def test_unsubscribe_nonexistent(self, event_bus):
        """Test unsubscribing from non-existent subscription."""
        result = event_bus.unsubscribe("non-existent-id")
        assert result is False


class TestEventPublishing:
    """Test event publishing functionality."""

    def test_publish_to_single_subscriber(self, event_bus, sample_sequence_event):
        """Test publishing event to single subscriber."""
        handler = Mock()

        event_bus.subscribe("sequence.created", handler)
        event_bus.publish(sample_sequence_event)

        handler.assert_called_once_with(sample_sequence_event)

    def test_publish_to_multiple_subscribers(self, event_bus, sample_sequence_event):
        """Test publishing event to multiple subscribers."""
        handler1 = Mock()
        handler2 = Mock()
        handler3 = Mock()

        event_bus.subscribe("sequence.created", handler1)
        event_bus.subscribe("sequence.created", handler2)
        event_bus.subscribe("sequence.created", handler3)

        event_bus.publish(sample_sequence_event)

        handler1.assert_called_once_with(sample_sequence_event)
        handler2.assert_called_once_with(sample_sequence_event)
        handler3.assert_called_once_with(sample_sequence_event)

    def test_publish_no_subscribers(self, event_bus, sample_sequence_event):
        """Test publishing event with no subscribers."""
        # Should not raise any exceptions
        event_bus.publish(sample_sequence_event)

        # Verify stats are still tracked
        stats = event_bus.get_event_stats()
        assert stats.get("sequence.created", 0) == 1

    def test_publish_wrong_event_type(self, event_bus, sample_sequence_event):
        """Test publishing event to wrong event type subscribers."""
        handler = Mock()

        event_bus.subscribe("arrow.positioned", handler)
        event_bus.publish(sample_sequence_event)  # Different event type

        handler.assert_not_called()


class TestEventPriority:
    """Test event priority handling."""

    def test_priority_ordering(self, event_bus, sample_sequence_event):
        """Test that events are handled in priority order."""
        call_order = []

        def high_priority_handler(event):
            call_order.append("high")

        def normal_priority_handler(event):
            call_order.append("normal")

        def low_priority_handler(event):
            call_order.append("low")

        # Subscribe in reverse priority order
        event_bus.subscribe("sequence.created", low_priority_handler, EventPriority.LOW)
        event_bus.subscribe(
            "sequence.created", normal_priority_handler, EventPriority.NORMAL
        )
        event_bus.subscribe(
            "sequence.created", high_priority_handler, EventPriority.HIGH
        )

        event_bus.publish(sample_sequence_event)

        # Should be called in priority order (HIGH, NORMAL, LOW)
        assert call_order == ["high", "normal", "low"]


class TestAsyncEventHandling:
    """Test asynchronous event handling."""

    @pytest.mark.asyncio
    async def test_async_publish(self, event_bus, sample_sequence_event):
        """Test asynchronous event publishing."""
        handler = Mock()

        event_bus.subscribe("sequence.created", handler)
        await event_bus.publish_async(sample_sequence_event)

        handler.assert_called_once_with(sample_sequence_event)

    @pytest.mark.asyncio
    async def test_async_handler(self, event_bus, sample_sequence_event):
        """Test async event handler."""
        call_log = []

        async def async_handler(event):
            call_log.append("async_start")
            await asyncio.sleep(0.01)  # Simulate async work
            call_log.append("async_end")

        event_bus.subscribe("sequence.created", async_handler)
        await event_bus.publish_async(sample_sequence_event)

        assert call_log == ["async_start", "async_end"]

    @pytest.mark.asyncio
    async def test_mixed_sync_async_handlers(self, event_bus, sample_sequence_event):
        """Test mixing sync and async handlers."""
        call_log = []

        def sync_handler(event):
            call_log.append("sync")

        async def async_handler(event):
            call_log.append("async")

        event_bus.subscribe("sequence.created", sync_handler)
        event_bus.subscribe("sequence.created", async_handler)

        await event_bus.publish_async(sample_sequence_event)

        # Both should be called
        assert "sync" in call_log
        assert "async" in call_log


class TestEventFiltering:
    """Test event filtering functionality."""

    def test_event_filter(self, event_bus):
        """Test event filtering with filter function."""
        handler = Mock()

        # Filter that only allows events from "test" source
        def test_source_filter(event):
            return event.source == "test"

        event_bus.subscribe("sequence.created", handler, filter_func=test_source_filter)

        # Event with matching source
        event1 = SequenceEvent(sequence_id="seq1", operation="created", source="test")

        # Event with non-matching source
        event2 = SequenceEvent(sequence_id="seq2", operation="created", source="other")

        event_bus.publish(event1)
        event_bus.publish(event2)

        # Only event1 should trigger handler
        handler.assert_called_once_with(event1)


class TestEventTypes:
    """Test different event types."""

    def test_sequence_event(self, event_bus):
        """Test sequence event handling."""
        handler = Mock()

        event_bus.subscribe("sequence.updated", handler)

        event = SequenceEvent(
            sequence_id="seq-123", operation="updated", data={"beats_added": 2}
        )

        event_bus.publish(event)
        handler.assert_called_once_with(event)

        # Verify event properties
        assert event.event_type == "sequence.updated"
        assert event.sequence_id == "seq-123"

    def test_arrow_event(self, event_bus, sample_arrow_event):
        """Test arrow event handling."""
        handler = Mock()

        event_bus.subscribe("arrow.positioned", handler)
        event_bus.publish(sample_arrow_event)

        handler.assert_called_once_with(sample_arrow_event)
        assert sample_arrow_event.event_type == "arrow.positioned"

    def test_motion_event(self, event_bus):
        """Test motion event handling."""
        handler = Mock()

        event_bus.subscribe("motion.validated", handler)

        event = MotionEvent(
            motion_id="motion-789",
            operation="validated",
            validation_result=True,
            errors=[],
        )

        event_bus.publish(event)
        handler.assert_called_once_with(event)
        assert event.event_type == "motion.validated"

    def test_ui_event(self, event_bus):
        """Test UI event handling."""
        handler = Mock()

        event_bus.subscribe("ui.button.clicked", handler)

        event = UIEvent(
            component="button", action="clicked", state_data={"button_id": "save_btn"}
        )

        event_bus.publish(event)
        handler.assert_called_once_with(event)
        assert event.event_type == "ui.button.clicked"


class TestEventBusUtilities:
    """Test event bus utility functions."""

    def test_event_stats(self, event_bus, sample_sequence_event):
        """Test event statistics tracking."""
        handler = Mock()
        event_bus.subscribe("sequence.created", handler)

        # Publish multiple events
        event_bus.publish(sample_sequence_event)
        event_bus.publish(sample_sequence_event)
        event_bus.publish(sample_sequence_event)

        stats = event_bus.get_event_stats()
        assert stats["sequence.created"] == 3

    def test_subscription_count(self, event_bus):
        """Test subscription counting."""
        handler1 = Mock()
        handler2 = Mock()

        assert event_bus.get_subscription_count() == 0

        event_bus.subscribe("test.event1", handler1)
        assert event_bus.get_subscription_count() == 1
        assert event_bus.get_subscription_count("test.event1") == 1

        event_bus.subscribe("test.event2", handler2)
        assert event_bus.get_subscription_count() == 2
        assert event_bus.get_subscription_count("test.event2") == 1

    def test_clear_dead_references(self, event_bus):
        """Test cleaning up dead weak references."""
        # This is hard to test directly, but we can verify the method exists
        removed_count = event_bus.clear_dead_references()
        assert isinstance(removed_count, int)
        assert removed_count >= 0


class TestGlobalEventBus:
    """Test global event bus functionality."""

    def test_get_global_event_bus(self):
        """Test getting global event bus instance."""
        reset_event_bus()  # Ensure clean state

        bus1 = get_event_bus()
        bus2 = get_event_bus()

        # Should return same instance
        assert bus1 is bus2

        reset_event_bus()  # Cleanup

    def test_reset_global_event_bus(self):
        """Test resetting global event bus."""
        bus1 = get_event_bus()
        reset_event_bus()
        bus2 = get_event_bus()

        # Should be different instances
        assert bus1 is not bus2

        reset_event_bus()  # Cleanup


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
