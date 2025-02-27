import logging
from typing import TYPE_CHECKING
from data.constants import BLUE_ATTRIBUTES, END_POS, RED_ATTRIBUTES, START_POS
from data.locations import vertical_loc_mirror_map
from data.positions import mirrored_positions

logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from .codex_control_widget import CodexControlWidget
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt


class CodexReflector:
    """Handles mirroring of pictographs in the Codex."""

    def __init__(self, control_widget: "CodexControlWidget"):
        self.codex = control_widget.codex
        self.vertical_mirror_positions = mirrored_positions["vertical"]

    def mirror_codex(self):
        """Apply mirroring logic to all pictographs in the Codex."""
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        for letter, pictograph in self.codex.data_manager.pictograph_data.items():
            if pictograph:
                self._mirror_pictograph(pictograph)
        self._refresh_pictograph_views()
        QApplication.restoreOverrideCursor()

    def _mirror_pictograph(self, pictograph):
        """Mirror an individual pictograph dictionary."""
        if START_POS in pictograph:
            pictograph[START_POS] = self.vertical_mirror_positions.get(
                pictograph[START_POS], pictograph[START_POS]
            )
        if END_POS in pictograph:
            pictograph[END_POS] = self.vertical_mirror_positions.get(
                pictograph[END_POS], pictograph[END_POS]
            )

        for color in [BLUE_ATTRIBUTES, RED_ATTRIBUTES]:
            if color in pictograph:
                attributes = pictograph[color]
                if "start_loc" in attributes:
                    attributes["start_loc"] = vertical_loc_mirror_map.get(
                        attributes["start_loc"], attributes["start_loc"]
                    )
                if "end_loc" in attributes:
                    attributes["end_loc"] = vertical_loc_mirror_map.get(
                        attributes["end_loc"], attributes["end_loc"]
                    )
                if "prop_rot_dir" in attributes:
                    attributes["prop_rot_dir"] = self._reverse_prop_rot_dir(
                        attributes["prop_rot_dir"]
                    )

    def _reverse_prop_rot_dir(self, prop_rot_dir):
        """Reverse the rotation direction."""
        return {"cw": "ccw", "ccw": "cw"}.get(prop_rot_dir)

    def _refresh_pictograph_views(self):
        """Refresh all views to reflect the updated pictograph data."""
        for letter, view in self.codex.section_manager.codex_views.items():
            if letter in self.codex.data_manager.pictograph_data:
                pictograph_data = self.codex.data_manager.pictograph_data[letter]
                view.pictograph.managers.updater.update_pictograph(pictograph_data)
                view.scene().update()
