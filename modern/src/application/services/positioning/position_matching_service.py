"""
Position Matching Service - Data-Driven Motion Generation

This service implements a data-driven position matching algorithm for motion generation.
The algorithm is simple: find all pictographs where start_pos matches the target position.
"""

import pandas as pd
from typing import Dict, List, Any, Optional
from ..core.pictograph_management_service import PictographManagementService

from domain.models.core_models import (
    BeatData,
    GlyphData,
    Location,
    MotionType,
    RotationDirection,
)


class PositionMatchingService:
    """
    Data-driven position matching service for motion generation.

    This service implements the core algorithm:
    `if item.get("start_pos") == target_position: next_opts.append(item)`

    No complex validation or rule-based generation - just simple dataset lookups.
    """

    def __init__(self):
        """Initialize position matching service with Modern's native dataset."""
        self.pictograph_management_service = PictographManagementService()

        self.pictograph_dataset: Optional[Dict[str, List[Dict[str, Any]]]] = None
        self._load_dataset()

    def _load_dataset(self):
        """Load dataset using Modern's native pictograph management service."""
        try:
            # Get the raw CSV dataset from Modern's service
            raw_dataset = self.pictograph_management_service._load_csv_data()

            if raw_dataset is None or raw_dataset.empty:
                print("❌ Dataset is empty")
                self.pictograph_dataset = {}
                return

            # Convert to grouped dictionary format: {letter: [pictograph_data_list]}
            self.pictograph_dataset = self._convert_dataframe_to_grouped_dict(
                raw_dataset
            )

            # Log statistics
            total_pictographs = sum(
                len(group) for group in self.pictograph_dataset.values()
            )
            print(f"📊 Position matching service initialized:")
            print(f"   - {total_pictographs} pictographs")
            print(f"   - {len(self.pictograph_dataset)} letters")

        except Exception as e:
            print(f"❌ Failed to load dataset: {e}")
            self.pictograph_dataset = {}

    def _convert_dataframe_to_grouped_dict(
        self, df: pd.DataFrame
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Convert pandas DataFrame to grouped dictionary format for position matching.

        Args:
            df: Pandas DataFrame with pictograph data

        Returns:
            Dictionary in format: {letter: [pictograph_data_list]}
        """
        grouped_dict = {}

        for _, row in df.iterrows():
            letter = str(row.get("letter", "Unknown"))

            # Convert row to pictograph data format
            pictograph_data = {
                "letter": letter,
                "start_pos": str(row.get("start_pos", "unknown")),
                "end_pos": str(row.get("end_pos", "unknown")),
                "blue_attributes": {
                    "motion_type": str(row.get("blue_motion_type", "static")),
                    "prop_rot_dir": str(row.get("blue_prop_rot_dir", "no_rotation")),
                    "start_loc": str(row.get("blue_start_loc", "n")),
                    "end_loc": str(row.get("blue_end_loc", "n")),
                    "start_ori": str(row.get("blue_start_ori", "in")),
                    "end_ori": str(row.get("blue_end_ori", "in")),
                },
                "red_attributes": {
                    "motion_type": str(row.get("red_motion_type", "static")),
                    "prop_rot_dir": str(row.get("red_prop_rot_dir", "no_rotation")),
                    "start_loc": str(row.get("red_start_loc", "s")),
                    "end_loc": str(row.get("red_end_loc", "s")),
                    "start_ori": str(row.get("red_start_ori", "out")),
                    "end_ori": str(row.get("red_end_ori", "out")),
                },
            }

            if letter not in grouped_dict:
                grouped_dict[letter] = []

            grouped_dict[letter].append(pictograph_data)

        return grouped_dict

    def get_next_options(self, last_beat_end_pos: str) -> List[BeatData]:
        """
        Validated algorithm: find all pictographs where start_pos matches.

        This is the complete algorithm from the option_getter.py lines 120-131:
        ```python
        for group in self.pictograph_dataset.values():
            for item in group:
                if item.get("start_pos") == start:
                    next_opts.append(item)
        ```

        Args:
            last_beat_end_pos: The end position of the last beat

        Returns:
            List of BeatData objects that can follow the given position
        """
        print(f"\n🔍 POSITION MATCHING ANALYSIS")
        print(f"🎯 Searching for options with start_pos = '{last_beat_end_pos}'")

        if not self.pictograph_dataset:
            print("❌ No dataset loaded")
            return []

        next_opts = []
        dataset_groups_checked = 0
        total_items_checked = 0
        matches_found = 0

        # Validated algorithm implementation
        for group_key, group in self.pictograph_dataset.items():
            dataset_groups_checked += 1
            for item in group:
                total_items_checked += 1
                if item.get("start_pos") == last_beat_end_pos:  # ← THE ENTIRE ALGORITHM
                    letter = item.get("letter", "Unknown")
                    end_pos = item.get("end_pos", "N/A")
                    matches_found += 1

                    # Convert dictionary to BeatData object
                    try:
                        # Convert dictionary to BeatData using native Modern methods
                        beat_data = self._convert_dict_to_beat_data(item)
                        next_opts.append(beat_data)  # ← ADD TO VALID OPTIONS
                        print(
                            f"   ✅ Match {matches_found}: {letter} ({last_beat_end_pos} → {end_pos})"
                        )
                    except Exception as e:
                        print(f"   ❌ Failed to convert match {matches_found}: {e}")
                        continue

        # Log analysis results
        print(f"\n📊 POSITION MATCHING RESULTS:")
        print(f"   - Dataset groups checked: {dataset_groups_checked}")
        print(f"   - Total items checked: {total_items_checked}")
        print(f"   - Matches found: {matches_found}")
        print(
            f"   - Success rate: {(matches_found/total_items_checked*100):.1f}%"
            if total_items_checked > 0
            else "   - Success rate: 0%"
        )

        if matches_found > 0:
            letters = [opt.letter or "?" for opt in next_opts]
            print(f"   - Letters found: {', '.join(letters)}")

        print("=" * 60)

        return next_opts

    def _convert_dict_to_beat_data(self, item: Dict[str, Any]) -> BeatData:
        """Convert dictionary item to BeatData using actual motion data from the dictionary."""
        from domain.models.core_models import (
            MotionData,
            MotionType,
            Location,
            RotationDirection,
        )

        # Extract basic data
        letter = item.get("letter", "")

        # Extract actual motion data from the dictionary
        blue_attrs = item.get("blue_attributes", {})
        red_attrs = item.get("red_attributes", {})

        # Convert blue motion
        blue_motion = MotionData(
            motion_type=self._parse_motion_type(
                blue_attrs.get("motion_type", "static")
            ),
            prop_rot_dir=self._parse_rotation_direction(
                blue_attrs.get("prop_rot_dir", "no_rot")
            ),
            start_loc=self._parse_location(blue_attrs.get("start_loc", "s")),
            end_loc=self._parse_location(blue_attrs.get("end_loc", "s")),
            turns=float(blue_attrs.get("turns", 0.0)),
            start_ori=blue_attrs.get("start_ori", "in"),
            end_ori=blue_attrs.get("end_ori", "in"),
        )

        # Convert red motion
        red_motion = MotionData(
            motion_type=self._parse_motion_type(red_attrs.get("motion_type", "static")),
            prop_rot_dir=self._parse_rotation_direction(
                red_attrs.get("prop_rot_dir", "no_rot")
            ),
            start_loc=self._parse_location(red_attrs.get("start_loc", "s")),
            end_loc=self._parse_location(red_attrs.get("end_loc", "s")),
            turns=float(red_attrs.get("turns", 0.0)),
            start_ori=red_attrs.get("start_ori", "in"),
            end_ori=red_attrs.get("end_ori", "in"),
        )

        # Create initial BeatData object with position info in metadata
        beat_data = BeatData(
            beat_number=1,
            letter=letter,
            blue_motion=blue_motion,
            red_motion=red_motion,
            metadata={
                "start_pos": item.get("start_pos", "unknown"),
                "end_pos": item.get("end_pos", "unknown"),
            },
        )

        # Generate glyph data using the glyph data service
        glyph_data = self._generate_glyph_data(beat_data)

        # Return final BeatData object with glyph data
        return BeatData(
            beat_number=1,
            letter=letter,
            blue_motion=blue_motion,
            red_motion=red_motion,
            glyph_data=glyph_data,
            metadata={
                "start_pos": item.get("start_pos", "unknown"),
                "end_pos": item.get("end_pos", "unknown"),
            },
        )

    def _generate_glyph_data(self, beat_data: "BeatData") -> Optional["GlyphData"]:
        """Generate glyph data for beat data using the consolidated pictograph management service."""
        from application.services.core.pictograph_management_service import (
            PictographManagementService,
        )

        pictograph_service = PictographManagementService()
        return pictograph_service._generate_glyph_data(beat_data)

    def _parse_motion_type(self, motion_type_str: str) -> "MotionType":
        """Parse motion type string to MotionType enum."""
        from domain.models.core_models import MotionType

        motion_type_map = {
            "pro": MotionType.PRO,
            "anti": MotionType.ANTI,
            "static": MotionType.STATIC,
            "dash": MotionType.DASH,
            "float": MotionType.FLOAT,
        }
        return motion_type_map.get(motion_type_str.lower(), MotionType.STATIC)

    def _parse_rotation_direction(self, rot_dir_str: str) -> "RotationDirection":
        """Parse rotation direction string to RotationDirection enum."""
        from domain.models.core_models import RotationDirection

        rot_dir_map = {
            "cw": RotationDirection.CLOCKWISE,
            "ccw": RotationDirection.COUNTER_CLOCKWISE,
            "no_rot": RotationDirection.NO_ROTATION,
        }
        return rot_dir_map.get(rot_dir_str.lower(), RotationDirection.NO_ROTATION)

    def _parse_location(self, location_str: str) -> "Location":
        """Parse location string to Location enum."""
        from domain.models.core_models import Location

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
        return location_map.get(location_str.lower(), Location.SOUTH)

    def get_alpha1_options(self) -> List[BeatData]:
        """
        Convenience method to get Alpha 1 options (the canonical test case).

        Returns:
            List of BeatData objects that start from alpha1 position
        """
        return self.get_next_options("alpha1")

    def get_available_start_positions(self) -> List[str]:
        """
        Get all available start positions in the dataset.

        Returns:
            List of unique start position strings
        """
        if not self.pictograph_dataset:
            return []

        start_positions = set()
        for group in self.pictograph_dataset.values():
            for item in group:
                start_pos = item.get("start_pos")
                if start_pos:
                    start_positions.add(start_pos)

        return sorted(list(start_positions))

    def get_position_statistics(self, position: str) -> Dict[str, Any]:
        """
        Get statistics for a specific position.

        Args:
            position: The position to analyze

        Returns:
            Dictionary with statistics about the position
        """
        options = self.get_next_options(position)

        if not options:
            return {
                "position": position,
                "total_options": 0,
                "letters": [],
                "letter_types": {},
            }

        # Import here to avoid circular imports
        from domain.models.letter_type_classifier import LetterTypeClassifier

        letters = [opt.letter or "Unknown" for opt in options]
        letter_types = {}

        for letter in letters:
            letter_type = LetterTypeClassifier.get_letter_type(letter)
            letter_types[letter_type] = letter_types.get(letter_type, 0) + 1

        return {
            "position": position,
            "total_options": len(options),
            "letters": letters,
            "letter_types": letter_types,
            "unique_letters": len(set(letters)),
        }

    def validate_dataset_integrity(self) -> Dict[str, Any]:
        """
        Validate the integrity of the loaded dataset.

        Returns:
            Dictionary with validation results
        """
        if not self.pictograph_dataset:
            return {"valid": False, "error": "No dataset loaded"}

        issues = []
        total_pictographs = 0

        for letter, pictographs in self.pictograph_dataset.items():
            total_pictographs += len(pictographs)

            for i, pictograph in enumerate(pictographs):
                # Check required fields
                required_fields = [
                    "letter",
                    "start_pos",
                    "end_pos",
                    "blue_attributes",
                    "red_attributes",
                ]
                for field in required_fields:
                    if field not in pictograph:
                        issues.append(f"Letter {letter}[{i}]: Missing field '{field}'")

                # Check letter consistency
                if pictograph.get("letter") != letter:
                    issues.append(f"Letter {letter}[{i}]: Letter mismatch in data")

        return {
            "valid": len(issues) == 0,
            "total_pictographs": total_pictographs,
            "total_letters": len(self.pictograph_dataset),
            "issues": issues[:10],  # Limit to first 10 issues
            "total_issues": len(issues),
        }
