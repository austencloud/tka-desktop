from typing import TYPE_CHECKING
from data.positions_map import positions_map
from data.locations import cw_loc_order

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from main_window.main_widget.grid_mode_checker import GridModeChecker

if TYPE_CHECKING:
    from .codex_control_widget import CodexControlWidget


class CodexRotationManager:
    """Handles rotating the codex in 45° increments."""

    def __init__(self, control_widget: "CodexControlWidget"):
        self.codex = control_widget.codex

    def rotate_codex(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        for letter, pictograph_data in self.codex.data_manager.pictograph_data.items():
            if pictograph_data:
                pictograph_data = self._rotate_pictograph_data(pictograph_data)
                self.codex.data_manager.pictograph_data[letter] = pictograph_data

        for view in self.codex.section_manager.codex_views.values():
            view.pictograph.elements.grid.update_grid_mode()

        self._refresh_pictograph_views()

        QApplication.restoreOverrideCursor()

    def _rotate_pictograph_data(self, pictograph_data: dict) -> dict:
        """Rotate a single pictograph dictionary."""
        for color in ["blue_attributes", "red_attributes"]:
            if color in pictograph_data:
                attributes = pictograph_data[color]
                if "start_loc" in attributes:
                    attributes["start_loc"] = self._rotate_location(
                        attributes["start_loc"]
                    )
                if "end_loc" in attributes:
                    attributes["end_loc"] = self._rotate_location(attributes["end_loc"])

        if "blue_attributes" in pictograph_data and "red_attributes" in pictograph_data:
            bl = pictograph_data["blue_attributes"]
            rl = pictograph_data["red_attributes"]
            if "start_loc" in bl and "start_loc" in rl:
                pictograph_data["start_pos"] = positions_map[
                    (bl["start_loc"], rl["start_loc"])
                ]
            if "end_loc" in bl and "end_loc" in rl:
                pictograph_data["end_pos"] = positions_map[
                    (bl["end_loc"], rl["end_loc"])
                ]
        return pictograph_data

    def _rotate_location(self, location: str) -> str:
        """Rotate a single location by 45° increments."""
        if location not in cw_loc_order:
            return location
        idx = cw_loc_order.index(location)
        new_idx = (idx + 1) % len(cw_loc_order)
        new_loc = cw_loc_order[new_idx]
        return new_loc

    def update_grid_mode(self):
        for view in self.codex.section_manager.codex_views.values():
            grid_mode = GridModeChecker.get_grid_mode(
                view.pictograph.state.pictograph_data
            )
            view.pictograph.elements.grid.hide()
            view.pictograph.elements.grid.__init__(
                view.pictograph, view.pictograph.elements.grid.grid_data, grid_mode
            )

    def _refresh_pictograph_views(self):
        """Refresh all views to reflect the updated pictograph data."""
        for letter, view in self.codex.section_manager.codex_views.items():
            if letter in self.codex.data_manager.pictograph_data:
                pictograph_data = self.codex.data_manager.pictograph_data[letter]
                view.pictograph.managers.arrow_placement_manager.default_positioner.__init__(
                    view.pictograph.managers.arrow_placement_manager
                )
                view.pictograph.managers.updater.update_pictograph(pictograph_data)
