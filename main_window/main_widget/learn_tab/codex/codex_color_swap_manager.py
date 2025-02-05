from typing import TYPE_CHECKING

import logging

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.codex.codex_control_widget import (
        CodexControlWidget,
    )


class CodexColorSwapManager:
    def __init__(self, control_widget: "CodexControlWidget"):
        self.codex = control_widget.codex

    def _swap_colors(self, pictograph):
        if not pictograph:
            return
        pictograph["blue_attributes"], pictograph["red_attributes"] = (
            pictograph["red_attributes"],
            pictograph["blue_attributes"],
        )

    def swap_colors_in_codex(self):
        for pictograph in self.codex.data_manager.pictograph_data.values():
            self._swap_colors(pictograph)
        try:
            for letter_str, view in self.codex.section_manager.codex_views.items():
                scene = view.pictograph
                if scene.pictograph_data:
                    # Implement actual color swap logic here
                    scene.updater.update_pictograph(scene.pictograph_data)
                    logger.debug(f"Swapped colors for pictograph '{letter_str}'.")
        except Exception as e:
            logger.exception(f"Error during color_swap_all: {e}")
