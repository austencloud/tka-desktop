"""
Type 2 pictograph exporter for the codex pictograph exporter.

This exporter handles the Type 2 letters (W, X, Y, Z, Σ, Δ, θ, Ω) with their specific
positions and variations.
"""

from typing import TYPE_CHECKING

from .type2.one_zero_turn_exporter import OneZeroTurnExporter
from .type2.both_non_zero_turn_exporter import BothNonZeroTurnExporter

if TYPE_CHECKING:
    from ..pictograph_data_manager import PictographDataManager
    from ..pictograph_factory import PictographFactory
    from ..pictograph_renderer import PictographRenderer
    from ..turn_configuration import TurnConfiguration


class Type23Exporter:
    """Exports Type 2 pictographs for the codex."""

    def __init__(
        self,
        data_manager: "PictographDataManager",
        factory: "PictographFactory",
        renderer: "PictographRenderer",
        turn_configuration: "TurnConfiguration",
    ):
        """Initialize the Type 2 exporter.

        Args:
            data_manager: The pictograph data manager
            factory: The pictograph factory
            renderer: The pictograph renderer
            turn_configuration: The turn configuration
        """
        self.data_manager = data_manager
        self.factory = factory
        self.renderer = renderer
        self.turn_configuration = turn_configuration

        # Initialize specialized exporters
        self.one_zero_turn_exporter = OneZeroTurnExporter(
            data_manager, factory, renderer, turn_configuration
        )
        self.both_non_zero_turn_exporter = BothNonZeroTurnExporter(
            data_manager, factory, renderer, turn_configuration
        )

    def export_pictograph(
        self,
        letter: str,
        directory: str,
        red_turns: float,
        blue_turns: float,
        grid_mode: str = "diamond",
    ) -> int:
        """Exports a Type 2 pictograph with specified turns.

        Args:
            letter: The letter to export.
            directory: The directory to save to.
            red_turns: The number of turns for the red hand.
            blue_turns: The number of turns for the blue hand.
            grid_mode: The grid mode to use ('diamond' or 'box').

        Returns:
            The number of exported pictographs.
        """
        start_pos, end_pos = self.turn_configuration.get_letter_positions(letter)
        matching_pictographs = self.data_manager.fetch_matching_pictographs(
            letter, start_pos, end_pos
        )

        if not matching_pictographs:
            print(f"Warning: No Type 2 data found for letter {letter}")
            return 0

        # For Type 2 letters, we have different cases:
        # 1. If one turn value is 0, we'll have 12 variations total
        # 2. If both turn values are non-zero, we'll have 16 variations total

        if red_turns == 0 or blue_turns == 0:
            return self.one_zero_turn_exporter.export_pictograph(
                letter,
                directory,
                red_turns,
                blue_turns,
                matching_pictographs,
                grid_mode,
            )
        else:
            return self.both_non_zero_turn_exporter.export_pictograph(
                letter,
                directory,
                red_turns,
                blue_turns,
                matching_pictographs,
                grid_mode,
            )
