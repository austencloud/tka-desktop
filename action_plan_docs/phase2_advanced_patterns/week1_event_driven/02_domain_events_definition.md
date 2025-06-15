# **Task 2.2: Domain Events Definition**

**Timeline**: Week 1 of Phase 2  
**Priority**: HIGH  
**Goal**: Define comprehensive domain events for TKA application state changes

---

## **Create Event Types:**

### **FILE: src/core/events/domain_events.py**

```python
"""
Domain events for TKA application.
These events represent significant business state changes.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Any, Tuple
from datetime import datetime
import uuid

from src.core.events.event_bus import BaseEvent
from src.domain.models.core_models import BeatData, SequenceData, MotionData
from src.domain.models.pictograph_models import PictographData

# === Sequence Events ===

@dataclass(frozen=True)
class SequenceCreatedEvent(BaseEvent):
    """Published when a new sequence is created."""
    sequence: SequenceData

@dataclass(frozen=True)
class SequenceUpdatedEvent(BaseEvent):
    """Published when sequence data changes."""
    sequence: SequenceData
    previous_sequence: Optional[SequenceData] = None
    change_type: str = "general"  # "beat_added", "beat_removed", "beat_updated", etc.

@dataclass(frozen=True)
class SequenceDeletedEvent(BaseEvent):
    """Published when a sequence is deleted."""
    sequence_id: str
    sequence_name: str

@dataclass(frozen=True)
class SequenceLoadedEvent(BaseEvent):
    """Published when a sequence is loaded from storage."""
    sequence: SequenceData
    load_source: str  # "file", "database", "import", etc.

@dataclass(frozen=True)
class SequenceSavedEvent(BaseEvent):
    """Published when a sequence is saved to storage."""
    sequence: SequenceData
    save_destination: str  # "file", "database", "export", etc.

# === Beat Events ===

@dataclass(frozen=True)
class BeatSelectedEvent(BaseEvent):
    """Published when a beat is selected in the UI."""
    beat: BeatData
    beat_index: int
    sequence_id: str

@dataclass(frozen=True)
class BeatUpdatedEvent(BaseEvent):
    """Published when beat data changes."""
    beat: BeatData
    beat_index: int
    sequence_id: str
    field_changed: str  # "letter", "duration", "blue_motion", etc.
    previous_value: Optional[Any] = None

@dataclass(frozen=True)
class BeatCreatedEvent(BaseEvent):
    """Published when a new beat is added."""
    beat: BeatData
    beat_index: int
    sequence_id: str

@dataclass(frozen=True)
class BeatDeletedEvent(BaseEvent):
    """Published when a beat is removed."""
    beat_id: str
    beat_index: int
    sequence_id: str
    deleted_beat: BeatData  # Preserve for undo functionality

@dataclass(frozen=True)
class BeatMovedEvent(BaseEvent):
    """Published when a beat is moved to a different position."""
    beat: BeatData
    old_index: int
    new_index: int
    sequence_id: str

@dataclass(frozen=True)
class BeatDuplicatedEvent(BaseEvent):
    """Published when a beat is duplicated."""
    original_beat: BeatData
    duplicated_beat: BeatData
    original_index: int
    new_index: int
    sequence_id: str

# === Motion Events ===

@dataclass(frozen=True)
class MotionGeneratedEvent(BaseEvent):
    """Published when new motion is generated."""
    motion: MotionData
    beat_index: int
    color: str  # "blue" or "red"
    sequence_id: str
    generation_method: str  # "manual", "random", "smart_fill", etc.

@dataclass(frozen=True)
class MotionValidationEvent(BaseEvent):
    """Published when motion validation occurs."""
    motion: MotionData
    is_valid: bool
    validation_errors: List[str] = field(default_factory=list)
    sequence_id: str
    beat_index: int

@dataclass(frozen=True)
class MotionClearedEvent(BaseEvent):
    """Published when motion is cleared from a beat."""
    previous_motion: MotionData
    beat_index: int
    color: str
    sequence_id: str

@dataclass(frozen=True)
class MotionCopiedEvent(BaseEvent):
    """Published when motion is copied between beats."""
    motion: MotionData
    source_beat_index: int
    target_beat_index: int
    color: str
    sequence_id: str

# === Pictograph Events ===

@dataclass(frozen=True)
class PictographUpdatedEvent(BaseEvent):
    """Published when pictograph visualization changes."""
    pictograph: PictographData
    beat_index: int
    sequence_id: str
    update_type: str  # "position", "visibility", "styling", etc.

@dataclass(frozen=True)
class PictographGeneratedEvent(BaseEvent):
    """Published when pictograph is generated from motion data."""
    pictograph: PictographData
    beat_index: int
    sequence_id: str
    generation_time_ms: float

@dataclass(frozen=True)
class PictographRenderingStartedEvent(BaseEvent):
    """Published when pictograph rendering begins."""
    beat_index: int
    sequence_id: str
    render_mode: str  # "full", "preview", "thumbnail"

@dataclass(frozen=True)
class PictographRenderingCompletedEvent(BaseEvent):
    """Published when pictograph rendering completes."""
    pictograph: PictographData
    beat_index: int
    sequence_id: str
    render_time_ms: float
    render_mode: str

@dataclass(frozen=True)
class PictographExportedEvent(BaseEvent):
    """Published when pictograph is exported."""
    pictograph: PictographData
    beat_index: int
    sequence_id: str
    export_format: str  # "svg", "png", "pdf", etc.
    export_path: str

# === UI State Events ===

@dataclass(frozen=True)
class UIStateChangedEvent(BaseEvent):
    """Published when UI state changes."""
    state_key: str
    new_value: Any
    previous_value: Optional[Any] = None

@dataclass(frozen=True)
class ComponentResizedEvent(BaseEvent):
    """Published when layout components are resized."""
    component_name: str
    new_size: Tuple[int, int]
    previous_size: Optional[Tuple[int, int]] = None

@dataclass(frozen=True)
class TabChangedEvent(BaseEvent):
    """Published when user switches tabs."""
    new_tab: str
    previous_tab: Optional[str] = None

@dataclass(frozen=True)
class ViewModeChangedEvent(BaseEvent):
    """Published when view mode changes."""
    new_mode: str  # "edit", "preview", "browse", etc.
    previous_mode: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class SelectionChangedEvent(BaseEvent):
    """Published when selection changes in UI."""
    selection_type: str  # "beat", "sequence", "motion", etc.
    selected_items: List[str]  # IDs of selected items
    previous_selection: Optional[List[str]] = None

# === Navigation Events ===

@dataclass(frozen=True)
class NavigationEvent(BaseEvent):
    """Published when user navigates within the application."""
    navigation_type: str  # "forward", "backward", "jump"
    destination: str
    source: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class BrowseNavigationEvent(BaseEvent):
    """Published when navigating in browse mode."""
    sequence_id: str
    beat_index: Optional[int] = None
    navigation_direction: str  # "next", "previous", "first", "last", "jump"

# === Application Events ===

@dataclass(frozen=True)
class ApplicationStartedEvent(BaseEvent):
    """Published when application completes initialization."""
    version: str
    startup_time_ms: float

@dataclass(frozen=True)
class ApplicationShuttingDownEvent(BaseEvent):
    """Published when application begins shutdown."""
    shutdown_reason: str  # "user_request", "error", "system"

@dataclass(frozen=True)
class ErrorOccurredEvent(BaseEvent):
    """Published when recoverable errors occur."""
    error_type: str
    error_message: str
    component: str
    stack_trace: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class PerformanceWarningEvent(BaseEvent):
    """Published when performance issues are detected."""
    operation: str
    duration_ms: float
    threshold_ms: float
    component: str
    details: Dict[str, Any] = field(default_factory=dict)

# === File System Events ===

@dataclass(frozen=True)
class FileOpenedEvent(BaseEvent):
    """Published when a file is opened."""
    file_path: str
    file_type: str  # "sequence", "dictionary", "config", etc.
    file_size_bytes: int

@dataclass(frozen=True)
class FileSavedEvent(BaseEvent):
    """Published when a file is saved."""
    file_path: str
    file_type: str
    file_size_bytes: int
    save_duration_ms: float

@dataclass(frozen=True)
class FileExportedEvent(BaseEvent):
    """Published when content is exported to file."""
    file_path: str
    export_type: str  # "sequence", "pictograph", "video", etc.
    export_format: str
    item_count: int

# === User Interaction Events ===

@dataclass(frozen=True)
class UserActionEvent(BaseEvent):
    """Published when user performs significant actions."""
    action_type: str  # "create", "edit", "delete", "copy", etc.
    target_type: str  # "beat", "sequence", "motion", etc.
    target_id: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class UndoRedoEvent(BaseEvent):
    """Published when undo/redo operations occur."""
    operation: str  # "undo" or "redo"
    command_description: str
    affected_items: List[str]

@dataclass(frozen=True)
class KeyboardShortcutEvent(BaseEvent):
    """Published when keyboard shortcuts are used."""
    shortcut: str  # "Ctrl+Z", "Ctrl+C", etc.
    action: str
    context: str  # "sequence_editor", "beat_editor", etc.

# === Validation Events ===

@dataclass(frozen=True)
class ValidationStartedEvent(BaseEvent):
    """Published when validation begins."""
    validation_type: str  # "sequence", "motion", "export", etc.
    target_id: str

@dataclass(frozen=True)
class ValidationCompletedEvent(BaseEvent):
    """Published when validation completes."""
    validation_type: str
    target_id: str
    is_valid: bool
    issues: List[str] = field(default_factory=list)
    validation_time_ms: float

# === Dictionary Events ===

@dataclass(frozen=True)
class DictionarySearchEvent(BaseEvent):
    """Published when dictionary search is performed."""
    search_term: str
    result_count: int
    search_time_ms: float

@dataclass(frozen=True)
class DictionaryEntrySelectedEvent(BaseEvent):
    """Published when dictionary entry is selected."""
    entry_id: str
    entry_name: str
    selection_method: str  # "click", "keyboard", "search"

# === Settings Events ===

@dataclass(frozen=True)
class SettingsChangedEvent(BaseEvent):
    """Published when application settings change."""
    setting_key: str
    new_value: Any
    previous_value: Optional[Any] = None
    requires_restart: bool = False

@dataclass(frozen=True)
class ThemeChangedEvent(BaseEvent):
    """Published when UI theme changes."""
    new_theme: str
    previous_theme: Optional[str] = None

# === Progress Events ===

@dataclass(frozen=True)
class ProgressStartedEvent(BaseEvent):
    """Published when long-running operation starts."""
    operation_id: str
    operation_name: str
    total_steps: Optional[int] = None

@dataclass(frozen=True)
class ProgressUpdatedEvent(BaseEvent):
    """Published when operation progress updates."""
    operation_id: str
    current_step: int
    total_steps: Optional[int] = None
    progress_percentage: float
    status_message: str = ""

@dataclass(frozen=True)
class ProgressCompletedEvent(BaseEvent):
    """Published when long-running operation completes."""
    operation_id: str
    operation_name: str
    success: bool
    duration_ms: float
    result_summary: str = ""
```

