from typing import List, Optional, Dict, Any, Callable, TYPE_CHECKING
from PyQt6.QtCore import QObject

from domain.models.core_models import BeatData

if TYPE_CHECKING:
    from application.services.positioning.position_matching_service import (
        PositionMatchingService,
    )
    from domain.models.core_models import SequenceData


class BeatDataLoader(QObject):
    """Handles loading beat options and position matching logic"""

    # Position mapping from location combinations to position names
    # Tuple format: (blue_location, red_location) -> position_name
    # Where: blue = left hand, red = right hand
    POSITIONS_MAP = {
        ("s", "n"): "alpha1",
        ("sw", "ne"): "alpha2",
        ("w", "e"): "alpha3",
        ("nw", "se"): "alpha4",
        ("n", "s"): "alpha5",
        ("ne", "sw"): "alpha6",
        ("e", "w"): "alpha7",
        ("se", "nw"): "alpha8",
        ("n", "n"): "beta1",
        ("ne", "ne"): "beta2",
        ("e", "e"): "beta3",
        ("se", "se"): "beta4",
        ("s", "s"): "beta5",
        ("sw", "sw"): "beta6",
        ("w", "w"): "beta7",
        ("nw", "nw"): "beta8",
        ("w", "n"): "gamma1",
        ("nw", "ne"): "gamma2",
        ("n", "e"): "gamma3",
        ("ne", "se"): "gamma4",
        ("e", "s"): "gamma5",
        ("se", "sw"): "gamma6",
        ("s", "w"): "gamma7",
        ("sw", "nw"): "gamma8",
        ("e", "n"): "gamma9",
        ("se", "ne"): "gamma10",
        ("s", "e"): "gamma11",
        ("sw", "se"): "gamma12",
        ("w", "s"): "gamma13",
        ("nw", "sw"): "gamma14",
        ("n", "w"): "gamma15",
        ("ne", "nw"): "gamma16",
    }

    def __init__(self):
        super().__init__()
        self._beat_options: List[BeatData] = (
            []
        )  # Create reverse mapping from positions_map for location tuples to positions
        self._location_to_position_map = self._create_location_to_position_mapping()

        # Initialize services for dynamic refresh
        try:
            from application.services.positioning.position_matching_service import (
                PositionMatchingService,
            )
            from application.services.core.data_conversion_service import (
                DataConversionService,
            )

            self.position_service = PositionMatchingService()
            self.conversion_service = DataConversionService()
        except Exception as e:
            # Failed to initialize services for BeatDataLoader
            self.position_service = None
            self.conversion_service = None

    def _create_location_to_position_mapping(self) -> Dict[tuple, str]:
        """Create reverse mapping from location tuples to position names using the class POSITIONS_MAP

        Tuple format: (blue_location, red_location) -> position_name
        Where: blue = left hand, red = right hand
        """
        return self.POSITIONS_MAP.copy()

    def load_motion_combinations(
        self, sequence_data: List[Dict[str, Any]]
    ) -> List[BeatData]:
        """Load motion combinations using data-driven position matching"""

        try:
            from application.services.positioning.position_matching_service import (
                PositionMatchingService,
            )
            from application.services.core.data_conversion_service import (
                DataConversionService,
            )

            position_service = PositionMatchingService()
            conversion_service = DataConversionService()

            if not sequence_data or len(sequence_data) < 2:
                return self._load_sample_beat_options()

            last_beat = sequence_data[-1]
            last_end_pos = self._extract_end_position(last_beat, position_service)

            if not last_end_pos:
                return self._load_sample_beat_options()

            next_options = position_service.get_next_options(last_end_pos)
            if not next_options:
                return self._load_sample_beat_options()

            beat_options = []
            for option_data in next_options:
                try:
                    # Check if it's already a BeatData object
                    from domain.models.core_models import BeatData

                    if isinstance(option_data, BeatData):
                        # It's already a BeatData object, use it directly
                        beat_options.append(option_data)
                    elif hasattr(option_data, "get"):
                        # It's a dictionary, convert it to BeatData
                        beat_data = (
                            conversion_service.convert_v1_pictograph_to_beat_data(
                                option_data
                            )
                        )
                        beat_options.append(beat_data)
                    else:
                        # Try to use it as BeatData anyway
                        if hasattr(option_data, "letter"):
                            beat_options.append(option_data)
                        else:
                            continue
                except Exception as e:
                    # Skip invalid options silently
                    continue

            self._beat_options = beat_options
            return beat_options

        except Exception as e:
            return self._load_sample_beat_options()

    def _extract_end_position(
        self, last_beat: Dict[str, Any], position_service: "PositionMatchingService"
    ) -> Optional[str]:
        """Extract end position from last beat data using V1-compatible logic"""
        if "end_pos" in last_beat:
            end_pos = last_beat.get("end_pos")
            return end_pos

        if "metadata" in last_beat and "end_pos" in last_beat["metadata"]:
            end_pos = last_beat["metadata"].get("end_pos")
            return end_pos

        # Extract from motion data (V1 logic)
        if self._has_motion_attributes(last_beat):
            end_pos = self._calculate_end_position_from_motions(last_beat)
            if end_pos:
                return end_pos  # Fallback to position service
        try:
            available_positions = position_service.get_available_start_positions()
            if available_positions:
                fallback_pos = available_positions[0]
                return fallback_pos
            else:
                alpha1_options = position_service.get_alpha1_options()
                fallback_pos = "alpha1" if alpha1_options else None
                return fallback_pos
        except Exception as e:
            return None

    def _has_motion_attributes(self, beat_data: Dict[str, Any]) -> bool:
        """Check if beat data has motion attributes for end position calculation"""
        return (
            "blue_attributes" in beat_data
            and "red_attributes" in beat_data
            and "end_loc" in beat_data["blue_attributes"]
            and "end_loc" in beat_data["red_attributes"]
        )

    def _calculate_end_position_from_motions(
        self, beat_data: Dict[str, Any]
    ) -> Optional[str]:
        """Calculate end position from motion data using correct positions mapping"""
        try:
            blue_attrs = beat_data.get("blue_attributes", {})
            red_attrs = beat_data.get("red_attributes", {})

            blue_end_loc = blue_attrs.get("end_loc")
            red_end_loc = red_attrs.get("end_loc")

            if blue_end_loc and red_end_loc:
                # Create position key: (blue_location, red_location) where blue=left, red=right
                position_key = (blue_end_loc, red_end_loc)
                end_position = self._location_to_position_map.get(position_key)

                if end_position:
                    return end_position
                else:
                    return None

        except Exception as e:
            pass

        return None

    def _load_sample_beat_options(self) -> List[BeatData]:
        """Load sample beat options as fallback"""
        try:
            from application.services.old_services_before_consolidation.pictograph_dataset_service import (
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

            from application.services.positioning.position_matching_service import (
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
            self._beat_options = []
            return self._beat_options

    def get_beat_options(self) -> List[BeatData]:
        """Get current beat options"""
        return self._beat_options

    def refresh_options(self) -> List[BeatData]:
        """Refresh beat options (reload sample data)"""
        return self._load_sample_beat_options()

    def refresh_options_from_sequence(
        self, sequence_data: List[Dict[str, Any]]
    ) -> List[BeatData]:
        """Refresh options based on provided sequence data (V1-compatible)"""
        if not sequence_data or len(sequence_data) <= 1:
            return self.load_beat_options()

        # Get the last beat (excluding metadata at index 0)
        last_beat = sequence_data[-1]

        try:
            # Check if services are available
            if not self.position_service or not self.conversion_service:
                return self._load_sample_beat_options()

            # Extract end position from last beat
            end_position = self._extract_end_position(last_beat, self.position_service)

            if not end_position:
                return self._load_sample_beat_options()

            # Get next options from position service
            next_options = self.position_service.get_next_options(end_position)

            if not next_options:
                return self._load_sample_beat_options()

            # Optimized: Batch convert to BeatData format
            beat_options = self._batch_convert_options(next_options)
            return beat_options

        except Exception as e:
            return self._load_sample_beat_options()

    def _batch_convert_options(self, options_list: List[Any]) -> List[BeatData]:
        """Optimized batch conversion of options to BeatData format"""
        from domain.models.core_models import BeatData

        beat_options = []

        # Pre-filter and categorize options for batch processing
        beat_data_objects = []
        dict_objects = []
        other_objects = []

        for option_data in options_list:
            if isinstance(option_data, BeatData):
                beat_data_objects.append(option_data)
            elif hasattr(option_data, "get"):
                dict_objects.append(option_data)
            elif hasattr(option_data, "letter"):
                other_objects.append(option_data)

        # Add already-converted BeatData objects directly
        beat_options.extend(beat_data_objects)

        # Batch convert dictionary objects
        if dict_objects:
            try:
                for option_data in dict_objects:
                    beat_data = (
                        self.conversion_service.convert_v1_pictograph_to_beat_data(
                            option_data
                        )
                    )
                    beat_options.append(beat_data)
            except Exception as e:
                print(f"⚠️ Batch conversion error for dict objects: {e}")

        # Add other valid objects
        beat_options.extend(other_objects)

        return beat_options

    def refresh_options_from_v2_sequence(
        self, sequence: "SequenceData"
    ) -> List[BeatData]:
        """PURE V2: Refresh options based on V2 SequenceData - no conversion needed!"""
        import time

        start_time = time.perf_counter()

        try:
            # Work directly with V2 SequenceData
            if not sequence or sequence.length == 0:
                return self._load_sample_beat_options()

            # Get the last beat directly from V2 sequence
            last_beat = sequence.beats[-1] if sequence.beats else None
            if not last_beat or last_beat.is_blank:
                return self._load_sample_beat_options()

            # Extract end position directly from V2 BeatData
            end_position = self._extract_v2_end_position(last_beat)
            if not end_position:
                return self._load_sample_beat_options()

            # Get next options using position service
            if not self.position_service:
                return self._load_sample_beat_options()

            next_options = self.position_service.get_next_options(end_position)
            if not next_options:
                return self._load_sample_beat_options()

            # Options are already BeatData objects from position service
            total_time = (time.perf_counter() - start_time) * 1000
            print(f"⚡ PURE V2 BEAT LOADER: {total_time:.1f}ms")
            print(
                f"🎯 Found {len(next_options)} options for end position: {end_position}"
            )

            return next_options

        except Exception as e:
            print(f"❌ Error in pure V2 option refresh: {e}")
            return self._load_sample_beat_options()

    def _extract_v2_end_position(self, beat_data: "BeatData") -> Optional[str]:
        """Extract end position directly from V2 BeatData"""
        # First check metadata
        if beat_data.metadata and "end_pos" in beat_data.metadata:
            return beat_data.metadata["end_pos"]

        # Calculate from motion data if available
        if beat_data.blue_motion and beat_data.red_motion:
            blue_end = (
                beat_data.blue_motion.end_loc.value
                if beat_data.blue_motion.end_loc
                else "s"
            )
            red_end = (
                beat_data.red_motion.end_loc.value
                if beat_data.red_motion.end_loc
                else "s"
            )  # Create position key: (blue_location, red_location) where blue=left, red=right
            position_key = (blue_end, red_end)
            end_pos = self._location_to_position_map.get(position_key, "beta5")
            print(f"🎯 Calculated V2 end_pos: {end_pos} for beat {beat_data.letter}")
            return end_pos

        # Fallback
        return "beta5"
