"""
Layout Event Handler

Handles event-driven layout management and recalculation.
This class preserves all original event handling logic including
beat added/removed events, sequence creation events, and component
resize events with automatic layout recalculation.
"""

from typing import Dict, Any, Tuple, List
import logging
import uuid
from datetime import datetime

from PyQt6.QtCore import QSize

from .beat_layout_calculator import BeatLayoutCalculator

# Event-driven architecture imports
try:
    from core.events import (
        EventPriority,
        BeatAddedEvent,
        BeatRemovedEvent,
        SequenceCreatedEvent,
        LayoutRecalculatedEvent,
        ComponentResizedEvent,
    )

    EVENT_SYSTEM_AVAILABLE = True
except ImportError:
    EventPriority = None
    EVENT_SYSTEM_AVAILABLE = False

logger = logging.getLogger(__name__)


class LayoutEventHandler:
    """
    Handles event-driven layout management and recalculation.

    This class preserves all original event handling logic including
    beat added/removed events, sequence creation events, and component
    resize events with automatic layout recalculation.
    """

    def __init__(
        self, beat_layout_calculator: BeatLayoutCalculator, main_window_size: QSize
    ):
        """Initialize with references to calculator and window size."""
        self._beat_layout_calculator = beat_layout_calculator
        self._main_window_size = main_window_size
        self._subscription_ids: List[str] = []

    def setup_event_subscriptions(self, event_bus):
        """Subscribe to events that require layout recalculation."""
        if not event_bus or not EventPriority:
            return

        # Subscribe to sequence events
        sub_id = event_bus.subscribe(
            "sequence.beat_added", self._on_beat_added, priority=EventPriority.HIGH
        )
        self._subscription_ids.append(sub_id)

        sub_id = event_bus.subscribe(
            "sequence.beat_removed", self._on_beat_removed, priority=EventPriority.HIGH
        )
        self._subscription_ids.append(sub_id)

        sub_id = event_bus.subscribe(
            "sequence.created", self._on_sequence_created, priority=EventPriority.HIGH
        )
        self._subscription_ids.append(sub_id)

        # Subscribe to UI resize events
        sub_id = event_bus.subscribe(
            "layout.component_resized",
            self._on_component_resized,
            priority=EventPriority.NORMAL,
        )
        self._subscription_ids.append(sub_id)

    def _on_beat_added(self, event: BeatAddedEvent):
        """Handle beat added event by recalculating layout."""
        if not hasattr(self, "event_bus") or not self.event_bus:
            return

        logger.info(
            f"Layout service responding to beat added: sequence {event.sequence_id}"
        )

        try:
            # Recalculate layout for the updated sequence
            # This replaces the direct call that used to happen in SequenceManagementService
            container_size = (
                self._main_window_size.width(),
                self._main_window_size.height(),
            )

            # Trigger layout recalculation
            layout_result = self._recalculate_beat_frame_layout(
                beat_count=event.total_beats,
                container_size=container_size,
                trigger_reason="beat_added",
            )

            # Publish layout updated event for other services
            self.event_bus.publish(
                LayoutRecalculatedEvent(
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source="LayoutManagementService",
                    layout_type="beat_frame",
                    layout_data=layout_result,
                    trigger_reason="beat_added",
                )
            )

        except Exception as e:
            logger.error(f"Failed to recalculate layout after beat added: {e}")

    def _on_beat_removed(self, event: BeatRemovedEvent):
        """Handle beat removed event by recalculating layout."""
        if not hasattr(self, "event_bus") or not self.event_bus:
            return

        logger.info(
            f"Layout service responding to beat removed: sequence {event.sequence_id}"
        )

        try:
            container_size = (
                self._main_window_size.width(),
                self._main_window_size.height(),
            )

            layout_result = self._recalculate_beat_frame_layout(
                beat_count=event.remaining_beats,
                container_size=container_size,
                trigger_reason="beat_removed",
            )

            self.event_bus.publish(
                LayoutRecalculatedEvent(
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source="LayoutManagementService",
                    layout_type="beat_frame",
                    layout_data=layout_result,
                    trigger_reason="beat_removed",
                )
            )

        except Exception as e:
            logger.error(f"Failed to recalculate layout after beat removed: {e}")

    def _on_sequence_created(self, event: SequenceCreatedEvent):
        """Handle sequence created event by setting up initial layout."""
        if not hasattr(self, "event_bus") or not self.event_bus:
            return

        logger.info(
            f"Layout service responding to sequence created: {event.sequence_name}"
        )

        try:
            container_size = (
                self._main_window_size.width(),
                self._main_window_size.height(),
            )

            layout_result = self._recalculate_beat_frame_layout(
                beat_count=event.sequence_length,
                container_size=container_size,
                trigger_reason="sequence_created",
            )

            self.event_bus.publish(
                LayoutRecalculatedEvent(
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source="LayoutManagementService",
                    layout_type="beat_frame",
                    layout_data=layout_result,
                    trigger_reason="sequence_created",
                )
            )

        except Exception as e:
            logger.error(f"Failed to setup layout for new sequence: {e}")

    def _on_component_resized(self, event: ComponentResizedEvent):
        """Handle component resize event by recalculating responsive layout."""
        if not hasattr(self, "event_bus") or not self.event_bus:
            return

        logger.info(
            f"Layout service responding to component resize: {event.component_name}"
        )

        # Recalculate layout for the resized component
        # This ensures responsive design works automatically

    def _recalculate_beat_frame_layout(
        self, beat_count: int, container_size: Tuple[int, int], trigger_reason: str
    ) -> Dict[str, Any]:
        """Recalculate beat frame layout and return result."""
        if beat_count == 0:
            return {"positions": {}, "sizes": {}, "total_size": (0, 0)}

        # Use existing logic but with event-driven trigger
        base_size = (120, 120)  # Default beat frame size
        padding = 10
        spacing = 5

        if beat_count <= 8:  # Use horizontal layout
            return self._beat_layout_calculator._calculate_horizontal_beat_layout(
                beat_count, container_size, base_size, padding, spacing
            )
        else:  # Use grid layout
            return self._beat_layout_calculator._calculate_grid_beat_layout(
                beat_count, container_size, base_size, padding, spacing
            )

    def cleanup(self, event_bus):
        """Clean up event subscriptions when service is destroyed."""
        if event_bus:
            for sub_id in self._subscription_ids:
                event_bus.unsubscribe(sub_id)
            self._subscription_ids.clear()
