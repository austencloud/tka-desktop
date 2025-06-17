"""
Motion Management Service - Unified Motion Operations

Consolidates all motion-related services into a single cohesive service:
- Motion validation (motion_validation_service)
- Motion combination generation (motion_combination_service)
- Motion orientation calculations (motion_orientation_service)

This service provides a clean, unified interface for all motion operations
while maintaining the proven algorithms from the individual services.

NOTE: This service is being split into focused services:
- MotionValidationService
- MotionGenerationService
- MotionOrientationService
"""

from typing import List, Dict, Any, Optional, Tuple, Set
from abc import ABC, abstractmethod
from enum import Enum
import warnings

from domain.models.core_models import (
    MotionData,
    MotionType,
    Location,
    RotationDirection,
    Orientation,
    BeatData,
)


class IMotionManagementService(ABC):
    """Unified interface for all motion management operations."""

    @abstractmethod
    def validate_motion_combination(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> bool:
        """Validate that two motions can be combined in a beat."""
        pass

    @abstractmethod
    def get_valid_motion_combinations(
        self, motion_type: MotionType, location: Location
    ) -> List[MotionData]:
        """Get all valid motion combinations for a given type and location."""
        pass

    @abstractmethod
    def calculate_motion_orientation(
        self, motion: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> Orientation:
        """Calculate end orientation for a motion."""
        pass

    @abstractmethod
    def get_motion_validation_errors(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> List[str]:
        """Get detailed validation errors for motion combination."""
        pass

    @abstractmethod
    def generate_motion_combinations_for_letter(
        self, letter: str, start_position: str = "alpha1"
    ) -> List[Tuple[MotionData, MotionData]]:
        """Generate valid motion combinations for a specific letter."""
        pass


class MotionValidationError(Enum):
    """Types of motion validation errors."""

    INVALID_LOCATION_COMBINATION = "invalid_location_combination"
    INVALID_MOTION_TYPE_COMBINATION = "invalid_motion_type_combination"
    INVALID_ROTATION_COMBINATION = "invalid_rotation_combination"
    INVALID_TURNS_COMBINATION = "invalid_turns_combination"
    CONFLICTING_ORIENTATIONS = "conflicting_orientations"


class MotionManagementService(IMotionManagementService):
    """
    Unified motion management service consolidating all motion operations.

    Provides comprehensive motion management including:
    - Motion combination validation with detailed error reporting
    - Motion combination generation from datasets
    - Motion orientation calculations for all motion types
    - Letter-specific motion generation
    """

    def __init__(self):
        warnings.warn(
            "MotionManagementService is deprecated. Use focused services: "
            "MotionValidationService, MotionGenerationService, MotionOrientationService",
            DeprecationWarning,
            stacklevel=2,
        )

        # Motion validation rules
        self._invalid_location_combinations = self._load_invalid_location_combinations()
        self._invalid_motion_type_combinations = (
            self._load_invalid_motion_type_combinations()
        )
        self._valid_rotation_combinations = self._load_valid_rotation_combinations()

        # Motion generation datasets
        self._motion_datasets = self._load_motion_datasets()
        self._letter_specific_rules = self._load_letter_specific_rules()

        # Orientation calculation rules
        self._orientation_flip_rules = self._load_orientation_flip_rules()

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

    def get_valid_motion_combinations(
        self, motion_type: MotionType, location: Location
    ) -> List[MotionData]:
        """Get all valid motion combinations for a given type and location."""
        combinations = []

        # Get base motions from dataset
        base_motions = self._motion_datasets.get(motion_type, [])

        for base_motion in base_motions:
            # Create variations with different locations and rotations
            for rot_dir in RotationDirection:
                for turns in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
                    motion = MotionData(
                        motion_type=motion_type,
                        prop_rot_dir=rot_dir,
                        start_loc=location,
                        end_loc=self._calculate_end_location(
                            location, motion_type, turns
                        ),
                        turns=turns,
                    )

                    if self._is_valid_single_motion(motion):
                        combinations.append(motion)

        return combinations

    def calculate_motion_orientation(
        self, motion: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> Orientation:
        """Calculate end orientation for a motion."""
        motion_type = motion.motion_type
        turns = motion.turns

        # Handle integer turns (most common case)
        if turns in {0, 1, 2, 3}:
            return self._calculate_integer_turns_orientation(
                motion_type, int(turns), start_orientation
            )

        # Handle half turns
        if turns in {0.5, 1.5, 2.5}:
            return self._calculate_half_turns_orientation(
                motion_type, turns, start_orientation
            )

        # Default fallback
        return start_orientation

    def generate_motion_combinations_for_letter(
        self, letter: str, start_position: str = "alpha1"
    ) -> List[Tuple[MotionData, MotionData]]:
        """Generate valid motion combinations for a specific letter."""
        combinations = []

        # Get letter-specific rules
        letter_rules = self._letter_specific_rules.get(letter.lower(), {})

        # Get allowed motion types for this letter
        allowed_blue_types = letter_rules.get("blue_motion_types", list(MotionType))
        allowed_red_types = letter_rules.get("red_motion_types", list(MotionType))

        # Generate combinations
        for blue_type in allowed_blue_types:
            for red_type in allowed_red_types:
                blue_motions = self.get_valid_motion_combinations(
                    blue_type, Location.NORTH
                )
                red_motions = self.get_valid_motion_combinations(
                    red_type, Location.NORTH
                )

                for blue_motion in blue_motions:
                    for red_motion in red_motions:
                        if self.validate_motion_combination(blue_motion, red_motion):
                            combinations.append((blue_motion, red_motion))

        return combinations[:50]  # Limit to prevent excessive combinations

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
        blue_end_orientation = self.calculate_motion_orientation(blue_motion)
        red_end_orientation = self.calculate_motion_orientation(red_motion)

        # Most orientation combinations are valid
        # Add specific rules here if needed
        return True

    def _is_valid_single_motion(self, motion: MotionData) -> bool:
        """Check if a single motion is valid."""
        # Basic motion validation
        if motion.turns < 0 or motion.turns > 3:
            return False

        # Motion type specific validation
        if motion.motion_type == MotionType.STATIC and motion.turns != 0:
            return False

        return True

    # Private orientation calculation methods

    def _calculate_integer_turns_orientation(
        self, motion_type: MotionType, turns: int, start_orientation: Orientation
    ) -> Orientation:
        """Calculate orientation for integer turns."""
        if motion_type in [MotionType.PRO, MotionType.STATIC]:
            # PRO and STATIC: even turns = same orientation, odd turns = flipped
            return (
                start_orientation
                if turns % 2 == 0
                else self._flip_orientation(start_orientation)
            )
        elif motion_type in [MotionType.ANTI, MotionType.DASH]:
            # ANTI and DASH: even turns = flipped orientation, odd turns = same
            return (
                self._flip_orientation(start_orientation)
                if turns % 2 == 0
                else start_orientation
            )
        else:
            # FLOAT and others: use PRO logic as default
            return (
                start_orientation
                if turns % 2 == 0
                else self._flip_orientation(start_orientation)
            )

    def _calculate_half_turns_orientation(
        self, motion_type: MotionType, turns: float, start_orientation: Orientation
    ) -> Orientation:
        """Calculate orientation for half turns."""
        # Half turns always flip orientation regardless of motion type
        return self._flip_orientation(start_orientation)

    def _flip_orientation(self, orientation: Orientation) -> Orientation:
        """Flip orientation between IN and OUT."""
        return Orientation.OUT if orientation == Orientation.IN else Orientation.IN

    def _calculate_end_location(
        self, start_loc: Location, motion_type: MotionType, turns: float
    ) -> Location:
        """Calculate end location based on motion type and turns."""
        if motion_type == MotionType.STATIC:
            return start_loc

        # For other motion types, calculate based on turns
        # This is a simplified calculation - real implementation would be more complex
        location_order = [
            Location.NORTH,
            Location.NORTHEAST,
            Location.EAST,
            Location.SOUTHEAST,
            Location.SOUTH,
            Location.SOUTHWEST,
            Location.WEST,
            Location.NORTHWEST,
        ]

        try:
            start_index = location_order.index(start_loc)
            offset = int(turns * 2) % len(location_order)  # 2 positions per turn
            end_index = (start_index + offset) % len(location_order)
            return location_order[end_index]
        except ValueError:
            return start_loc

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

    def _load_motion_datasets(self) -> Dict[MotionType, List[Dict[str, Any]]]:
        """Load motion datasets for generation."""
        # In production, this would load from JSON/database
        return {
            MotionType.PRO: [
                {
                    "base_turns": 1.0,
                    "common_locations": [
                        Location.NORTH,
                        Location.EAST,
                        Location.SOUTH,
                        Location.WEST,
                    ],
                },
                {
                    "base_turns": 2.0,
                    "common_locations": [
                        Location.NORTHEAST,
                        Location.SOUTHEAST,
                        Location.SOUTHWEST,
                        Location.NORTHWEST,
                    ],
                },
            ],
            MotionType.ANTI: [
                {
                    "base_turns": 1.0,
                    "common_locations": [
                        Location.NORTH,
                        Location.EAST,
                        Location.SOUTH,
                        Location.WEST,
                    ],
                },
                {
                    "base_turns": 2.0,
                    "common_locations": [
                        Location.NORTHEAST,
                        Location.SOUTHEAST,
                        Location.SOUTHWEST,
                        Location.NORTHWEST,
                    ],
                },
            ],
            MotionType.STATIC: [
                {"base_turns": 0.0, "common_locations": list(Location)},
            ],
            MotionType.DASH: [
                {
                    "base_turns": 0.0,
                    "common_locations": [
                        Location.NORTH,
                        Location.EAST,
                        Location.SOUTH,
                        Location.WEST,
                    ],
                },
                {
                    "base_turns": 1.0,
                    "common_locations": [
                        Location.NORTHEAST,
                        Location.SOUTHEAST,
                        Location.SOUTHWEST,
                        Location.NORTHWEST,
                    ],
                },
            ],
            MotionType.FLOAT: [
                {"base_turns": 1.0, "common_locations": list(Location)},
            ],
        }

    def _load_letter_specific_rules(self) -> Dict[str, Dict[str, Any]]:
        """Load letter-specific motion rules."""
        # In production, this would load from JSON/database
        return {
            "a": {
                "blue_motion_types": [MotionType.PRO, MotionType.ANTI],
                "red_motion_types": [MotionType.PRO, MotionType.ANTI],
            },
            "b": {
                "blue_motion_types": [MotionType.STATIC, MotionType.DASH],
                "red_motion_types": [MotionType.STATIC, MotionType.DASH],
            },
            # Add more letter rules as needed
        }

    def _load_orientation_flip_rules(self) -> Dict[str, Any]:
        """Load orientation flip rules for complex calculations."""
        # In production, this would load from JSON/database
        return {
            "special_cases": {},
            "motion_type_modifiers": {},
        }

    def calculate_prop_rotation_angle(
        self, motion_data: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> float:
        """Calculate prop rotation angle based on motion data and orientation."""
        motion_type = motion_data.motion_type
        prop_rot_dir = motion_data.prop_rot_dir
        location = motion_data.end_loc

        # Diamond grid orientation-based rotation mapping (simplified for Modern)
        angle_map = {
            Orientation.IN: {
                Location.NORTH: 90,
                Location.SOUTH: 270,
                Location.WEST: 0,
                Location.EAST: 180,
            },
            Orientation.OUT: {
                Location.NORTH: 270,
                Location.SOUTH: 90,
                Location.WEST: 180,
                Location.EAST: 0,
            },
        }

        # Calculate end orientation for this motion
        end_orientation = self.calculate_motion_orientation(
            motion_data, start_orientation
        )

        # Get rotation angle from mapping
        orientation_map = angle_map.get(end_orientation, angle_map[Orientation.IN])
        rotation_angle = orientation_map.get(location, 0)

        return float(rotation_angle)
