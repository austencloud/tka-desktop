from typing import TYPE_CHECKING

from Enums.letters import Letter
from main_window.settings_manager.global_settings.app_context import AppContext


if TYPE_CHECKING:
    from .hotkey_graph_adjuster import HotkeyGraphAdjuster


class PropPlacementOverrideManager:
    def __init__(self, hotkey_adjuster: "HotkeyGraphAdjuster") -> None:
        self.pictograph = hotkey_adjuster.pictograph
        self.data_updater = (
            hotkey_adjuster.pictograph.managers.arrow_placement_manager.data_updater
        )
        self.turns_tuple_generator = hotkey_adjuster.turns_tuple_generator

    def handle_prop_placement_override(self, key) -> None:
        self.special_placements = (
            AppContext.special_placement_loader().load_or_return_special_placements()
        )
        if self._is_mixed_ori():
            return
        beta_ori = self._get_beta_ori()
        self.letter = self.pictograph.state.letter

        if self.pictograph.managers.check.ends_with_beta():
            adjustment_key_str, ori_key, override_key = self._get_keys(beta_ori)
            letter_data = self._get_letter_data(ori_key, self.letter)
            turn_data = self._get_turn_data(letter_data, adjustment_key_str)

            if override_key in turn_data:
                del turn_data[override_key]
            else:
                turn_data[override_key] = True

            letter_data[adjustment_key_str] = turn_data
            self.special_placements[self.pictograph.state.grid_mode][ori_key][
                self.letter
            ] = letter_data
            self._update_json_entry(self.letter, letter_data)
            self.pictograph.managers.updater.update_pictograph()

        AppContext.special_placement_loader().reload()

    def _get_keys(self, beta_ori):
        adjustment_key_str = self._generate_adjustment_key_str(self.letter)
        ori_key = self.data_updater.ori_key_generator.generate_ori_key_from_motion(
            self.pictograph.elements.blue_motion
        )
        override_key = self._generate_override_key(beta_ori)
        return adjustment_key_str, ori_key, override_key

    def _is_mixed_ori(self) -> bool:
        return not (
            self.pictograph.managers.check.ends_with_nonradial_ori()
            or self.pictograph.managers.check.ends_with_radial_ori()
        )

    def _get_beta_ori(self):
        if self.pictograph.managers.check.ends_with_nonradial_ori():
            beta_ori = "nonradial"
        elif self.pictograph.managers.check.ends_with_radial_ori():
            beta_ori = "radial"
        return beta_ori

    def _generate_adjustment_key_str(self, letter) -> str:
        return self.turns_tuple_generator.generate_turns_tuple(self.pictograph)

    def _generate_override_key(self, beta_state) -> str:
        return (
            f"swap_beta_{self.pictograph.elements.blue_prop.loc}_{beta_state}_"
            f"blue_{self.pictograph.elements.blue_motion.state.motion_type}_{self.pictograph.elements.blue_arrow.state.loc}_"
            f"red_{self.pictograph.elements.red_motion.state.motion_type}_{self.pictograph.elements.red_arrow.state.loc}"
        )

    def _get_letter_data(self, ori_key, letter: Letter) -> dict:
        return (
            AppContext.special_placement_loader()
            .load_or_return_special_placements()[self.pictograph.state.grid_mode][
                ori_key
            ]
            .get(letter.value, {})
        )

    def _get_turn_data(self, letter_data, adjustment_key_str) -> dict:
        return letter_data.get(adjustment_key_str, {})

    def _update_json_entry(self, letter, letter_data) -> None:
        ori_key = self.data_updater.ori_key_generator.generate_ori_key_from_motion(
            self.pictograph.elements.blue_motion
        )
        self.data_updater.update_specific_entry_in_json(letter, letter_data, ori_key)
