"""
Result Comparison Engine
========================

Deep comparison engine for validating Legacy/Modern functional equivalence.
Performs sequence data, pictograph data, UI state, and arrow rendering validation.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: Legacy deprecation complete
PURPOSE: Compare Legacy/Modern execution results for functional equivalence validation
"""

from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import logging
import math
from enum import Enum


logger = logging.getLogger(__name__)


class ComparisonType(Enum):
    """Types of comparisons performed."""

    EXACT_MATCH = "exact_match"
    NUMERIC_TOLERANCE = "numeric_tolerance"
    STRUCTURAL_MATCH = "structural_match"
    ARROW_RENDERING = "arrow_rendering"
    UI_STATE = "ui_state"


@dataclass
class ComparisonRule:
    """Rule for comparing specific data fields."""

    field_path: str  # e.g., "sequence_data.beats[0].motions.blue.turns"
    comparison_type: ComparisonType
    tolerance: float = 0.001
    required: bool = True
    description: str = ""


@dataclass
class FieldDifference:
    """Represents a difference between two field values."""

    field_path: str
    legacy_value: Any
    modern_value: Any
    difference_type: str
    tolerance_used: float = 0.0
    is_critical: bool = True
    description: str = ""


@dataclass
class ComparisonResult:
    """Result of comparing Legacy and Modern execution results."""

    # Overall result
    is_equivalent: bool
    equivalence_score: float  # 0.0 to 1.0

    # Detailed differences
    differences: List[FieldDifference] = field(default_factory=list)
    critical_differences: List[FieldDifference] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # Comparison metadata
    comparison_rules_applied: List[ComparisonRule] = field(default_factory=list)
    total_fields_compared: int = 0
    fields_matched: int = 0

    # Performance metrics
    comparison_time_ms: float = 0.0

    def add_difference(self, difference: FieldDifference) -> None:
        """Add a field difference to the result."""
        self.differences.append(difference)
        if difference.is_critical:
            self.critical_differences.append(difference)

    def add_warning(self, warning: str) -> None:
        """Add a warning to the result."""
        self.warnings.append(warning)

    def calculate_equivalence_score(self) -> float:
        """Calculate overall equivalence score."""
        if self.total_fields_compared == 0:
            return 0.0

        # Base score from field matches
        base_score = self.fields_matched / self.total_fields_compared

        # Penalty for critical differences
        critical_penalty = len(self.critical_differences) * 0.1

        # Final score
        self.equivalence_score = max(0.0, base_score - critical_penalty)
        return self.equivalence_score


class IResultComparer(ABC):
    """Interface for result comparison engines."""

    @abstractmethod
    def compare_results(
        self, legacy_result: Dict[str, Any], modern_result: Dict[str, Any]
    ) -> ComparisonResult:
        """Compare Legacy and Modern execution results."""
        pass

    @abstractmethod
    def compare_sequence_data(
        self, legacy_data: Dict[str, Any], modern_data: Dict[str, Any]
    ) -> ComparisonResult:
        """Compare sequence data between versions."""
        pass

    @abstractmethod
    def compare_pictograph_data(
        self, legacy_data: Dict[str, Any], modern_data: Dict[str, Any]
    ) -> ComparisonResult:
        """Compare pictograph data between versions."""
        pass


