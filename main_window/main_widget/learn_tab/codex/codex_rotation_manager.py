from typing import TYPE_CHECKING
from data.positions_map import positions_map
from data.locations import cw_loc_order

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from .codex_control_widget import CodexControlWidget


class CodexRotationManager:
    """Handles rotating the codex in 45° increments."""

    def __init__(self, control_widget: "CodexControlWidget"):
        self.codex = control_widget.codex

    def rotate_codex(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        for letter, pictograph_dict in self.codex.data_manager.pictograph_data.items():
            if pictograph_dict:
                pictograph_dict = self._rotate_pictograph_dict(pictograph_dict)
                self.codex.data_manager.pictograph_data[letter] = pictograph_dict

        for view in self.codex.section_manager.codex_views.values():
            view.pictograph.grid.update_grid_mode()

        self._refresh_pictograph_views()

        QApplication.restoreOverrideCursor()

    def _rotate_pictograph_dict(self, pictograph_dict: dict) -> dict:
        """Rotate a single pictograph dictionary."""
        for color in ["blue_attributes", "red_attributes"]:
            if color in pictograph_dict:
                attributes = pictograph_dict[color]
                if "start_loc" in attributes:
                    attributes["start_loc"] = self._rotate_location(
                        attributes["start_loc"]
                    )
                if "end_loc" in attributes:
                    attributes["end_loc"] = self._rotate_location(attributes["end_loc"])

        if "blue_attributes" in pictograph_dict and "red_attributes" in pictograph_dict:
            bl = pictograph_dict["blue_attributes"]
            rl = pictograph_dict["red_attributes"]
            if "start_loc" in bl and "start_loc" in rl:
                pictograph_dict["start_pos"] = positions_map[
                    (bl["start_loc"], rl["start_loc"])
                ]
            if "end_loc" in bl and "end_loc" in rl:
                pictograph_dict["end_pos"] = positions_map[
                    (bl["end_loc"], rl["end_loc"])
                ]
        return pictograph_dict

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
            grid_mode = self.codex.main_widget.grid_mode_checker.get_grid_mode(
                view.pictograph.pictograph_dict
            )
            view.pictograph.grid.hide()
            view.pictograph.grid.__init__(
                view.pictograph, view.pictograph.grid.grid_data, grid_mode
            )

    def _refresh_pictograph_views(self):
        """Refresh all views to reflect the updated pictograph data."""
        for letter, view in self.codex.section_manager.codex_views.items():
            if letter in self.codex.data_manager.pictograph_data:
                pictograph_dict = self.codex.data_manager.pictograph_data[letter]
                view.pictograph.arrow_placement_manager.default_positioner.__init__(
                    view.pictograph.arrow_placement_manager
                )
                view.pictograph.updater.update_pictograph(pictograph_dict)