---

## **Event Categories and Organization:**

### **Event Category Helpers:**

```python
# FILE: src/core/events/event_categories.py

"""
Event categorization and helper functions for organizing events.
"""

from typing import Type, List, Set
from .domain_events import *

class EventCategories:
    """Categorizes events for easier management."""

    # Core business events
    SEQUENCE_EVENTS: Set[Type[BaseEvent]] = {
        SequenceCreatedEvent,
        SequenceUpdatedEvent,
        SequenceDeletedEvent,
        SequenceLoadedEvent,
        SequenceSavedEvent
    }

    BEAT_EVENTS: Set[Type[BaseEvent]] = {
        BeatSelectedEvent,
        BeatUpdatedEvent,
        BeatCreatedEvent,
        BeatDeletedEvent,
        BeatMovedEvent,
        BeatDuplicatedEvent
    }

    MOTION_EVENTS: Set[Type[BaseEvent]] = {
        MotionGeneratedEvent,
        MotionValidationEvent,
        MotionClearedEvent,
        MotionCopiedEvent
    }

    PICTOGRAPH_EVENTS: Set[Type[BaseEvent]] = {
        PictographUpdatedEvent,
        PictographGeneratedEvent,
        PictographRenderingStartedEvent,
        PictographRenderingCompletedEvent,
        PictographExportedEvent
    }

    # UI and interaction events
    UI_EVENTS: Set[Type[BaseEvent]] = {
        UIStateChangedEvent,
        ComponentResizedEvent,
        TabChangedEvent,
        ViewModeChangedEvent,
        SelectionChangedEvent
    }

    NAVIGATION_EVENTS: Set[Type[BaseEvent]] = {
        NavigationEvent,
        BrowseNavigationEvent
    }

    USER_INTERACTION_EVENTS: Set[Type[BaseEvent]] = {
        UserActionEvent,
        UndoRedoEvent,
        KeyboardShortcutEvent
    }

    # System events
    APPLICATION_EVENTS: Set[Type[BaseEvent]] = {
        ApplicationStartedEvent,
        ApplicationShuttingDownEvent,
        ErrorOccurredEvent,
        PerformanceWarningEvent
    }

    FILE_EVENTS: Set[Type[BaseEvent]] = {
        FileOpenedEvent,
        FileSavedEvent,
        FileExportedEvent
    }

    VALIDATION_EVENTS: Set[Type[BaseEvent]] = {
        ValidationStartedEvent,
        ValidationCompletedEvent
    }

    PROGRESS_EVENTS: Set[Type[BaseEvent]] = {
        ProgressStartedEvent,
        ProgressUpdatedEvent,
        ProgressCompletedEvent
    }

    # Settings and configuration
    SETTINGS_EVENTS: Set[Type[BaseEvent]] = {
        SettingsChangedEvent,
        ThemeChangedEvent
    }

    # Dictionary specific
    DICTIONARY_EVENTS: Set[Type[BaseEvent]] = {
        DictionarySearchEvent,
        DictionaryEntrySelectedEvent
    }

    @classmethod
    def get_all_events(cls) -> Set[Type[BaseEvent]]:
        """Get all defined event types."""
        all_events = set()
        for category_events in [
            cls.SEQUENCE_EVENTS,
            cls.BEAT_EVENTS,
            cls.MOTION_EVENTS,
            cls.PICTOGRAPH_EVENTS,
            cls.UI_EVENTS,
            cls.NAVIGATION_EVENTS,
            cls.USER_INTERACTION_EVENTS,
            cls.APPLICATION_EVENTS,
            cls.FILE_EVENTS,
            cls.VALIDATION_EVENTS,
            cls.PROGRESS_EVENTS,
            cls.SETTINGS_EVENTS,
            cls.DICTIONARY_EVENTS
        ]:
            all_events.update(category_events)
        return all_events

    @classmethod
    def get_category_for_event(cls, event_type: Type[BaseEvent]) -> Optional[str]:
        """Get category name for an event type."""
        category_map = {
            "SEQUENCE": cls.SEQUENCE_EVENTS,
            "BEAT": cls.BEAT_EVENTS,
            "MOTION": cls.MOTION_EVENTS,
            "PICTOGRAPH": cls.PICTOGRAPH_EVENTS,
            "UI": cls.UI_EVENTS,
            "NAVIGATION": cls.NAVIGATION_EVENTS,
            "USER_INTERACTION": cls.USER_INTERACTION_EVENTS,
            "APPLICATION": cls.APPLICATION_EVENTS,
            "FILE": cls.FILE_EVENTS,
            "VALIDATION": cls.VALIDATION_EVENTS,
            "PROGRESS": cls.PROGRESS_EVENTS,
            "SETTINGS": cls.SETTINGS_EVENTS,
            "DICTIONARY": cls.DICTIONARY_EVENTS
        }

        for category_name, category_events in category_map.items():
            if event_type in category_events:
                return category_name

        return None

    @classmethod
    def get_business_events(cls) -> Set[Type[BaseEvent]]:
        """Get events that represent core business state changes."""
        return (cls.SEQUENCE_EVENTS |
                cls.BEAT_EVENTS |
                cls.MOTION_EVENTS |
                cls.PICTOGRAPH_EVENTS)

    @classmethod
    def get_ui_events(cls) -> Set[Type[BaseEvent]]:
        """Get events related to UI state and user interaction."""
        return (cls.UI_EVENTS |
                cls.NAVIGATION_EVENTS |
                cls.USER_INTERACTION_EVENTS)

    @classmethod
    def get_system_events(cls) -> Set[Type[BaseEvent]]:
        """Get events related to system operations."""
        return (cls.APPLICATION_EVENTS |
                cls.FILE_EVENTS |
                cls.VALIDATION_EVENTS |
                cls.PROGRESS_EVENTS)
```

