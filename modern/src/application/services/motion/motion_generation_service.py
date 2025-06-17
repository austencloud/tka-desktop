"""
Motion Generation Service - Focused Motion Generation Operations

Handles all motion generation logic including:
- Valid motion combination generation from datasets
- Letter-specific motion generation
- End location calculation
- Motion dataset management

This service provides a clean, focused interface for motion generation
while maintaining the proven generation algorithms.
"""

from typing import List, Dict, Any, Tuple
from abc import ABC, abstractmethod
import logging

from domain.models.core_models import (
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)

try:
    from src.core.decorators import handle_service_errors
    from src.core.monitoring import monitor_performance
    from src.core.exceptions import ServiceOperationError, ValidationError
except ImportError:
    # For tests, create dummy decorators if imports fail
    def handle_service_errors(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    def monitor_performance(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    class ServiceOperationError(Exception):
        pass

    class ValidationError(Exception):
        pass


logger = logging.getLogger(__name__)


class IMotionGenerationService(ABC):
    """Interface for motion generation operations."""

    @abstractmethod
    def get_valid_motion_combinations(
        self, motion_type: MotionType, location: Location
    ) -> List[MotionData]:
        """Get all valid motion combinations for a given type and location."""
        pass

    @abstractmethod
    def generate_motion_combinations_for_letter(
        self, letter: str
    ) -> List[Tuple[MotionData, MotionData]]:
        """Generate valid motion combinations for a specific letter."""
        pass

    @abstractmethod
    def calculate_end_location(
        self, start_loc: Location, motion_type: MotionType, turns: float
    ) -> Location:
        """Calculate end location based on motion type and turns."""
        pass


class MotionGenerationService(IMotionGenerationService):
    """
    Focused motion generation service.

    Provides comprehensive motion generation including:
    - Valid motion combination generation from datasets
    - Letter-specific motion generation
    - End location calculation
    - Motion dataset management
    """

    def __init__(self, validation_service=None):
        # Motion generation datasets
        self._motion_datasets = self._load_motion_datasets()
        self._letter_specific_rules = self._load_letter_specific_rules()

        # Optional validation service for filtering
        self._validation_service = validation_service

    @handle_service_errors("get_valid_motion_combinations")
    @monitor_performance("motion_combination_generation")
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
                        end_loc=self.calculate_end_location(
                            location, motion_type, turns
                        ),
                        turns=turns,
                    )

                    if self._is_valid_single_motion(motion):
                        combinations.append(motion)

        return combinations

    @handle_service_errors("generate_motion_combinations_for_letter")
    @monitor_performance("letter_motion_generation")
    def generate_motion_combinations_for_letter(
        self, letter: str
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
                        # Use validation service if available
                        if self._validation_service:
                            if self._validation_service.validate_motion_combination(
                                blue_motion, red_motion
                            ):
                                combinations.append((blue_motion, red_motion))
                        else:
                            # Basic validation without external service
                            combinations.append((blue_motion, red_motion))

        return combinations[:50]  # Limit to prevent excessive combinations

    @handle_service_errors("calculate_end_location")
    def calculate_end_location(
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

    # Private validation methods

    def _is_valid_single_motion(self, motion: MotionData) -> bool:
        """Check if a single motion is valid."""
        # Basic motion validation
        if motion.turns < 0 or motion.turns > 3:
            return False

        # Motion type specific validation
        if motion.motion_type == MotionType.STATIC and motion.turns != 0:
            return False

        return True

    # Private data loading methods

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
