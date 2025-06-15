"""
Action Abstraction Layer
========================

Standardized action system for parallel testing between V1 and V2.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: V1 deprecation complete
PURPOSE: Provide standardized action abstractions for V1/V2 comparison
"""

from .user_actions import (
    ActionType,
    GridPosition,
    MotionTypeValue,
    OrientationValue,
    ActionParameters,
    ExpectedOutcome,
    UserAction,
    ActionSequence,
)

from .action_validators import (
    ValidationResult,
    IActionValidator,
    BaseActionValidator,
    StartPositionValidator,
    BeatOperationValidator,
    MotionModificationValidator,
    GraphEditorValidator,
    ActionValidatorFactory,
)

__all__ = [
    # Core action types
    "ActionType",
    "GridPosition", 
    "MotionTypeValue",
    "OrientationValue",
    
    # Action data structures
    "ActionParameters",
    "ExpectedOutcome",
    "UserAction",
    "ActionSequence",
    
    # Validation system
    "ValidationResult",
    "IActionValidator",
    "BaseActionValidator",
    "StartPositionValidator",
    "BeatOperationValidator", 
    "MotionModificationValidator",
    "GraphEditorValidator",
    "ActionValidatorFactory",
]
