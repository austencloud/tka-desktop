"""
TKA-specific domain events for sequence, motion, and layout operations.
These events replace direct method calls between services.
"""

from dataclasses import dataclass, field
from typing import Optional, Any, Dict, List
from datetime import datetime
import uuid
from .event_bus import BaseEvent, EventPriority


# === Sequence Domain Events ===


@dataclass(frozen=True)
class SequenceCreatedEvent(BaseEvent):
    """Published when a new sequence is created."""

    sequence_id: str = ""
    sequence_name: str = ""
    sequence_length: int = 0

    @property
    def event_type(self) -> str:
        return "sequence.created"


@dataclass(frozen=True)
class SequenceUpdatedEvent(BaseEvent):
    """Published when sequence data changes."""

    sequence_id: str = ""
    change_type: str = (
        ""  # "beat_added", "beat_removed", "beat_updated", "metadata_changed"
    )
    previous_state: Optional[Dict[str, Any]] = None
    new_state: Optional[Dict[str, Any]] = None

    @property
    def event_type(self) -> str:
        return f"sequence.{self.change_type}"


@dataclass(frozen=True)
class BeatAddedEvent(BaseEvent):
    """Published when a beat is added to a sequence."""

    sequence_id: str = ""
    beat_data: Dict[str, Any] = field(default_factory=dict)
    beat_position: int = 0
    total_beats: int = 0

    @property
    def event_type(self) -> str:
        return "sequence.beat_added"


@dataclass(frozen=True)
class BeatUpdatedEvent(BaseEvent):
    """Published when a beat's data changes."""

    sequence_id: str = ""
    beat_number: int = 0
    field_changed: str = ""  # "letter", "blue_motion", "red_motion", etc.
    old_value: Any = None
    new_value: Any = None

    @property
    def event_type(self) -> str:
        return "sequence.beat_updated"


@dataclass(frozen=True)
class BeatRemovedEvent(BaseEvent):
    """Published when a beat is removed from a sequence."""

    sequence_id: str = ""
    removed_beat_data: Dict[str, Any] = field(default_factory=dict)
    old_position: int = 0
    remaining_beats: int = 0

    @property
    def event_type(self) -> str:
        return "sequence.beat_removed"


# === Motion Domain Events ===


@dataclass(frozen=True)
class MotionValidatedEvent(BaseEvent):
    """Published when motion validation occurs."""

    motion_id: str = ""
    motion_data: Dict[str, Any] = field(default_factory=dict)
    is_valid: bool = False
    validation_errors: List[str] = field(default_factory=list)

    @property
    def event_type(self) -> str:
        return "motion.validated"


# === Layout Domain Events ===


@dataclass(frozen=True)
class LayoutRecalculatedEvent(BaseEvent):
    """Published when layout is recalculated."""

    layout_type: str = ""  # "beat_frame", "component", "responsive"
    layout_data: Dict[str, Any] = field(default_factory=dict)
    trigger_reason: str = ""  # "sequence_changed", "window_resized", "manual"

    @property
    def event_type(self) -> str:
        return f"layout.{self.layout_type}_recalculated"


@dataclass(frozen=True)
class ComponentResizedEvent(BaseEvent):
    """Published when UI components are resized."""

    component_name: str = ""
    old_size: tuple[int, int] = (0, 0)
    new_size: tuple[int, int] = (0, 0)

    @property
    def event_type(self) -> str:
        return "layout.component_resized"


# === Arrow/Pictograph Domain Events ===


@dataclass(frozen=True)
class ArrowPositionedEvent(BaseEvent):
    """Published when arrow positioning is calculated."""

    sequence_id: str = ""
    beat_number: int = 0
    arrow_color: str = ""
    position_data: Dict[str, Any] = field(default_factory=dict)

    @property
    def event_type(self) -> str:
        return "arrow.positioned"


@dataclass(frozen=True)
class PropPositionedEvent(BaseEvent):
    """Published when prop positioning or separation is calculated."""

    sequence_id: str = ""
    beat_number: int = 0
    prop_color: str = ""
    positioning_type: str = ""  # "beta_positioning", "separation", "overlap_detected"
    position_data: Dict[str, Any] = field(default_factory=dict)

    @property
    def event_type(self) -> str:
        return f"prop.{self.positioning_type}"


@dataclass(frozen=True)
class PictographUpdatedEvent(BaseEvent):
    """Published when pictograph visualization changes."""

    sequence_id: str = ""
    beat_number: int = 0
    update_type: str = ""  # "arrows", "glyphs", "background", "all"

    @property
    def event_type(self) -> str:
        return f"pictograph.{self.update_type}_updated"


# === UI State Events ===


@dataclass(frozen=True)
class UIStateChangedEvent(BaseEvent):
    """Published when UI state changes."""

    component: str = ""
    state_key: str = ""
    old_value: Any = None
    new_value: Any = None

    @property
    def event_type(self) -> str:
        return f"ui.{self.component}.state_changed"


# === Command Events (for undo/redo) ===


@dataclass(frozen=True)
class CommandExecutedEvent(BaseEvent):
    """Published when a command is executed."""

    command_id: str = ""
    command_type: str = ""
    command_description: str = ""
    can_undo: bool = False
    can_redo: bool = False

    @property
    def event_type(self) -> str:
        return "command.executed"


@dataclass(frozen=True)
class CommandUndoneEvent(BaseEvent):
    """Published when a command is undone."""

    command_id: str = ""
    command_type: str = ""
    command_description: str = ""
    can_undo: bool = False
    can_redo: bool = False

    @property
    def event_type(self) -> str:
        return "command.undone"


@dataclass(frozen=True)
class CommandRedoneEvent(BaseEvent):
    """Published when a command is redone."""

    command_id: str = ""
    command_type: str = ""
    command_description: str = ""
    can_undo: bool = False
    can_redo: bool = False

    @property
    def event_type(self) -> str:
        return "command.redone"
