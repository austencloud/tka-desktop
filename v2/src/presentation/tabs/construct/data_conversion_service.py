"""
DataConversionService

Handles data conversions, position calculations, and caching utilities for the construct tab.
Responsible for converting between different data formats and optimizing performance through caching.
"""

from typing import List, Dict, Any
from domain.models.core_models import SequenceData, BeatData


class DataConversionService:
    """
    Handles data conversion operations and caching for the construct tab.
    
    Responsibilities:
    - Position key extraction and parsing
    - End position calculations with caching
    - Sequence format conversions (Modern to Legacy)
    - Cache management for performance optimization
    """
    
    def __init__(self):
        # Performance optimization: Cache for position calculations
        self._position_cache = {}
        self._sequence_conversion_cache = {}
    
    def extract_end_position_from_position_key(self, position_key: str) -> str:
        """Extract the actual end position from a position key like 'beta5_beta5'"""
        # Position keys are in format "start_end", we want the end part
        if "_" in position_key:
            parts = position_key.split("_")
            if len(parts) == 2:
                return parts[1]  # Return the end position part

        # Fallback: if no underscore, assume it's already the position
        return position_key

    def get_cached_end_position(self, beat: BeatData) -> str:
        """Get end position with caching to eliminate redundant calculations"""
        # Create cache key from motion data
        blue_end = (
            beat.blue_motion.end_loc.value
            if beat.blue_motion and beat.blue_motion.end_loc
            else "s"
        )
        red_end = (
            beat.red_motion.end_loc.value
            if beat.red_motion and beat.red_motion.end_loc
            else "s"
        )

        cache_key = f"{blue_end}_{red_end}"

        # Check cache first
        if cache_key in self._position_cache:
            return self._position_cache[cache_key]

        # Calculate and cache the result
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

        end_pos = position_map.get((blue_end, red_end), "beta5")
        self._position_cache[cache_key] = end_pos
        return end_pos

    def convert_sequence_to_legacy_format(
        self, sequence: SequenceData
    ) -> List[Dict[str, Any]]:
        """Convert Modern SequenceData to Legacy-compatible format for option picker with caching"""
        # Create cache key from sequence hash
        sequence_hash = hash(
            tuple(beat.letter + str(beat.beat_number) for beat in sequence.beats)
        )

        # Check cache first
        if sequence_hash in self._sequence_conversion_cache:
            return self._sequence_conversion_cache[sequence_hash]

        try:
            # Start with metadata entry (Legacy format)
            legacy_sequence = [{"metadata": "sequence_info"}]

            # Convert each beat to Legacy format
            for beat in sequence.beats:
                if beat and not beat.is_blank:
                    beat_dict = beat.to_dict()

                    # Ensure Legacy-compatible structure
                    if "metadata" not in beat_dict:
                        beat_dict["metadata"] = {}

                    # CRITICAL FIX: Use end_pos from metadata if available, otherwise calculate
                    if "end_pos" not in beat_dict:
                        # First try to get end_pos from beat metadata
                        metadata_end_pos = (
                            beat.metadata.get("end_pos") if beat.metadata else None
                        )

                        if metadata_end_pos:
                            # Use the correct end position from metadata
                            beat_dict["end_pos"] = metadata_end_pos
                            print(
                                f"🎯 Using metadata end_pos: {metadata_end_pos} for beat {beat.letter}"
                            )
                        elif beat.blue_motion and beat.red_motion:
                            # Optimized: Use cached position calculation
                            end_pos = self.get_cached_end_position(beat)
                            beat_dict["end_pos"] = end_pos
                            print(
                                f"🎯 Cached end_pos: {end_pos} for beat {beat.letter} from motion data"
                            )
                        else:
                            # Final fallback
                            beat_dict["end_pos"] = "beta5"
                            print(
                                f"⚠️ Using fallback end_pos: beta5 for beat {beat.letter}"
                            )

                    legacy_sequence.append(beat_dict)

            # Cache the result for future use
            self._sequence_conversion_cache[sequence_hash] = legacy_sequence

            # Limit cache size to prevent memory issues
            if len(self._sequence_conversion_cache) > 100:
                # Remove oldest entries (simple FIFO)
                oldest_key = next(iter(self._sequence_conversion_cache))
                del self._sequence_conversion_cache[oldest_key]

            return legacy_sequence

        except Exception as e:
            print(f"❌ Error converting sequence to Legacy format: {e}")
            return [{"metadata": "sequence_info"}]  # Fallback to empty sequence
    
    def clear_caches(self):
        """Clear all caches to free memory"""
        self._position_cache.clear()
        self._sequence_conversion_cache.clear()
        print("🧹 Data conversion caches cleared")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get statistics about cache usage"""
        return {
            "position_cache_size": len(self._position_cache),
            "sequence_conversion_cache_size": len(self._sequence_conversion_cache),
        }
