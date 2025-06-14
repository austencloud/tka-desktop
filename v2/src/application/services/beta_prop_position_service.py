"""
Beta Prop Position Service for V2 Kinetic Constructor

Implements V1's beta prop position handler logic for handling overlapping props.
Provides prop overlap detection and separation algorithms to maintain visual clarity
when multiple props occupy identical grid positions.
"""

from typing import Tuple
from PyQt6.QtCore import QPointF
from enum import Enum

from application.services.beta_prop_swap_service import BetaPropSwapService
from domain.models.core_models import BeatData, MotionData, MotionType, Location


class PropCategory(Enum):
    """Prop categories for overlap detection (from V1 PropClassifier)."""

    BIG_UNILATERAL = "big_uni"
    SMALL_UNILATERAL = "small_uni"
    SMALL_BILATERAL = "small_bi"
    BIG_BILATERAL = "big_bi"
    HANDS = "hands"


class SeparationDirection(Enum):
    """Separation directions for prop positioning (from V1 constants)."""

    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
    DOWNRIGHT = "downright"
    UPLEFT = "upleft"
    DOWNLEFT = "downleft"
    UPRIGHT = "upright"


class BetaPropPositionService:
    """
    Service for handling beta prop positioning and overlap detection.

    Replicates V1's beta prop position handler logic:
    1. Detects when props overlap (same position, same category)
    2. Calculates appropriate separation directions
    3. Applies pixel-perfect offset values for visual separation
    """

    def __init__(self):
        # V1 offset constants (from BetaOffsetCalculator)
        self._large_offset_divisor = 60  # For Club, EightRings, BigEightRings
        self._medium_offset_divisor = 50  # For Doublestar, Bigdoublestar
        self._small_offset_divisor = 45  # Default for other props
        self._scene_reference_size = 950  # V1 reference scene size

        # Initialize swap service for override handling
        self.swap_service = BetaPropSwapService()

        # Prop type classifications (from V1 PropType enums)
        self._prop_classifications = {
            # Big unilateral props
            "Bighoop": PropCategory.BIG_UNILATERAL,
            "Guitar": PropCategory.BIG_UNILATERAL,
            "Sword": PropCategory.BIG_UNILATERAL,
            # Small unilateral props
            "Fan": PropCategory.SMALL_UNILATERAL,
            "Club": PropCategory.SMALL_UNILATERAL,
            "Minihoop": PropCategory.SMALL_UNILATERAL,
            "Triad": PropCategory.SMALL_UNILATERAL,
            "Ukulele": PropCategory.SMALL_UNILATERAL,
            "Triquetra": PropCategory.SMALL_UNILATERAL,
            "Triquetra2": PropCategory.SMALL_UNILATERAL,
            # Big bilateral props
            "Bigstaff": PropCategory.BIG_BILATERAL,
            "Bigbuugeng": PropCategory.BIG_BILATERAL,
            "Bigdoublestar": PropCategory.BIG_BILATERAL,
            "BigEightRings": PropCategory.BIG_BILATERAL,
            # Small bilateral props
            "Staff": PropCategory.SMALL_BILATERAL,
            "Simplestaff": PropCategory.SMALL_BILATERAL,
            "Buugeng": PropCategory.SMALL_BILATERAL,
            "Doublestar": PropCategory.SMALL_BILATERAL,
            "Quiad": PropCategory.SMALL_BILATERAL,
            "Fractalgeng": PropCategory.SMALL_BILATERAL,
            "Eightrings": PropCategory.SMALL_BILATERAL,
            "Chicken": PropCategory.SMALL_BILATERAL,
            # Hands
            "Hand": PropCategory.HANDS,
        }

        # Prop type to offset mapping (from V1 BetaOffsetCalculator)
        self._prop_offset_map = {
            "Club": self._large_offset_divisor,
            "Eightrings": self._large_offset_divisor,
            "BigEightRings": self._large_offset_divisor,
            "Doublestar": self._medium_offset_divisor,
            "Bigdoublestar": self._medium_offset_divisor,
        }

    def should_apply_beta_positioning(self, beat_data: BeatData) -> bool:
        """
        Determine if beta positioning should be applied.

        Based on V1 logic:
        - Must be a beta-ending letter
        - Must have exactly 2 props of the same category
        - All motions must be visible

        Args:
            beat_data: Beat data to analyze

        Returns:
            True if beta positioning should be applied
        """
        if not beat_data or not beat_data.letter:
            return False

        # Check if letter ends with beta (simplified check for V2)
        # In V1 this checks against LetterCondition.BETA_ENDING
        letter = beat_data.letter.lower()
        beta_ending_letters = ["β", "beta", "b"]  # Simplified for V2

        if not any(beta_letter in letter for beta_letter in beta_ending_letters):
            return False

        # Check if we have exactly 2 props that would overlap
        return self._detect_prop_overlap(beat_data)

    def _detect_prop_overlap(self, beat_data: BeatData) -> bool:
        """
        Detect if props overlap based on V1 classification logic.

        Args:
            beat_data: Beat data to analyze

        Returns:
            True if props overlap and need separation
        """
        if not beat_data.blue_motion or not beat_data.red_motion:
            return False

        # Get prop types (assuming Staff for now, can be extended)
        blue_prop_type = "Staff"  # TODO: Extract from motion data when available
        red_prop_type = "Staff"  # TODO: Extract from motion data when available

        # Classify props
        blue_category = self._prop_classifications.get(blue_prop_type)
        red_category = self._prop_classifications.get(red_prop_type)

        if not blue_category or not red_category:
            return False

        # Check if props are in same category (indicating potential overlap)
        if blue_category != red_category:
            return False

        # Check if props are at same location (indicating actual overlap)
        blue_end_loc = beat_data.blue_motion.end_loc
        red_end_loc = beat_data.red_motion.end_loc

        return blue_end_loc == red_end_loc

    def calculate_separation_offsets(
        self, beat_data: BeatData, prop_type: str = "Staff"
    ) -> Tuple[QPointF, QPointF]:
        """
        Calculate separation offsets for overlapping props.

        Args:
            beat_data: Beat data containing motion information
            prop_type: Type of prop for offset calculation

        Returns:
            Tuple of (blue_offset, red_offset) as QPointF objects
        """
        # Calculate base offset using V1 algorithm
        offset_divisor = self._prop_offset_map.get(
            prop_type, self._small_offset_divisor
        )
        base_offset = self._scene_reference_size / offset_divisor

        # Calculate diagonal offset for diagonal directions
        diagonal_offset = base_offset / (2**0.5)

        # Determine separation directions using V1 logic
        if not beat_data.blue_motion or not beat_data.red_motion:
            return QPointF(0, 0), QPointF(0, 0)

        blue_direction = self._get_separation_direction(beat_data.blue_motion, "blue")
        red_direction = self._get_separation_direction(beat_data.red_motion, "red")

        # Check for swap overrides (V1 SwapBetaHandler logic)
        grid_mode = (
            "diamond"
            if beat_data.blue_motion.end_loc.value in ["n", "s", "e", "w"]
            else "box"
        )
        should_swap = self.swap_service.should_swap_beta_props(beat_data, grid_mode)

        if should_swap:
            # Swap the directions (V1 swap behavior)
            blue_direction, red_direction = red_direction, blue_direction

        # Convert directions to offset vectors
        blue_offset = self._direction_to_offset(
            blue_direction, base_offset, diagonal_offset
        )
        red_offset = self._direction_to_offset(
            red_direction, base_offset, diagonal_offset
        )

        return blue_offset, red_offset

    def _get_separation_direction(
        self, motion_data: MotionData, color: str
    ) -> SeparationDirection:
        """
        Determine separation direction based on V1 BetaPropDirectionCalculator logic.

        Args:
            motion_data: Motion data for the prop
            color: Prop color ("blue" or "red")

        Returns:
            Separation direction for the prop
        """
        # Replicate V1's get_dir_for_non_shift method exactly
        location = motion_data.end_loc

        # Determine if prop is radial or nonradial based on end orientation
        # V1 logic: RADIAL = IN/OUT, NONRADIAL = CLOCK/COUNTER
        is_radial = motion_data.end_ori in ["in", "out"]

        # Determine grid mode based on location
        if location.value in ["n", "s", "e", "w"]:
            grid_mode = "diamond"
        else:
            grid_mode = "box"

        if grid_mode == "diamond":
            if is_radial:
                # V1 diamond_layer_reposition_map[RADIAL]
                direction_map = {
                    (Location.NORTH, "red"): SeparationDirection.RIGHT,
                    (Location.NORTH, "blue"): SeparationDirection.LEFT,
                    (Location.EAST, "red"): SeparationDirection.DOWN,
                    (Location.EAST, "blue"): SeparationDirection.UP,
                    (Location.SOUTH, "red"): SeparationDirection.LEFT,
                    (Location.SOUTH, "blue"): SeparationDirection.RIGHT,
                    (Location.WEST, "blue"): SeparationDirection.DOWN,
                    (Location.WEST, "red"): SeparationDirection.UP,
                }
            else:
                # V1 diamond_layer_reposition_map[NONRADIAL]
                direction_map = {
                    (Location.NORTH, "red"): SeparationDirection.UP,
                    (Location.NORTH, "blue"): SeparationDirection.DOWN,
                    (Location.SOUTH, "red"): SeparationDirection.UP,
                    (Location.SOUTH, "blue"): SeparationDirection.DOWN,
                    (Location.EAST, "red"): SeparationDirection.RIGHT,
                    (Location.WEST, "blue"): SeparationDirection.LEFT,
                    (Location.WEST, "red"): SeparationDirection.RIGHT,
                    (Location.EAST, "blue"): SeparationDirection.LEFT,
                }
        else:  # box grid
            if is_radial:
                # V1 box_layer_reposition_map[RADIAL]
                direction_map = {
                    (Location.NORTHEAST, "red"): SeparationDirection.DOWNRIGHT,
                    (Location.NORTHEAST, "blue"): SeparationDirection.UPLEFT,
                    (Location.SOUTHEAST, "red"): SeparationDirection.UPRIGHT,
                    (Location.SOUTHEAST, "blue"): SeparationDirection.DOWNLEFT,
                    (Location.SOUTHWEST, "red"): SeparationDirection.DOWNRIGHT,
                    (Location.SOUTHWEST, "blue"): SeparationDirection.UPLEFT,
                    (Location.NORTHWEST, "red"): SeparationDirection.UPRIGHT,
                    (Location.NORTHWEST, "blue"): SeparationDirection.DOWNLEFT,
                }
            else:
                # V1 box_layer_reposition_map[NONRADIAL]
                direction_map = {
                    (Location.NORTHEAST, "red"): SeparationDirection.UPRIGHT,
                    (Location.NORTHEAST, "blue"): SeparationDirection.DOWNLEFT,
                    (Location.SOUTHEAST, "red"): SeparationDirection.DOWNRIGHT,
                    (Location.SOUTHEAST, "blue"): SeparationDirection.UPLEFT,
                    (Location.SOUTHWEST, "red"): SeparationDirection.UPRIGHT,
                    (Location.SOUTHWEST, "blue"): SeparationDirection.DOWNLEFT,
                    (Location.NORTHWEST, "red"): SeparationDirection.DOWNRIGHT,
                    (Location.NORTHWEST, "blue"): SeparationDirection.UPLEFT,
                }

        return direction_map.get((location, color), SeparationDirection.RIGHT)

    def _direction_to_offset(
        self, direction: SeparationDirection, base_offset: float, diagonal_offset: float
    ) -> QPointF:
        """
        Convert separation direction to offset vector.

        Args:
            direction: Separation direction
            base_offset: Base offset value for cardinal directions
            diagonal_offset: Offset value for diagonal directions

        Returns:
            QPointF offset vector
        """
        offset_map = {
            SeparationDirection.LEFT: QPointF(-base_offset, 0),
            SeparationDirection.RIGHT: QPointF(base_offset, 0),
            SeparationDirection.UP: QPointF(0, -base_offset),
            SeparationDirection.DOWN: QPointF(0, base_offset),
            SeparationDirection.DOWNRIGHT: QPointF(diagonal_offset, diagonal_offset),
            SeparationDirection.UPLEFT: QPointF(-diagonal_offset, -diagonal_offset),
            SeparationDirection.DOWNLEFT: QPointF(-diagonal_offset, diagonal_offset),
            SeparationDirection.UPRIGHT: QPointF(diagonal_offset, -diagonal_offset),
        }

        return offset_map.get(direction, QPointF(0, 0))

    def get_opposite_direction(
        self, direction: SeparationDirection
    ) -> SeparationDirection:
        """
        Get opposite direction for paired prop separation.

        Args:
            direction: Original separation direction

        Returns:
            Opposite separation direction
        """
        opposite_map = {
            SeparationDirection.LEFT: SeparationDirection.RIGHT,
            SeparationDirection.RIGHT: SeparationDirection.LEFT,
            SeparationDirection.UP: SeparationDirection.DOWN,
            SeparationDirection.DOWN: SeparationDirection.UP,
            SeparationDirection.DOWNRIGHT: SeparationDirection.UPLEFT,
            SeparationDirection.UPLEFT: SeparationDirection.DOWNRIGHT,
            SeparationDirection.UPRIGHT: SeparationDirection.DOWNLEFT,
            SeparationDirection.DOWNLEFT: SeparationDirection.UPRIGHT,
        }

        return opposite_map.get(direction, SeparationDirection.RIGHT)
