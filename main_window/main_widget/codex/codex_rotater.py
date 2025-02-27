from typing import TYPE_CHECKING
from data.constants import BLUE_ATTRIBUTES, END_POS, RED_ATTRIBUTES, START_POS
from data.positions_map import positions_map
from data.locations import cw_loc_order

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from main_window.main_widget.grid_mode_checker import GridModeChecker

if TYPE_CHECKING:
    from .codex_control_widget import CodexControlWidget


class CodexRotater:
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
        for color in [BLUE_ATTRIBUTES, RED_ATTRIBUTES]:
            if color in pictograph_data:
                attributes = pictograph_data[color]
                if START_LOC in attributes:
                    attributes[START_LOC] = self._rotate_location(attributes[START_LOC])
                if END_LOC in attributes:
                    attributes[END_LOC] = self._rotate_location(attributes[END_LOC])

        if BLUE_ATTRIBUTES in pictograph_data and RED_ATTRIBUTES in pictograph_data:
            bl = pictograph_data[BLUE_ATTRIBUTES]
            rl = pictograph_data[RED_ATTRIBUTES]
            if START_LOC in bl and START_LOC in rl:
                pictograph_data[START_POS] = positions_map[
                    (bl[START_LOC], rl[START_LOC])
                ]
            if END_LOC in bl and END_LOC in rl:
                pictograph_data[END_POS] = positions_map[(bl[END_LOC], rl[END_LOC])]
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
