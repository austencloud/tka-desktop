from typing import TYPE_CHECKING

from data.constants import BOX, DIAMOND
from main_window.main_widget.grid_mode_checker import GridModeChecker
from src.legacy_settings_manager.global_settings.app_context import AppContext
from utils.path_helpers import get_image_path

from .grid_data import GridData
from .grid_item import GridItem
from .non_radial_points_group import NonRadialPointsGroup

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph

GRID_DIR = "grid/"


class Grid:
    def __init__(
        self, pictograph: "LegacyPictograph", grid_data: GridData, grid_mode: str
    ):

        self.pictograph = pictograph
        self.grid_data = grid_data
        self.grid_mode = grid_mode
        self.items: dict[str, GridItem] = {}
        self.center = self.grid_data.center_points.get(grid_mode)

        self._create_grid_items()

    def _create_grid_items(self):
        paths = {
            DIAMOND: f"{GRID_DIR}{DIAMOND}_grid.svg",
            BOX: f"{GRID_DIR}{BOX}_grid.svg",
        }

        for mode, path in paths.items():
            grid_item = GridItem(get_image_path(path))
            self.pictograph.addItem(grid_item)
            grid_item.setVisible(mode == self.grid_mode)
            self.items[mode] = grid_item

        non_radial_paths = {
            DIAMOND: f"{GRID_DIR}{DIAMOND}_nonradial_points.svg",
            BOX: f"{GRID_DIR}{BOX}_nonradial_points.svg",
        }

        non_radial_path = non_radial_paths.get(self.grid_mode)
        if non_radial_path:
            non_radial_points = NonRadialPointsGroup(non_radial_path)
            self.pictograph.addItem(non_radial_points)
            is_visible = (
                AppContext.settings_manager().visibility.get_non_radial_visibility()
            )
            non_radial_points.setVisible(is_visible)
            self.items[f"{self.grid_mode}_nonradial"] = non_radial_points

    def toggle_non_radial_points(self, visible: bool):
        if not self.grid_mode:
            self.grid_mode = GridModeChecker.get_grid_mode(
                self.pictograph.state.pictograph_data
            )
        non_radial_key = f"{self.grid_mode}_nonradial"
        self.items[non_radial_key].setVisible(visible)

    def hide(self):
        for item in self.items.values():
            item.setVisible(False)

    def update_grid_mode(self):
        grid_mode = self.pictograph.state.grid_mode
        grid_data = self.pictograph.elements.grid.grid_data
        self.pictograph.elements.grid.hide()
        self.pictograph.elements.grid.__init__(self.pictograph, grid_data, grid_mode)
