"""
Motion Combination Service for Kinetic Constructor v2

This service generates valid motion combinations based on the selected start position
and current sequence state, providing options for the option picker.
"""

from typing import List, Dict, Any, Optional

from domain.models.core_models import BeatData
from .position_matching_service import PositionMatchingService
from .data_conversion_service import DataConversionService


class MotionCombinationService:
    """Service for generating valid motion combinations using real dataset."""

    def __init__(self):
        self.position_service = PositionMatchingService()
        self.conversion_service = DataConversionService()

    def generate_motion_combinations(
        self, sequence_data: List[Dict[str, Any]], max_combinations: int = 36
    ) -> List[BeatData]:
        """Generate real motion combinations from dataset."""
        if len(sequence_data) <= 1:
            alpha1_options = self.position_service.get_alpha1_options()[
                :max_combinations
            ]
            return [
                self.conversion_service.convert_v1_pictograph_to_beat_data(opt)
                for opt in alpha1_options
            ]

        # Get last beat's end position
        last_beat = sequence_data[-1]
        last_end_pos = self._extract_end_position(last_beat)

        if not last_end_pos:
            alpha1_options = self.position_service.get_alpha1_options()[
                :max_combinations
            ]
            return [
                self.conversion_service.convert_v1_pictograph_to_beat_data(opt)
                for opt in alpha1_options
            ]

        # Use position matching to get real next options
        next_options = self.position_service.get_next_options(last_end_pos)

        # Convert to BeatData format
        combinations = []
        for option_data in next_options[:max_combinations]:
            try:
                beat_data = self.conversion_service.convert_v1_pictograph_to_beat_data(
                    option_data
                )
                combinations.append(beat_data)
            except Exception as e:
                print(f"Failed to convert option: {e}")
                continue

        return combinations

    def _extract_end_position(self, beat_data: Dict[str, Any]) -> Optional[str]:
        """Extract end position from beat data."""
        return (
            beat_data.get("end_pos")
            or beat_data.get("metadata", {}).get("end_pos")
            or "beta5"
        )  # fallback
