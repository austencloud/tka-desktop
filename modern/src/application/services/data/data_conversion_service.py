"""
Data Conversion Service - Convert External Data to Modern Format

This service converts external pictograph data formats to modern BeatData format
while preserving all motion information and ensuring compatibility.
"""

from typing import Dict, Any, Optional, List
import logging

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
    from .glyph_data_service import GlyphDataService
    from core.decorators import handle_service_errors
    from core.monitoring import monitor_performance
    from core.exceptions import DataProcessingError, ValidationError
except ImportError:
    # Fallback to absolute imports (for standalone tests)
    try:
        from domain.models.core_models import (
            BeatData,
            MotionData,
            MotionType,
            HandMotionType,
            RotationDirection,
            Location,
            GlyphData,
        )
        from .glyph_data_service import GlyphDataService
        from core.decorators import handle_service_errors
        from core.monitoring import monitor_performance
        from core.exceptions import DataProcessingError, ValidationError
    except ImportError:
        # For tests, create dummy decorators if imports fail
        def handle_service_errors(*args, **kwargs):
            def decorator(func):
                return func

            return decorator

        def monitor_performance(*args, **kwargs):
            def decorator(func):
                return func

            return decorator

        class DataProcessingError(Exception):
            def __init__(
                self,
                message: str,
                data_type: Optional[str] = None,
                processing_stage: Optional[str] = None,
            ):
                super().__init__(message)
                self.data_type = data_type
                self.processing_stage = processing_stage

        class ValidationError(Exception):
            def __init__(
                self, message: str, field: Optional[str] = None, value: Any = None
            ):
                super().__init__(message)
                self.field = field
                self.value = value


logger = logging.getLogger(__name__)


