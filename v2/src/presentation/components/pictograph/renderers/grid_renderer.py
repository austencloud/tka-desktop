"""
Grid renderer for pictograph components.

Handles rendering of grid elements using SVG assets.
"""

import os
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from presentation.components.pictograph.asset_utils import get_image_path


class GridRenderer:
    """Handles grid rendering for pictographs."""

    def __init__(self, scene):
        self.scene = scene

    def render_grid(self) -> None:
        """Render the grid using SVG assets."""
        grid_svg_path = get_image_path("grid/diamond_grid.svg")

        if os.path.exists(grid_svg_path):
            grid_item = QGraphicsSvgItem()
            renderer = QSvgRenderer(grid_svg_path)

            if renderer.isValid():
                grid_item.setSharedRenderer(renderer)
                grid_item.setScale(1.0)
                grid_item.setPos(0, 0)
                self.scene.addItem(grid_item)
