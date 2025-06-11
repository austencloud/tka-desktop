"""
Motion Validation Service for Kinetic Constructor v2

This service provides validation and generation of valid motion/position combinations
based on the proven dataset from the original system. It ensures that v2 never
generates impossible combinations like "B" positions with "pro" motions.

The service uses the historical pictograph data as the source of truth for what
combinations are valid in the kinetic constructor system.
"""

import os
import random
from typing import Dict, List, Optional, Any
import pandas as pd
from abc import ABC, abstractmethod

from ...domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
)


class IMotionValidationService(ABC):
    """Interface for motion validation and data generation operations."""

    @abstractmethod
    def get_random_valid_pictograph_data(
        self, letter: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get a random valid pictograph data from the validated dataset."""
        pass

    @abstractmethod
    def validate_motion_position_combination(
        self,
        letter: str,
        start_pos: str,
        end_pos: str,
        blue_motion: str,
        red_motion: str,
    ) -> bool:
        """Validate if a motion/position combination is valid according to system rules."""
        pass

    @abstractmethod
    def get_valid_letters(self) -> List[str]:
        """Get list of valid letters from the dataset."""
        pass

    @abstractmethod
    def get_valid_motions_for_letter(self, letter: str) -> List[str]:
        """Get list of valid motion types for a specific letter."""
        pass


class MotionValidationService(IMotionValidationService):
    """
    Service that provides motion validation and valid data generation.

    This service loads the proven pictograph dataset and ensures all generated
    pictographs use valid motion/position combinations that exist in the
    historical system data.

    Key Rules Enforced:
    - B positions never have "pro" motions
    - Static positions only have "static" motions
    - All combinations must exist in the validated dataset
    """

    def __init__(self):
        self._dataset: Optional[pd.DataFrame] = None
        self._load_dataset()

    def _load_dataset(self) -> None:
        """Load the validated pictograph datasets."""
        try:
            # PRIORITY 1: Try to load from v2 data directory (copied files)
            diamond_path_v2 = os.path.join("src", "data", "DiamondPictographDataframe.csv")
            box_path_v2 = os.path.join("src", "data", "BoxPictographDataframe.csv")

            # FALLBACK: Try to load from original directory
            diamond_path_v1 = os.path.join(
                "the-kinetic-constructor-desktop-v1",
                "src",
                "data",
                "DiamondPictographDataframe.csv",
            )
            box_path_v1 = os.path.join(
                "the-kinetic-constructor-desktop-v1",
                "src",
                "data",
                "BoxPictographDataframe.csv",
            )

            # Try v2 files first
            if os.path.exists(diamond_path_v2) and os.path.exists(box_path_v2):
                diamond_df = pd.read_csv(diamond_path_v2)
                box_df = pd.read_csv(box_path_v2)
                self._dataset = pd.concat([diamond_df, box_df], ignore_index=True)
                print(
                    f"✅ Loaded motion validation dataset from v2 data directory with {len(self._dataset)} entries"
                )
            # Fall back to original files
            elif os.path.exists(diamond_path_v1) and os.path.exists(box_path_v1):
                diamond_df = pd.read_csv(diamond_path_v1)
                box_df = pd.read_csv(box_path_v1)
                self._dataset = pd.concat([diamond_df, box_df], ignore_index=True)
                print(
                    f"✅ Loaded motion validation dataset from original directory with {len(self._dataset)} entries"
                )
            else:
                print(
                    "⚠️ Pictograph data files not found in either location, creating sample valid data"
                )
                self._create_sample_dataset()

        except Exception as e:
            print(f"⚠️ Error loading pictograph data: {e}, creating sample valid data")
            self._create_sample_dataset()

    def _create_sample_dataset(self) -> None:
        """Create sample dataset with valid motion/position combinations."""
        # Create sample data based on proven system patterns
        sample_data = []

        # Valid combinations from historical system data
        valid_combinations = [
            # Letter A patterns (pro motions allowed)
            {
                "letter": "A",
                "start_pos": "alpha3",
                "end_pos": "alpha5",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            {
                "letter": "A",
                "start_pos": "alpha5",
                "end_pos": "alpha7",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            # Letter B patterns (anti motions only - B never has pro!)
            {
                "letter": "B",
                "start_pos": "beta2",
                "end_pos": "beta4",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            {
                "letter": "B",
                "start_pos": "beta4",
                "end_pos": "beta6",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            # Letter C patterns (mixed motions allowed)
            {
                "letter": "C",
                "start_pos": "gamma2",
                "end_pos": "gamma4",
                "blue_motion_type": "pro",
                "red_motion_type": "anti",
            },
            {
                "letter": "C",
                "start_pos": "gamma4",
                "end_pos": "gamma6",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            # Static patterns (start positions)
            {
                "letter": "α",
                "start_pos": "alpha1",
                "end_pos": "alpha1",
                "blue_motion_type": "static",
                "red_motion_type": "static",
            },
            {
                "letter": "β",
                "start_pos": "beta1",
                "end_pos": "beta1",
                "blue_motion_type": "static",
                "red_motion_type": "static",
            },
        ]

        for combo in valid_combinations:
            sample_data.append(
                {
                    "letter": combo["letter"],
                    "start_pos": combo["start_pos"],
                    "end_pos": combo["end_pos"],
                    "timing": "split",
                    "direction": "same",
                    "blue_motion_type": combo["blue_motion_type"],
                    "blue_prop_rot_dir": "cw",
                    "blue_start_loc": "n",
                    "blue_end_loc": "s",
                    "red_motion_type": combo["red_motion_type"],
                    "red_prop_rot_dir": "ccw",
                    "red_start_loc": "s",
                    "red_end_loc": "n",
                }
            )

        self._dataset = pd.DataFrame(sample_data)
        print(
            f"✅ Created sample motion validation dataset with {len(self._dataset)} valid entries"
        )

    def get_random_valid_pictograph_data(
        self, letter: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get a random valid pictograph data from the validated dataset."""
        if self._dataset is None or len(self._dataset) == 0:
            raise ValueError("No motion validation dataset available")

        # Filter by letter if specified
        if letter:
            filtered_df = self._dataset[self._dataset["letter"] == letter]
            if len(filtered_df) == 0:
                # Fall back to any letter
                filtered_df = self._dataset
        else:
            filtered_df = self._dataset

        # Get random row
        random_row = filtered_df.sample(n=1).iloc[0]

        # Convert to the format expected by v2
        return {
            "letter": random_row["letter"],
            "start_position": random_row["start_pos"],
            "end_position": random_row["end_pos"],
            "blue_motion": {
                "motion_type": random_row["blue_motion_type"],
                "prop_rot_dir": random_row["blue_prop_rot_dir"],
                "start_loc": random_row["blue_start_loc"],
                "end_loc": random_row["blue_end_loc"],
                "turns": 1.0,
                "start_ori": "in",
                "end_ori": "out",
            },
            "red_motion": {
                "motion_type": random_row["red_motion_type"],
                "prop_rot_dir": random_row["red_prop_rot_dir"],
                "start_loc": random_row["red_start_loc"],
                "end_loc": random_row["red_end_loc"],
                "turns": 1.0,
                "start_ori": "in",
                "end_ori": "out",
            },
        }

    def validate_motion_position_combination(
        self,
        letter: str,
        start_pos: str,
        end_pos: str,
        blue_motion: str,
        red_motion: str,
    ) -> bool:
        """Validate if a motion/position combination is valid according to system rules."""
        if self._dataset is None:
            return False

        # Check if this exact combination exists in the dataset
        matches = self._dataset[
            (self._dataset["letter"] == letter)
            & (self._dataset["start_pos"] == start_pos)
            & (self._dataset["end_pos"] == end_pos)
            & (self._dataset["blue_motion_type"] == blue_motion)
            & (self._dataset["red_motion_type"] == red_motion)
        ]

        return len(matches) > 0

    def get_valid_letters(self) -> List[str]:
        """Get list of valid letters from the dataset."""
        if self._dataset is None:
            return []

        return self._dataset["letter"].unique().tolist()

    def get_valid_motions_for_letter(self, letter: str) -> List[str]:
        """Get list of valid motion types for a specific letter."""
        if self._dataset is None:
            return []

        letter_data = self._dataset[self._dataset["letter"] == letter]
        if len(letter_data) == 0:
            return []

        # Get unique motion types for this letter
        blue_motions = letter_data["blue_motion_type"].unique().tolist()
        red_motions = letter_data["red_motion_type"].unique().tolist()

        # Combine and deduplicate
        all_motions = list(set(blue_motions + red_motions))
        return all_motions

    def get_dataset_info(self) -> Dict[str, Any]:
        """Get information about the loaded dataset."""
        if self._dataset is None:
            return {"loaded": False, "entries": 0}

        return {
            "loaded": True,
            "entries": len(self._dataset),
            "letters": self.get_valid_letters(),
            "sample_entry": (
                self._dataset.iloc[0].to_dict() if len(self._dataset) > 0 else None
            ),
        }
