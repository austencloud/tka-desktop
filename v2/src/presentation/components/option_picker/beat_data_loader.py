from typing import List, Optional, Dict, Any, Callable
from PyQt6.QtCore import QObject

from ....domain.models.core_models import BeatData


class BeatDataLoader(QObject):
    """Handles loading beat options and position matching logic"""

    def __init__(self):
        super().__init__()
        self._beat_options: List[BeatData] = []

        # Initialize services for dynamic refresh
        try:
            from ....application.services.positioning.position_matching_service import (
                PositionMatchingService,
            )
            from ....application.services.core.data_conversion_service import (
                DataConversionService,
            )

            self.position_service = PositionMatchingService()
            self.conversion_service = DataConversionService()
        except Exception as e:
            print(f"⚠️ Failed to initialize services for BeatDataLoader: {e}")
            self.position_service = None
            self.conversion_service = None

    def load_motion_combinations(
        self, sequence_data: List[Dict[str, Any]]
    ) -> List[BeatData]:
        """Load motion combinations using data-driven position matching"""
        print(f"\n🔄 BEAT DATA LOADER: Loading motion combinations")
        print(f"   Sequence Data Length: {len(sequence_data) if sequence_data else 0}")
        if sequence_data:
            print(f"   Sequence Data: {sequence_data}")

        try:
            from ....application.services.positioning.position_matching_service import (
                PositionMatchingService,
            )
            from ....application.services.core.data_conversion_service import (
                DataConversionService,
            )

            position_service = PositionMatchingService()
            conversion_service = DataConversionService()

            if not sequence_data or len(sequence_data) < 2:
                print(
                    "⚠️ No valid sequence data for position matching - FALLING BACK TO ALPHA-1"
                )
                return self._load_sample_beat_options()

            last_beat = sequence_data[-1]
            print(f"   Last Beat: {last_beat}")

            last_end_pos = self._extract_end_position(last_beat, position_service)

            if not last_end_pos:
                print("❌ No end position found in last beat - FALLING BACK TO ALPHA-1")
                return self._load_sample_beat_options()

            print(f"🎯 Using position matching for end_pos: {last_end_pos}")

            next_options = position_service.get_next_options(last_end_pos)
            if not next_options:
                print(
                    f"❌ No options found for position: {last_end_pos} - FALLING BACK TO ALPHA-1"
                )
                return self._load_sample_beat_options()

            beat_options = []
            for option_data in next_options:
                try:
                    # Check if it's already a BeatData object
                    from ....domain.models.core_models import BeatData

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
            print(f"❌ Error in position matching: {e} - FALLING BACK TO ALPHA-1")
            return self._load_sample_beat_options()

    def _extract_end_position(
        self, last_beat: Dict[str, Any], position_service
    ) -> Optional[str]:
        """Extract end position from last beat data using V1-compatible logic"""
        # First try direct end_pos field (V1 format)
        if "end_pos" in last_beat:
            end_pos = last_beat.get("end_pos")
            print(f"🎯 Found direct end_pos: {end_pos}")
            return end_pos

        # Try metadata end_pos (V2 format)
        if "metadata" in last_beat and "end_pos" in last_beat["metadata"]:
            end_pos = last_beat["metadata"].get("end_pos")
            print(f"🎯 Found metadata end_pos: {end_pos}")
            return end_pos

        # Extract from motion data (V1 logic)
        if self._has_motion_attributes(last_beat):
            end_pos = self._calculate_end_position_from_motions(last_beat)
            if end_pos:
                print(f"🎯 Calculated end_pos from motions: {end_pos}")
                return end_pos

        # Fallback to position service
        print("🔍 Attempting to extract end position from position service...")
        try:
            available_positions = position_service.get_available_start_positions()
            if available_positions:
                fallback_pos = available_positions[0]
                print(f"⚠️ Using fallback position: {fallback_pos}")
                return fallback_pos
            else:
                alpha1_options = position_service.get_alpha1_options()
                fallback_pos = "alpha1" if alpha1_options else None
                print(f"⚠️ Using alpha1 fallback: {fallback_pos}")
                return fallback_pos
        except Exception as e:
            print(f"❌ Failed to get dataset positions: {e}")
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
        """Calculate end position from motion data (V1 logic)"""
        try:
            blue_attrs = beat_data.get("blue_attributes", {})
            red_attrs = beat_data.get("red_attributes", {})

            blue_end_loc = blue_attrs.get("end_loc")
            red_end_loc = red_attrs.get("end_loc")

            if blue_end_loc and red_end_loc:
                # Map V1 location format to position format
                position_map = {
                    ("n", "n"): "alpha1",
                    ("n", "e"): "alpha2",
                    ("n", "s"): "alpha3",
                    ("n", "w"): "alpha4",
                    ("e", "n"): "alpha5",
                    ("e", "e"): "alpha6",
                    ("e", "s"): "alpha7",
                    ("e", "w"): "alpha8",
                    ("s", "n"): "beta1",
                    ("s", "e"): "beta2",
                    ("s", "s"): "beta3",
                    ("s", "w"): "beta4",
                    ("w", "n"): "beta5",
                    ("w", "e"): "beta6",
                    ("w", "s"): "beta7",
                    ("w", "w"): "beta8",
                }

                position_key = (blue_end_loc, red_end_loc)
                end_position = position_map.get(position_key)

                if end_position:
                    return end_position
                else:
                    print(f"⚠️ Unknown location combination: {position_key}")
                    return None

        except Exception as e:
            print(f"❌ Error calculating end position from motions: {e}")

        return None

    def _load_sample_beat_options(self) -> List[BeatData]:
        """Load sample beat options as fallback"""
        print("🔄 FALLBACK: Loading sample beat options (hardcoded data)")
        try:
            from ....application.services.old_services_before_consolidation.pictograph_dataset_service import (
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

            from ....application.services.positioning.position_matching_service import (
                PositionMatchingService,
            )

            position_service = PositionMatchingService()
            alpha1_options = position_service.get_alpha1_options()

            if alpha1_options:
                self._beat_options = alpha1_options[:6]
                print(
                    f"🔄 FALLBACK: Using alpha1 options as fallback: {len(self._beat_options)} options"
                )
                if self._beat_options:
                    letters = [opt.letter for opt in self._beat_options[:5]]
                    print(f"   📋 Fallback option letters: {letters}")
                return self._beat_options
            else:
                self._beat_options = []
                print("🔄 FALLBACK: No alpha1 options available, returning empty list")
                return self._beat_options

        except Exception as e:
            print(f"❌ FALLBACK: Failed to load real sample data: {e}")
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
        print(
            f"🔄 DYNAMIC UPDATE DEBUG: Refreshing options from sequence with {len(sequence_data)} entries"
        )
        print(f"   📊 Full sequence data: {sequence_data}")

        if not sequence_data or len(sequence_data) <= 1:
            print(
                "⚠️ FALLBACK TRIGGER: No sequence data or only metadata, using initial options"
            )
            return self.load_beat_options()

        # Get the last beat (excluding metadata at index 0)
        last_beat = sequence_data[-1]
        print(
            f"🎯 Last beat data: {last_beat.get('letter', 'Unknown')} at position {last_beat.get('end_pos', 'Unknown')}"
        )
        print(f"   📋 Last beat full data: {last_beat}")

        try:
            # Check if services are available
            if not self.position_service or not self.conversion_service:
                print(
                    "⚠️ FALLBACK TRIGGER: Services not available, using fallback options"
                )
                print(f"   Position service: {self.position_service}")
                print(f"   Conversion service: {self.conversion_service}")
                return self._load_sample_beat_options()

            # Extract end position from last beat
            end_position = self._extract_end_position(last_beat, self.position_service)

            if not end_position:
                print(
                    "⚠️ FALLBACK TRIGGER: Could not extract end position, using fallback options"
                )
                return self._load_sample_beat_options()

            print(f"🎯 SUCCESS: Using end position: {end_position}")

            # Get next options from position service
            next_options = self.position_service.get_next_options(end_position)

            if not next_options:
                print(
                    f"⚠️ FALLBACK TRIGGER: No options found for position {end_position}"
                )
                return self._load_sample_beat_options()

            # Convert to BeatData format
            beat_options = []
            for option_data in next_options:
                try:
                    # Check if it's already a BeatData object
                    from ....domain.models.core_models import BeatData

                    if isinstance(option_data, BeatData):
                        # It's already a BeatData object, use it directly
                        beat_options.append(option_data)
                    elif hasattr(option_data, "get"):
                        # It's a dictionary, convert it to BeatData
                        beat_data = (
                            self.conversion_service.convert_v1_pictograph_to_beat_data(
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
                    print(f"❌ Failed to convert option: {e}")
                    continue

            print(
                f"✅ SUCCESS: Loaded {len(beat_options)} next options for position {end_position}"
            )
            if beat_options:
                letters = [opt.letter for opt in beat_options[:5]]
                print(f"   📋 First 5 option letters: {letters}")
            return beat_options

        except Exception as e:
            print(f"❌ FALLBACK TRIGGER: Error refreshing options from sequence: {e}")
            import traceback

            traceback.print_exc()
            return self._load_sample_beat_options()