---

## **Event Validation and Utilities:**

### **Event Validation:**

```python
# FILE: src/core/events/event_validation.py

"""
Validation utilities for domain events.
"""

from typing import Type, List, Optional
import logging
from .domain_events import BaseEvent

class EventValidator:
    """Validates domain events for consistency and completeness."""

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def validate_event(self, event: BaseEvent) -> Tuple[bool, List[str]]:
        """Validate an event instance."""
        errors = []

        # Basic validation
        if not hasattr(event, 'timestamp') or event.timestamp <= 0:
            errors.append("Invalid timestamp")

        if not hasattr(event, 'source_component') or not event.source_component:
            errors.append("Missing source_component")

        if not hasattr(event, 'event_id') or not event.event_id:
            errors.append("Missing event_id")

        # Event-specific validation
        event_errors = self._validate_event_specific(event)
        errors.extend(event_errors)

        return len(errors) == 0, errors

    def _validate_event_specific(self, event: BaseEvent) -> List[str]:
        """Validate specific event types."""
        errors = []

        # Sequence events
        if isinstance(event, SequenceCreatedEvent):
            if not event.sequence:
                errors.append("SequenceCreatedEvent: Missing sequence data")
            elif not event.sequence.id:
                errors.append("SequenceCreatedEvent: Sequence missing ID")

        elif isinstance(event, BeatUpdatedEvent):
            if not event.beat or not event.sequence_id:
                errors.append("BeatUpdatedEvent: Missing beat or sequence_id")
            if event.beat_index < 0:
                errors.append("BeatUpdatedEvent: Invalid beat_index")

        elif isinstance(event, MotionGeneratedEvent):
            if not event.motion or not event.sequence_id:
                errors.append("MotionGeneratedEvent: Missing motion or sequence_id")
            if event.color not in ["blue", "red"]:
                errors.append("MotionGeneratedEvent: Invalid color")

        # Add more specific validations as needed

        return errors

    def validate_event_sequence(self, events: List[BaseEvent]) -> Tuple[bool, List[str]]:
        """Validate a sequence of events for logical consistency."""
        errors = []

        # Check timestamp ordering
        for i in range(1, len(events)):
            if events[i].timestamp < events[i-1].timestamp:
                errors.append(f"Event {i} has timestamp before previous event")

        # Check for logical consistency (e.g., can't update a deleted sequence)
        sequence_states = {}  # Track sequence states

        for event in events:
            if isinstance(event, SequenceCreatedEvent):
                sequence_states[event.sequence.id] = "created"
            elif isinstance(event, SequenceDeletedEvent):
                if event.sequence_id not in sequence_states:
                    errors.append(f"Attempting to delete non-existent sequence: {event.sequence_id}")
                else:
                    sequence_states[event.sequence_id] = "deleted"
            elif isinstance(event, (SequenceUpdatedEvent, BeatCreatedEvent, BeatUpdatedEvent)):
                sequence_id = getattr(event, 'sequence_id', getattr(event, 'sequence', {}).get('id'))
                if sequence_id and sequence_states.get(sequence_id) == "deleted":
                    errors.append(f"Attempting to modify deleted sequence: {sequence_id}")

        return len(errors) == 0, errors
```

