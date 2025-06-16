"""
Creates pictographs for the codex exporter.
"""

from typing import TYPE_CHECKING, Dict, Any, Union
from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
from data.constants import GRID_MODE

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
        ImageExportTab,
    )
    from main_window.main_widget.settings_dialog.ui.codex_exporter.codex_exporter_tab import (
        CodexExporterTab,
    )


class CustomPropSvgManager:
    """Custom PropSvgManager that uses simple_staff.svg instead of staff.svg."""

    def __init__(self, manager):
        """Initialize the prop SVG manager.

        Args:
            manager: The parent SVG manager
        """
        self.manager = manager

    def update_prop_image(self, prop) -> None:
        """Update the prop image.

        Args:
            prop: The prop to update
        """
        # Use simple_staff.svg for all props
        svg_path = "props/simple_staff.svg"

        # For hands, use the appropriate hand SVG
        if prop.prop_type_str == "Hand":
            from data.constants import BLUE

            hand_color = "left" if prop.state.color == BLUE else "right"
            svg_path = f"hands/{hand_color}_hand.svg"

        # Load the SVG data
        from utils.path_helpers import get_image_path

        with open(get_image_path(svg_path), "r") as file:
            svg_data = file.read()

        # Apply color transformations if needed
        if prop.prop_type_str != "Hand" and hasattr(self.manager, "color_manager"):
            svg_data = self.manager.color_manager.apply_color_transformations(
                svg_data, prop.state.color
            )

        # Set up the renderer
        from PyQt6.QtSvg import QSvgRenderer

        prop.renderer = QSvgRenderer()
        prop.renderer.load(svg_data.encode("utf-8"))
        prop.setSharedRenderer(prop.renderer)


class CustomSvgManager:
    """Custom SVG manager for pictographs."""

    def __init__(self, pictograph: LegacyPictograph):
        """Initialize the SVG manager.

        Args:
            pictograph: The pictograph to manage SVGs for
        """
        self.pictograph = pictograph
        self.svg_path = "resources/svg/simple_staff.svg"

        # Create color manager
        from svg_manager.svg_color_handler import SvgColorHandler

        self.color_manager = SvgColorHandler(self)

        # Create arrow manager
        from objects.arrow.arrow_svg_manager import ArrowSvgManager

        self.arrow_manager = ArrowSvgManager(self)

        # Create prop manager
        self.prop_manager = CustomPropSvgManager(self)

    def get_svg_path(self) -> str:
        """Get the SVG path.

        Returns:
            The SVG path
        """
        return self.svg_path

    def load_svg_file(self, svg_path: str) -> str:
        """Load an SVG file.

        Args:
            svg_path: The path to the SVG file

        Returns:
            The SVG data
        """
        from utils.path_helpers import get_image_path

        with open(get_image_path(svg_path), "r") as file:
            svg_data = file.read()
        return svg_data


class PictographFactory:
    """Creates pictographs for the codex exporter."""

    def __init__(self, parent: Union["ImageExportTab", "CodexExporterTab"]):
        """Initialize the factory.

        Args:
            parent: The parent tab (either ImageExportTab or CodexExporterTab)
        """
        self.parent = parent
        self.main_widget = parent.main_widget

    def create_pictograph_from_data(
        self, pictograph_data: Dict[str, Any], grid_mode: str
    ) -> LegacyPictograph:
        """Create a pictograph from the given data.

        Args:
            pictograph_data: The pictograph data
            grid_mode: The grid mode to use

        Returns:
            The created pictograph
        """
        # Create a new pictograph
        pictograph = LegacyPictograph()

        # Replace the default SvgManager with our custom one that uses simple_staff.svg
        pictograph.managers.svg_manager = CustomSvgManager(pictograph)

        # Add grid mode to the data
        data_copy = pictograph_data.copy()
        data_copy[GRID_MODE] = grid_mode

        # Update the pictograph with the data
        pictograph.managers.updater.update_pictograph(data_copy)

        # Disable the default border by setting a flag
        pictograph.state.disable_borders = True

        # Create a custom view without borders
        from base_widgets.pictograph.elements.views.base_pictograph_view import (
            BasePictographView,
        )

        view = BasePictographView(pictograph)
        view.setStyleSheet("border: none;")
        pictograph.elements.view = view

        return pictograph
