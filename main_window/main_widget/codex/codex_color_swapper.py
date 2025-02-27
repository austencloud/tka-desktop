from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
import logging

from data.constants import BLUE_ATTRIBUTES, RED_ATTRIBUTES


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .codex_control_widget import CodexControlWidget


class CodexColorSwapper:
    def __init__(self, control_widget: "CodexControlWidget"):
        self.codex = control_widget.codex
        self.control_widget = control_widget

    def _swap_colors(self, pictograph):

        if not pictograph:
            return
        pictograph[BLUE_ATTRIBUTES], pictograph[RED_ATTRIBUTES] = (
            pictograph[RED_ATTRIBUTES],
            pictograph[BLUE_ATTRIBUTES],
        )

    def swap_colors_in_codex(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        for pictograph in self.codex.data_manager.pictograph_data.values():
            self._swap_colors(pictograph)
        self.control_widget.refresh_pictograph_views()
        QApplication.restoreOverrideCursor()
