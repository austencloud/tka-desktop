"""
Dash Location Service

This service implements comprehensive dash location calculation logic,
providing all the complex dash location maps and calculations with high precision.
"""

from typing import Optional, Dict, Tuple
from domain.models.core_models import (
    LetterType,
    MotionData,
    MotionType,
    Location,
    RotationDirection,
    ArrowColor,
    GridMode,
    BeatData,
)
from application.services.data.pictograph_analysis_service import (
    PictographAnalysisService,
)


class DashLocationService:
    """
    Dash location calculation service.

    Implements comprehensive dash location calculation logic including:
    - Φ_DASH and Ψ_DASH special handling
    - Λ (Lambda) zero turns special case
    - Type 3 scenario detection and handling
    - Grid mode specific calculations (Diamond/Box)
    - Complex location mappings for different scenarios
    """

    def __init__(self):
        """Initialize the dash location service with pictograph analysis."""
        self.analysis_service = PictographAnalysisService()

    def calculate_dash_location_from_beat(
        self, beat_data: BeatData, is_blue_arrow: bool
    ) -> Location:
        """
        High-level method to calculate dash location from beat data.

        This method automatically extracts all necessary parameters from the beat data
        using the pictograph analysis service, then calls the detailed calculation method.

        Args:
            beat_data: The beat data containing motion information
            is_blue_arrow: True if calculating for blue arrow, False for red arrow

        Returns:
            Location where the dash arrow should be positioned
        """
        # Extract motion data for the specified arrow
        motion = beat_data.blue_motion if is_blue_arrow else beat_data.red_motion
        other_motion = beat_data.red_motion if is_blue_arrow else beat_data.blue_motion

        if not motion or motion.motion_type != MotionType.DASH:
            # If not a dash motion, return start location as fallback
            return motion.start_loc if motion else Location.NORTH

        # Use analysis service to extract all the parameters
        letter_info = self.analysis_service.get_letter_info(beat_data)
        grid_info = self.analysis_service.get_grid_info(beat_data)
        arrow_color = self.analysis_service.get_arrow_color(is_blue_arrow)

        # Call the detailed calculation method with all parameters
        return self.calculate_dash_location(
            motion=motion,
            other_motion=other_motion,
            letter_type=letter_info["letter_type"],
            arrow_color=arrow_color,
            grid_mode=grid_info["grid_mode"],
            shift_location=grid_info["shift_location"],
            is_phi_dash=letter_info["is_phi_dash"],
            is_psi_dash=letter_info["is_psi_dash"],
            is_lambda=letter_info["is_lambda"],
        )

    # Predefined location mappings for dash calculations - comprehensive mapping
    PHI_DASH_PSI_DASH_LOCATION_MAP = {
        (ArrowColor.RED, (Location.NORTH, Location.SOUTH)): Location.EAST,
        (ArrowColor.RED, (Location.EAST, Location.WEST)): Location.NORTH,
        (ArrowColor.RED, (Location.SOUTH, Location.NORTH)): Location.EAST,
        (ArrowColor.RED, (Location.WEST, Location.EAST)): Location.NORTH,
        (ArrowColor.BLUE, (Location.NORTH, Location.SOUTH)): Location.WEST,
        (ArrowColor.BLUE, (Location.EAST, Location.WEST)): Location.SOUTH,
        (ArrowColor.BLUE, (Location.SOUTH, Location.NORTH)): Location.WEST,
        (ArrowColor.BLUE, (Location.WEST, Location.EAST)): Location.SOUTH,
        (ArrowColor.RED, (Location.NORTHWEST, Location.SOUTHEAST)): Location.NORTHEAST,
        (ArrowColor.RED, (Location.NORTHEAST, Location.SOUTHWEST)): Location.SOUTHEAST,
        (ArrowColor.RED, (Location.SOUTHWEST, Location.NORTHEAST)): Location.SOUTHEAST,
        (ArrowColor.RED, (Location.SOUTHEAST, Location.NORTHWEST)): Location.NORTHEAST,
        (ArrowColor.BLUE, (Location.NORTHWEST, Location.SOUTHEAST)): Location.SOUTHWEST,
        (ArrowColor.BLUE, (Location.NORTHEAST, Location.SOUTHWEST)): Location.NORTHWEST,
        (ArrowColor.BLUE, (Location.SOUTHWEST, Location.NORTHEAST)): Location.NORTHWEST,
        (ArrowColor.BLUE, (Location.SOUTHEAST, Location.NORTHWEST)): Location.SOUTHWEST,
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
        other_motion: Optional[MotionData] = None,
        letter_type: Optional[LetterType] = None,
        arrow_color: Optional[ArrowColor] = None,
        grid_mode: Optional[GridMode] = None,
        shift_location: Optional[Location] = None,
        is_phi_dash: bool = False,
        is_psi_dash: bool = False,
        is_lambda: bool = False,
    ) -> Location:
        """
        Calculate dash arrow location using proven calculation algorithms.

        Args:
            motion: The dash motion data
            other_motion: The other arrow's motion (for Φ/Ψ dash calculations)
            letter_type: Letter type for Type 3 detection
            arrow_color: Arrow color for Φ/Ψ dash calculations
            grid_mode: Grid mode for Type 3 calculations
            shift_location: Location of the shift arrow for Type 3
            is_phi_dash: Whether this is a Φ_DASH letter
            is_psi_dash: Whether this is a Ψ_DASH letter
            is_lambda: Whether this is a Λ or Λ_DASH letter
        """

        # Φ_DASH and Ψ_DASH special handling
        if is_phi_dash or is_psi_dash:
            return self._get_phi_dash_psi_dash_location(
                motion, other_motion, arrow_color
            )

        # Λ (Lambda) zero turns special case
        if is_lambda and motion.turns == 0 and other_motion:
            return self._get_lambda_zero_turns_location(motion, other_motion)

        # Zero turns - check for Type 3 or default
        if motion.turns == 0:
            return self._default_zero_turns_dash_location(
                motion, letter_type, grid_mode, shift_location
            )

        # Non-zero turns
        return self._dash_location_non_zero_turns(motion)

    def _get_phi_dash_psi_dash_location(
        self,
        motion: MotionData,
        other_motion: Optional[MotionData],
        arrow_color: Optional[ArrowColor],
    ) -> Location:
        """Handle Φ_DASH and Ψ_DASH location calculation."""
        if not other_motion or not arrow_color:
            # Fallback to default logic if missing data
            return self._default_zero_turns_dash_location(motion)

        # Both motions have zero turns
        if motion.turns == 0 and other_motion.turns == 0:
            key = (arrow_color, (motion.start_loc, motion.end_loc))
            return self.PHI_DASH_PSI_DASH_LOCATION_MAP.get(key, motion.start_loc)

        # Current motion has zero turns, other doesn't
        elif motion.turns == 0:
            opposite_location = self._dash_location_non_zero_turns(other_motion)
            return self._get_opposite_location(opposite_location)

        # Current motion has non-zero turns
        else:
            return self._dash_location_non_zero_turns(motion)

    def _get_lambda_zero_turns_location(
        self, motion: MotionData, other_motion: MotionData
    ) -> Location:
        """Handle Λ (Lambda) zero turns special case."""
        key = ((motion.start_loc, motion.end_loc), other_motion.end_loc)
        return self.LAMBDA_ZERO_TURNS_LOCATION_MAP.get(key, motion.start_loc)

    def _default_zero_turns_dash_location(
        self,
        motion: MotionData,
        letter_type: Optional[LetterType] = None,
        grid_mode: Optional[GridMode] = None,
        shift_location: Optional[Location] = None,
    ) -> Location:
        """Calculate default zero turns dash location."""
        # Type 3 scenario detection and handling
        if letter_type == LetterType.TYPE3 and grid_mode and shift_location:
            return self._calculate_dash_location_based_on_shift(
                motion, grid_mode, shift_location
            )

        # Default zero turns mapping
        key = (motion.start_loc, motion.end_loc)
        return self.DEFAULT_ZERO_TURNS_DASH_LOCATION_MAP.get(key, motion.start_loc)

    def _dash_location_non_zero_turns(self, motion: MotionData) -> Location:
        """Calculate dash location for non-zero turns."""
        if motion.prop_rot_dir == RotationDirection.NO_ROTATION:
            # Fallback for no rotation
            return motion.start_loc

        return self.NON_ZERO_TURNS_DASH_LOCATION_MAP[motion.prop_rot_dir][
            motion.start_loc
        ]

    def _calculate_dash_location_based_on_shift(
        self, motion: MotionData, grid_mode: GridMode, shift_location: Location
    ) -> Location:
        """Calculate Type 3 dash location based on shift arrow location."""
        start_loc = motion.start_loc

        if grid_mode == GridMode.DIAMOND:
            return self.DIAMOND_DASH_LOCATION_MAP.get(
                (start_loc, shift_location), start_loc
            )
        elif grid_mode == GridMode.BOX:
            return self.BOX_DASH_LOCATION_MAP.get(
                (start_loc, shift_location), start_loc
            )

        # Fallback to default if grid mode not recognized
        return self._default_zero_turns_dash_location(motion)

    def _get_opposite_location(self, location: Location) -> Location:
        """Get opposite location using proven location mapping."""
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
