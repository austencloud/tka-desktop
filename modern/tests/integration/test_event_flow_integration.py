"""
Event Flow Integration Tests

Tests the end-to-end event flow between services that have been integrated
with the event-driven architecture. Validates that events are properly
published and consumed across service boundaries.

TESTS:
- ArrowManagementService event publishing
- PropManagementService event publishing
- Event bus message routing
- Cross-service event communication
- Event subscription and cleanup
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock
import uuid
from datetime import datetime

# Add src to path for imports
test_dir = Path(__file__).parent.parent.parent
src_dir = test_dir / "src"
sys.path.insert(0, str(src_dir))

from core.events import (
    get_event_bus,
    reset_event_bus,
    ArrowPositionedEvent,
    PropPositionedEvent,
)
from application.services.positioning.arrow_management_service import (
    ArrowManagementService,
)
from application.services.positioning.prop_management_service import (
    PropManagementService,
)
from domain.models.core_models import (
    MotionData,
    MotionType,
    RotationDirection,
    Location,
    BeatData,
)
from domain.models.pictograph_models import (
    ArrowData,
    PictographData,
    GridData,
    GridMode,
)


class TestEventFlowIntegration:
    """Test event flow integration across services."""

    def setup_method(self):
        """Set up fresh event bus for each test."""
        reset_event_bus()
        self.event_bus = get_event_bus()
        self.events_received = []

    def teardown_method(self):
        """Clean up after each test."""
        reset_event_bus()

    def _create_event_logger(self, event_type: str):
        """Create an event logger for testing."""

        def log_event(event):
            self.events_received.append(
                {
                    "type": event.event_type,
                    "source": event.source,
                    "timestamp": event.timestamp,
                    "data": event,
                }
            )

        return log_event

    def test_arrow_management_service_event_publishing(self):
        """Test that ArrowManagementService publishes events correctly."""
        # Subscribe to arrow events
        logger = self._create_event_logger("arrow.positioned")
        sub_id = self.event_bus.subscribe("arrow.positioned", logger)

        # Create service with event integration
        service = ArrowManagementService(event_bus=self.event_bus)

        # Create test data
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
        )

        arrow = ArrowData(color="blue", motion_data=motion, is_visible=True)

        grid_data = GridData(
            grid_mode=GridMode.DIAMOND, center_x=475.0, center_y=475.0, radius=100.0
        )

        pictograph = PictographData(
            grid_data=grid_data, arrows={"blue": arrow}, is_blank=False
        )

        # Test arrow positioning with events
        x, y, rotation = service.calculate_arrow_position(arrow, pictograph)

        # Verify event was published
        assert len(self.events_received) == 1
        event_data = self.events_received[0]
        assert event_data["type"] == "arrow.positioned"
        assert event_data["source"] == "ArrowManagementService"

        # Verify event data
        event = event_data["data"]
        assert isinstance(event, ArrowPositionedEvent)
        assert event.arrow_color == "blue"
        assert "x" in event.position_data
        assert "y" in event.position_data
        assert "rotation" in event.position_data

        # Clean up
        self.event_bus.unsubscribe(sub_id)

    def test_prop_management_service_event_publishing(self):
        """Test that PropManagementService publishes events correctly."""
        # Subscribe to prop events
        overlap_logger = self._create_event_logger("prop.overlap_detected")
        separation_logger = self._create_event_logger("prop.separation")
        beta_logger = self._create_event_logger("prop.beta_positioning")

        overlap_sub = self.event_bus.subscribe("prop.overlap_detected", overlap_logger)
        separation_sub = self.event_bus.subscribe("prop.separation", separation_logger)
        beta_sub = self.event_bus.subscribe("prop.beta_positioning", beta_logger)

        # Create service with event integration
        service = PropManagementService(event_bus=self.event_bus)

        # Create test data for overlap detection
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
        )

        red_motion = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.EAST,
            end_loc=Location.SOUTH,  # Same end location as blue
            turns=1.0,
        )

        beat_data = BeatData(
            beat_number=1,
            letter="G",  # Beta-ending letter
            blue_motion=blue_motion,
            red_motion=red_motion,
        )

        # Test overlap detection
        overlap = service.detect_prop_overlap(beat_data)

        # Test separation calculation
        blue_offset, red_offset = service.calculate_separation_offsets(beat_data)

        # Test beta positioning
        result = service.apply_beta_positioning(beat_data)

        # Verify events were published
        assert (
            len(self.events_received) >= 2
        )  # At least separation and beta positioning

        # Check for separation events
        separation_events = [
            e for e in self.events_received if e["type"] == "prop.separation"
        ]
        assert len(separation_events) >= 1

        # Check for beta positioning events
        beta_events = [
            e for e in self.events_received if e["type"] == "prop.beta_positioning"
        ]
        assert len(beta_events) == 1

        # Verify event sources
        for event_data in self.events_received:
            assert event_data["source"] == "PropManagementService"

        # Clean up
        self.event_bus.unsubscribe(overlap_sub)
        self.event_bus.unsubscribe(separation_sub)
        self.event_bus.unsubscribe(beta_sub)

    def test_cross_service_event_communication(self):
        """Test event communication between multiple services."""
        # Create both services with shared event bus
        arrow_service = ArrowManagementService(event_bus=self.event_bus)
        prop_service = PropManagementService(event_bus=self.event_bus)

        # Subscribe to all events
        all_logger = self._create_event_logger("all")
        arrow_sub = self.event_bus.subscribe("arrow.positioned", all_logger)
        prop_sub = self.event_bus.subscribe("prop.separation", all_logger)

        # Create test data
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
        )

        # Test arrow service
        arrow = ArrowData(color="blue", motion_data=motion, is_visible=True)
        grid_data = GridData(
            grid_mode=GridMode.DIAMOND, center_x=475.0, center_y=475.0, radius=100.0
        )
        pictograph = PictographData(
            grid_data=grid_data, arrows={"blue": arrow}, is_blank=False
        )

        arrow_service.calculate_arrow_position(arrow, pictograph)

        # Test prop service
        beat_data = BeatData(
            beat_number=1,
            letter="G",
            blue_motion=motion,
            red_motion=motion,
        )

        prop_service.calculate_separation_offsets(beat_data)

        # Verify events from both services
        assert len(self.events_received) >= 2

        sources = {event["source"] for event in self.events_received}
        assert "ArrowManagementService" in sources
        assert "PropManagementService" in sources

        # Clean up
        self.event_bus.unsubscribe(arrow_sub)
        self.event_bus.unsubscribe(prop_sub)

    def test_event_subscription_cleanup(self):
        """Test that services properly clean up event subscriptions."""
        # Create service
        service = ArrowManagementService(event_bus=self.event_bus)

        # Verify service has subscription tracking
        assert hasattr(service, "_subscription_ids")
        assert isinstance(service._subscription_ids, list)

        # Test cleanup method
        service.cleanup()

        # Verify subscriptions were cleared
        assert len(service._subscription_ids) == 0

    def test_event_bus_message_routing(self):
        """Test that event bus correctly routes messages to subscribers."""
        # Create multiple subscribers for the same event type
        logger1 = self._create_event_logger("test1")
        logger2 = self._create_event_logger("test2")

        sub1 = self.event_bus.subscribe("arrow.positioned", logger1)
        sub2 = self.event_bus.subscribe("arrow.positioned", logger2)

        # Create service and trigger event
        service = ArrowManagementService(event_bus=self.event_bus)

        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
        )

        arrow = ArrowData(color="blue", motion_data=motion, is_visible=True)
        grid_data = GridData(
            grid_mode=GridMode.DIAMOND, center_x=475.0, center_y=475.0, radius=100.0
        )
        pictograph = PictographData(
            grid_data=grid_data, arrows={"blue": arrow}, is_blank=False
        )

        service.calculate_arrow_position(arrow, pictograph)

        # Verify both subscribers received the event
        assert len(self.events_received) == 2

        # Clean up
        self.event_bus.unsubscribe(sub1)
        self.event_bus.unsubscribe(sub2)

    def test_event_data_integrity(self):
        """Test that event data maintains integrity across the event flow."""
        # Subscribe to events
        logger = self._create_event_logger("arrow.positioned")
        sub_id = self.event_bus.subscribe("arrow.positioned", logger)

        # Create service
        service = ArrowManagementService(event_bus=self.event_bus)

        # Create test data with specific values
        motion = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.NORTHEAST,
            end_loc=Location.SOUTHWEST,
            turns=2.5,
        )

        arrow = ArrowData(color="red", motion_data=motion, is_visible=True)
        grid_data = GridData(
            grid_mode=GridMode.BOX, center_x=400.0, center_y=300.0, radius=150.0
        )
        pictograph = PictographData(
            grid_data=grid_data, arrows={"red": arrow}, is_blank=False
        )

        # Calculate position
        x, y, rotation = service.calculate_arrow_position(arrow, pictograph)

        # Verify event data matches input
        assert len(self.events_received) == 1
        event = self.events_received[0]["data"]

        assert event.arrow_color == "red"
        assert event.position_data["motion_type"] == "anti"
        assert event.position_data["arrow_location"] == "northeast"
        assert event.position_data["x"] == x
        assert event.position_data["y"] == y
        assert event.position_data["rotation"] == rotation

        # Clean up
        self.event_bus.unsubscribe(sub_id)
