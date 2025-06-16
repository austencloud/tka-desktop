"""
Hybrid pictograph exporter for the codex pictograph exporter.
"""

import os
from typing import TYPE_CHECKING


from ..turn_applier import TurnApplier

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
    from ..pictograph_data_manager import PictographDataManager
    from ..pictograph_factory import PictographFactory
    from ..pictograph_renderer import PictographRenderer
    from ..turn_configuration import TurnConfiguration


class HybridExporter:
    """Exports hybrid pictographs for the codex."""

    def __init__(
        self,
        data_manager: "PictographDataManager",
        factory: "PictographFactory",
        renderer: "PictographRenderer",
        turn_configuration: "TurnConfiguration",
    ):
        self.data_manager = data_manager
        self.factory = factory
        self.renderer = renderer
        self.turn_configuration = turn_configuration

    def _save_pictograph(
        self, pictograph: "LegacyPictograph", filepath: str, message: str
    ):
        """Saves a pictograph image to a file."""
        image = self.renderer.create_pictograph_image(pictograph)
        image.save(filepath, "PNG", 100)
        print(message)

    def _export_non_hybrid(
        self,
        letter: str,
        directory: str,
        turns: float,
        matching_pictographs: list,
        grid_mode: str = "diamond",
    ) -> int:
        """Exports a non-hybrid pictograph (red_turns == blue_turns)."""
        for pictograph_data in matching_pictographs:
            pictograph = self.factory.create_pictograph_from_data(
                pictograph_data, grid_mode
            )
            TurnApplier.apply_turns_to_pictograph(
                pictograph, red_turns=turns, blue_turns=turns
            )
            filename = self.turn_configuration.get_non_hybrid_filename(letter)
            filepath = os.path.join(directory, filename)
            message = f"Saved non-hybrid pictograph {letter} with turns ({turns}) to {filepath}"
            self._save_pictograph(pictograph, filepath, message)
        return 1

    def _export_hybrid_pair(
        self,
        letter: str,
        directory: str,
        red_turns: float,
        blue_turns: float,
        matching_pictographs: list,
        grid_mode: str = "diamond",
    ) -> int:
        """Exports a pair of hybrid pictographs (red_turns != blue_turns).

        For hybrid pictographs like C and F, we need to generate both variations:
        1. One with red=pro/blue=anti
        2. One with red=anti/blue=pro

        For each variation, we apply the same turn combination (red_turns, blue_turns).

        For S, T, U, and V, we need two variations with swapped turn values:
        1. First variation: Red has red_turns, Blue has blue_turns
        2. Second variation: Red has blue_turns, Blue has red_turns
        """
        exported_count = 0

        # Special case for S, T, U, V
        if letter in ["S", "T", "U", "V"]:
            return self._export_stuv_pair(
                letter, directory, red_turns, blue_turns, matching_pictographs
            )

        # Find a pictograph with red=pro and blue=anti
        pro_red_pictograph = None
        # Find a pictograph with red=anti and blue=pro
        pro_blue_pictograph = None

        # Categorize the matching pictographs
        print(
            f"Found {len(matching_pictographs)} matching pictographs for letter {letter}"
        )
        for i, pic_data in enumerate(matching_pictographs):
            red_motion_type = pic_data.get("red_attributes", {}).get("motion_type", "")
            blue_motion_type = pic_data.get("blue_attributes", {}).get(
                "motion_type", ""
            )

            print(f"Pictograph {i}: red={red_motion_type}, blue={blue_motion_type}")

            if red_motion_type == "pro" and blue_motion_type == "anti":
                pro_red_pictograph = pic_data.copy()
                print(
                    f"Found pro_red pictograph with red={red_motion_type}, blue={blue_motion_type}"
                )
            elif red_motion_type == "anti" and blue_motion_type == "pro":
                pro_blue_pictograph = pic_data.copy()
                print(
                    f"Found pro_blue pictograph with red={red_motion_type}, blue={blue_motion_type}"
                )

        # If we don't have both versions, use what we have for both
        if pro_red_pictograph is None and pro_blue_pictograph is None:
            # No matching pictographs found
            return 0
        elif pro_red_pictograph is None:
            pro_red_pictograph = pro_blue_pictograph.copy()
        elif pro_blue_pictograph is None:
            pro_blue_pictograph = pro_red_pictograph.copy()

        # Export the pro_red version (red=pro, blue=anti)
        pictograph = self.factory.create_pictograph_from_data(
            pro_red_pictograph, grid_mode
        )
        TurnApplier.apply_turns_to_pictograph(
            pictograph, red_turns=red_turns, blue_turns=blue_turns
        )
        filename = self.turn_configuration.get_hybrid_filename(
            letter, red_turns, blue_turns, "pro_red"
        )
        filepath = os.path.join(directory, filename)
        message = f"Saved hybrid pictograph {letter} (pro_red) with turns (red:{red_turns}, blue:{blue_turns}) to {filepath}"
        self._save_pictograph(pictograph, filepath, message)
        exported_count += 1

        # Export the pro_blue version (red=anti, blue=pro)
        pictograph = self.factory.create_pictograph_from_data(
            pro_blue_pictograph, grid_mode
        )
        TurnApplier.apply_turns_to_pictograph(
            pictograph, red_turns=red_turns, blue_turns=blue_turns
        )
        filename = self.turn_configuration.get_hybrid_filename(
            letter, red_turns, blue_turns, "pro_blue"
        )
        filepath = os.path.join(directory, filename)
        message = f"Saved hybrid pictograph {letter} (pro_blue) with turns (red:{red_turns}, blue:{blue_turns}) to {filepath}"
        self._save_pictograph(pictograph, filepath, message)
        exported_count += 1

        return exported_count

    def _export_stuv_pair(
        self,
        letter: str,
        directory: str,
        red_turns: float,
        blue_turns: float,
        matching_pictographs: list,
        grid_mode: str = "diamond",
    ) -> int:
        """Exports a pair of hybrid pictographs for S, T, U, V with swapped turn values.

        For S, T, U, and V, we need two variations with swapped turn values:
        1. First variation: Red has red_turns, Blue has blue_turns
        2. Second variation: Red has blue_turns, Blue has red_turns
        """
        exported_count = 0

        if not matching_pictographs:
            return 0

        # For S, T, U, V, we just need one pictograph and we'll apply different turn combinations
        pictograph_data = matching_pictographs[0].copy()

        # Export the first variation (red=red_turns, blue=blue_turns)
        pictograph = self.factory.create_pictograph_from_data(
            pictograph_data, grid_mode
        )
        TurnApplier.apply_turns_to_pictograph(
            pictograph, red_turns=red_turns, blue_turns=blue_turns
        )
        filename = self.turn_configuration.get_hybrid_filename(
            letter, red_turns, blue_turns, "normal"
        )
        filepath = os.path.join(directory, filename)
        message = f"Saved hybrid pictograph {letter} (normal) with turns (red:{red_turns}, blue:{blue_turns}) to {filepath}"
        self._save_pictograph(pictograph, filepath, message)
        exported_count += 1

        # Export the second variation (red=blue_turns, blue=red_turns)
        pictograph = self.factory.create_pictograph_from_data(
            pictograph_data, grid_mode
        )
        TurnApplier.apply_turns_to_pictograph(
            pictograph, red_turns=blue_turns, blue_turns=red_turns
        )
        filename = self.turn_configuration.get_hybrid_filename(
            letter, blue_turns, red_turns, "swapped"
        )
        filepath = os.path.join(directory, filename)
        message = f"Saved hybrid pictograph {letter} (swapped) with turns (red:{blue_turns}, blue:{red_turns}) to {filepath}"
        self._save_pictograph(pictograph, filepath, message)
        exported_count += 1

        return exported_count

    def export_pictograph(
        self,
        letter: str,
        directory: str,
        red_turns: float,
        blue_turns: float,
        grid_mode: str = "diamond",
    ) -> int:
        """Exports a hybrid pictograph with specified turns.

        Args:
            letter: The letter to export.
            directory: The directory to save to.
            red_turns: The number of turns for the red hand.
            blue_turns: The number of turns for the blue hand.
            grid_mode: The grid mode to use ('diamond' or 'box').

        Returns:
            The number of exported pictographs (0, 1, or 2).
        """
        start_pos, end_pos = self.turn_configuration.get_letter_positions(letter)
        matching_pictographs = self.data_manager.fetch_matching_pictographs(
            letter, start_pos, end_pos
        )

        if not matching_pictographs:
            print(f"Warning: No hybrid data found for letter {letter}")
            return 0

        if red_turns == blue_turns:
            return self._export_non_hybrid(
                letter, directory, red_turns, matching_pictographs, grid_mode
            )
        else:
            return self._export_hybrid_pair(
                letter,
                directory,
                red_turns,
                blue_turns,
                matching_pictographs,
                grid_mode,
            )