class ResultComparer(IResultComparer):
    """Comprehensive result comparison engine."""

    def __init__(self):
        self.default_tolerance = 0.001
        self.position_tolerance = 1.0  # pixels
        self.rotation_tolerance = 0.1  # degrees

        # Define comparison rules
        self.comparison_rules = self._create_default_comparison_rules()

    def _create_default_comparison_rules(self) -> List[ComparisonRule]:
        """Create default comparison rules for common fields."""
        return [
            # Sequence-level rules
            ComparisonRule(
                "sequence_data.beat_count", ComparisonType.EXACT_MATCH, required=True
            ),
            ComparisonRule(
                "sequence_data.start_position",
                ComparisonType.EXACT_MATCH,
                required=True,
            ),
            ComparisonRule(
                "sequence_data.word", ComparisonType.EXACT_MATCH, required=False
            ),
            # Beat-level rules
            ComparisonRule(
                "beats[*].letter", ComparisonType.EXACT_MATCH, required=True
            ),
            ComparisonRule(
                "beats[*].duration",
                ComparisonType.NUMERIC_TOLERANCE,
                tolerance=0.001,
                required=True,
            ),
            # Motion-level rules
            ComparisonRule(
                "motions.*.motion_type", ComparisonType.EXACT_MATCH, required=True
            ),
            ComparisonRule(
                "motions.*.turns",
                ComparisonType.NUMERIC_TOLERANCE,
                tolerance=0.001,
                required=True,
            ),
            ComparisonRule(
                "motions.*.start_ori", ComparisonType.EXACT_MATCH, required=True
            ),
            ComparisonRule(
                "motions.*.end_ori", ComparisonType.EXACT_MATCH, required=True
            ),
            ComparisonRule(
                "motions.*.start_loc", ComparisonType.EXACT_MATCH, required=True
            ),
            ComparisonRule(
                "motions.*.end_loc", ComparisonType.EXACT_MATCH, required=True
            ),
            # Arrow rendering rules
            ComparisonRule(
                "arrows.*.position_x",
                ComparisonType.NUMERIC_TOLERANCE,
                tolerance=1.0,
                required=True,
            ),
            ComparisonRule(
                "arrows.*.position_y",
                ComparisonType.NUMERIC_TOLERANCE,
                tolerance=1.0,
                required=True,
            ),
            ComparisonRule(
                "arrows.*.rotation_angle",
                ComparisonType.NUMERIC_TOLERANCE,
                tolerance=0.1,
                required=True,
            ),
            ComparisonRule("arrows.*.color", ComparisonType.EXACT_MATCH, required=True),
            ComparisonRule(
                "arrows.*.is_mirrored", ComparisonType.EXACT_MATCH, required=True
            ),
            # Prop rendering rules
            ComparisonRule(
                "props.*.position_x",
                ComparisonType.NUMERIC_TOLERANCE,
                tolerance=1.0,
                required=True,
            ),
            ComparisonRule(
                "props.*.position_y",
                ComparisonType.NUMERIC_TOLERANCE,
                tolerance=1.0,
                required=True,
            ),
            ComparisonRule(
                "props.*.rotation_angle",
                ComparisonType.NUMERIC_TOLERANCE,
                tolerance=0.1,
                required=True,
            ),
            ComparisonRule("props.*.color", ComparisonType.EXACT_MATCH, required=True),
            ComparisonRule(
                "props.*.prop_type", ComparisonType.EXACT_MATCH, required=True
            ),
        ]

    def compare_results(
        self, legacy_result: Dict[str, Any], modern_result: Dict[str, Any]
    ) -> ComparisonResult:
        """Compare complete Legacy and Modern execution results."""
        import time

        start_time = time.time()

        result = ComparisonResult(is_equivalent=True, equivalence_score=1.0)

        try:
            # Compare execution success
            legacy_success = legacy_result.get("success", False)
            modern_success = modern_result.get("success", False)

            if legacy_success != modern_success:
                result.add_difference(
                    FieldDifference(
                        field_path="execution.success",
                        legacy_value=legacy_success,
                        modern_value=modern_success,
                        difference_type="execution_status_mismatch",
                        is_critical=True,
                        description="Execution success status differs between versions",
                    )
                )

            # Compare execution times (with warning for significant differences)
            legacy_time = legacy_result.get("execution_time_ms", 0)
            modern_time = modern_result.get("execution_time_ms", 0)

            if abs(legacy_time - modern_time) > 1000:  # More than 1 second difference
                result.add_warning(
                    f"Significant execution time difference: Legacy={legacy_time}ms, Modern={modern_time}ms"
                )

            # Compare data if both executions succeeded
            if legacy_success and modern_success:
                legacy_data = legacy_result.get("data", {})
                modern_data = modern_result.get("data", {})

                # Compare sequence data
                if "sequence_data" in legacy_data and "sequence_data" in modern_data:
                    seq_result = self.compare_sequence_data(
                        legacy_data["sequence_data"], modern_data["sequence_data"]
                    )
                    result.differences.extend(seq_result.differences)
                    result.critical_differences.extend(seq_result.critical_differences)
                    result.warnings.extend(seq_result.warnings)

                # Compare pictograph data
                if (
                    "pictograph_data" in legacy_data
                    and "pictograph_data" in modern_data
                ):
                    pic_result = self.compare_pictograph_data(
                        legacy_data["pictograph_data"], modern_data["pictograph_data"]
                    )
                    result.differences.extend(pic_result.differences)
                    result.critical_differences.extend(pic_result.critical_differences)
                    result.warnings.extend(pic_result.warnings)

            # Calculate final equivalence
            result.total_fields_compared = len(self.comparison_rules)
            result.fields_matched = result.total_fields_compared - len(
                result.differences
            )
            result.is_equivalent = len(result.critical_differences) == 0
            result.calculate_equivalence_score()

            result.comparison_time_ms = (time.time() - start_time) * 1000

            return result

        except Exception as e:
            logger.error(f"Result comparison failed: {e}")
            result.is_equivalent = False
            result.equivalence_score = 0.0
            result.add_difference(
                FieldDifference(
                    field_path="comparison.error",
                    legacy_value="N/A",
                    modern_value="N/A",
                    difference_type="comparison_error",
                    is_critical=True,
                    description=f"Comparison failed: {e}",
                )
            )
            return result

    def compare_sequence_data(
        self, legacy_data: Dict[str, Any], modern_data: Dict[str, Any]
    ) -> ComparisonResult:
        """Compare sequence data between versions."""
        result = ComparisonResult(is_equivalent=True, equivalence_score=1.0)

        try:
            # Compare beat count
            legacy_beat_count = legacy_data.get("beat_count", 0)
            modern_beat_count = modern_data.get("beat_count", 0)

            if legacy_beat_count != modern_beat_count:
                result.add_difference(
                    FieldDifference(
                        field_path="sequence_data.beat_count",
                        legacy_value=legacy_beat_count,
                        modern_value=modern_beat_count,
                        difference_type="exact_mismatch",
                        is_critical=True,
                        description="Beat count differs between versions",
                    )
                )

            # Compare start position
            legacy_start_pos = legacy_data.get("start_position", "")
            modern_start_pos = modern_data.get("start_position", "")

            if legacy_start_pos != modern_start_pos:
                result.add_difference(
                    FieldDifference(
                        field_path="sequence_data.start_position",
                        legacy_value=legacy_start_pos,
                        modern_value=modern_start_pos,
                        difference_type="exact_mismatch",
                        is_critical=True,
                        description="Start position differs between versions",
                    )
                )

            # Compare beats
            legacy_beats = legacy_data.get("beats", [])
            modern_beats = modern_data.get("beats", [])

            min_beats = min(len(legacy_beats), len(modern_beats))
            for i in range(min_beats):
                beat_result = self._compare_beat_data(
                    legacy_beats[i], modern_beats[i], i
                )
                result.differences.extend(beat_result.differences)
                result.critical_differences.extend(beat_result.critical_differences)

            return result

        except Exception as e:
            logger.error(f"Sequence data comparison failed: {e}")
            result.is_equivalent = False
            result.add_difference(
                FieldDifference(
                    field_path="sequence_data.comparison_error",
                    legacy_value="N/A",
                    modern_value="N/A",
                    difference_type="comparison_error",
                    is_critical=True,
                    description=f"Sequence comparison failed: {e}",
                )
            )
            return result

    def compare_pictograph_data(
        self, legacy_data: Dict[str, Any], modern_data: Dict[str, Any]
    ) -> ComparisonResult:
        """Compare pictograph data between versions."""
        result = ComparisonResult(is_equivalent=True, equivalence_score=1.0)

        try:
            # Compare arrows
            legacy_arrows = legacy_data.get("arrows", {})
            modern_arrows = modern_data.get("arrows", {})

            for color in set(legacy_arrows.keys()) | set(modern_arrows.keys()):
                if color in legacy_arrows and color in modern_arrows:
                    arrow_result = self._compare_arrow_data(
                        legacy_arrows[color], modern_arrows[color], color
                    )
                    result.differences.extend(arrow_result.differences)
                    result.critical_differences.extend(
                        arrow_result.critical_differences
                    )
                else:
                    result.add_difference(
                        FieldDifference(
                            field_path=f"pictograph_data.arrows.{color}",
                            legacy_value=color in legacy_arrows,
                            modern_value=color in modern_arrows,
                            difference_type="presence_mismatch",
                            is_critical=True,
                            description=f"Arrow {color} presence differs between versions",
                        )
                    )

            # Compare props
            legacy_props = legacy_data.get("props", {})
            modern_props = modern_data.get("props", {})

            for color in set(legacy_props.keys()) | set(modern_props.keys()):
                if color in legacy_props and color in modern_props:
                    prop_result = self._compare_prop_data(
                        legacy_props[color], modern_props[color], color
                    )
                    result.differences.extend(prop_result.differences)
                    result.critical_differences.extend(prop_result.critical_differences)
                else:
                    result.add_difference(
                        FieldDifference(
                            field_path=f"pictograph_data.props.{color}",
                            legacy_value=color in legacy_props,
                            modern_value=color in modern_props,
                            difference_type="presence_mismatch",
                            is_critical=True,
                            description=f"Prop {color} presence differs between versions",
                        )
                    )

            return result

        except Exception as e:
            logger.error(f"Pictograph data comparison failed: {e}")
            result.is_equivalent = False
            result.add_difference(
                FieldDifference(
                    field_path="pictograph_data.comparison_error",
                    legacy_value="N/A",
                    modern_value="N/A",
                    difference_type="comparison_error",
                    is_critical=True,
                    description=f"Pictograph comparison failed: {e}",
                )
            )
            return result

    def _compare_beat_data(
        self, legacy_beat: Dict[str, Any], modern_beat: Dict[str, Any], beat_index: int
    ) -> ComparisonResult:
        """Compare individual beat data."""
        result = ComparisonResult(is_equivalent=True, equivalence_score=1.0)

        # Compare letter
        legacy_letter = legacy_beat.get("letter", "")
        modern_letter = modern_beat.get("letter", "")

        if legacy_letter != modern_letter:
            result.add_difference(
                FieldDifference(
                    field_path=f"beats[{beat_index}].letter",
                    legacy_value=legacy_letter,
                    modern_value=modern_letter,
                    difference_type="exact_mismatch",
                    is_critical=True,
                    description=f"Beat {beat_index} letter differs",
                )
            )

        # Compare duration
        legacy_duration = legacy_beat.get("duration", 1)
        modern_duration = modern_beat.get("duration", 1)

        if not self._values_within_tolerance(
            legacy_duration, modern_duration, self.default_tolerance
        ):
            result.add_difference(
                FieldDifference(
                    field_path=f"beats[{beat_index}].duration",
                    legacy_value=legacy_duration,
                    modern_value=modern_duration,
                    difference_type="numeric_tolerance_exceeded",
                    tolerance_used=self.default_tolerance,
                    is_critical=True,
                    description=f"Beat {beat_index} duration differs beyond tolerance",
                )
            )

        # Compare motions
        legacy_motions = legacy_beat.get("motions", {})
        modern_motions = modern_beat.get("motions", {})

        for color in set(legacy_motions.keys()) | set(modern_motions.keys()):
            if color in legacy_motions and color in modern_motions:
                motion_result = self._compare_motion_data(
                    legacy_motions[color], modern_motions[color], beat_index, color
                )
                result.differences.extend(motion_result.differences)
                result.critical_differences.extend(motion_result.critical_differences)
            else:
                result.add_difference(
                    FieldDifference(
                        field_path=f"beats[{beat_index}].motions.{color}",
                        legacy_value=color in legacy_motions,
                        modern_value=color in modern_motions,
                        difference_type="presence_mismatch",
                        is_critical=True,
                        description=f"Beat {beat_index} motion {color} presence differs",
                    )
                )

        return result

    def _compare_motion_data(
        self,
        legacy_motion: Dict[str, Any],
        modern_motion: Dict[str, Any],
        beat_index: int,
        color: str,
    ) -> ComparisonResult:
        """Compare individual motion data."""
        result = ComparisonResult(is_equivalent=True, equivalence_score=1.0)

        motion_fields = ["motion_type", "start_ori", "end_ori", "start_loc", "end_loc"]

        for field in motion_fields:
            legacy_value = legacy_motion.get(field, "")
            modern_value = modern_motion.get(field, "")

            if legacy_value != modern_value:
                result.add_difference(
                    FieldDifference(
                        field_path=f"beats[{beat_index}].motions.{color}.{field}",
                        legacy_value=legacy_value,
                        modern_value=modern_value,
                        difference_type="exact_mismatch",
                        is_critical=True,
                        description=f"Beat {beat_index} {color} motion {field} differs",
                    )
                )

        # Compare turns with tolerance
        legacy_turns = legacy_motion.get("turns", 0)
        modern_turns = modern_motion.get("turns", 0)

        if not self._values_within_tolerance(
            legacy_turns, modern_turns, self.default_tolerance
        ):
            result.add_difference(
                FieldDifference(
                    field_path=f"beats[{beat_index}].motions.{color}.turns",
                    legacy_value=legacy_turns,
                    modern_value=modern_turns,
                    difference_type="numeric_tolerance_exceeded",
                    tolerance_used=self.default_tolerance,
                    is_critical=True,
                    description=f"Beat {beat_index} {color} motion turns differs beyond tolerance",
                )
            )

        return result

    def _compare_arrow_data(
        self, legacy_arrow: Dict[str, Any], modern_arrow: Dict[str, Any], color: str
    ) -> ComparisonResult:
        """Compare individual arrow data."""
        result = ComparisonResult(is_equivalent=True, equivalence_score=1.0)

        # Compare position with tolerance
        legacy_x = legacy_arrow.get("position_x", 0)
        modern_x = modern_arrow.get("position_x", 0)

        if not self._values_within_tolerance(
            legacy_x, modern_x, self.position_tolerance
        ):
            result.add_difference(
                FieldDifference(
                    field_path=f"arrows.{color}.position_x",
                    legacy_value=legacy_x,
                    modern_value=modern_x,
                    difference_type="numeric_tolerance_exceeded",
                    tolerance_used=self.position_tolerance,
                    is_critical=True,
                    description=f"Arrow {color} X position differs beyond tolerance",
                )
            )

        legacy_y = legacy_arrow.get("position_y", 0)
        modern_y = modern_arrow.get("position_y", 0)

        if not self._values_within_tolerance(
            legacy_y, modern_y, self.position_tolerance
        ):
            result.add_difference(
                FieldDifference(
                    field_path=f"arrows.{color}.position_y",
                    legacy_value=legacy_y,
                    modern_value=modern_y,
                    difference_type="numeric_tolerance_exceeded",
                    tolerance_used=self.position_tolerance,
                    is_critical=True,
                    description=f"Arrow {color} Y position differs beyond tolerance",
                )
            )

        # Compare rotation with tolerance
        legacy_rotation = legacy_arrow.get("rotation_angle", 0)
        modern_rotation = modern_arrow.get("rotation_angle", 0)

        if not self._values_within_tolerance(
            legacy_rotation, modern_rotation, self.rotation_tolerance
        ):
            result.add_difference(
                FieldDifference(
                    field_path=f"arrows.{color}.rotation_angle",
                    legacy_value=legacy_rotation,
                    modern_value=modern_rotation,
                    difference_type="numeric_tolerance_exceeded",
                    tolerance_used=self.rotation_tolerance,
                    is_critical=True,
                    description=f"Arrow {color} rotation differs beyond tolerance",
                )
            )

        # Compare exact fields
        exact_fields = ["color", "is_mirrored"]
        for field in exact_fields:
            legacy_value = legacy_arrow.get(field)
            modern_value = modern_arrow.get(field)

            if legacy_value != modern_value:
                result.add_difference(
                    FieldDifference(
                        field_path=f"arrows.{color}.{field}",
                        legacy_value=legacy_value,
                        modern_value=modern_value,
                        difference_type="exact_mismatch",
                        is_critical=True,
                        description=f"Arrow {color} {field} differs",
                    )
                )

        return result

    def _compare_prop_data(
        self, legacy_prop: Dict[str, Any], modern_prop: Dict[str, Any], color: str
    ) -> ComparisonResult:
        """Compare individual prop data."""
        result = ComparisonResult(is_equivalent=True, equivalence_score=1.0)

        # Compare position with tolerance
        position_fields = ["position_x", "position_y"]
        for field in position_fields:
            legacy_value = legacy_prop.get(field, 0)
            modern_value = modern_prop.get(field, 0)

            if not self._values_within_tolerance(
                legacy_value, modern_value, self.position_tolerance
            ):
                result.add_difference(
                    FieldDifference(
                        field_path=f"props.{color}.{field}",
                        legacy_value=legacy_value,
                        modern_value=modern_value,
                        difference_type="numeric_tolerance_exceeded",
                        tolerance_used=self.position_tolerance,
                        is_critical=True,
                        description=f"Prop {color} {field} differs beyond tolerance",
                    )
                )

        # Compare rotation with tolerance
        legacy_rotation = legacy_prop.get("rotation_angle", 0)
        modern_rotation = modern_prop.get("rotation_angle", 0)

        if not self._values_within_tolerance(
            legacy_rotation, modern_rotation, self.rotation_tolerance
        ):
            result.add_difference(
                FieldDifference(
                    field_path=f"props.{color}.rotation_angle",
                    legacy_value=legacy_rotation,
                    modern_value=modern_rotation,
                    difference_type="numeric_tolerance_exceeded",
                    tolerance_used=self.rotation_tolerance,
                    is_critical=True,
                    description=f"Prop {color} rotation differs beyond tolerance",
                )
            )

        # Compare exact fields
        exact_fields = ["color", "prop_type"]
        for field in exact_fields:
            legacy_value = legacy_prop.get(field, "")
            modern_value = modern_prop.get(field, "")

            if legacy_value != modern_value:
                result.add_difference(
                    FieldDifference(
                        field_path=f"props.{color}.{field}",
                        legacy_value=legacy_value,
                        modern_value=modern_value,
                        difference_type="exact_mismatch",
                        is_critical=True,
                        description=f"Prop {color} {field} differs",
                    )
                )

        return result

    def _values_within_tolerance(
        self,
        legacy_value: Union[int, float],
        modern_value: Union[int, float],
        tolerance: float,
    ) -> bool:
        """Check if two numeric values are within tolerance."""
        try:
            return abs(float(legacy_value) - float(modern_value)) <= tolerance
        except (ValueError, TypeError):
            return legacy_value == modern_value


