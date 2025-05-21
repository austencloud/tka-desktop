"""
Manages pictograph data for the codex exporter.
"""

from typing import TYPE_CHECKING, Dict, Any, Optional, List, Tuple, Union
from enums.letter.letter import Letter

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
        ImageExportTab,
    )
    from main_window.main_widget.settings_dialog.ui.codex_exporter.codex_exporter_tab import (
        CodexExporterTab,
    )


class PictographDataManager:
    """Manages pictograph data for the codex exporter."""

    def __init__(self, parent: Union["ImageExportTab", "CodexExporterTab"]):
        """Initialize the data manager.

        Args:
            parent: The parent tab (either ImageExportTab or CodexExporterTab)
        """
        self.parent = parent
        self.main_widget = parent.main_widget

    def get_pictograph_data_for_letter(
        self, letter: str, start_pos: str, end_pos: str
    ) -> Optional[Dict[str, Any]]:
        """Get pictograph data for a letter with specific start and end positions.

        Args:
            letter: The letter to get data for
            start_pos: The start position
            end_pos: The end position

        Returns:
            The pictograph data, or None if not found
        """
        # Try to convert string letter to enum
        try:
            letter_enum = Letter(letter)
        except ValueError:
            # If letter is not in enum, return None
            return None

        # Check if we have access to the dataset
        if (
            not hasattr(self.main_widget, "pictograph_dataset")
            or not self.main_widget.pictograph_dataset
        ):
            return None

        # Get all pictographs for this letter
        letter_pictographs = self.main_widget.pictograph_dataset.get(letter_enum, [])

        # Find one that matches the start and end positions
        for pic_data in letter_pictographs:
            if (
                pic_data.get("start_pos") == start_pos
                and pic_data.get("end_pos") == end_pos
            ):
                return pic_data

        return None

    def fetch_matching_pictographs(
        self, letter: str, start_pos: str, end_pos: str
    ) -> list[dict[str, Any]]:
        """Get pro and anti versions of a hybrid pictograph.

        Args:
            letter: The letter to get data for
            start_pos: The start position
            end_pos: The end position

        Returns:
            A list of matching pictographs
        """
        # Try to convert string letter to enum
        try:
            letter_enum = Letter(letter)
        except ValueError:
            # If letter is not in enum, return empty list
            return []

        # Check if we have access to the dataset
        if (
            not hasattr(self.main_widget, "pictograph_dataset")
            or not self.main_widget.pictograph_dataset
        ):
            return []

        # Get all pictographs for this letter
        letter_pictographs = self.main_widget.pictograph_dataset.get(letter_enum, [])

        # Find ones that match the start and end positions
        matching_pictographs = []
        print(f"Looking for pictographs with start_pos={start_pos}, end_pos={end_pos}")
        print(f"Found {len(letter_pictographs)} pictographs for letter {letter}")

        for pic_data in letter_pictographs:
            pic_start_pos = pic_data.get("start_pos")
            pic_end_pos = pic_data.get("end_pos")

            print(
                f"Checking pictograph with start_pos={pic_start_pos}, end_pos={pic_end_pos}"
            )

            if pic_start_pos == start_pos and pic_end_pos == end_pos:
                red_motion_type = pic_data.get("red_attributes", {}).get(
                    "motion_type", ""
                )
                blue_motion_type = pic_data.get("blue_attributes", {}).get(
                    "motion_type", ""
                )
                print(
                    f"Found matching pictograph with red={red_motion_type}, blue={blue_motion_type}"
                )
                matching_pictographs.append(pic_data)

        print(f"Found {len(matching_pictographs)} matching pictographs")

        # Print details of each matching pictograph
        for i, pic in enumerate(matching_pictographs):
            red_motion = pic.get("red_attributes", {}).get("motion_type", "")
            blue_motion = pic.get("blue_attributes", {}).get("motion_type", "")
            print(f"Matching pictograph {i}: red={red_motion}, blue={blue_motion}")

        return matching_pictographs

    def create_minimal_data_for_letter(self, letter: str) -> Dict[str, Any]:
        """Create minimal data for a letter.

        Args:
            letter: The letter to create data for

        Returns:
            The minimal data
        """
        # Determine the correct start and end positions based on the letter
        # Define position groups for all letter types
        _POSITION_GROUPS: Dict[Tuple[str, str], List[str]] = {
            # Type 1 letters
            ("alpha1", "alpha3"): ["A", "B", "C"],
            ("beta1", "alpha3"): ["D", "E", "F"],
            ("beta3", "beta5"): ["G", "H", "I"],
            ("alpha3", "beta5"): ["J", "K", "L"],
            ("gamma11", "gamma1"): ["M", "N", "O"],
            ("gamma1", "gamma15"): ["P", "Q", "R"],
            ("gamma13", "gamma11"): ["S", "T", "U", "V"],
            # Type 2 letters
            ("gamma13", "alpha3"): ["W", "X"],
            ("gamma11", "beta5"): ["Y", "Z"],
            ("alpha3", "gamma13"): ["Σ", "Δ"],
            ("beta7", "gamma13"): ["θ", "Ω"],
            # Type 3 letters
            ("gamma11", "alpha3"): ["W-", "X-"],
            ("gamma3", "beta5"): ["Y-", "Z-"],
            ("beta3", "gamma13"): ["Σ-", "Δ-"],
            ("alpha8", "gamma13"): ["θ-", "Ω-"],
        }

        start_pos = "alpha1"  # Default start position
        end_pos = "alpha3"  # Default end position

        for (sp, ep), letters in _POSITION_GROUPS.items():
            if letter in letters:
                start_pos = sp
                end_pos = ep
                break

        # Create minimal data
        return {
            "letter": letter,
            "start_pos": start_pos,
            "end_pos": end_pos,
            "red_attributes": {
                "motion_type": "pro",  # Default to PRO motion
                "turns": 0,  # Default to 0 turns
                "prop_rot_dir": "clockwise",  # Default to clockwise
                "start_ori": "in",  # Default to IN orientation
                "start_loc": "n",  # Default to NORTH location
                "end_loc": "n",  # Default to NORTH location for end_loc as well
            },
            "blue_attributes": {
                "motion_type": "pro",  # Default to PRO motion
                "turns": 0,  # Default to 0 turns
                "prop_rot_dir": "clockwise",  # Default to clockwise
                "start_ori": "in",  # Default to IN orientation
                "start_loc": "n",  # Default to NORTH location
                "end_loc": "n",  # Default to NORTH location for end_loc as well
            },
        }
