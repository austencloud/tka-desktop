import logging
from typing import TYPE_CHECKING
from data.constants import (
    BLUE_ATTRS,
    END_LOC,
    END_POS,
    PROP_ROT_DIR,
    RED_ATTRS,
    START_LOC,
    START_POS,
    VERTICAL,
)
from data.locations import vertical_loc_mirror_map
from data.positions_maps import mirrored_positions

logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from .codex_control_widget import CodexControlWidget
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt


class CodexReflector:
    """Handles mirroring of pictographs in the Codex."""

    def __init__(self, control_widget: "CodexControlWidget"):
        self.codex = control_widget.codex
        self.vertical_mirror_positions = mirrored_positions[VERTICAL]
        self.control_widget = control_widget

    def mirror_codex(self):
        """Apply mirroring logic to all pictographs in the Codex."""
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        for letter, pictograph in self.codex.data_manager.pictograph_data.items():
            if pictograph:
                self._mirror_pictograph(pictograph)
        self.control_widget.refresh_pictograph_views()
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

        for color_attrs in [BLUE_ATTRS, RED_ATTRS]:
            if color_attrs in pictograph:
                attributes = pictograph[color_attrs]
                if START_LOC in attributes:
                    attributes[START_LOC] = vertical_loc_mirror_map.get(
                        attributes[START_LOC], attributes[START_LOC]
                    )
                if END_LOC in attributes:
                    attributes[END_LOC] = vertical_loc_mirror_map.get(
                        attributes[END_LOC], attributes[END_LOC]
                    )
                if PROP_ROT_DIR in attributes:
                    attributes[PROP_ROT_DIR] = self._reverse_prop_rot_dir(
                        attributes[PROP_ROT_DIR]
                    )

    def _reverse_prop_rot_dir(self, prop_rot_dir):
        """Reverse the rotation direction."""
        return {"cw": "ccw", "ccw": "cw"}.get(prop_rot_dir)
