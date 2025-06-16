"""
User Action Abstraction Layer
============================

Standardized action system for parallel testing between Legacy and Modern.
Provides enum-based action types, parameters, expected outcomes, and validation.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: Legacy deprecation complete
PURPOSE: Standardize user actions for Legacy/Modern comparison testing
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import uuid


class ActionType(Enum):
    """Standardized user action types for TKA testing."""

    # Start position and initialization
    SELECT_START_POSITION = auto()
    INITIALIZE_SEQUENCE = auto()
    CLEAR_SEQUENCE = auto()

    # Beat and motion operations
    ADD_BEAT = auto()
    DELETE_BEAT = auto()
    MODIFY_MOTION = auto()
    SELECT_PICTOGRAPH_OPTION = auto()

    # Motion property modifications
    ADJUST_TURNS = auto()
    CHANGE_MOTION_TYPE = auto()
    MODIFY_ORIENTATION = auto()

    # Graph editor operations
    TOGGLE_GRAPH_EDITOR = auto()
    GRAPH_EDITOR_TURN_ADJUSTMENT = auto()
    GRAPH_EDITOR_MOTION_CHANGE = auto()

    # Sequence operations
    EXPORT_SEQUENCE = auto()
    IMPORT_SEQUENCE = auto()
    SAVE_SEQUENCE = auto()
    LOAD_SEQUENCE = auto()

    # UI state operations
    CHANGE_VIEW_MODE = auto()
    TOGGLE_VISIBILITY = auto()
    RESIZE_WINDOW = auto()

    # Validation and verification
    VERIFY_STATE = auto()
    CAPTURE_SCREENSHOT = auto()
    EXTRACT_DATA = auto()


class GridPosition(Enum):
    """Grid position identifiers."""

    ALPHA = "alpha"
    BETA = "beta"
    GAMMA = "gamma"


class MotionTypeValue(Enum):
    """Motion type values for actions."""

    PRO = "pro"
    ANTI = "anti"
    DASH = "dash"
    STATIC = "static"
    FLOAT = "float"


class OrientationValue(Enum):
    """Orientation values for actions."""

    IN = "in"
    OUT = "out"
    CLOCK = "clock"
    COUNTER = "counter"


@dataclass
class ActionParameters:
    """Parameters for user actions with validation."""

    # Position parameters
    grid_position: Optional[GridPosition] = None
    beat_index: Optional[int] = None
    motion_index: Optional[int] = None

    # Motion parameters
    motion_type: Optional[MotionTypeValue] = None
    turns: Optional[float] = None
    orientation: Optional[OrientationValue] = None

    # UI parameters
    click_coordinates: Optional[tuple] = None
    key_sequence: Optional[str] = None

    # Data parameters
    pictograph_data: Optional[Dict[str, Any]] = None
    sequence_data: Optional[Dict[str, Any]] = None

    # Validation parameters
    expected_result: Optional[Dict[str, Any]] = None
    tolerance: float = 0.001
    timeout_ms: int = 5000

    # Additional context
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExpectedOutcome:
    """Expected outcome for action validation."""

    # State expectations
    sequence_length: Optional[int] = None
    beat_count: Optional[int] = None
    motion_count: Optional[int] = None

    # Data expectations
    expected_data: Optional[Dict[str, Any]] = None
    expected_ui_state: Optional[Dict[str, Any]] = None

    # Validation rules
    tolerance_rules: Dict[str, float] = field(
        default_factory=lambda: {"turns": 0.001, "position": 1.0, "rotation": 0.1}
    )

    # Success criteria
    must_match_exactly: List[str] = field(default_factory=list)
    can_have_tolerance: List[str] = field(default_factory=list)

    # Timing expectations
    max_execution_time_ms: int = 10000
    min_execution_time_ms: int = 0


@dataclass
class UserAction:
    """
    Standardized user action for parallel testing.

    Represents a single user interaction that can be executed
    on both Legacy and Modern for comparison testing.
    """

    # Core identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    action_type: ActionType = ActionType.VERIFY_STATE
    timestamp: datetime = field(default_factory=datetime.now)

    # Action configuration
    parameters: ActionParameters = field(default_factory=ActionParameters)
    expected_outcome: ExpectedOutcome = field(default_factory=ExpectedOutcome)

    # Execution context
    description: str = ""
    prerequisites: List[str] = field(default_factory=list)
    cleanup_actions: List[str] = field(default_factory=list)

    # Validation settings
    is_critical: bool = True
    retry_count: int = 0
    max_retries: int = 3

    # Metadata
    tags: List[str] = field(default_factory=list)
    category: str = "general"

    def validate_prerequisites(self, current_state: Dict[str, Any]) -> bool:
        """Validate that prerequisites are met for this action."""
        # Implementation will be added based on specific validation needs
        return True

    def is_valid_for_state(self, current_state: Dict[str, Any]) -> bool:
        """Check if this action is valid for the current application state."""
        # Implementation will be added based on state validation needs
        return True


@dataclass
class ActionSequence:
    """Sequence of related user actions."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    actions: List[UserAction] = field(default_factory=list)

    # Sequence metadata
    category: str = "workflow"
    priority: int = 1
    estimated_duration_ms: int = 30000

    # Validation settings
    stop_on_first_failure: bool = True
    allow_partial_success: bool = False

    def add_action(self, action: UserAction) -> None:
        """Add an action to the sequence."""
        self.actions.append(action)

    def get_critical_actions(self) -> List[UserAction]:
        """Get only critical actions from the sequence."""
        return [action for action in self.actions if action.is_critical]

    def estimate_total_duration(self) -> int:
        """Estimate total execution time for the sequence."""
        return sum(
            action.expected_outcome.max_execution_time_ms for action in self.actions
        )
