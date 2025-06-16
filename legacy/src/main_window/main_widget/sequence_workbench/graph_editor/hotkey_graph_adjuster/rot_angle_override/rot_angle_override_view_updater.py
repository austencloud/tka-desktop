# src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/arrow_rot_angle_override_manager.py
from typing import TYPE_CHECKING

from src.legacy_settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from .rot_angle_override_manager import RotAngleOverrideManager


class RotAngleOverrideViewUpdater:
    """Handles UI updates related to rotation overrides"""

    def __init__(self, manager: "RotAngleOverrideManager"):
        self.manager = manager

    def refresh_affected_views(self) -> None:
        AppContext.special_placement_loader().reload()
        self._update_pictographs()

    def _update_pictographs(self) -> None:
        target_letter = self.manager.current_letter
        collector = self.manager.view.main_widget.pictograph_collector

        for pictograph in collector.collect_all_pictographs():
            if pictograph.state.letter == target_letter:
                pictograph.managers.updater.update_pictograph(
                    pictograph.state.pictograph_data
                )
                pictograph.managers.arrow_placement_manager.update_arrow_placements()
