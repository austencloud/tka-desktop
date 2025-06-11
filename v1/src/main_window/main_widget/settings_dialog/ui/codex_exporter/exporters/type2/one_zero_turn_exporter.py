"""
Exporter for Type 2 pictographs with one zero turn.

This module handles the export of Type 2 pictographs when one turn value is 0.
"""

import os
from typing import TYPE_CHECKING, List, Dict, Any

from ...turn_applier import TurnApplier
from .base_exporter import Type2BaseExporter

if TYPE_CHECKING:
    pass


class OneZeroTurnExporter(Type2BaseExporter):
    """Exports Type 2 pictographs when one turn value is 0."""

    def _export_single_variation(
        self,
        letter: str,
        pictograph_data: Dict[str, Any],
        grid_mode: str,
        turns1: float,
        turns2: float,
        output_dir: str,
        direction_label: str = "",
        blue_prop_rot_dir: str = None,
    ) -> int:
        """Exports a single variation of a Type 2 pictograph."""
        pictograph = self.factory.create_pictograph_from_data(
            pictograph_data, grid_mode
        )

        if blue_prop_rot_dir:
            pictograph.state.update_pictograph_state(
                {"blue_attributes": {"prop_rot_dir": blue_prop_rot_dir}}
            )

        TurnApplier.apply_turns_to_pictograph(
            pictograph, red_turns=turns1, blue_turns=turns2
        )

        filename = self.turn_configuration.get_hybrid_filename(
            letter, turns1, turns2, direction_label
        )
        filepath = os.path.join(output_dir, filename)

        message_direction_label = f" ({direction_label})" if direction_label else ""
        message = (
            f"Saved Type 2 pictograph {letter}{message_direction_label} "
            f"with turns (red:{turns1}, blue:{turns2}) "
            f"to {filepath}"
        )

        self._save_pictograph(pictograph, filepath, message)
        return 4  # Representing 4 variations for each core configuration

    def export_pictograph(
        self,
        letter: str,
        directory: str,
        turns1: float,
        turns2: float,
        matching_pictographs: List[Dict[str, Any]],
        grid_mode: str = "diamond",
    ) -> int:
        """Exports Type 2 pictographs when one turn value is 0.

        For Type 2 letters, the blue hand is static and the red hand is non-static.
        When one turn value is 0, we'll have 12 variations total:

        If turns2 = 0 (static hand has no turns):
        - 4 for applying turns to the non-static motion (red)
        - 4 for applying turns to the static motion (blue) in clockwise direction
        - 4 for applying turns to the static motion (blue) in counter-clockwise direction

        If turns1 = 0 (non-static hand has no turns):
        - 4 for applying turns to the static motion (blue)
        - 4 for applying turns to the static motion (blue) in clockwise direction
        - 4 for applying turns to the static motion (blue) in counter-clockwise direction

        Args:
            letter: The letter to export
            directory: The directory to save to
            red_turns: The number of turns for the red hand
            blue_turns: The number of turns for the blue hand
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

        # Case 1: Base export (non-static red hand gets turns)
        # Saved directly in the main Type2/{letter} directory.
        exported_count += self._export_single_variation(
            letter=letter,
            pictograph_data=pictograph_data,
            grid_mode=grid_mode,
            turns1=turns2,
            turns2=turns1,
            output_dir=directory,
            direction_label="",
            blue_prop_rot_dir=None,
        )

        # Case 2: Static motion (blue) rotates clockwise
        # Saved in the "same" subdirectory.
        exported_count += self._export_single_variation(
            letter=letter,
            pictograph_data=pictograph_data,
            grid_mode=grid_mode,
            turns1=turns1,
            turns2=turns2,
            output_dir=same_dir,
            direction_label="same",
            blue_prop_rot_dir="cw",
        )

        # Case 3: Static motion (blue) rotates counter-clockwise
        # Saved in the "opp" subdirectory.
        exported_count += self._export_single_variation(
            letter=letter,
            pictograph_data=pictograph_data,
            grid_mode=grid_mode,
            turns1=turns1,
            turns2=turns2,
            output_dir=opp_dir,
            direction_label="opp",
            blue_prop_rot_dir="ccw",
        )

        return exported_count
