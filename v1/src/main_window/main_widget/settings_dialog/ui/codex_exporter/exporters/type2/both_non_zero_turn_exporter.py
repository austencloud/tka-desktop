"""
Exporter for Type 2 pictographs with both non-zero turns.

This module handles the export of Type 2 pictographs when both turn values are non-zero.
"""

import os
from typing import TYPE_CHECKING, List, Dict, Any

from ...turn_applier import TurnApplier
from .base_exporter import Type2BaseExporter

if TYPE_CHECKING:
    pass


class BothNonZeroTurnExporter(Type2BaseExporter):
    """Exports Type 2 pictographs when both turn values are non-zero."""

    def _export_single_variation_set(
        self,
        letter: str,
        pictograph_data: Dict[str, Any],
        grid_mode: str,
        blue_prop_rot_dir: str,
        current_turns1: float,
        current_turns2: float,
        direction_label: str,
        output_subdir: str,
    ) -> int:
        """Exports a single set of variations for a Type 2 pictograph."""
        pictograph = self.factory.create_pictograph_from_data(
            pictograph_data, grid_mode
        )

        pictograph.state.update_pictograph_state(
            {"blue_attributes": {"prop_rot_dir": blue_prop_rot_dir}}
        )

        TurnApplier.apply_turns_to_pictograph(
            pictograph, red_turns=current_turns1, blue_turns=current_turns2
        )

        filename = self.turn_configuration.get_hybrid_filename(
            letter, current_turns1, current_turns2, direction_label
        )
        filepath = os.path.join(output_subdir, filename)
        message = f"Saved Type 2 pictograph {letter} ({direction_label}) with turns (red:{current_turns1}, blue:{current_turns2}) to {filepath}"
        self._save_pictograph(pictograph, filepath, message)
        return 4  # Representing 4 variations

    def export_pictograph(
        self,
        letter: str,
        directory: str,
        turns1: float,
        turns2: float,
        matching_pictographs: List[Dict[str, Any]],
        grid_mode: str = "diamond",
    ) -> int:
        """Exports Type 2 pictographs when both turn values are non-zero.

        For Type 2 letters, the blue hand is static and the red hand is non-static.
        When both turn values are non-zero (e.g., 3,2), we'll have 16 variations total:
        - 4 variations with static motion (blue) rotating clockwise, applying first turn value to non-static (red) and second to static (blue)
        - 4 variations with static motion (blue) rotating counter-clockwise, applying first turn value to non-static (red) and second to static (blue)
        - 4 variations with static motion (blue) rotating clockwise, applying second turn value to non-static (red) and first to static (blue)
        - 4 variations with static motion (blue) rotating counter-clockwise, applying second turn value to non-static (red) and first to static (blue)

        Args:
            letter: The letter to export
            directory: The directory to save to
            turns1: The first turns value
            turns2: The second turns value
            matching_pictographs: The matching pictographs
            grid_mode: The grid mode to use ('diamond' or 'box')

        Returns:
            The number of exported pictographs
        """
        exported_count = 0

        if not matching_pictographs:
            return 0

        same_dir = os.path.join(directory, "same")
        opp_dir = os.path.join(directory, "opp")
        os.makedirs(same_dir, exist_ok=True)
        os.makedirs(opp_dir, exist_ok=True)

        pictograph_data = matching_pictographs[0].copy()

        # Case 1: Static motion (blue) rotating clockwise, turns1 to red, turns2 to blue
        exported_count += self._export_single_variation_set(
            letter,
            pictograph_data,
            grid_mode,
            "cw",
            turns1,
            turns2,
            "same",
            same_dir,
        )

        # Case 2: Static motion (blue) rotating counter-clockwise, turns1 to red, turns2 to blue
        exported_count += self._export_single_variation_set(
            letter,
            pictograph_data,
            grid_mode,
            "ccw",
            turns1,
            turns2,
            "opp",
            opp_dir,
        )

        # Case 3: Static motion (blue) rotating clockwise, turns2 to red, turns1 to blue
        exported_count += self._export_single_variation_set(
            letter,
            pictograph_data,
            grid_mode,
            "cw",
            turns2,  # Swapped
            turns1,  # Swapped
            "same",
            same_dir,
        )

        # Case 4: Static motion (blue) rotating counter-clockwise, turns2 to red, turns1 to blue
        exported_count += self._export_single_variation_set(
            letter,
            pictograph_data,
            grid_mode,
            "ccw",
            turns2,  # Swapped
            turns1,  # Swapped
            "opp",
            opp_dir,
        )

        return exported_count
