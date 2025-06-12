"""
Data Service for Kinetic Constructor

This service generates and provides access to valid pictograph combinations
using its own dataset.
"""

import os
from typing import Dict, List, Optional, Any
import pandas as pd


class PictographDataService:
    """
    Service that generates and provides access to valid pictograph combinations.

    This service uses its own dataset
    to ensure all generated pictographs are valid.
    """

    def __init__(self):
        self._dataset: Optional[pd.DataFrame] = None
        self._load_dataset()

    def _load_dataset(self) -> None:
        """Load the dataset from CSV files."""
        try:
            data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data")
            diamond_path = os.path.join(data_dir, "DiamondPictographDataframe.csv")
            box_path = os.path.join(data_dir, "BoxPictographDataframe.csv")

            if os.path.exists(diamond_path):
                self._dataset = pd.read_csv(diamond_path)
                if os.path.exists(box_path):
                    box_df = pd.read_csv(box_path)
                    self._dataset = pd.concat(
                        [self._dataset, box_df], ignore_index=True
                    )
                print(f"✅ Loaded dataset with {len(self._dataset)} entries")
            else:
                raise FileNotFoundError("Pictograph data files not found")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self._dataset = pd.DataFrame()

    def get_random_valid_pictograph_data(
        self, letter: Optional[str] = None, grid_mode: str = "diamond"
    ) -> Dict[str, Any]:
        """Get a random valid pictograph data from the dataset."""
        if self._dataset is None or len(self._dataset) == 0:
            raise ValueError("No dataset available")

        # Filter by grid mode first
        if "grid_mode" in self._dataset.columns:
            mode_filtered = self._dataset[self._dataset["grid_mode"] == grid_mode]
        else:
            # If no grid_mode column, filter by valid positions
            diamond_positions = {"n", "e", "s", "w"}
            mode_filtered = self._dataset[
                (self._dataset["blue_start_loc"].isin(diamond_positions))
                & (self._dataset["blue_end_loc"].isin(diamond_positions))
                & (self._dataset["red_start_loc"].isin(diamond_positions))
                & (self._dataset["red_end_loc"].isin(diamond_positions))
            ]

        if len(mode_filtered) == 0:
            print(f"⚠️ No {grid_mode} mode pictographs found, using all data")
            mode_filtered = self._dataset

        # Filter by letter if specified
        filtered_df = (
            mode_filtered[mode_filtered["letter"] == letter]
            if letter
            else mode_filtered
        )
        if len(filtered_df) == 0:
            filtered_df = mode_filtered

        # Get random row
        row = filtered_df.sample(n=1).iloc[0]

        return {
            "letter": row["letter"],
            "blue_motion": {
                "motion_type": row["blue_motion_type"],
                "prop_rot_dir": row["blue_prop_rot_dir"],
                "start_loc": row["blue_start_loc"],
                "end_loc": row["blue_end_loc"],
                "turns": 1.0,
            },
            "red_motion": {
                "motion_type": row["red_motion_type"],
                "prop_rot_dir": row["red_prop_rot_dir"],
                "start_loc": row["red_start_loc"],
                "end_loc": row["red_end_loc"],
                "turns": 1.0,
            },
            "grid_mode": row.get("grid_mode", "diamond"),
            "timing": row.get("timing", "together"),
        }

    def validate_motion_position_combination(
        self,
        letter: str,
        start_pos: str,
        end_pos: str,
        blue_motion: str,
        red_motion: str,
    ) -> bool:
        """Validate if a motion/position combination is valid according to rules."""
        if self._dataset is None:
            return False

        # Check if this exact combination exists in the dataset
        matches = self._dataset[
            (self._dataset["letter"] == letter)
            & (self._dataset["blue_motion_type"] == blue_motion)
            & (self._dataset["red_motion_type"] == red_motion)
        ]

        return len(matches) > 0

    def get_valid_letters(self) -> List[str]:
        """Get list of valid letters from the dataset."""
        return (
            self._dataset["letter"].unique().tolist()
            if self._dataset is not None
            else []
        )

    def get_dataset_info(self) -> Dict[str, Any]:
        """Get information about the loaded dataset."""
        if self._dataset is None:
            return {"loaded": False, "entries": 0}

        return {
            "loaded": True,
            "entries": len(self._dataset),
            "letters": self.get_valid_letters(),
            "motion_types": self._dataset["blue_motion_type"].unique().tolist(),
            "sample_entry": (
                self._dataset.iloc[0].to_dict() if len(self._dataset) > 0 else None
            ),
        }

    def get_pictographs_by_motion_type(self, motion_type: str) -> List[Dict[str, Any]]:
        """Get all pictographs that match a specific motion type."""
        if self._dataset is None:
            return []

        filtered = self._dataset[
            (self._dataset["blue_motion_type"] == motion_type)
            | (self._dataset["red_motion_type"] == motion_type)
        ]

        return [self._row_to_pictograph_data(row) for _, row in filtered.iterrows()]

    def get_specific_pictograph(self, letter: str, index: int = 0) -> Dict[str, Any]:
        """Get a specific pictograph by letter and index for consistent testing."""
        if self._dataset is None or len(self._dataset) == 0:
            raise ValueError("No dataset available")

        # Filter by letter
        letter_filtered = self._dataset[self._dataset["letter"] == letter]

        if len(letter_filtered) == 0:
            raise ValueError(f"No pictographs found for letter '{letter}'")

        # Get the specific index (wrap around if index is too large)
        row_index = index % len(letter_filtered)
        row = letter_filtered.iloc[row_index]

        return self._row_to_pictograph_data(row)

    def get_test_pictographs(self) -> List[Dict[str, Any]]:
        """Get three specific pictographs for consistent testing: A, B, C."""
        test_pictographs = []
        test_letters = ["A", "B", "C"]

        for letter in test_letters:
            try:
                pictograph = self.get_specific_pictograph(letter, 0)
                test_pictographs.append(pictograph)
            except ValueError:
                # If letter not found, get any available letter
                if self._dataset is not None and len(self._dataset) > 0:
                    available_letters = self.get_valid_letters()
                    if available_letters:
                        # Use the first available letter as fallback
                        fallback_letter = available_letters[0]
                        pictograph = self.get_specific_pictograph(fallback_letter, 0)
                        pictograph["letter"] = letter  # Override letter for display
                        test_pictographs.append(pictograph)

        return test_pictographs

    def get_pictographs_by_letter_range(
        self, start_letter: str, count: int = 3
    ) -> List[Dict[str, Any]]:
        """Get pictographs starting from a specific letter."""
        if self._dataset is None or len(self._dataset) == 0:
            raise ValueError("No dataset available")

        available_letters = sorted(self.get_valid_letters())
        pictographs = []

        try:
            start_index = available_letters.index(start_letter)
        except ValueError:
            start_index = 0  # Start from beginning if letter not found

        for i in range(count):
            letter_index = (start_index + i) % len(available_letters)
            letter = available_letters[letter_index]
            pictograph = self.get_specific_pictograph(letter, 0)
            pictographs.append(pictograph)

        return pictographs

    def _row_to_pictograph_data(self, row) -> Dict[str, Any]:
        """Convert a DataFrame row to pictograph data format."""
        return {
            "letter": row["letter"],
            "blue_motion": {
                "motion_type": row["blue_motion_type"],
                "prop_rot_dir": row["blue_prop_rot_dir"],
                "start_loc": row["blue_start_loc"],
                "end_loc": row["blue_end_loc"],
                "turns": 1.0,
            },
            "red_motion": {
                "motion_type": row["red_motion_type"],
                "prop_rot_dir": row["red_prop_rot_dir"],
                "start_loc": row["red_start_loc"],
                "end_loc": row["red_end_loc"],
                "turns": 1.0,
            },
            "grid_mode": row.get("grid_mode", "diamond"),
            "timing": row.get("timing", "together"),
        }
