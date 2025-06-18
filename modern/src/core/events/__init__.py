"""Event system exports for easy importing."""

from .event_bus import (
    TypeSafeEventBus,
    IEventBus,
    get_event_bus,
    reset_event_bus,
    BaseEvent,
    EventPriority,
)

from .domain_events import (
    # Sequence events
    SequenceCreatedEvent,
    SequenceUpdatedEvent,
    BeatAddedEvent,
    BeatUpdatedEvent,
    BeatRemovedEvent,
    # Motion events
    MotionValidatedEvent,
    # Layout events
    LayoutRecalculatedEvent,
    ComponentResizedEvent,
    # Arrow/Pictograph events
    ArrowPositionedEvent,
    PropPositionedEvent,
    PictographUpdatedEvent,
    # UI events
    UIStateChangedEvent,
    # Command events
    CommandExecutedEvent,
    CommandUndoneEvent,
    CommandRedoneEvent,
)

__all__ = [
    # Event bus core
    "TypeSafeEventBus",
    "IEventBus",
    "get_event_bus",
    "reset_event_bus",
    "BaseEvent",
    "EventPriority",
    # Domain events
    "SequenceCreatedEvent",
    "SequenceUpdatedEvent",
    "BeatAddedEvent",
    "BeatUpdatedEvent",
    "BeatRemovedEvent",
    "MotionValidatedEvent",
    "LayoutRecalculatedEvent",
    "ComponentResizedEvent",
    "ArrowPositionedEvent",
    "PropPositionedEvent",
    "PictographUpdatedEvent",
    "UIStateChangedEvent",
    "CommandExecutedEvent",
    "CommandUndoneEvent",
    "CommandRedoneEvent",
]