---

## **Event Factory:**

### **Event Creation Helpers:**

```python
# FILE: src/core/events/event_factory.py

"""
Factory for creating domain events with proper initialization.
"""

import time
import uuid
from typing import Optional, Any, Dict
from .domain_events import *

class EventFactory:
    """Factory for creating properly initialized domain events."""

    @staticmethod
    def create_sequence_created(sequence: SequenceData,
                              source_component: str) -> SequenceCreatedEvent:
        """Create a SequenceCreatedEvent."""
        return SequenceCreatedEvent(
            timestamp=time.time(),
            source_component=source_component,
            event_id=str(uuid.uuid4()),
            sequence=sequence
        )

    @staticmethod
    def create_beat_updated(beat: BeatData,
                           beat_index: int,
                           sequence_id: str,
                           field_changed: str,
                           previous_value: Optional[Any],
                           source_component: str) -> BeatUpdatedEvent:
        """Create a BeatUpdatedEvent."""
        return BeatUpdatedEvent(
            timestamp=time.time(),
            source_component=source_component,
            event_id=str(uuid.uuid4()),
            beat=beat,
            beat_index=beat_index,
            sequence_id=sequence_id,
            field_changed=field_changed,
            previous_value=previous_value
        )

    @staticmethod
    def create_motion_generated(motion: MotionData,
                              beat_index: int,
                              color: str,
                              sequence_id: str,
                              generation_method: str,
                              source_component: str) -> MotionGeneratedEvent:
        """Create a MotionGeneratedEvent."""
        return MotionGeneratedEvent(
            timestamp=time.time(),
            source_component=source_component,
            event_id=str(uuid.uuid4()),
            motion=motion,
            beat_index=beat_index,
            color=color,
            sequence_id=sequence_id,
            generation_method=generation_method
        )

    @staticmethod
    def create_ui_state_changed(state_key: str,
                              new_value: Any,
                              previous_value: Optional[Any],
                              source_component: str) -> UIStateChangedEvent:
        """Create a UIStateChangedEvent."""
        return UIStateChangedEvent(
            timestamp=time.time(),
            source_component=source_component,
            event_id=str(uuid.uuid4()),
            state_key=state_key,
            new_value=new_value,
            previous_value=previous_value
        )

    @staticmethod
    def create_error_occurred(error_type: str,
                            error_message: str,
                            component: str,
                            stack_trace: Optional[str] = None,
                            context: Optional[Dict[str, Any]] = None,
                            source_component: str = "ErrorHandler") -> ErrorOccurredEvent:
        """Create an ErrorOccurredEvent."""
        return ErrorOccurredEvent(
            timestamp=time.time(),
            source_component=source_component,
            event_id=str(uuid.uuid4()),
            error_type=error_type,
            error_message=error_message,
            component=component,
            stack_trace=stack_trace,
            context=context or {}
        )

    @staticmethod
    def create_progress_updated(operation_id: str,
                              current_step: int,
                              total_steps: Optional[int],
                              progress_percentage: float,
                              status_message: str = "",
                              source_component: str = "ProgressTracker") -> ProgressUpdatedEvent:
        """Create a ProgressUpdatedEvent."""
        return ProgressUpdatedEvent(
            timestamp=time.time(),
            source_component=source_component,
            event_id=str(uuid.uuid4()),
            operation_id=operation_id,
            current_step=current_step,
            total_steps=total_steps,
            progress_percentage=progress_percentage,
            status_message=status_message
        )

    # Add more factory methods as needed for common events

    @staticmethod
    def create_generic_event(event_class: Type[BaseEvent],
                           source_component: str,
                           **kwargs) -> BaseEvent:
        """Create any event type with automatic timestamp and ID."""
        return event_class(
            timestamp=time.time(),
            source_component=source_component,
            event_id=str(uuid.uuid4()),
            **kwargs
        )
```

