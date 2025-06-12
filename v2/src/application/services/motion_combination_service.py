"""
Motion Combination Service for Kinetic Constructor v2

This service generates valid motion combinations based on the selected start position
and current sequence state, providing options for the option picker.
"""

from typing import List, Dict, Any, Optional
from itertools import product

from ...domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
)
from .glyph_data_service import GlyphDataService


class MotionCombinationService:
    """
    Service for generating valid motion combinations for the option picker.

    This service:
    1. Takes the current sequence state (including start position)
    2. Generates valid next motion combinations
    3. Creates BeatData objects with proper glyph information
    4. Filters combinations based on sequence rules
    """

    def __init__(self):
        self.glyph_service = GlyphDataService()

        # Define available motion types and properties
        self.motion_types = [
            MotionType.PRO,
            MotionType.ANTI,
            MotionType.STATIC,
            MotionType.DASH,
        ]
        self.rotation_directions = [
            RotationDirection.CLOCKWISE,
            RotationDirection.COUNTER_CLOCKWISE,
        ]
        self.locations = [
            Location.NORTH,
            Location.NORTHEAST,
            Location.EAST,
            Location.SOUTHEAST,
            Location.SOUTH,
            Location.SOUTHWEST,
            Location.WEST,
            Location.NORTHWEST,
        ]
        self.letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

    def generate_motion_combinations(
        self, sequence_data: List[Dict[str, Any]], max_combinations: int = 36
    ) -> List[BeatData]:
        """
        Generate valid motion combinations based on current sequence state.

        Args:
            sequence_data: Current sequence data (including start position)
            max_combinations: Maximum number of combinations to generate

        Returns:
            List of BeatData objects representing valid motion combinations
        """
        if len(sequence_data) <= 1:
            print("⚠️ No start position found in sequence data")
            return []

        start_position_data = sequence_data[1]  # Index 1 is start position
        last_beat_data = (
            sequence_data[-1] if len(sequence_data) > 2 else start_position_data
        )

        print(
            f"🎯 Generating motion combinations from: {last_beat_data.get('letter', 'Unknown')}"
        )

        combinations = []

        # Generate basic motion combinations
        for i, (blue_motion_type, red_motion_type) in enumerate(
            product(
                self.motion_types[:2], self.motion_types[:2]
            )  # PRO and ANTI only for now
        ):
            if len(combinations) >= max_combinations:
                break

            # Create motion combination
            beat_data = self._create_motion_combination(
                last_beat_data, blue_motion_type, red_motion_type, i
            )

            if beat_data and self._is_valid_combination(beat_data, sequence_data):
                combinations.append(beat_data)

        # Add some variety with different locations and rotations
        for i in range(
            len(combinations), min(max_combinations, len(combinations) + 12)
        ):
            beat_data = self._create_varied_combination(last_beat_data, i)
            if beat_data and self._is_valid_combination(beat_data, sequence_data):
                combinations.append(beat_data)

        print(f"✅ Generated {len(combinations)} motion combinations")
        return combinations

    def _create_motion_combination(
        self,
        last_beat_data: Dict[str, Any],
        blue_motion_type: MotionType,
        red_motion_type: MotionType,
        index: int,
    ) -> Optional[BeatData]:
        """Create a motion combination based on the last beat."""
        try:
            # Get last positions
            last_blue_loc = self._parse_location(
                last_beat_data["blue_attributes"]["end_loc"]
            )
            last_red_loc = self._parse_location(
                last_beat_data["red_attributes"]["end_loc"]
            )

            # Generate new positions (simple progression)
            blue_start_loc = last_blue_loc
            red_start_loc = last_red_loc

            # Calculate end locations based on motion type
            blue_end_loc = self._calculate_end_location(
                blue_start_loc, blue_motion_type, index
            )
            red_end_loc = self._calculate_end_location(
                red_start_loc, red_motion_type, index
            )

            # Create motion data
            blue_motion = MotionData(
                motion_type=blue_motion_type,
                prop_rot_dir=(
                    RotationDirection.CLOCKWISE
                    if index % 2 == 0
                    else RotationDirection.COUNTER_CLOCKWISE
                ),
                start_loc=blue_start_loc,
                end_loc=blue_end_loc,
                turns=(
                    1.0
                    if blue_motion_type in [MotionType.PRO, MotionType.ANTI]
                    else 0.0
                ),
                start_ori="in",
                end_ori=(
                    "out"
                    if blue_motion_type in [MotionType.PRO, MotionType.ANTI]
                    else "in"
                ),
            )

            red_motion = MotionData(
                motion_type=red_motion_type,
                prop_rot_dir=(
                    RotationDirection.COUNTER_CLOCKWISE
                    if index % 2 == 0
                    else RotationDirection.CLOCKWISE
                ),
                start_loc=red_start_loc,
                end_loc=red_end_loc,
                turns=(
                    1.0 if red_motion_type in [MotionType.PRO, MotionType.ANTI] else 0.0
                ),
                start_ori="in",
                end_ori=(
                    "out"
                    if red_motion_type in [MotionType.PRO, MotionType.ANTI]
                    else "in"
                ),
            )

            # Generate letter
            letter = self.letters[index % len(self.letters)]

            # Create beat data
            beat_data = BeatData(
                beat_number=len([1]),  # Will be set properly later
                letter=letter,
                duration=1.0,
                blue_motion=blue_motion,
                red_motion=red_motion,
            )

            # Generate glyph data
            glyph_data = self.glyph_service.determine_glyph_data(beat_data)

            return BeatData(
                beat_number=beat_data.beat_number,
                letter=beat_data.letter,
                duration=beat_data.duration,
                blue_motion=beat_data.blue_motion,
                red_motion=beat_data.red_motion,
                glyph_data=glyph_data,
            )

        except Exception as e:
            print(f"⚠️ Error creating motion combination: {e}")
            return None

    def _create_varied_combination(
        self, last_beat_data: Dict[str, Any], index: int
    ) -> Optional[BeatData]:
        """Create a varied motion combination with different patterns."""
        try:
            # Create more interesting combinations
            motion_patterns = [
                (MotionType.PRO, MotionType.ANTI),
                (MotionType.ANTI, MotionType.PRO),
                (MotionType.PRO, MotionType.STATIC),
                (MotionType.STATIC, MotionType.PRO),
                (MotionType.ANTI, MotionType.STATIC),
                (MotionType.STATIC, MotionType.ANTI),
            ]

            pattern_index = index % len(motion_patterns)
            blue_type, red_type = motion_patterns[pattern_index]

            # Use different starting locations for variety
            location_cycle = [
                Location.NORTH,
                Location.EAST,
                Location.SOUTH,
                Location.WEST,
                Location.NORTHEAST,
                Location.SOUTHEAST,
                Location.SOUTHWEST,
                Location.NORTHWEST,
            ]

            blue_start = location_cycle[index % len(location_cycle)]
            red_start = location_cycle[
                (index + 4) % len(location_cycle)
            ]  # Opposite-ish

            blue_end = location_cycle[(index + 2) % len(location_cycle)]
            red_end = location_cycle[(index + 6) % len(location_cycle)]

            # Create motion data
            blue_motion = MotionData(
                motion_type=blue_type,
                prop_rot_dir=(
                    RotationDirection.CLOCKWISE
                    if index % 3 == 0
                    else RotationDirection.COUNTER_CLOCKWISE
                ),
                start_loc=blue_start,
                end_loc=blue_end,
                turns=1.0 if blue_type in [MotionType.PRO, MotionType.ANTI] else 0.0,
                start_ori="in",
                end_ori=(
                    "out" if blue_type in [MotionType.PRO, MotionType.ANTI] else "in"
                ),
            )

            red_motion = MotionData(
                motion_type=red_type,
                prop_rot_dir=(
                    RotationDirection.COUNTER_CLOCKWISE
                    if index % 3 == 0
                    else RotationDirection.CLOCKWISE
                ),
                start_loc=red_start,
                end_loc=red_end,
                turns=1.0 if red_type in [MotionType.PRO, MotionType.ANTI] else 0.0,
                start_ori="in",
                end_ori=(
                    "out" if red_type in [MotionType.PRO, MotionType.ANTI] else "in"
                ),
            )

            # Generate letter
            letter = self.letters[(index + 3) % len(self.letters)]

            # Create beat data
            beat_data = BeatData(
                beat_number=1,
                letter=letter,
                duration=1.0,
                blue_motion=blue_motion,
                red_motion=red_motion,
            )

            # Generate glyph data
            glyph_data = self.glyph_service.determine_glyph_data(beat_data)

            return BeatData(
                beat_number=beat_data.beat_number,
                letter=beat_data.letter,
                duration=beat_data.duration,
                blue_motion=beat_data.blue_motion,
                red_motion=beat_data.red_motion,
                glyph_data=glyph_data,
            )

        except Exception as e:
            print(f"⚠️ Error creating varied combination: {e}")
            return None

    def _parse_location(self, location_str: str) -> Location:
        """Parse location string to Location enum."""
        location_map = {
            "n": Location.NORTH,
            "ne": Location.NORTHEAST,
            "e": Location.EAST,
            "se": Location.SOUTHEAST,
            "s": Location.SOUTH,
            "sw": Location.SOUTHWEST,
            "w": Location.WEST,
            "nw": Location.NORTHWEST,
        }
        return location_map.get(location_str.lower(), Location.NORTH)

    def _calculate_end_location(
        self, start_loc: Location, motion_type: MotionType, index: int
    ) -> Location:
        """Calculate end location based on start location and motion type."""
        if motion_type == MotionType.STATIC:
            return start_loc

        # Simple progression for now
        locations = list(Location)
        start_index = locations.index(start_loc)

        if motion_type == MotionType.PRO:
            end_index = (start_index + 2 + index) % len(locations)
        elif motion_type == MotionType.ANTI:
            end_index = (start_index - 2 - index) % len(locations)
        else:
            end_index = (start_index + 1) % len(locations)

        return locations[end_index]

    def _is_valid_combination(
        self, beat_data: BeatData, sequence_data: List[Dict[str, Any]]
    ) -> bool:
        """Check if a motion combination is valid."""
        # Basic validation rules
        if not beat_data.blue_motion or not beat_data.red_motion:
            return False

        # Don't allow both motions to be static
        if (
            beat_data.blue_motion.motion_type == MotionType.STATIC
            and beat_data.red_motion.motion_type == MotionType.STATIC
        ):
            return False

        # Additional validation rules can be added here
        return True
