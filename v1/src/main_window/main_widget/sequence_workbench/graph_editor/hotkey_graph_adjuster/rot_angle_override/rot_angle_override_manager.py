from typing import TYPE_CHECKING
from enums.letter.letter import Letter
from ..data_updater.special_placement_data_updater import SpecialPlacementDataUpdater
from .rot_angle_override_data_handler import RotAngleOverrideDataHandler
from .rot_angle_override_coordinator import RotAngleOverrideCoordinator
from .rot_angle_override_validator import RotAngleOverrideValidator
from .rot_angle_override_mirror_handler import RotAngleOverrideMirrorHandler
from .rot_angle_override_view_updater import RotAngleOverrideViewUpdater
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)

if TYPE_CHECKING:
    from ..hotkey_graph_adjuster import HotkeyGraphAdjuster


class RotAngleOverrideManager:
    """Main coordinator for arrow rotation angle override functionality"""

    def __init__(self, hotkey_graph_adjuster: "HotkeyGraphAdjuster") -> None:
        self.hotkey_graph_adjuster = hotkey_graph_adjuster
        self.view = hotkey_graph_adjuster.ge_view
        self.current_letter = self.view.pictograph.state.letter

        self.data_updater = self._get_data_updater()
        self.turns_generator = TurnsTupleGenerator()

        self.validator = RotAngleOverrideValidator(self)
        self.data_handler = RotAngleOverrideDataHandler(self)
        self.view_updater = RotAngleOverrideViewUpdater(self)
        self.mirror_handler = RotAngleOverrideMirrorHandler(self)
        self.coordinator = RotAngleOverrideCoordinator(self)

    def handle_arrow_rot_angle_override(self) -> None:
        """Main entry point for handling rotation angle overrides"""
        self.coordinator.execute_override_flow()

    def _get_data_updater(self) -> SpecialPlacementDataUpdater:
        return self.view.pictograph.managers.arrow_placement_manager.data_updater

    @property
    def current_letter(self) -> Letter:
        return self.view.pictograph.state.letter

    @current_letter.setter
    def current_letter(self, value: Letter):
        self.view.pictograph.state.letter = value
