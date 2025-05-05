"""
Main class for the codex pictograph exporter.
"""

from typing import TYPE_CHECKING, List

from .pictograph_data_manager import PictographDataManager
from .pictograph_factory import PictographFactory
from .pictograph_renderer import PictographRenderer
from .turn_configuration import TurnConfiguration
from .exporters.main_exporter import MainExporter

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
        ImageExportTab,
    )


class CodexExporter:
    """Main class for the codex pictograph exporter."""

    def __init__(self, image_export_tab: "ImageExportTab"):
        """Initialize the exporter.

        Args:
            image_export_tab: The parent image export tab
        """
        self.image_export_tab = image_export_tab
        self.main_widget = image_export_tab.main_widget

        # Create the components
        self.data_manager = PictographDataManager(image_export_tab)
        self.factory = PictographFactory(image_export_tab)
        self.renderer = PictographRenderer(image_export_tab)
        self.turn_configuration = TurnConfiguration()

        # Create the main exporter
        self.main_exporter = MainExporter(
            image_export_tab,
            self.data_manager,
            self.factory,
            self.renderer,
            self.turn_configuration,
        )

    def _create_pictograph_from_data(self, pictograph_data, grid_mode: str):
        """Create a pictograph from the given data.

        Args:
            pictograph_data: The pictograph data
            grid_mode: The grid mode to use

        Returns:
            The created pictograph
        """
        return self.factory.create_pictograph_from_data(pictograph_data, grid_mode)

    def _create_pictograph_image(self, pictograph, add_border: bool = False):
        """Create a QImage from a pictograph.

        Args:
            pictograph: The pictograph to convert to an image
            add_border: Whether to add a border

        Returns:
            The created image
        """
        if add_border:
            return self.renderer.create_pictograph_image_with_border(pictograph)
        else:
            return self.renderer.create_pictograph_image(pictograph)

    def export_pictographs(
        self,
        selected_types: List[str],
        red_turns: int,
        blue_turns: int,
        generate_all: bool = False,
    ) -> int:
        """Export pictographs with the specified turns.

        Args:
            selected_types: The letters to export
            red_turns: The number of turns for the red hand
            blue_turns: The number of turns for the blue hand
            generate_all: Whether to generate all turn combinations

        Returns:
            The number of exported pictographs
        """
        return self.main_exporter.export_pictographs(
            selected_types, red_turns, blue_turns, generate_all
        )
