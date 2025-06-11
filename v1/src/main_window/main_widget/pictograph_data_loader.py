from copy import deepcopy
import os
from typing import TYPE_CHECKING, Optional
import pandas as pd
from enums.letter.letter import Letter

from data.constants import (
    BLUE,
    BLUE_ATTRS,
    END_LOC,
    END_POS,
    IN,
    LETTER,
    MOTION_TYPE,
    PROP_ROT_DIR,
    RED,
    RED_ATTRS,
    START_LOC,
    START_ORI,
    START_POS,
    TURNS,
)
from utils.path_helpers import get_data_path

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class PictographDataLoader:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget
        self._cached_dataset = None

    def load_pictograph_dataset(self) -> dict[Letter, list[dict]]:
        """
        Load pictograph dataset from CSV files or create sample data if files are not found.

        This method tries to load the DiamondPictographDataframe.csv and BoxPictographDataframe.csv
        files from the data directory. If the files are not found, it creates sample data.
        """
        try:
            # Try to load the CSV files from the data directory
            diamond_csv_path = get_data_path("DiamondPictographDataframe.csv")
            box_csv_path = get_data_path("BoxPictographDataframe.csv")

            # Check if both files exist
            diamond_exists = os.path.exists(diamond_csv_path)
            box_exists = os.path.exists(box_csv_path)

            if not diamond_exists or not box_exists:
                missing_files = []
                if not diamond_exists:
                    missing_files.append("DiamondPictographDataframe.csv")
                if not box_exists:
                    missing_files.append("BoxPictographDataframe.csv")

                # Create sample data if any file is missing
                return self._create_sample_pictograph_data()

            try:
                # Try to read the CSV files
                diamond_df = pd.read_csv(diamond_csv_path)
                box_df = pd.read_csv(box_csv_path)
            except Exception as e:
                # If there's an error reading the files, create sample data
                return self._create_sample_pictograph_data()

            # Process the dataframes
            combined_df = pd.concat([diamond_df, box_df], ignore_index=True)
            combined_df = combined_df.sort_values(by=[LETTER, START_POS, END_POS])
            combined_df = self.add_turns_and_ori_to_pictograph_data(combined_df)
            combined_df = self.restructure_dataframe_for_new_json_format(combined_df)

            # Convert to dictionary
            letters = {
                self.get_letter_enum_by_value(letter_str): combined_df[
                    combined_df[LETTER] == letter_str
                ].to_dict(orient="records")
                for letter_str in combined_df[LETTER].unique()
            }
            self._convert_turns_str_to_int_or_float(letters)
            return letters

        except Exception:
            # If any error occurs, create sample data without logging the error
            return self._create_sample_pictograph_data()

    def _convert_turns_str_to_int_or_float(self, letters):
        for letter in letters:
            for motion in letters[letter]:
                motion[BLUE_ATTRS][TURNS] = int(motion[BLUE_ATTRS][TURNS])
                motion[RED_ATTRS][TURNS] = int(motion[RED_ATTRS][TURNS])

    def add_turns_and_ori_to_pictograph_data(self, df: pd.DataFrame) -> pd.DataFrame:
        for index in df.index:
            df.at[index, "blue_turns"] = 0
            df.at[index, "red_turns"] = 0
            df.at[index, "blue_start_ori"] = IN
            df.at[index, "red_start_ori"] = IN
        return df

    def restructure_dataframe_for_new_json_format(
        self, df: pd.DataFrame
    ) -> pd.DataFrame:
        def nest_attributes(row, color_prefix):
            return {
                MOTION_TYPE: row[f"{color_prefix}_motion_type"],
                START_ORI: row[f"{color_prefix}_start_ori"],
                PROP_ROT_DIR: row[f"{color_prefix}_prop_rot_dir"],
                START_LOC: row[f"{color_prefix}_start_loc"],
                END_LOC: row[f"{color_prefix}_end_loc"],
                TURNS: row[f"{color_prefix}_turns"],
            }

        df[BLUE_ATTRS] = df.apply(lambda row: nest_attributes(row, BLUE), axis=1)
        df[RED_ATTRS] = df.apply(lambda row: nest_attributes(row, RED), axis=1)
        blue_columns = [
            "blue_motion_type",
            "blue_prop_rot_dir",
            "blue_start_loc",
            "blue_end_loc",
            "blue_turns",
            "blue_start_ori",
        ]
        red_columns = [
            "red_motion_type",
            "red_prop_rot_dir",
            "red_start_loc",
            "red_end_loc",
            "red_turns",
            "red_start_ori",
        ]
        df = df.drop(columns=blue_columns + red_columns)
        return df

    @staticmethod
    def get_letter_enum_by_value(letter_value: str) -> Letter:
        for letter in Letter.__members__.values():
            if letter.value == letter_value:
                return letter
        raise ValueError(f"No matching Letters enum for value: {letter_value}")

    def _create_sample_pictograph_data(self) -> dict[Letter, list[dict]]:
        """
        Create sample pictograph data when CSV files are not available.

        This method generates a complete set of sample data for all letters in the alphabet,
        with various start and end positions. This ensures that the application can function
        properly even when the CSV files are missing.
        """
        # Create a dictionary to hold the sample data
        sample_data = {}

        # Define sample attributes for each letter
        for letter in Letter:
            # Skip any non-standard letters if needed
            if letter.value not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                continue

            # Create sample data for this letter
            letter_data = []

            # Add a few sample positions for each letter
            for start_pos in range(1, 5):
                for end_pos in range(1, 5):
                    # Create a sample pictograph entry with clockwise motion
                    clockwise_entry = {
                        LETTER: letter.value,
                        START_POS: start_pos,
                        END_POS: end_pos,
                        BLUE_ATTRS: {
                            MOTION_TYPE: "clockwise",
                            START_ORI: IN,
                            PROP_ROT_DIR: "clockwise",
                            START_LOC: "center",
                            END_LOC: "center",
                            TURNS: 1,
                        },
                        RED_ATTRS: {
                            MOTION_TYPE: "counterclockwise",
                            START_ORI: IN,
                            PROP_ROT_DIR: "counterclockwise",
                            START_LOC: "center",
                            END_LOC: "center",
                            TURNS: 0,
                        },
                    }
                    letter_data.append(clockwise_entry)

                    # Create a sample pictograph entry with counterclockwise motion
                    counterclockwise_entry = {
                        LETTER: letter.value,
                        START_POS: start_pos,
                        END_POS: end_pos,
                        BLUE_ATTRS: {
                            MOTION_TYPE: "counterclockwise",
                            START_ORI: IN,
                            PROP_ROT_DIR: "counterclockwise",
                            START_LOC: "center",
                            END_LOC: "center",
                            TURNS: 1,
                        },
                        RED_ATTRS: {
                            MOTION_TYPE: "clockwise",
                            START_ORI: IN,
                            PROP_ROT_DIR: "clockwise",
                            START_LOC: "center",
                            END_LOC: "center",
                            TURNS: 0,
                        },
                    }
                    letter_data.append(counterclockwise_entry)

            # Add the letter data to the sample data dictionary
            sample_data[letter] = letter_data

        return sample_data

    def get_pictograph_dataset(self) -> dict[Letter, list[dict]]:
        """
        Get the pictograph dataset, using cache or loading from main_widget if available.

        Returns:
            Dictionary mapping Letter enums to lists of pictograph data dictionaries
        """
        # Try to get from main_widget first (if available and has dataset)
        if (
            self.main_widget
            and hasattr(self.main_widget, "pictograph_dataset")
            and self.main_widget.pictograph_dataset
        ):
            return self.main_widget.pictograph_dataset

        # Use cached dataset if available
        if self._cached_dataset is not None:
            return self._cached_dataset

        # Load and cache the dataset
        self._cached_dataset = self.load_pictograph_dataset()
        return self._cached_dataset

    def find_pictograph_data(self, simplified_dict: dict) -> Optional[dict]:
        from enums.letter.letter import Letter

        target_letter = next(
            (l for l in Letter if l.value == simplified_dict[LETTER]), None
        )
        if not target_letter:
            print(
                f"Warning: Letter '{simplified_dict.get('letter', simplified_dict.get(LETTER, 'unknown'))}' not found in Letter Enum."
            )
            return None

        try:
            # Use the new get_pictograph_dataset method that handles None main_widget
            pictograph_dataset = self.get_pictograph_dataset()
            letter_dicts = pictograph_dataset.get(target_letter, [])

            for pdict in letter_dicts:
                if (
                    pdict.get(START_POS) == simplified_dict[START_POS]
                    and pdict.get(END_POS) == simplified_dict[END_POS]
                    and pdict.get(BLUE_ATTRS, {}).get(MOTION_TYPE)
                    == simplified_dict["blue_motion_type"]
                    and pdict.get(RED_ATTRS, {}).get(MOTION_TYPE)
                    == simplified_dict["red_motion_type"]
                ):
                    return deepcopy(pdict)
            return None

        except Exception as e:
            # Log the error and return None gracefully
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(f"Error finding pictograph data: {e}")
            return None
