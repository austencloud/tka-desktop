"""
Main class for the codex pictograph exporter.
"""

from typing import TYPE_CHECKING, List, Union

from .pictograph_data_manager import PictographDataManager
from .pictograph_factory import PictographFactory
from .pictograph_renderer import PictographRenderer
from .turn_configuration import TurnConfiguration
from .exporters.main_exporter import MainExporter

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
        ImageExportTab,
    )
    from main_window.main_widget.settings_dialog.ui.codex_exporter.codex_exporter_tab import (
        CodexExporterTab,
    )


class CodexExporter:
    """Main class for the codex pictograph exporter."""

    def __init__(self, parent: Union["ImageExportTab", "CodexExporterTab"]):
        """Initialize the exporter.

        Args:
            parent: The parent tab (either ImageExportTab or CodexExporterTab)
        """
        self.parent = parent
        self.main_widget = parent.main_widget

        # Create the components
        self.data_manager = PictographDataManager(parent)
        self.factory = PictographFactory(parent)
        self.renderer = PictographRenderer(parent)
        self.turn_configuration = TurnConfiguration()

        # Create the main exporter
        self.main_exporter = MainExporter(
            parent,
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
        red_turns: float,
        blue_turns: float,
        generate_all: bool = False,
        grid_mode: str = "diamond",
    ) -> int:
        """Export pictographs with the specified turns.

        Args:
            selected_types: The letters to export
            red_turns: The number of turns for the red hand
            blue_turns: The number of turns for the blue hand
            generate_all: Whether to generate all turn combinations
            grid_mode: The grid mode to use ('diamond' or 'box')

        Returns:
            The number of exported pictographs
        """
        return self.main_exporter.export_pictographs(
            selected_types, red_turns, blue_turns, generate_all, grid_mode
        )
