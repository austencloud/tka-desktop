#!/usr/bin/env python3
"""
Standalone Beat Factory - Processes sequence data into beat data structures.

This module converts sequence dictionaries into simplified beat data structures
that can be used for image rendering without dependencies on the main application.
"""

from typing import Dict, List, Optional


class StandaloneBeatFactory:
    """
    Factory for processing sequence data into beat data structures.

    This class extracts the essential information from sequence dictionaries
    and creates simplified beat data that can be rendered independently.
    """

    def __init__(self):
        """Initialize the standalone beat factory."""
        pass

    def process_sequence_to_beat_data(self, sequence_data: List[Dict]) -> List[Dict]:
        """
        Process sequence data into simplified beat data structures.

        Args:
            sequence_data: List of sequence dictionaries

        Returns:
            List of simplified beat data dictionaries
        """
        beat_data_list = []

        for entry in sequence_data:
            # Skip metadata entries
            if not entry.get("beat"):
                continue

            # Extract essential beat information
            beat_data = self._extract_beat_data(entry)
            if beat_data:
                beat_data_list.append(beat_data)

        return beat_data_list

    def _extract_beat_data(self, sequence_entry: Dict) -> Optional[Dict]:
        """
        Extract essential beat data from a sequence entry.

        Args:
            sequence_entry: Single sequence dictionary entry

        Returns:
            Simplified beat data dictionary or None if invalid
        """
        try:
            beat_data = {
                "beat_number": sequence_entry.get("beat", 0),
                "letter": sequence_entry.get("letter", ""),
                "start_pos": sequence_entry.get("start_pos", ""),
                "end_pos": sequence_entry.get("end_pos", ""),
                "motion_type": sequence_entry.get("motion_type", "static"),
                "prop_rot_dir": sequence_entry.get("prop_rot_dir", "cw"),
                "turns": sequence_entry.get("turns", 0),
            }

            # Extract color-specific attributes if available
            blue_attrs = sequence_entry.get("blue_attributes", {})
            red_attrs = sequence_entry.get("red_attributes", {})

            beat_data["blue_attributes"] = {
                "motion_type": blue_attrs.get("motion_type", beat_data["motion_type"]),
                "prop_rot_dir": blue_attrs.get(
                    "prop_rot_dir", beat_data["prop_rot_dir"]
                ),
                "start_loc": blue_attrs.get("start_loc", beat_data["start_pos"]),
                "end_loc": blue_attrs.get("end_loc", beat_data["end_pos"]),
                "turns": blue_attrs.get("turns", beat_data["turns"]),
            }

            beat_data["red_attributes"] = {
                "motion_type": red_attrs.get("motion_type", beat_data["motion_type"]),
                "prop_rot_dir": red_attrs.get(
                    "prop_rot_dir", "ccw"
                ),  # Default opposite
                "start_loc": red_attrs.get("start_loc", beat_data["start_pos"]),
                "end_loc": red_attrs.get("end_loc", beat_data["end_pos"]),
                "turns": red_attrs.get("turns", beat_data["turns"]),
            }

            return beat_data

        except Exception as e:
            print(f"Warning: Failed to extract beat data from entry: {e}")
            return None

    def create_start_position_data(self, sequence_data: List[Dict]) -> Optional[Dict]:
        """
        Create start position data from sequence.

        Args:
            sequence_data: List of sequence dictionaries

        Returns:
            Start position data dictionary or None
        """
        # Look for explicit start position data
        for entry in sequence_data:
            if entry.get("sequence_start_position"):
                return entry

        # If no explicit start position, derive from first beat
        for entry in sequence_data:
            if entry.get("beat") == 1:
                return {
                    "sequence_start_position": True,
                    "start_pos": entry.get("start_pos", "alpha1"),
                    "blue_attributes": entry.get("blue_attributes", {}),
                    "red_attributes": entry.get("red_attributes", {}),
                }

        return None

    def validate_beat_data(self, beat_data: Dict) -> bool:
        """
        Validate that beat data contains required fields.

        Args:
            beat_data: Beat data dictionary to validate

        Returns:
            True if valid, False otherwise
        """
        required_fields = [
            "beat_number",
            "letter",
            "start_pos",
            "end_pos",
            "blue_attributes",
            "red_attributes",
        ]

        for field in required_fields:
            if field not in beat_data:
                return False

        # Validate attribute dictionaries
        attr_fields = ["motion_type", "prop_rot_dir", "start_loc", "end_loc", "turns"]

        for color in ["blue_attributes", "red_attributes"]:
            if not isinstance(beat_data[color], dict):
                return False
            for attr_field in attr_fields:
                if attr_field not in beat_data[color]:
                    return False

        return True

    def get_beat_count(self, sequence_data: List[Dict]) -> int:
        """
        Get the number of actual beats in the sequence.

        Args:
            sequence_data: List of sequence dictionaries

        Returns:
            Number of beats (excluding metadata)
        """
        return len([entry for entry in sequence_data if entry.get("beat")])

    def get_sequence_word(self, sequence_data: List[Dict]) -> str:
        """
        Extract the word from sequence data.

        Args:
            sequence_data: List of sequence dictionaries

        Returns:
            Sequence word or default
        """
        for entry in sequence_data:
            if entry.get("word"):
                return entry["word"]
        return "Sequence"

    def get_sequence_metadata(self, sequence_data: List[Dict]) -> Dict:
        """
        Extract metadata from sequence data.

        Args:
            sequence_data: List of sequence dictionaries

        Returns:
            Dictionary containing sequence metadata
        """
        metadata = {
            "word": self.get_sequence_word(sequence_data),
            "beat_count": self.get_beat_count(sequence_data),
            "has_start_position": any(
                entry.get("sequence_start_position") for entry in sequence_data
            ),
        }

        # Extract difficulty if available
        for entry in sequence_data:
            if entry.get("difficulty_level"):
                metadata["difficulty_level"] = entry["difficulty_level"]
                break

        return metadata