class DataConversionService:
    """
    Converts external pictograph data to modern BeatData format.

    This service handles the mapping between string-based data formats
    and modern enum-based data structures while preserving all motion information.
    """

    def __init__(self):
        """Initialize the data conversion service with glyph data service."""
        self.glyph_data_service = GlyphDataService()

    # String to modern motion type mappings (for props)
    MOTION_TYPE_MAPPING = {
        "pro": MotionType.PRO,
        "anti": MotionType.ANTI,
        "float": MotionType.FLOAT,
        "dash": MotionType.DASH,
        "static": MotionType.STATIC,
    }

    # String to modern hand motion type mappings (for hands without props)
    HAND_MOTION_TYPE_MAPPING = {
        "shift": HandMotionType.SHIFT,
        "dash": HandMotionType.DASH,
        "static": HandMotionType.STATIC,
    }

    # String to modern rotation direction mappings
    ROTATION_DIRECTION_MAPPING = {
        "cw": RotationDirection.CLOCKWISE,
        "ccw": RotationDirection.COUNTER_CLOCKWISE,
        "no_rotation": RotationDirection.NO_ROTATION,
        "": RotationDirection.NO_ROTATION,
    }

    # String to modern location mappings
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

    @handle_service_errors("convert_external_pictograph_to_beat_data")
    @monitor_performance("data_conversion")
    def convert_external_pictograph_to_beat_data(
        self, external_data: Dict[str, Any]
    ) -> BeatData:
        """
        Convert external pictograph data to modern BeatData format.

        Args:
            external_data: External pictograph data dictionary

        Returns:
            BeatData object with converted motion information

        Raises:
            DataProcessingError: If required data is missing or invalid
            ValidationError: If data format is invalid
        """
        # Validate input data
        if not isinstance(external_data, dict):
            raise ValidationError("External data must be a dictionary")

        if not external_data:
            raise ValidationError("External data cannot be empty")

        try:
            # Extract basic information
            letter = external_data.get("letter", "Unknown")
            start_pos = external_data.get("start_pos", "unknown")
            end_pos = external_data.get("end_pos", "unknown")

            # Convert blue motion attributes
            blue_attrs = external_data.get("blue_attributes", {})
            blue_motion = self._convert_motion_attributes(blue_attrs, "blue")

            # Convert red motion attributes
            red_attrs = external_data.get("red_attributes", {})
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

        except (ValidationError, DataProcessingError):
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            logger.error(
                f"Failed to convert external data to BeatData: {e}",
                extra={"external_data": external_data},
            )
            raise DataProcessingError(
                f"Data conversion failed: {e}",
                data_type="external_pictograph",
                processing_stage="conversion",
            ) from e

    @handle_service_errors("convert_motion_attributes")
    def _convert_motion_attributes(
        self, external_attrs: Dict[str, Any], color: str
    ) -> MotionData:
        """
        Convert external motion attributes to modern MotionData.

        Args:
            external_attrs: External motion attributes dictionary
            color: Color identifier for error reporting ("blue" or "red")

        Returns:
            MotionData object with converted attributes
        """
        try:
            # Convert motion type (handle both prop and hand motions)
            motion_type_str = str(external_attrs.get("motion_type", "static")).lower()

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
            rot_dir_str = str(external_attrs.get("prop_rot_dir", "no_rotation")).lower()
            prop_rot_dir = self.ROTATION_DIRECTION_MAPPING.get(
                rot_dir_str, RotationDirection.NO_ROTATION
            )

            # Convert locations
            start_loc_str = str(external_attrs.get("start_loc", "n")).lower()
            start_loc = self.LOCATION_MAPPING.get(start_loc_str, Location.NORTH)

            end_loc_str = str(external_attrs.get("end_loc", "n")).lower()
            end_loc = self.LOCATION_MAPPING.get(end_loc_str, Location.NORTH)

            # Preserve orientations as strings from external format
            start_ori = str(external_attrs.get("start_ori", "in"))
            end_ori = str(external_attrs.get("end_ori", "in"))

            return MotionData(
                motion_type=motion_type,
                prop_rot_dir=prop_rot_dir,
                start_loc=start_loc,
                end_loc=end_loc,
                start_ori=start_ori,
                end_ori=end_ori,
            )

        except Exception as e:
            logger.error(
                f"Failed to convert {color} motion attributes: {e}",
                extra={"attributes": external_attrs, "color": color},
            )
            raise DataProcessingError(
                f"Motion attribute conversion failed for {color}: {e}",
                data_type="motion_attributes",
                processing_stage="attribute_conversion",
            ) from e

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
            # Fallback to alternative service if primary service fails
            try:
                return self.glyph_data_service.determine_glyph_data(beat_data)
            except Exception as fallback_e:
                print(f"⚠️ Fallback glyph generation also failed: {fallback_e}")
                return None

    @handle_service_errors("convert_multiple_external_pictographs")
    @monitor_performance("batch_data_conversion")
    def convert_multiple_external_pictographs(
        self, external_pictographs: List[Dict[str, Any]]
    ) -> List[BeatData]:
        """
        Convert multiple external pictographs to modern BeatData format.

        Args:
            external_pictographs: List of external pictograph data dictionaries

        Returns:
            List of BeatData objects

        Raises:
            ValidationError: If input list is invalid
            DataProcessingError: If conversion fails for any pictograph
        """
        # Validate input
        if not isinstance(external_pictographs, list):
            raise ValidationError("External pictographs must be a list")

        if not external_pictographs:
            logger.warning("Empty pictograph list provided for conversion")
            return []

        converted_beats = []
        conversion_errors = []

        for i, external_data in enumerate(external_pictographs):
            try:
                beat_data = self.convert_external_pictograph_to_beat_data(external_data)
                converted_beats.append(beat_data)
            except Exception as e:
                error_msg = f"Pictograph {i}: {e}"
                conversion_errors.append(error_msg)
                logger.warning(f"Conversion error for pictograph {i}: {e}")

        if conversion_errors:
            logger.warning(
                f"Conversion completed with {len(conversion_errors)} errors out of {len(external_pictographs)} pictographs"
            )
        else:
            logger.info(f"Successfully converted {len(converted_beats)} pictographs")

        return converted_beats

    @handle_service_errors("validate_conversion")
    def validate_conversion(
        self, external_data: Dict[str, Any], beat_data: BeatData
    ) -> Dict[str, Any]:
        """
        Validate that conversion preserved all important data.

        Args:
            external_data: Original external data
            beat_data: Converted BeatData

        Returns:
            Dictionary with validation results including 'valid', 'issues', and 'total_issues'

        Raises:
            ValidationError: If input parameters are invalid
        """
        # Validate inputs
        if not isinstance(external_data, dict):
            raise ValidationError("External data must be a dictionary")
        if not isinstance(beat_data, BeatData):
            raise ValidationError("Beat data must be a BeatData instance")

        issues = []

        # Check letter preservation
        if external_data.get("letter") != beat_data.letter:
            issues.append(
                f"Letter mismatch: {external_data.get('letter')} → {beat_data.letter}"
            )

        # Check position preservation (stored in metadata)
        if external_data.get("start_pos") != beat_data.metadata.get("start_pos"):
            issues.append(
                f"Start position mismatch: {external_data.get('start_pos')} → {beat_data.metadata.get('start_pos')}"
            )

        if external_data.get("end_pos") != beat_data.metadata.get("end_pos"):
            issues.append(
                f"End position mismatch: {external_data.get('end_pos')} → {beat_data.metadata.get('end_pos')}"
            )

        # Check motion type preservation
        blue_attrs = external_data.get("blue_attributes", {})
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
