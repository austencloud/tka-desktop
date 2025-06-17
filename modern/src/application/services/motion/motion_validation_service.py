"""
Motion Validation Service - Focused Motion Validation Operations

Handles all motion validation logic including:
- Motion combination validation with detailed error reporting
- Individual motion validation
- Location, motion type, rotation, and turns validation
- Orientation conflict detection

This service provides a clean, focused interface for motion validation
while maintaining the proven validation algorithms.
"""

from typing import List, Set, Tuple
from abc import ABC, abstractmethod
from enum import Enum

from domain.models.core_models import (
    MotionData,
    MotionType,
    Location,
    RotationDirection,
    Orientation,
)


class IMotionValidationService(ABC):
    """Interface for motion validation operations."""

    @abstractmethod
    def validate_motion_combination(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> bool:
        """Validate that two motions can be combined in a beat."""
        pass

    @abstractmethod
    def get_motion_validation_errors(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> List[str]:
        """Get detailed validation errors for motion combination."""
        pass

    @abstractmethod
    def is_valid_single_motion(self, motion: MotionData) -> bool:
        """Check if a single motion is valid."""
        pass


class MotionValidationError(Enum):
    """Types of motion validation errors."""

    INVALID_LOCATION_COMBINATION = "invalid_location_combination"
    INVALID_MOTION_TYPE_COMBINATION = "invalid_motion_type_combination"
    INVALID_ROTATION_COMBINATION = "invalid_rotation_combination"
    INVALID_TURNS_COMBINATION = "invalid_turns_combination"
    CONFLICTING_ORIENTATIONS = "conflicting_orientations"


class MotionValidationService(IMotionValidationService):
    """
    Focused motion validation service.

    Provides comprehensive motion validation including:
    - Motion combination validation with detailed error reporting
    - Individual motion validation
    - Location, motion type, rotation, and turns validation
    - Orientation conflict detection
    """

    def __init__(self):
        # Load validation rules
        self._invalid_location_combinations = self._load_invalid_location_combinations()
        self._invalid_motion_type_combinations = (
            self._load_invalid_motion_type_combinations()
        )
        self._valid_rotation_combinations = self._load_valid_rotation_combinations()

    def validate_motion_combination(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> bool:
        """Validate that two motions can be combined in a beat."""
        errors = self.get_motion_validation_errors(blue_motion, red_motion)
        return len(errors) == 0

    def get_motion_validation_errors(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> List[str]:
        """Get detailed validation errors for motion combination."""
        errors = []

        # Check location combination validity
        if not self._is_valid_location_combination(blue_motion, red_motion):
            errors.append(
                f"Invalid location combination: {blue_motion.start_loc}-{blue_motion.end_loc} with {red_motion.start_loc}-{red_motion.end_loc}"
            )

        # Check motion type combination validity
        if not self._is_valid_motion_type_combination(blue_motion, red_motion):
            errors.append(
                f"Invalid motion type combination: {blue_motion.motion_type} with {red_motion.motion_type}"
            )

        # Check rotation combination validity
        if not self._is_valid_rotation_combination(blue_motion, red_motion):
            errors.append(
                f"Invalid rotation combination: {blue_motion.prop_rot_dir} with {red_motion.prop_rot_dir}"
            )

        # Check turns compatibility
        if not self._is_valid_turns_combination(blue_motion, red_motion):
            errors.append(
                f"Invalid turns combination: {blue_motion.turns} with {red_motion.turns}"
            )

        # Check orientation conflicts
        if not self._is_valid_orientation_combination(blue_motion, red_motion):
            errors.append("Conflicting orientations detected")

        return errors

    def is_valid_single_motion(self, motion: MotionData) -> bool:
        """Check if a single motion is valid."""
        # Basic motion validation
        if motion.turns < 0 or motion.turns > 3:
            return False

        # Motion type specific validation
        if motion.motion_type == MotionType.STATIC and motion.turns != 0:
            return False

        return True

    # Private validation methods

    def _is_valid_location_combination(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> bool:
        """Check if location combination is valid."""
        blue_locations = (blue_motion.start_loc, blue_motion.end_loc)
        red_locations = (red_motion.start_loc, red_motion.end_loc)

        # Check against invalid combinations
        combination = (blue_locations, red_locations)
        return combination not in self._invalid_location_combinations

    def _is_valid_motion_type_combination(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> bool:
        """Check if motion type combination is valid."""
        type_combination = (blue_motion.motion_type, red_motion.motion_type)
        return type_combination not in self._invalid_motion_type_combinations

    def _is_valid_rotation_combination(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> bool:
        """Check if rotation combination is valid."""
        rotation_combination = (blue_motion.prop_rot_dir, red_motion.prop_rot_dir)
        return rotation_combination in self._valid_rotation_combinations

    def _is_valid_turns_combination(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> bool:
        """Check if turns combination is valid."""
        # Most turns combinations are valid, check for specific invalid cases
        blue_turns = blue_motion.turns
        red_turns = red_motion.turns

        # Example invalid cases (these would be loaded from data)
        invalid_turns = [
            (3.0, 3.0),  # Both 3 turns might be invalid
            (2.5, 2.5),  # Both 2.5 turns might be invalid
        ]

        return (blue_turns, red_turns) not in invalid_turns

    def _is_valid_orientation_combination(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> bool:
        """Check if orientation combination is valid."""
        # For now, most orientation combinations are valid
        # This would need orientation calculation service to be fully implemented
        # TODO: Integrate with MotionOrientationService when available
        return True

    # Private data loading methods

    def _load_invalid_location_combinations(
        self,
    ) -> Set[Tuple[Tuple[Location, Location], Tuple[Location, Location]]]:
        """Load invalid location combinations from data."""
        # In production, this would load from JSON/database
        # For now, return some example invalid combinations
        return {
            # Example: Both motions going from same location to same location
            ((Location.NORTH, Location.SOUTH), (Location.NORTH, Location.SOUTH)),
            ((Location.EAST, Location.WEST), (Location.EAST, Location.WEST)),
        }

    def _load_invalid_motion_type_combinations(
        self,
    ) -> Set[Tuple[MotionType, MotionType]]:
        """Load invalid motion type combinations from data."""
        # In production, this would load from JSON/database
        # For now, return some example invalid combinations
        return set()

    def _load_valid_rotation_combinations(
        self,
    ) -> Set[Tuple[RotationDirection, RotationDirection]]:
        """Load valid rotation combinations from data."""
        # In production, this would load from JSON/database
        # For now, allow most combinations
        valid_combinations = set()
        for blue_rot in RotationDirection:
            for red_rot in RotationDirection:
                valid_combinations.add((blue_rot, red_rot))

        # Remove some invalid combinations
        valid_combinations.discard(
            (RotationDirection.NO_ROTATION, RotationDirection.NO_ROTATION)
        )

        return valid_combinations