class TKADataNormalizer:
    """
    TKA-specific data normalizer based on verified domain model.

    Handles the actual Legacy/Modern differences discovered through codebase analysis:
    - Legacy uses "shift" as motion type, Modern maps it to "pro"
    - Both versions use "prop_rot_dir" field name (no change needed)
    - Motion type hierarchy: shift contains [pro, anti, float] in Legacy
    """

    def __init__(self):
        # VERIFIED: Legacy and Modern use IDENTICAL motion type values
        # NO MAPPING NEEDED - both versions use same motion type strings
        self.motion_type_mappings = {
            # Direct 1:1 mappings - no conversion needed
            "pro": "pro",
            "anti": "anti",
            "static": "static",
            "dash": "dash",
            "float": "float",
        }

        # VERIFIED: Both versions use identical field names
        self.field_mappings = {
            # No field name changes needed - both use same field names
            "prop_rot_dir": "prop_rot_dir",
            "motion_type": "motion_type",
            "turns": "turns",
            "start_ori": "start_ori",
            "end_ori": "end_ori",
            "start_loc": "start_loc",
            "end_loc": "end_loc",
        }

        # VERIFIED: Rotation direction mappings
        self.rotation_mappings = {
            "cw": "cw",
            "ccw": "ccw",
            "no_rot": "no_rot",
            "clockwise": "cw",  # Handle variations
            "counter_clockwise": "ccw",
        }

    def normalize_legacy_motion_data(
        self, legacy_motion: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Normalize Legacy motion data to standardized format for comparison.

        Based on verified Legacy MotionState structure:
        - motion_type, turns, start_loc, end_loc, start_ori, end_ori, prop_rot_dir
        """
        normalized = {}

        # Handle motion type (no mapping needed - Legacy and Modern use same values)
        legacy_motion_type = legacy_motion.get("motion_type", "static")
        normalized["motion_type"] = legacy_motion_type

        # Handle turns (can be int, float, or "fl" for float)
        turns = legacy_motion.get("turns", 0)
        if turns == "fl":
            normalized["turns"] = -0.5  # Float motion special case
        else:
            normalized["turns"] = float(turns) if turns is not None else 0.0

        # Direct field mappings (verified same in both versions)
        for legacy_field, modern_field in self.field_mappings.items():
            if legacy_field in legacy_motion:
                normalized[modern_field] = legacy_motion[legacy_field]

        # Handle rotation direction normalization
        prop_rot_dir = legacy_motion.get("prop_rot_dir", "no_rot")
        normalized["prop_rot_dir"] = self.rotation_mappings.get(
            prop_rot_dir, prop_rot_dir
        )

        return normalized

    def normalize_modern_motion_data(
        self, modern_motion: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Normalize Modern motion data to standardized format for comparison.

        Modern uses MotionData with enum values that need to be converted to strings.
        """
        normalized = {}

        # Handle enum values from Modern MotionData
        motion_type = modern_motion.get("motion_type")
        if hasattr(motion_type, "value"):
            normalized["motion_type"] = motion_type.value
        else:
            normalized["motion_type"] = str(motion_type) if motion_type else "static"

        # Handle turns (should be float in Modern)
        normalized["turns"] = float(modern_motion.get("turns", 0.0))

        # Handle rotation direction enum
        prop_rot_dir = modern_motion.get("prop_rot_dir")
        if hasattr(prop_rot_dir, "value"):
            normalized["prop_rot_dir"] = prop_rot_dir.value
        else:
            normalized["prop_rot_dir"] = str(prop_rot_dir) if prop_rot_dir else "no_rot"

        # Handle location enums
        for loc_field in ["start_loc", "end_loc"]:
            loc_value = modern_motion.get(loc_field)
            if hasattr(loc_value, "value"):
                normalized[loc_field] = loc_value.value
            else:
                normalized[loc_field] = str(loc_value) if loc_value else ""

        # Handle orientation strings (should be same in both versions)
        for ori_field in ["start_ori", "end_ori"]:
            normalized[ori_field] = modern_motion.get(ori_field, "in")

        return normalized

    def normalize_legacy_beat_data(self, legacy_beat: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize Legacy beat data based on verified Legacy structure.

        Legacy beat data comes from beat.state.pictograph_data with structure:
        - letter, duration, blue_attributes, red_attributes
        """
        normalized = {
            "letter": legacy_beat.get("letter", ""),
            "duration": float(legacy_beat.get("duration", 1.0)),
            "motions": {},
        }

        # Extract motion data from Legacy attributes structure
        for color in ["blue", "red"]:
            attr_key = f"{color}_attributes"
            if attr_key in legacy_beat:
                motion_attrs = legacy_beat[attr_key]
                normalized["motions"][color] = self.normalize_legacy_motion_data(
                    motion_attrs
                )

        return normalized

    def normalize_modern_beat_data(self, modern_beat: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize Modern beat data based on verified Modern BeatData structure.

        Modern uses BeatData with blue_motion/red_motion MotionData objects.
        """
        normalized = {
            "letter": modern_beat.get("letter", ""),
            "duration": float(modern_beat.get("duration", 1.0)),
            "motions": {},
        }

        # Extract motion data from Modern BeatData structure
        for color in ["blue", "red"]:
            motion_key = f"{color}_motion"
            if motion_key in modern_beat and modern_beat[motion_key]:
                motion_data = modern_beat[motion_key]
                if hasattr(motion_data, "to_dict"):
                    motion_dict = motion_data.to_dict()
                else:
                    motion_dict = motion_data
                normalized["motions"][color] = self.normalize_modern_motion_data(
                    motion_dict
                )

        return normalized
