"""
Base exporter for Type 2 pictographs.

This module provides the base functionality for exporting Type 2 pictographs
(W, X, Y, Z, Σ, Δ, θ, Ω) with their specific positions and variations.
"""

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
    from ...pictograph_data_manager import PictographDataManager
    from ...pictograph_factory import PictographFactory
    from ...pictograph_renderer import PictographRenderer
    from ...turn_configuration import TurnConfiguration


class Type2BaseExporter:
    """Base class for Type 2 pictograph exporters."""

    def __init__(
        self,
        data_manager: "PictographDataManager",
        factory: "PictographFactory",
        renderer: "PictographRenderer",
        turn_configuration: "TurnConfiguration",
    ):
        """Initialize the Type 2 base exporter.

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

    def _save_pictograph(
        self, pictograph: "LegacyPictograph", filepath: str, message: str
    ):
        """Saves a pictograph image to a file.

        Args:
            pictograph: The pictograph to save
            filepath: The path to save the image to
            message: A message to print when the image is saved
        """
        image = self.renderer.create_pictograph_image(pictograph)
        image.save(filepath, "PNG", 100)
        print(message)

    def export_pictograph(
        self,
        letter: str,
        directory: str,
        red_turns: float,
        blue_turns: float,
        matching_pictographs: list,
        grid_mode: str = "diamond",
    ) -> int:
        """Export a Type 2 pictograph with specified turns.

        This is an abstract method that should be implemented by subclasses.

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
        raise NotImplementedError("Subclasses must implement export_pictograph")
