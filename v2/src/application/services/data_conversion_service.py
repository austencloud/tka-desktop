"""
Data Conversion Service - Focused Data Conversion Operations

Handles all data conversion operations including:
- V1 to V2 data format conversion
- CSV data loading and processing
- Row-to-pictograph conversion
- Beat data creation from CSV

This service provides a clean, focused interface for data conversion operations
while maintaining the proven conversion algorithms.
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from pathlib import Path
import uuid

import pandas as pd

from domain.models.core_models import BeatData, MotionData, MotionType, Location, RotationDirection
from domain.models.pictograph_models import PictographData, GridData, GridMode, ArrowData


class IDataConversionService(ABC):
    """Interface for data conversion operations."""

    @abstractmethod
    def convert_v1_to_v2(self, v1_data: Dict[str, Any]) -> PictographData:
        """Convert V1 pictograph data to V2 format."""
        pass

    @abstractmethod
    def load_csv_data(self, file_path: Path, category: str = "csv_data") -> List[PictographData]:
        """Load pictograph data from a CSV file."""
        pass

    @abstractmethod
    def get_specific_pictograph(self, letter: str, index: int = 0) -> Optional[BeatData]:
        """Get a specific pictograph by letter and index from CSV data."""
        pass

    @abstractmethod
    def get_pictographs_by_letter(self, letter: str) -> List[BeatData]:
        """Get all pictographs for a specific letter."""
        pass


class DataConversionService(IDataConversionService):
    """
    Focused data conversion service.

    Provides comprehensive data conversion including:
    - V1 to V2 data format conversion
    - CSV data loading and processing
    - Row-to-pictograph conversion
    - Beat data creation from CSV
    """

    def __init__(self):
        # CSV data loading
        self._csv_data = None
        self._data_path = (
            Path(__file__).parent.parent.parent.parent.parent
            / "data"
            / "DiamondPictographDataframe.csv"
        )

        # V1 conversion mappings
        self._v1_conversion_rules = self._load_v1_conversion_rules()

    def convert_v1_to_v2(self, v1_data: Dict[str, Any]) -> PictographData:
        """Convert V1 pictograph data to V2 format."""
        # Create base pictograph
        grid_data = GridData(
            grid_mode=GridMode.DIAMOND,
            center_x=200.0,
            center_y=200.0,
            radius=100.0,
        )

        pictograph = PictographData(
            grid_data=grid_data,
            arrows={},
            props={},
            is_blank=True,
            metadata={"created_by": "data_conversion_service"},
        )

        # Convert V1 arrows to V2 format
        arrows = {}

        if "blue_arrow" in v1_data:
            blue_motion = self._convert_v1_motion(v1_data["blue_arrow"])
            if blue_motion:
                arrows["blue"] = ArrowData(
                    color="blue",
                    motion_data=blue_motion,
                    is_visible=True,
                )

        if "red_arrow" in v1_data:
            red_motion = self._convert_v1_motion(v1_data["red_arrow"])
            if red_motion:
                arrows["red"] = ArrowData(
                    color="red",
                    motion_data=red_motion,
                    is_visible=True,
                )

        # Convert metadata
        metadata = {
            "converted_from_v1": True,
            "original_v1_id": v1_data.get("id"),
            "conversion_timestamp": str(uuid.uuid4()),
        }

        return pictograph.update(
            arrows=arrows,
            is_blank=len(arrows) == 0,
            metadata=metadata,
        )

    def load_csv_data(self, file_path: Path, category: str = "csv_data") -> List[PictographData]:
        """Load pictograph data from a CSV file."""
        pictographs = []

        # Read CSV file
        try:
            df = pd.read_csv(file_path)

            for _, row in df.iterrows():
                # Convert each row to pictograph
                pictograph = self._convert_row_to_pictograph(row)
                if pictograph:
                    pictographs.append(pictograph)

        except Exception as e:
            print(f"Error reading CSV file {file_path}: {e}")

        return pictographs

    def get_specific_pictograph(self, letter: str, index: int = 0) -> Optional[BeatData]:
        """Get a specific pictograph by letter and index from CSV data."""
        df = self._load_csv_data()

        # Filter by letter
        letter_data = df[df["letter"] == letter]

        if letter_data.empty or index >= len(letter_data):
            return None

        row = letter_data.iloc[index]
        return self._create_beat_data_from_csv_row(row)

    def get_pictographs_by_letter(self, letter: str) -> List[BeatData]:
        """Get all pictographs for a specific letter."""
        df = self._load_csv_data()
        letter_data = df[df["letter"] == letter]

        return [
            self._create_beat_data_from_csv_row(row) for _, row in letter_data.iterrows()
        ]

    def convert_csv_to_beat_data(self, csv_file_path: Path) -> List[BeatData]:
        """Convert entire CSV file to list of BeatData objects."""
        beat_data_list = []

        try:
            df = pd.read_csv(csv_file_path)

            for _, row in df.iterrows():
                beat_data = self._create_beat_data_from_csv_row(row)
                if beat_data:
                    beat_data_list.append(beat_data)

        except Exception as e:
            print(f"Error converting CSV to beat data {csv_file_path}: {e}")

        return beat_data_list

    # Private helper methods

    def _load_csv_data(self) -> pd.DataFrame:
        """Load CSV data if not already loaded."""
        if self._csv_data is None:
            self._csv_data = pd.read_csv(self._data_path)
        return self._csv_data

    def _create_beat_data_from_csv_row(self, row) -> BeatData:
        """Convert a CSV row to BeatData object."""
        # Map CSV values to enums
        motion_type_map = {
            "pro": MotionType.PRO,
            "anti": MotionType.ANTI,
            "static": MotionType.STATIC,
            "dash": MotionType.DASH,
            "float": MotionType.FLOAT,
        }
        rotation_map = {
            "cw": RotationDirection.CLOCKWISE,
            "ccw": RotationDirection.COUNTER_CLOCKWISE,
            "no_rot": RotationDirection.NO_ROTATION,
        }
        location_map = {
            "n": Location.NORTH,
            "e": Location.EAST,
            "s": Location.SOUTH,
            "w": Location.WEST,
            "ne": Location.NORTHEAST,
            "se": Location.SOUTHEAST,
            "sw": Location.SOUTHWEST,
            "nw": Location.NORTHWEST,
        }

        # Create motion data if motion type exists
        blue_motion = None
        if row["blue_motion_type"] in motion_type_map:
            blue_motion = MotionData(
                motion_type=motion_type_map[row["blue_motion_type"]],
                prop_rot_dir=rotation_map.get(
                    row["blue_prop_rot_dir"], RotationDirection.CLOCKWISE
                ),
                start_loc=location_map[row["blue_start_loc"]],
                end_loc=location_map[row["blue_end_loc"]],
            )

        red_motion = None
        if row["red_motion_type"] in motion_type_map:
            red_motion = MotionData(
                motion_type=motion_type_map[row["red_motion_type"]],
                prop_rot_dir=rotation_map.get(
                    row["red_prop_rot_dir"], RotationDirection.CLOCKWISE
                ),
                start_loc=location_map[row["red_start_loc"]],
                end_loc=location_map[row["red_end_loc"]],
            )

        return BeatData(
            beat_number=1,
            letter=row["letter"],
            blue_motion=blue_motion,
            red_motion=red_motion,
        )

    def _convert_v1_motion(self, v1_motion_data: Dict[str, Any]) -> Optional[MotionData]:
        """Convert V1 motion data to V2 MotionData."""
        try:
            # Map V1 motion types to V2
            v1_type = v1_motion_data.get("motion_type", "").lower()
            motion_type_map = {
                "shift": MotionType.PRO,
                "anti": MotionType.ANTI,
                "static": MotionType.STATIC,
                "dash": MotionType.DASH,
                "float": MotionType.FLOAT,
            }

            motion_type = motion_type_map.get(v1_type, MotionType.PRO)

            # Map rotation directions
            v1_rotation = v1_motion_data.get("rotation", "").lower()
            rotation_map = {
                "cw": RotationDirection.CLOCKWISE,
                "ccw": RotationDirection.COUNTER_CLOCKWISE,
                "no_rot": RotationDirection.NO_ROTATION,
            }

            rotation = rotation_map.get(v1_rotation, RotationDirection.CLOCKWISE)

            # Map locations (simplified)
            start_loc = Location.NORTH  # Default
            end_loc = Location.SOUTH  # Default

            return MotionData(
                motion_type=motion_type,
                prop_rot_dir=rotation,
                start_loc=start_loc,
                end_loc=end_loc,
                turns=v1_motion_data.get("turns", 1.0),
            )

        except Exception:
            return None

    def _convert_row_to_pictograph(self, row: pd.Series) -> Optional[PictographData]:
        """Convert a CSV row to PictographData."""
        try:
            # Create base pictograph
            grid_data = GridData(
                grid_mode=GridMode.DIAMOND,
                center_x=200.0,
                center_y=200.0,
                radius=100.0,
            )

            # Extract arrow data
            arrows = {}

            if "blue_arrow" in row and pd.notna(row["blue_arrow"]):
                blue_motion = self._convert_v1_motion(eval(row["blue_arrow"]))
                if blue_motion:
                    arrows["blue"] = ArrowData(
                        color="blue",
                        motion_data=blue_motion,
                        is_visible=True,
                    )

            if "red_arrow" in row and pd.notna(row["red_arrow"]):
                red_motion = self._convert_v1_motion(eval(row["red_arrow"]))
                if red_motion:
                    arrows["red"] = ArrowData(
                        color="red",
                        motion_data=red_motion,
                        is_visible=True,
                    )

            return PictographData(
                grid_data=grid_data,
                arrows=arrows,
                props={},
                is_blank=len(arrows) == 0,
                metadata={"converted_from_csv": True, "letter": row.get("letter", "")},
            )

        except Exception as e:
            print(f"Error converting row to pictograph: {e}")
            return None

    def _load_v1_conversion_rules(self) -> Dict[str, Any]:
        """Load V1 to V2 conversion rules."""
        return {
            "motion_type_mappings": {
                "shift": "pro",
                "anti": "anti",
                "static": "static",
                "dash": "dash",
                "float": "float",
            },
            "location_mappings": {
                "n": "north",
                "ne": "northeast",
                "e": "east",
                "se": "southeast",
                "s": "south",
                "sw": "southwest",
                "w": "west",
                "nw": "northwest",
            },
        }
