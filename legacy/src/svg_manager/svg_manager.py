from typing import TYPE_CHECKING
from objects.arrow.arrow_svg_manager import ArrowSvgManager
from svg_manager.svg_color_handler import SvgColorHandler
from svg_manager.prop_svg_manager import PropSvgManager
from utils.path_helpers import get_data_path, get_image_path

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class SvgManager:
    def __init__(self, pictograph: "LegacyPictograph") -> None:
        self.pictograph = pictograph

        self.color_manager = SvgColorHandler(self)
        self.arrow_manager = ArrowSvgManager(self)
        self.prop_manager = PropSvgManager(self)

    def load_svg_file(self, svg_path: str) -> str:
        """
        Load an SVG file from the specified path.

        If the file is not found, return a simple placeholder SVG.
        """
        try:
            file_path = get_image_path(svg_path)
            with open(file_path, "r") as file:
                svg_data = file.read()
            return svg_data
        except (FileNotFoundError, IOError):
            # If the file is not found, return a simple placeholder SVG
            return self._create_placeholder_svg(svg_path)

    def _create_placeholder_svg(self, svg_path: str) -> str:
        """Create a simple placeholder SVG when the requested file is not found."""
        # Extract the filename from the path
        filename = svg_path.split("/")[-1].split("\\")[-1]

        # Create a simple placeholder SVG
        placeholder_svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <rect width="100" height="100" fill="#333333" />
  <text x="50" y="50" font-family="Arial" font-size="10" fill="white" text-anchor="middle">
    {filename}
  </text>
  <text x="50" y="65" font-family="Arial" font-size="8" fill="white" text-anchor="middle">
    (Placeholder)
  </text>
</svg>"""
        return placeholder_svg
