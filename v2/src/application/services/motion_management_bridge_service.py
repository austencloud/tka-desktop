"""
Motion Management Bridge Service - Temporary Compatibility Layer

This is a temporary bridge service that delegates to the new focused services
while maintaining the original MotionManagementService interface.

This allows existing consumers to continue working while we update them
to use the new focused services directly.

TEMPORARY: This service should be removed once all consumers are updated.
"""

from typing import List, Tuple
from application.services.motion_validation_service import IMotionValidationService
from application.services.motion_generation_service import IMotionGenerationService
from application.services.motion_orientation_service import IMotionOrientationService
from domain.models.core_models import (
    MotionData,
    MotionType,
    Location,
    Orientation,
)


class MotionManagementBridgeService:
    """
    Temporary bridge service that delegates to focused motion services.
    
    This maintains compatibility with the original MotionManagementService
    interface while using the new focused services internally.
    """

    def __init__(
        self,
        validation_service: IMotionValidationService,
        generation_service: IMotionGenerationService,
        orientation_service: IMotionOrientationService,
    ):
        self._validation_service = validation_service
        self._generation_service = generation_service
        self._orientation_service = orientation_service

    def validate_motion_combination(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> bool:
        """Validate that two motions can be combined in a beat."""
        return self._validation_service.validate_motion_combination(
            blue_motion, red_motion
        )

    def get_motion_validation_errors(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> List[str]:
        """Get detailed validation errors for motion combination."""
        return self._validation_service.get_motion_validation_errors(
            blue_motion, red_motion
        )

    def get_valid_motion_combinations(
        self, motion_type: MotionType, location: Location
    ) -> List[MotionData]:
        """Get all valid motion combinations for a given type and location."""
        return self._generation_service.get_valid_motion_combinations(
            motion_type, location
        )

    def generate_motion_combinations_for_letter(
        self, letter: str, start_position: str = "alpha1"
    ) -> List[Tuple[MotionData, MotionData]]:
        """Generate valid motion combinations for a specific letter."""
        return self._generation_service.generate_motion_combinations_for_letter(letter)

    def calculate_motion_orientation(
        self, motion: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> Orientation:
        """Calculate end orientation for a motion."""
        return self._orientation_service.calculate_motion_orientation(
            motion, start_orientation
        )
