from typing import TYPE_CHECKING

from enums.letter.letter import Letter

from src.legacy_settings_manager.global_settings.app_context import AppContext
from objects.prop.prop import Prop
from placement_managers.prop_placement_manager.handlers.beta_offset_calculator import (
    BetaOffsetCalculator,
)


if TYPE_CHECKING:
    from .hotkey_graph_adjuster import HotkeyGraphAdjuster


class PropPlacementOverrideManager:
    def __init__(self, hotkey_adjuster: "HotkeyGraphAdjuster") -> None:
        self.view = hotkey_adjuster.ge_view
        self.data_updater = (
            hotkey_adjuster.ge_view.scene().managers.arrow_placement_manager.data_updater
        )
        self.turns_tuple_generator = hotkey_adjuster.turns_tuple_generator
        self.beta_offset_calculator = BetaOffsetCalculator(self)

    def handle_prop_placement_override(self) -> None:
        self.ge_pictograph = self.view.scene()
        self.special_placements = (
            AppContext.special_placement_loader().load_or_return_special_placements()
        )
        if self._is_mixed_ori():
            return
        beta_ori = self._get_beta_ori()
        self.letter = self.ge_pictograph.state.letter

        if self.view.scene().managers.check.ends_with_beta():
            adjustment_key_str, ori_key, override_key = self._get_keys(beta_ori)
            letter_data = self._get_letter_data(ori_key, self.letter)
            turn_data = self._get_turn_data(letter_data, adjustment_key_str)

            if override_key in turn_data:
                del turn_data[override_key]
            else:
                turn_data[override_key] = True

            letter_data[adjustment_key_str] = turn_data
            self.special_placements[self.view.scene().state.grid_mode][ori_key][
                self.letter
            ] = letter_data
            self._update_json_entry(self.letter, letter_data)
            self.view.scene().managers.updater.update_pictograph()
            for (
                pictograph
            ) in (
                self.ge_pictograph.main_widget.pictograph_collector.collect_all_pictographs()
            ):
                if pictograph.state.letter == self.ge_pictograph.state.letter:
                    pictograph.managers.updater.update_pictograph()

        AppContext.special_placement_loader().reload()

    def _get_keys(self, beta_ori):
        adjustment_key_str = self._generate_adjustment_key_str(self.letter)
        ori_key = self.data_updater.ori_key_generator.generate_ori_key_from_motion(
            self.view.scene().elements.blue_motion
        )
        override_key = self._generate_override_key(beta_ori)
        return adjustment_key_str, ori_key, override_key

    def _is_mixed_ori(self) -> bool:
        return not (
            self.view.scene().managers.check.ends_with_nonradial_ori()
            or self.view.scene().managers.check.ends_with_radial_ori()
        )

    def _get_beta_ori(self):
        if self.view.scene().managers.check.ends_with_nonradial_ori():
            beta_ori = "nonradial"
        elif self.view.scene().managers.check.ends_with_radial_ori():
            beta_ori = "radial"
        return beta_ori

    def _generate_adjustment_key_str(self, letter) -> str:
        return self.turns_tuple_generator.generate_turns_tuple(self.view.scene())

    def _generate_override_key(self, beta_state) -> str:
        return (
            f"swap_beta_{self.view.scene().elements.blue_prop.state.loc}_{beta_state}_"
            f"blue_{self.view.scene().elements.blue_motion.state.motion_type}_{self.view.scene().elements.blue_arrow.state.loc}_"
            f"red_{self.view.scene().elements.red_motion.state.motion_type}_{self.view.scene().elements.red_arrow.state.loc}"
        )

    def _get_letter_data(self, ori_key, letter: Letter) -> dict:
        return (
            AppContext.special_placement_loader()
            .load_or_return_special_placements()[self.view.scene().state.grid_mode][
                ori_key
            ]
            .get(letter.value, {})
        )

    def _get_turn_data(self, letter_data, adjustment_key_str) -> dict:
        return letter_data.get(adjustment_key_str, {})

    def _update_json_entry(self, letter, letter_data) -> None:
        ori_key = self.data_updater.ori_key_generator.generate_ori_key_from_motion(
            self.view.scene().elements.blue_motion
        )
        self.data_updater.update_specific_entry_in_json(letter, letter_data, ori_key)

    def move_prop(self, prop: Prop, direction: str) -> None:
        offset_calculator = self.beta_offset_calculator
        offset = offset_calculator.calculate_new_position_with_offset(
            prop.pos(), direction
        )
        prop.setPos(offset)

    def _swap_props(
        self, prop_a: Prop, prop_b: Prop, direction_a: str, direction_b: str
    ) -> None:
        """Yes, this DOES have to be called twice for each prop to swap them. It's complicated."""
        self.move_prop(prop_a, direction_a)
        self.move_prop(prop_a, direction_a)
        self.move_prop(prop_b, direction_b)
        self.move_prop(prop_b, direction_b)
