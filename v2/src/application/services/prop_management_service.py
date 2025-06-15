"""
Prop Management Service - Beta Positioning and Prop Operations

Handles all prop-related positioning logic including:
- Beta prop positioning for overlapping props
- Prop separation based on motion and letter types
- Special placement overrides for specific configurations
- Offset calculations based on prop types and sizes

This service is responsible for determining when and how to separate props
to avoid overlaps, particularly for beta-ending letters.
"""

from typing import Tuple, Dict, Any, Optional
from abc import ABC, abstractmethod
from PyQt6.QtCore import QPointF
import json
from pathlib import Path
from enum import Enum

from domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    Location,
    Orientation,
)
from domain.models.pictograph_models import PropType


class IPropManagementService(ABC):
    """Interface for prop management operations."""

    @abstractmethod
    def should_apply_beta_positioning(self, beat_data: BeatData) -> bool:
        """Determine if beta positioning should be applied."""
        pass

    @abstractmethod
    def apply_beta_positioning(self, beat_data: BeatData) -> BeatData:
        """Apply beta prop positioning if conditions are met."""
        pass

    @abstractmethod
    def calculate_separation_offsets(
        self, beat_data: BeatData
    ) -> Tuple[QPointF, QPointF]:
        """Calculate separation offsets for blue and red props."""
        pass

    @abstractmethod
    def detect_prop_overlap(self, beat_data: BeatData) -> bool:
        """Detect if props overlap based on position and category."""
        pass


