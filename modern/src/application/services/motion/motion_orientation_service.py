"""
Motion Orientation Service - Focused Motion Orientation Operations

Handles all motion orientation calculations including:
- End orientation calculation for all motion types
- Integer and half-turn orientation calculations
- Orientation flipping logic
- Motion type specific orientation rules

This service provides a clean, focused interface for motion orientation
while maintaining the proven orientation calculation algorithms.
"""

from typing import Dict, Any
from abc import ABC, abstractmethod

from domain.models.core_models import (
    MotionData,
    MotionType,
    Orientation,
)


class IMotionOrientationService(ABC):
    """Interface for motion orientation operations."""

    @abstractmethod
    def calculate_motion_orientation(
        self, motion: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> Orientation:
        """Calculate end orientation for a motion."""
        pass

    @abstractmethod
    def flip_orientation(self, orientation: Orientation) -> Orientation:
        """Flip orientation between IN and OUT."""
        pass


class MotionOrientationService(IMotionOrientationService):
    """
    Focused motion orientation service.

    Provides comprehensive motion orientation calculations including:
    - End orientation calculation for all motion types
    - Integer and half-turn orientation calculations
    - Orientation flipping logic
    - Motion type specific orientation rules
    """

    def __init__(self):
        # Orientation calculation rules
        self._orientation_flip_rules = self._load_orientation_flip_rules()

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

    def flip_orientation(self, orientation: Orientation) -> Orientation:
        """Flip orientation between IN and OUT."""
        return Orientation.OUT if orientation == Orientation.IN else Orientation.IN

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
                else self.flip_orientation(start_orientation)
            )
        elif motion_type in [MotionType.ANTI, MotionType.DASH]:
            # ANTI and DASH: even turns = flipped orientation, odd turns = same
            return (
                self.flip_orientation(start_orientation)
                if turns % 2 == 0
                else start_orientation
            )
        else:
            # FLOAT and others: use PRO logic as default
            return (
                start_orientation
                if turns % 2 == 0
                else self.flip_orientation(start_orientation)
            )

    def _calculate_half_turns_orientation(
        self, motion_type: MotionType, turns: float, start_orientation: Orientation
    ) -> Orientation:
        """Calculate orientation for half turns."""
        # Half turns always flip orientation regardless of motion type
        return self.flip_orientation(start_orientation)

    # Private data loading methods

    def _load_orientation_flip_rules(self) -> Dict[str, Any]:
        """Load orientation flip rules for complex calculations."""
        # In production, this would load from JSON/database
        return {
            "special_cases": {},
            "motion_type_modifiers": {},
        }
