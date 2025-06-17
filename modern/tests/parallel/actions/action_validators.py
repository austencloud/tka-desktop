"""
Action Validation System
========================

Pre/post-condition validation for user actions in parallel testing.
Ensures actions are executed in valid states and produce expected results.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: Legacy deprecation complete
PURPOSE: Validate action prerequisites and outcomes for Legacy/Modern testing
"""

from typing import Dict, Any, List, Optional, Tuple
from abc import ABC, abstractmethod
import logging
from dataclasses import dataclass

from .user_actions import UserAction, ActionType, GridPosition, MotionTypeValue


logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of action validation."""

    is_valid: bool
    errors: List[str]
    warnings: List[str]
    context: Dict[str, Any]

    def add_error(self, error: str) -> None:
        """Add validation error."""
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, warning: str) -> None:
        """Add validation warning."""
        self.warnings.append(warning)


class IActionValidator(ABC):
    """Interface for action validators."""

    @abstractmethod
    def validate_prerequisites(
        self, action: UserAction, state: Dict[str, Any]
    ) -> ValidationResult:
        """Validate action prerequisites against current state."""
        pass

    @abstractmethod
    def validate_parameters(self, action: UserAction) -> ValidationResult:
        """Validate action parameters for correctness."""
        pass

    @abstractmethod
    def validate_outcome(
        self, action: UserAction, result: Dict[str, Any]
    ) -> ValidationResult:
        """Validate action outcome against expected results."""
        pass


class BaseActionValidator(IActionValidator):
    """Base validator with common validation logic."""

    def validate_prerequisites(
        self, action: UserAction, state: Dict[str, Any]
    ) -> ValidationResult:
        """Base prerequisite validation."""
        result = ValidationResult(True, [], [], {})

        # Check if application is in valid state
        if not state.get("application_ready", False):
            result.add_error("Application not ready for action execution")

        # Check sequence state for beat-related actions
        if action.action_type in [
            ActionType.ADD_BEAT,
            ActionType.DELETE_BEAT,
            ActionType.MODIFY_MOTION,
        ]:
            if not state.get("sequence_initialized", False):
                result.add_error("Sequence not initialized for beat operations")

        return result

    def validate_parameters(self, action: UserAction) -> ValidationResult:
        """Base parameter validation."""
        result = ValidationResult(True, [], [], {})

        # Validate required parameters based on action type
        if action.action_type == ActionType.SELECT_START_POSITION:
            if not action.parameters.grid_position:
                result.add_error("Grid position required for start position selection")

        elif action.action_type == ActionType.ADJUST_TURNS:
            if action.parameters.turns is None:
                result.add_error("Turn value required for turn adjustment")
            elif not isinstance(action.parameters.turns, (int, float)):
                result.add_error("Turn value must be numeric")

        elif action.action_type == ActionType.CHANGE_MOTION_TYPE:
            if not action.parameters.motion_type:
                result.add_error("Motion type required for motion type change")

        return result

    def validate_outcome(
        self, action: UserAction, result: Dict[str, Any]
    ) -> ValidationResult:
        """Base outcome validation."""
        validation_result = ValidationResult(True, [], [], {})

        # Check execution success
        if not result.get("success", False):
            validation_result.add_error(
                f"Action execution failed: {result.get('error', 'Unknown error')}"
            )

        # Validate expected outcomes
        expected = action.expected_outcome
        actual_data = result.get("data", {})

        # Check sequence length if expected
        if expected.sequence_length is not None:
            actual_length = actual_data.get("sequence_length", 0)
            if actual_length != expected.sequence_length:
                validation_result.add_error(
                    f"Sequence length mismatch: expected {expected.sequence_length}, got {actual_length}"
                )

        # Check beat count if expected
        if expected.beat_count is not None:
            actual_beats = actual_data.get("beat_count", 0)
            if actual_beats != expected.beat_count:
                validation_result.add_error(
                    f"Beat count mismatch: expected {expected.beat_count}, got {actual_beats}"
                )

        return validation_result


class StartPositionValidator(BaseActionValidator):
    """Validator for start position selection actions."""

    def validate_prerequisites(
        self, action: UserAction, state: Dict[str, Any]
    ) -> ValidationResult:
        result = super().validate_prerequisites(action, state)

        # Check if sequence is clear for start position selection
        current_beats = state.get("beat_count", 0)
        if current_beats > 0:
            result.add_warning(
                "Selecting start position with existing beats may clear sequence"
            )

        return result

    def validate_parameters(self, action: UserAction) -> ValidationResult:
        result = super().validate_parameters(action)

        # Validate grid position
        if action.parameters.grid_position not in [
            GridPosition.ALPHA,
            GridPosition.BETA,
            GridPosition.GAMMA,
        ]:
            result.add_error("Invalid grid position for start position selection")

        return result


class BeatOperationValidator(BaseActionValidator):
    """Validator for beat-related operations."""

    def validate_prerequisites(
        self, action: UserAction, state: Dict[str, Any]
    ) -> ValidationResult:
        result = super().validate_prerequisites(action, state)

        # Check if start position is selected
        if not state.get("start_position_selected", False):
            result.add_error("Start position must be selected before beat operations")

        # For delete operations, check if beat exists
        if action.action_type == ActionType.DELETE_BEAT:
            beat_index = action.parameters.beat_index
            beat_count = state.get("beat_count", 0)
            if beat_index is None or beat_index >= beat_count:
                result.add_error(f"Invalid beat index {beat_index} for deletion")

        return result


class MotionModificationValidator(BaseActionValidator):
    """Validator for motion modification actions."""

    def validate_prerequisites(
        self, action: UserAction, state: Dict[str, Any]
    ) -> ValidationResult:
        result = super().validate_prerequisites(action, state)

        # Check if motion exists for modification
        beat_index = action.parameters.beat_index
        motion_index = action.parameters.motion_index

        if beat_index is not None:
            beat_count = state.get("beat_count", 0)
            if beat_index >= beat_count:
                result.add_error(f"Beat index {beat_index} out of range")

        return result

    def validate_parameters(self, action: UserAction) -> ValidationResult:
        result = super().validate_parameters(action)

        # Validate turn values
        if action.action_type == ActionType.ADJUST_TURNS:
            turns = action.parameters.turns
            if turns is not None and not (-10.0 <= turns <= 10.0):
                result.add_warning(
                    f"Turn value {turns} is outside typical range [-10.0, 10.0]"
                )

        return result


class GraphEditorValidator(BaseActionValidator):
    """Validator for graph editor operations."""

    def validate_prerequisites(
        self, action: UserAction, state: Dict[str, Any]
    ) -> ValidationResult:
        result = super().validate_prerequisites(action, state)

        # Check if graph editor operations require graph editor to be open
        if action.action_type in [
            ActionType.GRAPH_EDITOR_TURN_ADJUSTMENT,
            ActionType.GRAPH_EDITOR_MOTION_CHANGE,
        ]:
            if not state.get("graph_editor_open", False):
                result.add_error(
                    "Graph editor must be open for graph editor operations"
                )

        return result


class ActionValidatorFactory:
    """Factory for creating appropriate validators for actions."""

    _validators = {
        ActionType.SELECT_START_POSITION: StartPositionValidator,
        ActionType.ADD_BEAT: BeatOperationValidator,
        ActionType.DELETE_BEAT: BeatOperationValidator,
        ActionType.MODIFY_MOTION: MotionModificationValidator,
        ActionType.ADJUST_TURNS: MotionModificationValidator,
        ActionType.CHANGE_MOTION_TYPE: MotionModificationValidator,
        ActionType.TOGGLE_GRAPH_EDITOR: GraphEditorValidator,
        ActionType.GRAPH_EDITOR_TURN_ADJUSTMENT: GraphEditorValidator,
        ActionType.GRAPH_EDITOR_MOTION_CHANGE: GraphEditorValidator,
    }

    @classmethod
    def get_validator(cls, action_type: ActionType) -> IActionValidator:
        """Get appropriate validator for action type."""
        validator_class = cls._validators.get(action_type, BaseActionValidator)
        return validator_class()

    @classmethod
    def validate_action(
        cls, action: UserAction, state: Dict[str, Any]
    ) -> ValidationResult:
        """Validate action with appropriate validator."""
        validator = cls.get_validator(action.action_type)

        # Combine all validation results
        param_result = validator.validate_parameters(action)
        prereq_result = validator.validate_prerequisites(action, state)

        combined_result = ValidationResult(
            is_valid=param_result.is_valid and prereq_result.is_valid,
            errors=param_result.errors + prereq_result.errors,
            warnings=param_result.warnings + prereq_result.warnings,
            context={**param_result.context, **prereq_result.context},
        )

        return combined_result
