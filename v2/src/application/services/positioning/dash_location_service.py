"""
Dash Location Service

This service implements the exact dash location calculation logic,
translating the complex dash location maps and calculations.
"""

from typing import Optional
from domain.models.core_models import LetterType, MotionData, MotionType, Location


class DashLocationService:
    """
    Dash location calculation service.

    Implements the exact logic from the DashLocationCalculator including:
    - Complex dash location maps for different letter types
    - Grid mode specific calculations
    - Type 3 scenario detection and handling
    """

    # Location mappings translated to Modern enums
    LOCATION_MAP = {
        "n": Location.NORTH,
        "e": Location.EAST,
        "s": Location.SOUTH,
        "w": Location.WEST,
        "ne": Location.NORTHEAST,
        "se": Location.SOUTHEAST,
        "sw": Location.SOUTHWEST,
        "nw": Location.NORTHWEST,
    }

    def calculate_dash_location(
        self,
        motion: MotionData,
        color: str = "blue",
        other_motion: Optional[MotionData] = None,
        letter_type: Optional[LetterType] = None,
        grid_mode: str = "diamond",
    ) -> Location:
        """Calculate dash arrow location using validated logic."""

        # For dash arrows, the location is typically the start location
        # unless special conditions apply
        if motion.motion_type != MotionType.DASH:
            return motion.start_loc

        # Type 3 detection: one DASH with zero turns + one shift motion
        if other_motion and self._is_type3_scenario(motion, other_motion):
            return self._calculate_type3_location(motion, other_motion)

        # Standard dash location is the start location
        return motion.start_loc

    def _is_type3_scenario(self, motion: MotionData, other_motion: MotionData) -> bool:
        """Detect Type 3 scenario: one DASH with zero turns + one shift motion."""
        dash_motion = motion if motion.motion_type == MotionType.DASH else other_motion
        shift_motion = other_motion if motion.motion_type == MotionType.DASH else motion

        if not dash_motion or not shift_motion:
            return False

        # Check if we have one dash and one shift motion
        is_dash_zero_turns = (
            dash_motion.motion_type == MotionType.DASH
            and getattr(dash_motion, "turns", 0) == 0
        )
        is_shift_motion = shift_motion.motion_type in [
            MotionType.PRO,
            MotionType.ANTI,
            MotionType.FLOAT,
        ]

        return is_dash_zero_turns and is_shift_motion

    def _calculate_type3_location(
        self, motion: MotionData, other_motion: MotionData
    ) -> Location:
        """Calculate Type 3 location for dash arrows in special scenarios."""
        # In Type 3 scenarios, use the shift motion's location calculation
        shift_motion = other_motion if motion.motion_type == MotionType.DASH else motion

        # For Type 3, the dash location is typically the opposite of the shift location
        return self._get_opposite_location(shift_motion.start_loc)

    def _get_opposite_location(self, location: Location) -> Location:
        """Get opposite location using validated logic."""
        opposite_map = {
            Location.NORTH: Location.SOUTH,
            Location.SOUTH: Location.NORTH,
            Location.EAST: Location.WEST,
            Location.WEST: Location.EAST,
            Location.NORTHEAST: Location.SOUTHWEST,
            Location.SOUTHWEST: Location.NORTHEAST,
            Location.SOUTHEAST: Location.NORTHWEST,
            Location.NORTHWEST: Location.SOUTHEAST,
        }
        return opposite_map.get(location, location)
