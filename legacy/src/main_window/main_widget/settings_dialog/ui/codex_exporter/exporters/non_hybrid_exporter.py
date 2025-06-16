"""
Non-hybrid pictograph exporter for the codex pictograph exporter.
"""

from typing import TYPE_CHECKING
import os

if TYPE_CHECKING:
    from ..pictograph_data_manager import PictographDataManager
    from ..pictograph_factory import PictographFactory
    from ..pictograph_renderer import PictographRenderer
    from ..turn_configuration import TurnConfiguration


class NonHybridExporter:
    """Non-hybrid pictograph exporter for the codex pictograph exporter."""

    def __init__(
        self,
        data_manager: "PictographDataManager",
        factory: "PictographFactory",
        renderer: "PictographRenderer",
        turn_configuration: "TurnConfiguration",
    ):
        """Initialize the exporter.

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

    def export_pictograph(
        self,
        letter: str,
        directory: str,
        red_turns: float,
        blue_turns: float,
        grid_mode: str = "diamond",
    ) -> int:
        """Export a non-hybrid pictograph with specified turns.

        Args:
            letter: The letter to export
            directory: The directory to save to
            red_turns: The number of turns for the red hand
            blue_turns: The number of turns for the blue hand
            grid_mode: The grid mode to use ('diamond' or 'box')

        Returns:
            The number of exported pictographs (0 or 1)
        """
        # Get the start and end positions for this letter
        start_pos, end_pos = self.turn_configuration.get_letter_positions(letter)

        # Get pictograph data for this letter
        pictograph_data = self.data_manager.get_pictograph_data_for_letter(
            letter, start_pos, end_pos
        )

        # If we couldn't find data, create minimal data
        if not pictograph_data:
            pictograph_data = self.data_manager.create_minimal_data_for_letter(letter)

        # Create the pictograph
        pictograph = self.factory.create_pictograph_from_data(
            pictograph_data, grid_mode
        )

        # Apply the specified turns
        from ..turn_applier import TurnApplier

        TurnApplier.apply_turns_to_pictograph(
            pictograph, red_turns=red_turns, blue_turns=blue_turns
        )

        # Save the pictograph
        filename = self.turn_configuration.get_non_hybrid_filename(letter)
        filepath = os.path.join(directory, filename)

        # Create and save image
        image = self.renderer.create_pictograph_image(pictograph)
        image.save(filepath, "PNG", 100)

        return 1