class PropManagementService(IPropManagementService):
    """
    Prop management service handling beta positioning and prop operations.

    This service manages:
    - Detection of beta-ending letters requiring prop separation
    - Calculation of prop separation offsets based on size and type
    - Application of special placement overrides
    - Prop overlap detection and resolution
    """

    def __init__(self):
        # Beta prop positioning constants (from v1)
        self._large_offset_divisor = 60
        self._medium_offset_divisor = 50
        self._small_offset_divisor = 45
        self._scene_reference_size = 950

        # Initialize prop offset mapping based on available PropType
        self._init_prop_offset_map()

        # Direction constants
        self.LEFT = "left"
        self.RIGHT = "right"
        self.UP = "up"
        self.DOWN = "down"
        self.UPLEFT = "upleft"
        self.UPRIGHT = "upright"
        self.DOWNLEFT = "downleft"
        self.DOWNRIGHT = "downright"  # Load special placements for beta prop swaps
        self._special_placements: Optional[Dict[str, Any]] = None
        self._load_special_placements()

    def _init_prop_offset_map(self) -> None:
        """Initialize prop offset mapping based on v2 PropType enum."""
        self._prop_offset_map = {
            PropType.CLUB: self._large_offset_divisor,
            PropType.EIGHTRINGS: self._large_offset_divisor,
            PropType.BIG_EIGHT_RINGS: self._large_offset_divisor,
            PropType.DOUBLESTAR: self._medium_offset_divisor,
            PropType.BIGDOUBLESTAR: self._medium_offset_divisor,
            PropType.HAND: self._small_offset_divisor,
            PropType.BUUGENG: self._small_offset_divisor,
            PropType.TRIAD: self._small_offset_divisor,
            PropType.MINIHOOP: self._small_offset_divisor,
            PropType.BIGBUUGENG: self._medium_offset_divisor,
            PropType.BIGHOOP: self._large_offset_divisor,
            PropType.STAFF: self._small_offset_divisor,
            PropType.BIGSTAFF: self._large_offset_divisor,
            PropType.FAN: self._small_offset_divisor,
            PropType.SWORD: self._large_offset_divisor,
            PropType.GUITAR: self._large_offset_divisor,
            PropType.UKULELE: self._small_offset_divisor,
            PropType.SIMPLESTAFF: self._small_offset_divisor,
            PropType.FRACTALGENG: self._small_offset_divisor,
            PropType.QUIAD: self._small_offset_divisor,
            PropType.CHICKEN: self._small_offset_divisor,
            PropType.TRIQUETRA: self._small_offset_divisor,
            PropType.TRIQUETRA2: self._small_offset_divisor,
        }

    def should_apply_beta_positioning(self, beat_data: BeatData) -> bool:
        """
        Determine if beta positioning should be applied.

        Beta positioning is applied when:
        1. Letter is one that ends at beta positions (G, H, I, J, K, L, Y, Z, Y-, Z-, Ψ, Ψ-, β)
        """
        if not beat_data or not beat_data.letter:
            return False

        # Letters that end at beta positions (from v1 LetterCondition.BETA_ENDING)
        beta_ending_letters = [
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "Y",
            "Z",
            "Y-",
            "Z-",
            "Ψ",
            "Ψ-",
            "β",
        ]

        return beat_data.letter in beta_ending_letters

    def detect_prop_overlap(self, beat_data: BeatData) -> bool:
        """
        Detect if props overlap based on their end positions and orientations.

        Props overlap when they end at the same location with the same orientation.
        """
        if not beat_data.blue_motion or not beat_data.red_motion:
            return False

        blue_motion = beat_data.blue_motion
        red_motion = beat_data.red_motion

        # Check if both motions end at same location
        if blue_motion.end_loc != red_motion.end_loc:
            return False

        # Calculate end orientations for both motions
        blue_end_ori = self._calculate_end_orientation(blue_motion)
        red_end_ori = self._calculate_end_orientation(red_motion)

        # Props overlap if they end at same location with same orientation
        return blue_end_ori == red_end_ori

    def apply_beta_positioning(self, beat_data: BeatData) -> BeatData:
        """
        Apply beta prop positioning if conditions are met.

        First checks for manual swap overrides, then applies algorithmic positioning.
        """
        if not self.should_apply_beta_positioning(beat_data):
            return beat_data

        # Check for swap overrides first
        if self._has_swap_override(beat_data):
            return self._apply_swap_override(beat_data)

        # Apply algorithmic beta positioning
        return self._apply_algorithmic_beta_positioning(beat_data)

    def calculate_separation_offsets(
        self, beat_data: BeatData
    ) -> Tuple[QPointF, QPointF]:
        """
        Calculate separation offsets for blue and red props.

        Returns tuple of (blue_offset, red_offset) as QPointF objects.
        """
        if not beat_data.blue_motion or not beat_data.red_motion:
            return QPointF(0, 0), QPointF(0, 0)

        # Calculate separation directions based on motion types and letter
        blue_direction = self._calculate_separation_direction(
            beat_data.blue_motion, beat_data, "blue"
        )
        red_direction = self._calculate_separation_direction(
            beat_data.red_motion, beat_data, "red"
        )

        # Calculate offsets based on directions and prop types
        blue_offset = self._calculate_directional_offset(
            blue_direction, self._get_current_prop_type()
        )
        red_offset = self._calculate_directional_offset(
            red_direction, self._get_current_prop_type()
        )

        return blue_offset, red_offset

    def _calculate_end_orientation(
        self, motion_data: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> Orientation:
        """Calculate end orientation for placement calculations."""
        motion_type = motion_data.motion_type
        turns = motion_data.turns

        if turns in {0, 1, 2, 3}:
            if motion_type in [MotionType.PRO, MotionType.STATIC]:
                return (
                    start_orientation
                    if int(turns) % 2 == 0
                    else self._switch_orientation(start_orientation)
                )
            elif motion_type in [MotionType.ANTI, MotionType.DASH]:
                return (
                    self._switch_orientation(start_orientation)
                    if int(turns) % 2 == 0
                    else start_orientation
                )

        return start_orientation

    def _switch_orientation(self, orientation: Orientation) -> Orientation:
        """Switch between IN and OUT orientations."""
        return Orientation.OUT if orientation == Orientation.IN else Orientation.IN

    def _calculate_separation_direction(
        self, motion: MotionData, beat_data: BeatData, color: str
    ) -> str:
        """
        Calculate the direction props should be separated.

        Based on v1 logic for different prop types and letter patterns.
        """
        # Get motion type and end location
        motion_type = motion.motion_type
        end_location = motion.end_loc

        # Basic separation logic - more sophisticated logic would go here
        # following v1 patterns for different letters and configurations
        if color == "blue":
            # Blue prop typically moves left or up-left
            if end_location in [Location.NORTH, Location.NORTHEAST, Location.NORTHWEST]:
                return self.UPLEFT
            elif end_location in [
                Location.SOUTH,
                Location.SOUTHEAST,
                Location.SOUTHWEST,
            ]:
                return self.DOWNLEFT
            else:
                return self.LEFT
        else:  # red
            # Red prop typically moves right or down-right
            if end_location in [Location.NORTH, Location.NORTHEAST, Location.NORTHWEST]:
                return self.UPRIGHT
            elif end_location in [
                Location.SOUTH,
                Location.SOUTHEAST,
                Location.SOUTHWEST,
            ]:
                return self.DOWNRIGHT
            else:
                return self.RIGHT

    def _calculate_directional_offset(
        self, direction: str, prop_type: PropType
    ) -> QPointF:
        """
        Calculate offset based on direction and prop type.

        Uses the same logic as v1 BetaOffsetCalculator.
        """
        # Get offset divisor based on prop type
        offset_divisor = self._prop_offset_map.get(
            prop_type, self._small_offset_divisor
        )

        # Calculate base offset
        base_offset = self._scene_reference_size / offset_divisor

        # Calculate diagonal offset for diagonal directions
        diagonal_offset = base_offset / (2**0.5)

        # Direction to offset mapping
        offset_map = {
            self.LEFT: QPointF(-base_offset, 0),
            self.RIGHT: QPointF(base_offset, 0),
            self.UP: QPointF(0, -base_offset),
            self.DOWN: QPointF(0, base_offset),
            self.DOWNRIGHT: QPointF(diagonal_offset, diagonal_offset),
            self.UPLEFT: QPointF(-diagonal_offset, -diagonal_offset),
            self.DOWNLEFT: QPointF(-diagonal_offset, diagonal_offset),
            self.UPRIGHT: QPointF(diagonal_offset, -diagonal_offset),
        }

        return offset_map.get(direction, QPointF(0, 0))

    def _get_current_prop_type(self) -> PropType:
        """
        Get current prop type from settings.

        For now returns a default, but should integrate with settings system.
        """  # TODO: Integrate with actual settings system
        return PropType.HAND  # Default to smallest offset

    def _has_swap_override(self, beat_data: BeatData) -> bool:
        """Check if beat has manual swap override in special placements."""
        if not self._special_placements:
            return False

        override_key = self._generate_override_key(beat_data)
        return override_key in self._special_placements

    def _generate_override_key(self, beat_data: BeatData) -> str:
        """
        Generate key for swap override lookup.

        Based on v1 logic for special placement keys.
        """
        if not beat_data.blue_motion or not beat_data.red_motion:
            return ""

        blue_type = beat_data.blue_motion.motion_type.value
        red_type = beat_data.red_motion.motion_type.value
        letter = beat_data.letter or ""

        # Generate key similar to v1 format
        return f"{letter}_{blue_type}_{red_type}"

    def _apply_swap_override(self, beat_data: BeatData) -> BeatData:
        """
        Apply manual swap override from special placements.

        Loads specific positioning data for this configuration.
        """
        override_key = self._generate_override_key(beat_data)
        override_data = self._special_placements.get(override_key, {})

        # Apply override adjustments
        # TODO: Implement specific override application logic
        # This would modify the beat_data with specific positioning overrides
        return beat_data

    def _apply_algorithmic_beta_positioning(self, beat_data: BeatData) -> BeatData:
        """
        Apply algorithmic beta prop positioning.

        Uses classification and repositioning logic similar to v1.
        """
        if not beat_data.blue_motion or not beat_data.red_motion:
            return beat_data

        # Calculate separation offsets
        blue_offset, red_offset = self.calculate_separation_offsets(beat_data)

        # TODO: Apply offsets to beat_data
        # This would modify the actual positioning data in beat_data
        # For now, return unmodified data as we need renderer integration

        return beat_data

    def _load_special_placements(self) -> None:
        """Load special placement data from JSON configuration files."""
        try:
            # Look for special placements file in data directory
            placements_file = Path("data/special_placements.json")
            if placements_file.exists():
                with open(placements_file, "r") as f:
                    self._special_placements = json.load(f)
            else:
                # Try v1 path as fallback
                v1_placements_file = Path("v1/src/resources/special_placements.json")
                if v1_placements_file.exists():
                    with open(v1_placements_file, "r") as f:
                        self._special_placements = json.load(f)
                else:
                    self._special_placements = {}
        except Exception as e:
            print(f"Warning: Could not load special placements: {e}")
            self._special_placements = {}

    def classify_props_by_size(self, beat_data: BeatData) -> Dict[str, list]:
        """
        Classify props by size categories (big, small, hands).

        Based on v1 PropClassifier logic.
        """
        classification = {
            "big_props": [],
            "small_props": [],
            "hands": [],
        }

        # TODO: Implement prop classification logic
        # This would analyze the prop types in beat_data and categorize them

        return classification

    def get_repositioning_strategy(
        self, beat_data: BeatData, prop_classification: Dict[str, list]
    ) -> str:
        """
        Determine repositioning strategy based on prop classification and letter.

        Returns strategy name that determines how props should be separated.
        """
        letter = beat_data.letter or ""

        # Check prop categories
        has_big_props = bool(prop_classification["big_props"])
        has_small_props = bool(prop_classification["small_props"])
        has_hands = bool(prop_classification["hands"])

        if has_big_props and len(prop_classification["big_props"]) == 2:
            return "big_prop_repositioning"
        elif has_small_props and len(prop_classification["small_props"]) == 2:
            return "small_prop_repositioning"
        elif has_hands:
            return "hand_repositioning"
        else:
            return "default_repositioning"
