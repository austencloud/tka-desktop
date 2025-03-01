from typing import TYPE_CHECKING
from enums.letter.letter import Letter

from data.constants import STATIC, DASH

from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.rotation_angle_override_key_generator import (
    ArrowRotAngleOverrideKeyGenerator,
)
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)
from settings_manager.global_settings.app_context import AppContext


if TYPE_CHECKING:
    pass

    from .hotkey_graph_adjuster import HotkeyGraphAdjuster


class ArrowRotAngleOverrideManager:
    """
    Manages rotation angle overrides for arrows in a pictograph based on specific letter types and motions.

    This class handles special cases where the rotation angle of an arrow needs to be overridden, based on the data
    defined in the "{letter}_placements.json" file.
    """

    def __init__(self, hotkey_graph_adjuster: "HotkeyGraphAdjuster") -> None:
        self.hotkey_graph_adjuster = hotkey_graph_adjuster
        self.view = hotkey_graph_adjuster.ge_view

        self.arrow_placement_manager = (
            self.view.scene().managers.arrow_placement_manager
        )
        self.data_updater = self.arrow_placement_manager.data_updater
        self.key_generator = ArrowRotAngleOverrideKeyGenerator()

    def handle_arrow_rot_angle_override(self) -> None:
        if not self._is_valid_for_override():
            return

        ori_key = self.data_updater.ori_key_generator.generate_ori_key_from_motion(
            AppContext.get_selected_arrow().motion
        )
        data = AppContext.special_placement_loader().load_or_return_special_placements()
        letter = self.view.scene().state.letter
        self._apply_override_if_needed(letter, data, ori_key)
        AppContext.special_placement_loader().reload()
        for (
            pictograph
        ) in self.view.main_widget.pictograph_collector.collect_all_pictographs():
            if pictograph.state.letter == letter:
                pictograph.managers.updater.update_pictograph()
                pictograph.managers.arrow_placement_manager.update_arrow_placements()

    def _is_valid_for_override(self) -> bool:
        return (
            AppContext.get_selected_arrow()
            and AppContext.get_selected_arrow().motion.state.motion_type
            in [STATIC, DASH]
        )

    def _apply_override_if_needed(
        self, letter: Letter, data: dict, ori_key: str
    ) -> None:
        rot_angle_key = self.key_generator.generate_rotation_angle_override_key(
            AppContext.get_selected_arrow()
        )
        turns_tuple = TurnsTupleGenerator().generate_turns_tuple(
            self.hotkey_graph_adjuster.ge_view.scene()
        )
        self._apply_rotation_override(letter, data, ori_key, turns_tuple, rot_angle_key)

    def _apply_rotation_override(
        self,
        letter_enum: Letter,
        data: dict,
        ori_key: str,
        turns_tuple: str,
        rot_angle_key: str,
    ) -> None:
        letter_data = (
            data.get(self.view.scene().state.grid_mode, {})
            .get(ori_key, {})
            .get(letter_enum.value, {})
        )
        turn_data = letter_data.get(turns_tuple, {})
        letter_data[turns_tuple] = turn_data
        data.get(
            self.hotkey_graph_adjuster.ge_view.scene().state.grid_mode,
            {},
        ).get(
            ori_key, {}
        )[letter_enum.value] = letter_data
        if rot_angle_key in turn_data:
            del turn_data[rot_angle_key]
            self._update_mirrored_entry_with_rotation_override_removal(rot_angle_key)
        else:
            turn_data[rot_angle_key] = True
            self._update_mirrored_entry_with_rotation_override(turn_data)
        self.data_updater.update_specific_entry_in_json(
            letter_enum, letter_data, ori_key
        )
        self.view.scene().managers.updater.update_pictograph()

    def handle_mirrored_rotation_angle_override(
        self, other_letter_data, rotation_angle_override, mirrored_turns_tuple
    ) -> None:
        rot_angle_key = self.key_generator.generate_rotation_angle_override_key()
        if mirrored_turns_tuple not in other_letter_data:
            other_letter_data[mirrored_turns_tuple] = {}
        other_letter_data[mirrored_turns_tuple][rot_angle_key] = rotation_angle_override

    def _update_mirrored_entry_with_rotation_override(self, updated_turn_data: dict):
        mirrored_entry_manager = (
            self.hotkey_graph_adjuster.ge_view.scene().managers.arrow_placement_manager.data_updater.mirrored_entry_manager
        )
        mirrored_entry_manager.rot_angle_manager.update_rotation_angle_in_mirrored_entry(
            AppContext.get_selected_arrow(),
            updated_turn_data,
        )

    def _update_mirrored_entry_with_rotation_override_removal(self, hybrid_key: str):
        mirrored_entry_handler = (
            self.hotkey_graph_adjuster.ge_view.scene().managers.arrow_placement_manager.data_updater.mirrored_entry_manager
        )
        if mirrored_entry_handler:
            mirrored_entry_handler.rot_angle_manager.remove_rotation_angle_in_mirrored_entry(
                AppContext.get_selected_arrow(),
                hybrid_key,
            )
