from typing import TYPE_CHECKING
from Enums.letters import Letter
from data.constants import STATIC, DASH
from base_widgets.pictograph.hotkey_graph_adjuster.rotation_angle_override_key_generator import (
    ArrowRotAngleOverrideKeyGenerator,
)
from main_window.main_widget.special_placement_loader import SpecialPlacementLoader
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)
from main_window.settings_manager.global_settings.app_context import AppContext


if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph import Pictograph

    from .hotkey_graph_adjuster import HotkeyGraphAdjuster


class ArrowRotAngleOverrideManager:
    """
    Manages rotation angle overrides for arrows in a pictograph based on specific letter types and motions.

    This class handles special cases where the rotation angle of an arrow needs to be overridden, based on the data
    defined in the "{letter}_placements.json" file.
    """

    def __init__(self, hotkey_graph_adjuster: "HotkeyGraphAdjuster") -> None:
        self.wasd_manager = hotkey_graph_adjuster
        self.pictograph = hotkey_graph_adjuster.pictograph
        self.special_positioner = (
            self.pictograph.managers.arrow_placement_manager.special_positioner
        )
        self.key_generator = ArrowRotAngleOverrideKeyGenerator()

    def handle_arrow_rot_angle_override(self) -> None:
        if not self._is_valid_for_override():
            return

        ori_key = self.special_positioner.data_updater._generate_ori_key(
            self.pictograph.main_widget.sequence_workbench.graph_editor.selection_manager.selected_arrow.motion
        )
        data = AppContext.special_placement_loader().load_or_return_special_placements()
        letter = self.pictograph.state.letter
        self._apply_override_if_needed(letter, data, ori_key)
        AppContext.special_placement_loader().reload()
        for (
            pictograph
        ) in self.pictograph.main_widget.pictograph_collector.collect_all_pictographs():
            pictograph.managers.updater.update_pictograph()
            pictograph.managers.arrow_placement_manager.update_arrow_placements()

    def _is_valid_for_override(self) -> bool:
        return (
            self.pictograph.main_widget.sequence_workbench.graph_editor.selection_manager.selected_arrow
            and self.pictograph.main_widget.sequence_workbench.graph_editor.selection_manager.selected_arrow.motion.state.motion_type
            in [STATIC, DASH]
        )

    def _apply_override_if_needed(
        self, letter: Letter, data: dict, ori_key: str
    ) -> None:
        rot_angle_key = self.key_generator.generate_rotation_angle_override_key(
            self.pictograph.main_widget.sequence_workbench.graph_editor.selection_manager.selected_arrow
        )
        turns_tuple = TurnsTupleGenerator().generate_turns_tuple(self.pictograph)
        self._apply_rotation_override(letter, data, ori_key, turns_tuple, rot_angle_key)

    def _apply_rotation_override(
        self,
        letter_enum: Letter,
        data: dict,
        ori_key: str,
        turns_tuple: str,
        rot_angle_key: str,
    ) -> None:
        letter_data = data[self.pictograph.state.grid_mode][ori_key].get(
            letter_enum.value, {}
        )
        turn_data = letter_data.get(turns_tuple, {})
        letter_data[turns_tuple] = turn_data
        data[self.wasd_manager.pictograph.state.grid_mode][ori_key][
            letter_enum.value
        ] = letter_data
        if rot_angle_key in turn_data:
            del turn_data[rot_angle_key]
            self._update_mirrored_entry_with_rotation_override_removal(rot_angle_key)
        else:
            turn_data[rot_angle_key] = True
            self._update_mirrored_entry_with_rotation_override(turn_data)
        self.special_positioner.data_updater.update_specific_entry_in_json(
            letter_enum, letter_data, ori_key
        )
        self.pictograph.managers.updater.update_pictograph()

    def handle_mirrored_rotation_angle_override(
        self, other_letter_data, rotation_angle_override, mirrored_turns_tuple
    ) -> None:
        rot_angle_key = self.key_generator.generate_rotation_angle_override_key()
        if mirrored_turns_tuple not in other_letter_data:
            other_letter_data[mirrored_turns_tuple] = {}
        other_letter_data[mirrored_turns_tuple][rot_angle_key] = rotation_angle_override

    def _update_mirrored_entry_with_rotation_override(self, updated_turn_data: dict):
        mirrored_entry_manager = (
            self.wasd_manager.pictograph.managers.arrow_placement_manager.special_positioner.data_updater.mirrored_entry_manager
        )
        mirrored_entry_manager.rot_angle_manager.update_rotation_angle_in_mirrored_entry(
            self.pictograph.main_widget.sequence_workbench.graph_editor.selection_manager.selected_arrow,
            updated_turn_data,
        )

    def _update_mirrored_entry_with_rotation_override_removal(self, hybrid_key: str):
        mirrored_entry_handler = (
            self.wasd_manager.pictograph.managers.arrow_placement_manager.special_positioner.data_updater.mirrored_entry_manager
        )
        if mirrored_entry_handler:
            mirrored_entry_handler.rot_angle_manager.remove_rotation_angle_in_mirrored_entry(
                self.pictograph.main_widget.sequence_workbench.graph_editor.selection_manager.selected_arrow,
                hybrid_key,
            )
