from typing import List, Optional, Dict, Any, Callable
from PyQt6.QtCore import QObject

from ....domain.models.core_models import BeatData


class BeatDataLoader(QObject):
    """Handles loading beat options and position matching logic"""

    def __init__(self):
        super().__init__()
        self._beat_options: List[BeatData] = []

    def load_motion_combinations(
        self, sequence_data: List[Dict[str, Any]]
    ) -> List[BeatData]:
        """Load motion combinations using data-driven position matching"""
        try:
            from ....application.services.position_matching_service import (
                PositionMatchingService,
            )
            from ....application.services.data_conversion_service import (
                DataConversionService,
            )

            position_service = PositionMatchingService()
            conversion_service = DataConversionService()

            if not sequence_data or len(sequence_data) < 2:
                print("⚠️ No valid sequence data for position matching")
                return self._load_sample_beat_options()

            last_beat = sequence_data[-1]
            last_end_pos = self._extract_end_position(last_beat, position_service)

            if not last_end_pos:
                print("❌ No end position found in last beat")
                return self._load_sample_beat_options()

            print(f"🎯 Using position matching for end_pos: {last_end_pos}")

            next_options = position_service.get_next_options(last_end_pos)
            if not next_options:
                print(f"❌ No options found for position: {last_end_pos}")
                return self._load_sample_beat_options()

            beat_options = []
            for option_data in next_options:
                try:
                    beat_data = conversion_service.convert_v1_pictograph_to_beat_data(
                        option_data
                    )
                    beat_options.append(beat_data)
                except Exception as e:
                    print(f"⚠️ Failed to convert option: {e}")

            self._beat_options = beat_options
            print(
                f"✅ Loaded {len(beat_options)} motion combinations via position matching"
            )
            return beat_options

        except Exception as e:
            print(f"❌ Error in position matching: {e}")
            return self._load_sample_beat_options()

    def _extract_end_position(
        self, last_beat: Dict[str, Any], position_service
    ) -> Optional[str]:
        """Extract end position from last beat data"""
        if "end_pos" in last_beat:
            return last_beat.get("end_pos")
        elif "metadata" in last_beat and "end_pos" in last_beat["metadata"]:
            return last_beat["metadata"].get("end_pos")
        else:
            print("🔍 Attempting to extract end position from motion data...")
            try:
                available_positions = position_service.get_available_start_positions()
                if available_positions:
                    return available_positions[0]
                else:
                    alpha1_options = position_service.get_alpha1_options()
                    return "alpha1" if alpha1_options else None
            except Exception as e:
                print(f"❌ Failed to get dataset positions: {e}")
                return None

    def _load_sample_beat_options(self) -> List[BeatData]:
        """Load sample beat options as fallback"""
        try:
            from ....application.services.pictograph_dataset_service import (
                PictographDatasetService,
            )

            dataset_service = PictographDatasetService()

            if (
                hasattr(dataset_service, "_diamond_dataset")
                and dataset_service._diamond_dataset is not None
            ):
                if not dataset_service._diamond_dataset.empty:
                    sample_entries = dataset_service._diamond_dataset.head(6)
                    beat_options = []
                    for _, entry in sample_entries.iterrows():
                        try:
                            beat_data = dataset_service._dataset_entry_to_beat_data(
                                entry
                            )
                            beat_options.append(beat_data)
                        except Exception as e:
                            print(f"Failed to convert sample entry: {e}")
                            continue

                    if beat_options:
                        self._beat_options = beat_options
                        return beat_options

            from ....application.services.position_matching_service import (
                PositionMatchingService,
            )

            position_service = PositionMatchingService()
            alpha1_options = position_service.get_alpha1_options()

            if alpha1_options:
                self._beat_options = alpha1_options[:6]
                return self._beat_options
            else:
                self._beat_options = []
                return self._beat_options

        except Exception as e:
            print(f"Failed to load real sample data: {e}")
            self._beat_options = []
            return self._beat_options

    def get_beat_options(self) -> List[BeatData]:
        """Get current beat options"""
        return self._beat_options

    def refresh_options(self) -> List[BeatData]:
        """Refresh beat options (reload sample data)"""
        return self._load_sample_beat_options()
