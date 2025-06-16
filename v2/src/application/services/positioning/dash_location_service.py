"""
V1-Compatible Dash Location Service

This service implements the exact dash location calculation logic from V1,
translating the complex dash location maps and calculations.
"""

from enum import Enum
from typing import Dict, Tuple, Optional
from domain.models.core_models import (
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)


class DashLocationService:
    """
    V1-compatible dash location calculation service.

    Implements the exact logic from V1's DashLocationCalculator including:
    - Φ_DASH and Ψ_DASH special cases
    - Λ zero turns handling
    - Type 3 shift-aware positioning
    - Default zero turns mapping
    - Non-zero turns rotation-based calculation
    """

    # V1 Location mappings translated to V2 enums
    PHI_DASH_PSI_DASH_LOCATION_MAP = {
        ("red", (Location.NORTH, Location.SOUTH)): Location.EAST,
        ("red", (Location.EAST, Location.WEST)): Location.NORTH,
        ("red", (Location.SOUTH, Location.NORTH)): Location.EAST,
        ("red", (Location.WEST, Location.EAST)): Location.NORTH,
        ("blue", (Location.NORTH, Location.SOUTH)): Location.WEST,
        ("blue", (Location.EAST, Location.WEST)): Location.SOUTH,
        ("blue", (Location.SOUTH, Location.NORTH)): Location.WEST,
        ("blue", (Location.WEST, Location.EAST)): Location.SOUTH,
        ("red", (Location.NORTHWEST, Location.SOUTHEAST)): Location.NORTHEAST,
        ("red", (Location.NORTHEAST, Location.SOUTHWEST)): Location.SOUTHEAST,
        ("red", (Location.SOUTHWEST, Location.NORTHEAST)): Location.SOUTHEAST,
        ("red", (Location.SOUTHEAST, Location.NORTHWEST)): Location.NORTHEAST,
        ("blue", (Location.NORTHWEST, Location.SOUTHEAST)): Location.SOUTHWEST,
        ("blue", (Location.NORTHEAST, Location.SOUTHWEST)): Location.NORTHWEST,
        ("blue", (Location.SOUTHWEST, Location.NORTHEAST)): Location.NORTHWEST,
        ("blue", (Location.SOUTHEAST, Location.NORTHWEST)): Location.SOUTHWEST,
    }

    LAMBDA_ZERO_TURNS_LOCATION_MAP = {
        ((Location.NORTH, Location.SOUTH), Location.WEST): Location.EAST,
        ((Location.EAST, Location.WEST), Location.SOUTH): Location.NORTH,
        ((Location.NORTH, Location.SOUTH), Location.EAST): Location.WEST,
        ((Location.WEST, Location.EAST), Location.SOUTH): Location.NORTH,
        ((Location.SOUTH, Location.NORTH), Location.WEST): Location.EAST,
        ((Location.EAST, Location.WEST), Location.NORTH): Location.SOUTH,
        ((Location.SOUTH, Location.NORTH), Location.EAST): Location.WEST,
        ((Location.WEST, Location.EAST), Location.NORTH): Location.SOUTH,
        (
            (Location.NORTHEAST, Location.SOUTHWEST),
            Location.NORTHWEST,
        ): Location.SOUTHEAST,
        (
            (Location.NORTHWEST, Location.SOUTHEAST),
            Location.NORTHEAST,
        ): Location.SOUTHWEST,
        (
            (Location.SOUTHWEST, Location.NORTHEAST),
            Location.SOUTHEAST,
        ): Location.NORTHWEST,
        (
            (Location.SOUTHEAST, Location.NORTHWEST),
            Location.SOUTHWEST,
        ): Location.NORTHEAST,
        (
            (Location.NORTHEAST, Location.SOUTHWEST),
            Location.SOUTHEAST,
        ): Location.NORTHWEST,
        (
            (Location.NORTHWEST, Location.SOUTHEAST),
            Location.SOUTHWEST,
        ): Location.NORTHEAST,
        (
            (Location.SOUTHWEST, Location.NORTHEAST),
            Location.NORTHWEST,
        ): Location.SOUTHEAST,
        (
            (Location.SOUTHEAST, Location.NORTHWEST),
            Location.NORTHEAST,
        ): Location.SOUTHWEST,
    }

    DEFAULT_ZERO_TURNS_DASH_LOCATION_MAP = {
        (Location.NORTH, Location.SOUTH): Location.EAST,
        (Location.EAST, Location.WEST): Location.SOUTH,
        (Location.SOUTH, Location.NORTH): Location.WEST,
        (Location.WEST, Location.EAST): Location.NORTH,
        (Location.NORTHEAST, Location.SOUTHWEST): Location.SOUTHEAST,
        (Location.NORTHWEST, Location.SOUTHEAST): Location.NORTHEAST,
        (Location.SOUTHWEST, Location.NORTHEAST): Location.NORTHWEST,
        (Location.SOUTHEAST, Location.NORTHWEST): Location.SOUTHWEST,
    }

    NON_ZERO_TURNS_DASH_LOCATION_MAP = {
        RotationDirection.CLOCKWISE: {
            Location.NORTH: Location.EAST,
            Location.EAST: Location.SOUTH,
            Location.SOUTH: Location.WEST,
            Location.WEST: Location.NORTH,
            Location.NORTHEAST: Location.SOUTHEAST,
            Location.SOUTHEAST: Location.SOUTHWEST,
            Location.SOUTHWEST: Location.NORTHWEST,
            Location.NORTHWEST: Location.NORTHEAST,
        },
        RotationDirection.COUNTER_CLOCKWISE: {
            Location.NORTH: Location.WEST,
            Location.EAST: Location.NORTH,
            Location.SOUTH: Location.EAST,
            Location.WEST: Location.SOUTH,
            Location.NORTHEAST: Location.NORTHWEST,
            Location.SOUTHEAST: Location.NORTHEAST,
            Location.SOUTHWEST: Location.SOUTHEAST,
            Location.NORTHWEST: Location.SOUTHWEST,
        },
    }

    DIAMOND_DASH_LOCATION_MAP = {
        (Location.NORTH, Location.NORTHWEST): Location.EAST,
        (Location.NORTH, Location.NORTHEAST): Location.WEST,
        (Location.NORTH, Location.SOUTHEAST): Location.WEST,
        (Location.NORTH, Location.SOUTHWEST): Location.EAST,
        (Location.EAST, Location.NORTHWEST): Location.SOUTH,
        (Location.EAST, Location.NORTHEAST): Location.SOUTH,
        (Location.EAST, Location.SOUTHEAST): Location.NORTH,
        (Location.EAST, Location.SOUTHWEST): Location.NORTH,
        (Location.SOUTH, Location.NORTHWEST): Location.EAST,
        (Location.SOUTH, Location.NORTHEAST): Location.WEST,
        (Location.SOUTH, Location.SOUTHEAST): Location.WEST,
        (Location.SOUTH, Location.SOUTHWEST): Location.EAST,
        (Location.WEST, Location.NORTHWEST): Location.SOUTH,
        (Location.WEST, Location.NORTHEAST): Location.SOUTH,
        (Location.WEST, Location.SOUTHEAST): Location.NORTH,
        (Location.WEST, Location.SOUTHWEST): Location.NORTH,
    }

    BOX_DASH_LOCATION_MAP = {
        (Location.NORTHEAST, Location.NORTH): Location.SOUTHEAST,
        (Location.NORTHEAST, Location.EAST): Location.NORTHWEST,
        (Location.NORTHEAST, Location.SOUTH): Location.NORTHWEST,
        (Location.NORTHEAST, Location.WEST): Location.SOUTHEAST,
        (Location.SOUTHEAST, Location.NORTH): Location.SOUTHWEST,
        (Location.SOUTHEAST, Location.EAST): Location.SOUTHWEST,
        (Location.SOUTHEAST, Location.SOUTH): Location.NORTHEAST,
        (Location.SOUTHEAST, Location.WEST): Location.NORTHEAST,
        (Location.SOUTHWEST, Location.NORTH): Location.SOUTHEAST,
        (Location.SOUTHWEST, Location.EAST): Location.NORTHWEST,
        (Location.SOUTHWEST, Location.SOUTH): Location.NORTHWEST,
        (Location.SOUTHWEST, Location.WEST): Location.SOUTHEAST,
        (Location.NORTHWEST, Location.NORTH): Location.SOUTHWEST,
        (Location.NORTHWEST, Location.EAST): Location.SOUTHWEST,
        (Location.NORTHWEST, Location.SOUTH): Location.NORTHEAST,
        (Location.NORTHWEST, Location.WEST): Location.NORTHEAST,
    }

    def calculate_dash_location(
        self,
        motion: MotionData,
        color: str = "blue",
        other_motion: Optional[MotionData] = None,
        letter_type: Optional[str] = None,
        grid_mode: str = "box",
        shift_location: Optional[Location] = None,
    ) -> Location:
        """
        Calculate dash arrow location using V1 logic.

        Args:
            motion: The dash motion data
            color: Arrow color ("red" or "blue")
            other_motion: Other motion for special cases
            letter_type: Letter type (for special cases like Φ_DASH, Ψ_DASH)
            grid_mode: Grid mode ("diamond" or "box")
            shift_location: Location of shift arrow (for Type 3)
        """

        # Special case: Φ and Ψ letters (both regular and dash versions)
        if letter_type in ["Φ", "Ψ", "Φ_DASH", "Ψ_DASH"]:
            return self._get_phi_dash_psi_dash_location(
                motion, color, other_motion
            )  # Special case: Λ letter with zero turns
        elif letter_type in ["Λ", "Λ_DASH"] and motion.turns == 0:
            return self._get_lambda_zero_turns_location(motion, other_motion)

        # Type 3 case: Use proper shift avoidance logic
        elif letter_type == "Type3" and motion.turns == 0 and other_motion:
            return self.calculate_dash_location_for_type3(
                motion, other_motion, grid_mode
            )

        # Standard cases
        elif motion.turns == 0:
            return self._default_zero_turns_dash_location(
                motion, letter_type, grid_mode, shift_location
            )
        else:
            return self._dash_location_non_zero_turns(motion)

    def _get_phi_dash_psi_dash_location(
        self, motion: MotionData, color: str, other_motion: Optional[MotionData]
    ) -> Location:
        """Calculate location for Φ_DASH and Ψ_DASH letters."""

        if other_motion and motion.turns == 0 and other_motion.turns == 0:
            # Both motions have zero turns
            arrow_location = self.PHI_DASH_PSI_DASH_LOCATION_MAP.get(
                (color, (motion.start_loc, motion.end_loc))
            )
            if arrow_location:
                return arrow_location

        elif motion.turns == 0 and other_motion and other_motion.turns != 0:
            # This motion has zero turns, other has non-zero
            other_location = self._dash_location_non_zero_turns(other_motion)
            return self._get_opposite_location(other_location)

        elif motion.turns != 0:
            # This motion has non-zero turns
            return self._dash_location_non_zero_turns(motion)

        # Fallback
        return motion.start_loc

    def _get_lambda_zero_turns_location(
        self, motion: MotionData, other_motion: Optional[MotionData]
    ) -> Location:
        """Calculate location for Λ letter with zero turns."""
        if not other_motion:
            return motion.start_loc

        arrow_location = self.LAMBDA_ZERO_TURNS_LOCATION_MAP.get(
            ((motion.start_loc, motion.end_loc), other_motion.end_loc)
        )
        return arrow_location or motion.start_loc

    def _default_zero_turns_dash_location(
        self,
        motion: MotionData,
        letter_type: Optional[str] = None,
        grid_mode: str = "box",
        shift_location: Optional[Location] = None,
    ) -> Location:
        """Calculate default zero turns dash location."""

        # Type 3 special handling
        if letter_type == "Type3" and shift_location:
            return self._calculate_dash_location_based_on_shift(
                motion.start_loc, shift_location, grid_mode
            )

        # Default mapping
        return self.DEFAULT_ZERO_TURNS_DASH_LOCATION_MAP.get(
            (motion.start_loc, motion.end_loc), motion.start_loc
        )

    def _dash_location_non_zero_turns(self, motion: MotionData) -> Location:
        """Calculate dash location for non-zero turns."""
        return self.NON_ZERO_TURNS_DASH_LOCATION_MAP[motion.prop_rot_dir][
            motion.start_loc
        ]

    def _calculate_dash_location_based_on_shift(
        self, start_loc: Location, shift_location: Location, grid_mode: str
    ) -> Location:
        """
        Calculate dash location avoiding shift location.

        Args:
            start_loc: Dash arrow's start location
            shift_location: The calculated location of the shift arrow (not its end position!)
            grid_mode: Grid mode ("diamond" or "box")

        Note: shift_location should be the calculated position of the shift arrow,
        which is determined by the shift arrow's start→end movement pattern.
        For example, if shift goes NORTH→EAST, its calculated location is NORTHEAST.
        """

        if grid_mode == "diamond":
            return self.DIAMOND_DASH_LOCATION_MAP.get(
                (start_loc, shift_location), start_loc
            )
        elif grid_mode == "box":
            return self.BOX_DASH_LOCATION_MAP.get(
                (start_loc, shift_location), start_loc
            )
        else:
            return start_loc

    def _get_opposite_location(self, location: Location) -> Location:
        """Get opposite location (V1 logic)."""
        opposite_map = {
            Location.NORTH: Location.SOUTH,
            Location.SOUTH: Location.NORTH,
            Location.EAST: Location.WEST,
            Location.WEST: Location.EAST,
            Location.NORTHEAST: Location.SOUTHWEST,
            Location.SOUTHWEST: Location.NORTHEAST,
            Location.NORTHWEST: Location.SOUTHEAST,
            Location.SOUTHEAST: Location.NORTHWEST,
        }
        return opposite_map.get(location, location)

    def calculate_shift_arrow_location(
        self, start_loc: Location, end_loc: Location
    ) -> Location:
        """
        Calculate shift arrow location based on start→end movement pattern.
        This matches V1's ShiftLocationCalculator logic.
        """
        direction_pairs = {
            frozenset({Location.NORTH, Location.EAST}): Location.NORTHEAST,
            frozenset({Location.EAST, Location.SOUTH}): Location.SOUTHEAST,
            frozenset({Location.SOUTH, Location.WEST}): Location.SOUTHWEST,
            frozenset({Location.WEST, Location.NORTH}): Location.NORTHWEST,
            frozenset({Location.NORTHEAST, Location.NORTHWEST}): Location.NORTH,
            frozenset({Location.NORTHEAST, Location.SOUTHEAST}): Location.EAST,
            frozenset({Location.SOUTHWEST, Location.SOUTHEAST}): Location.SOUTH,
            frozenset({Location.NORTHWEST, Location.SOUTHWEST}): Location.WEST,
        }
        return direction_pairs.get(frozenset({start_loc, end_loc}), start_loc)

    def calculate_dash_location_for_type3(
        self,
        dash_motion: MotionData,
        shift_motion: MotionData,
        grid_mode: str = "box",
    ) -> Location:
        """
        Calculate dash location for Type 3 scenarios with proper shift avoidance.

        This implements the V1 logic where:
        1. Calculate where the shift arrow will be positioned
        2. Position the dash to avoid that location using lookup tables

        Args:
            dash_motion: The dash motion (should have turns=0)
            shift_motion: The shift motion (PRO/ANTI/FLOAT)
            grid_mode: Grid mode ("diamond" or "box")
        """
        if dash_motion.turns != 0:
            # Non-zero turns, use standard calculation
            return self._dash_location_non_zero_turns(dash_motion)

        # Calculate where the shift arrow will be positioned
        shift_arrow_location = self.calculate_shift_arrow_location(
            shift_motion.start_loc, shift_motion.end_loc
        )

        # Use lookup table to position dash away from shift location
        return self._calculate_dash_location_based_on_shift(
            dash_motion.start_loc, shift_arrow_location, grid_mode
        )