---

## **Testing Domain Events:**

### **FILE: tests/specification/core/test_domain_events.py**

```python
"""
Tests for domain events definition and validation.
"""

import pytest
import time
from src.core.events.domain_events import *
from src.core.events.event_categories import EventCategories
from src.core.events.event_validation import EventValidator
from src.core.events.event_factory import EventFactory

class TestDomainEvents:

    def test_event_creation(self):
        """Test basic event creation."""
        sequence_data = SequenceData(id="test_seq", name="Test Sequence")

        event = SequenceCreatedEvent(
            timestamp=time.time(),
            source_component="test",
            sequence=sequence_data
        )

        assert event.sequence.id == "test_seq"
        assert event.sequence.name == "Test Sequence"
        assert event.source_component == "test"
        assert event.timestamp > 0

    def test_event_immutability(self):
        """Test that events are immutable."""
        sequence_data = SequenceData(id="test_seq", name="Test Sequence")

        event = SequenceCreatedEvent(
            timestamp=time.time(),
            source_component="test",
            sequence=sequence_data
        )

        # Should not be able to modify event
        with pytest.raises(AttributeError):
            event.timestamp = time.time()

    def test_event_categories(self):
        """Test event categorization."""
        # Test sequence events
        assert SequenceCreatedEvent in EventCategories.SEQUENCE_EVENTS
        assert BeatCreatedEvent in EventCategories.BEAT_EVENTS
        assert MotionGeneratedEvent in EventCategories.MOTION_EVENTS

        # Test category detection
        category = EventCategories.get_category_for_event(SequenceCreatedEvent)
        assert category == "SEQUENCE"

    def test_event_validation(self):
        """Test event validation."""
        validator = EventValidator()

        # Valid event
        valid_event = SequenceCreatedEvent(
            timestamp=time.time(),
            source_component="test",
            sequence=SequenceData(id="test", name="Test")
        )

        is_valid, errors = validator.validate_event(valid_event)
        assert is_valid
        assert len(errors) == 0

        # Invalid event (missing timestamp)
        invalid_event = SequenceCreatedEvent(
            timestamp=0,  # Invalid
            source_component="test",
            sequence=SequenceData(id="test", name="Test")
        )

        is_valid, errors = validator.validate_event(invalid_event)
        assert not is_valid
        assert "Invalid timestamp" in errors

    def test_event_factory(self):
        """Test event factory methods."""
        sequence_data = SequenceData(id="test", name="Test")

        event = EventFactory.create_sequence_created(
            sequence=sequence_data,
            source_component="test_component"
        )

        assert isinstance(event, SequenceCreatedEvent)
        assert event.sequence.id == "test"
        assert event.source_component == "test_component"
        assert event.timestamp > 0
        assert event.event_id is not None

    def test_business_vs_ui_events(self):
        """Test distinction between business and UI events."""
        business_events = EventCategories.get_business_events()
        ui_events = EventCategories.get_ui_events()

        # Should be no overlap
        assert len(business_events.intersection(ui_events)) == 0

        # Sequence events should be business events
        assert SequenceCreatedEvent in business_events
        assert SequenceCreatedEvent not in ui_events

        # UI events should be UI events
        assert UIStateChangedEvent in ui_events
        assert UIStateChangedEvent not in business_events
```

---

## **Success Criteria:**

By the end of Task 2.2:

- ✅ **Comprehensive domain events** defined for all TKA operations
- ✅ **Event categories** organized for easy management
- ✅ **Event validation** ensures data integrity
- ✅ **Event factory** simplifies event creation
- ✅ **Immutable events** prevent accidental modification
- ✅ **Clear separation** between business and UI events

---

## **Next Step**

After completing domain events definition, proceed to: [Task 2.3: Event-Driven Service Integration](03_event_driven_services.md)
