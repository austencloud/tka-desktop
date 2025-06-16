"""
Data Conversion Service - Convert V1 Data to V2 Format

This service converts V1's pictograph data format to V2's BeatData format
while preserving all motion information and ensuring compatibility.
"""

from typing import Dict, Any, Optional

try:
    # Try relative imports first (for normal package usage)
    from domain.models.core_models import (
        BeatData,
        MotionData,
        MotionType,
        HandMotionType,
        RotationDirection,
        Location,
        GlyphData,
    )
    from ..old_services_before_consolidation.glyph_data_service import GlyphDataService
except ImportError:
    # Fallback to absolute imports (for standalone tests)
    from domain.models.core_models import (
        BeatData,
        MotionData,
        MotionType,
        HandMotionType,
        RotationDirection,
        Location,
        GlyphData,
    )
    from glyph_data_service import GlyphDataService


class DataConversionService:
    """
    Converts V1 pictograph data to V2 BeatData format.

    This service handles the mapping between V1's string-based data format
    and V2's enum-based data structures while preserving all motion information.
    """

    def __init__(self):
        """Initialize the data conversion service with glyph data service."""
        self.glyph_data_service = GlyphDataService()

    # V1 to V2 motion type mappings (for props)
    MOTION_TYPE_MAPPING = {
        "pro": MotionType.PRO,
        "anti": MotionType.ANTI,
        "float": MotionType.FLOAT,
        "dash": MotionType.DASH,
        "static": MotionType.STATIC,
    }

    # V1 to V2 hand motion type mappings (for hands without props)
    HAND_MOTION_TYPE_MAPPING = {
        "shift": HandMotionType.SHIFT,
        "dash": HandMotionType.DASH,
        "static": HandMotionType.STATIC,
    }

    # V1 to V2 rotation direction mappings
    ROTATION_DIRECTION_MAPPING = {
        "cw": RotationDirection.CLOCKWISE,
        "ccw": RotationDirection.COUNTER_CLOCKWISE,
        "no_rotation": RotationDirection.NO_ROTATION,
        "": RotationDirection.NO_ROTATION,
    }

    # V1 to V2 location mappings
    LOCATION_MAPPING = {
        "n": Location.NORTH,
        "ne": Location.NORTHEAST,
        "e": Location.EAST,
        "se": Location.SOUTHEAST,
        "s": Location.SOUTH,
        "sw": Location.SOUTHWEST,
        "w": Location.WEST,
        "nw": Location.NORTHWEST,
    }

    def convert_v1_pictograph_to_beat_data(self, v1_data: Dict[str, Any]) -> BeatData:
        """
        Convert V1 pictograph data to V2 BeatData format.

        Args:
            v1_data: V1 pictograph data dictionary

        Returns:
            BeatData object with converted motion information

        Raises:
            ValueError: If required data is missing or invalid
        """
        try:
            # Extract basic information
            letter = v1_data.get("letter", "Unknown")
            start_pos = v1_data.get("start_pos", "unknown")
            end_pos = v1_data.get("end_pos", "unknown")

            # Convert blue motion attributes
            blue_attrs = v1_data.get("blue_attributes", {})
            blue_motion = self._convert_motion_attributes(blue_attrs, "blue")

            # Convert red motion attributes
            red_attrs = v1_data.get("red_attributes", {})
            red_motion = self._convert_motion_attributes(red_attrs, "red")

            # Create initial BeatData object with position info in metadata
            beat_data = BeatData(
                letter=letter,
                blue_motion=blue_motion,
                red_motion=red_motion,
                metadata={
                    "start_pos": start_pos,
                    "end_pos": end_pos,
                },
            )

            # Generate glyph data using the glyph data service
            glyph_data = self._generate_glyph_data(beat_data)

            # Create final BeatData object with glyph data
            final_beat_data = BeatData(
                letter=letter,
                blue_motion=blue_motion,
                red_motion=red_motion,
                glyph_data=glyph_data,
                metadata={
                    "start_pos": start_pos,
                    "end_pos": end_pos,
                },
            )

            return final_beat_data

        except Exception as e:
            print(f"❌ Failed to convert V1 data to BeatData: {e}")
            print(f"   V1 data: {v1_data}")
            raise ValueError(f"Data conversion failed: {e}")

    def _convert_motion_attributes(
        self, v1_attrs: Dict[str, Any], color: str
    ) -> MotionData:
        """
        Convert V1 motion attributes to V2 MotionData.

        Args:
            v1_attrs: V1 motion attributes dictionary
            color: Color identifier for error reporting ("blue" or "red")

        Returns:
            MotionData object with converted attributes
        """
        try:
            # Convert motion type (handle both prop and hand motions)
            motion_type_str = str(v1_attrs.get("motion_type", "static")).lower()

            # Check if it's a hand motion (shift) or prop motion
            if motion_type_str == "shift":
                # For hand motions, we'll use STATIC as the base motion type
                # The actual hand motion type can be stored in metadata if needed
                motion_type = MotionType.STATIC
            else:
                motion_type = self.MOTION_TYPE_MAPPING.get(
                    motion_type_str, MotionType.STATIC
                )

            # Convert rotation direction
            rot_dir_str = str(v1_attrs.get("prop_rot_dir", "no_rotation")).lower()
            prop_rot_dir = self.ROTATION_DIRECTION_MAPPING.get(
                rot_dir_str, RotationDirection.NO_ROTATION
            )

            # Convert locations
            start_loc_str = str(v1_attrs.get("start_loc", "n")).lower()
            start_loc = self.LOCATION_MAPPING.get(start_loc_str, Location.NORTH)

            end_loc_str = str(v1_attrs.get("end_loc", "n")).lower()
            end_loc = self.LOCATION_MAPPING.get(end_loc_str, Location.NORTH)

            # Preserve orientations as strings (V1 format)
            start_ori = str(v1_attrs.get("start_ori", "in"))
            end_ori = str(v1_attrs.get("end_ori", "in"))

            return MotionData(
                motion_type=motion_type,
                prop_rot_dir=prop_rot_dir,
                start_loc=start_loc,
                end_loc=end_loc,
                start_ori=start_ori,
                end_ori=end_ori,
            )

        except Exception as e:
            print(f"❌ Failed to convert {color} motion attributes: {e}")
            print(f"   Attributes: {v1_attrs}")
            raise ValueError(f"Motion attribute conversion failed for {color}: {e}")

    def _generate_glyph_data(self, beat_data: BeatData) -> Optional[GlyphData]:
        """
        Generate glyph data for the beat data using the consolidated pictograph management service.

        Args:
            beat_data: The beat data to generate glyph data for

        Returns:
            GlyphData object or None if no glyphs needed
        """
        try:
            # CRITICAL FIX: Use consolidated service that respects metadata positions
            from ..core.pictograph_management_service import PictographManagementService

            pictograph_service = PictographManagementService()
            return pictograph_service._generate_glyph_data(beat_data)
        except Exception as e:
            print(f"⚠️ Failed to generate glyph data: {e}")
            # Fallback to old service if consolidated service fails
            try:
                return self.glyph_data_service.determine_glyph_data(beat_data)
            except Exception as fallback_e:
                print(f"⚠️ Fallback glyph generation also failed: {fallback_e}")
                return None

    def convert_multiple_v1_pictographs(
        self, v1_pictographs: list[Dict[str, Any]]
    ) -> list[BeatData]:
        """
        Convert multiple V1 pictographs to V2 BeatData format.

        Args:
            v1_pictographs: List of V1 pictograph data dictionaries

        Returns:
            List of BeatData objects
        """
        converted_beats = []
        conversion_errors = []

        for i, v1_data in enumerate(v1_pictographs):
            try:
                beat_data = self.convert_v1_pictograph_to_beat_data(v1_data)
                converted_beats.append(beat_data)
            except Exception as e:
                error_msg = f"Pictograph {i}: {e}"
                conversion_errors.append(error_msg)
                print(f"⚠️ {error_msg}")

        if conversion_errors:
            print(
                f"⚠️ Conversion completed with {len(conversion_errors)} errors out of {len(v1_pictographs)} pictographs"
            )
        else:
            print(f"✅ Successfully converted {len(converted_beats)} pictographs")

        return converted_beats

    def validate_conversion(
        self, v1_data: Dict[str, Any], beat_data: BeatData
    ) -> Dict[str, Any]:
        """
        Validate that conversion preserved all important data.

        Args:
            v1_data: Original V1 data
            beat_data: Converted BeatData

        Returns:
            Dictionary with validation results
        """
        issues = []

        # Check letter preservation
        if v1_data.get("letter") != beat_data.letter:
            issues.append(
                f"Letter mismatch: {v1_data.get('letter')} → {beat_data.letter}"
            )

        # Check position preservation (stored in metadata)
        if v1_data.get("start_pos") != beat_data.metadata.get("start_pos"):
            issues.append(
                f"Start position mismatch: {v1_data.get('start_pos')} → {beat_data.metadata.get('start_pos')}"
            )

        if v1_data.get("end_pos") != beat_data.metadata.get("end_pos"):
            issues.append(
                f"End position mismatch: {v1_data.get('end_pos')} → {beat_data.metadata.get('end_pos')}"
            )

        # Check motion type preservation
        blue_attrs = v1_data.get("blue_attributes", {})
        if blue_attrs.get("motion_type") and beat_data.blue_motion:
            expected_motion_type = self.MOTION_TYPE_MAPPING.get(
                blue_attrs["motion_type"].lower()
            )
            if (
                expected_motion_type
                and expected_motion_type != beat_data.blue_motion.motion_type
            ):
                issues.append(
                    f"Blue motion type mismatch: {blue_attrs['motion_type']} → {beat_data.blue_motion.motion_type}"
                )

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "total_issues": len(issues),
        }

    def get_conversion_statistics(self) -> Dict[str, Any]:
        """Get statistics about available conversions."""
        return {
            "motion_types": list(self.MOTION_TYPE_MAPPING.keys()),
            "rotation_directions": list(self.ROTATION_DIRECTION_MAPPING.keys()),
            "locations": list(self.LOCATION_MAPPING.keys()),
            "total_mappings": len(self.MOTION_TYPE_MAPPING)
            + len(self.ROTATION_DIRECTION_MAPPING)
            + len(self.LOCATION_MAPPING),
        }
