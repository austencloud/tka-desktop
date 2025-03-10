from typing import TYPE_CHECKING

from enums.letter.letter import Letter
from settings_manager.global_settings.app_context import AppContext
from objects.prop.prop import Prop
from placement_managers.prop_placement_manager.handlers.beta_offset_calculator import (
    BetaOffsetCalculator,
)


if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.pictograph_container.GE_pictograph_container import (
        GE_Pictograph,
    )
    from .hotkey_graph_adjuster import HotkeyGraphAdjuster


class PropPlacementOverrideManager:
    def __init__(self, hotkey_adjuster: "HotkeyGraphAdjuster") -> None:
        self.ge_view = hotkey_adjuster.ge_view
        self.graph_editor = hotkey_adjuster.graph_editor
        self.state = self.graph_editor.state  # Reference to centralized state

        # Get current pictograph from state or view
        pictograph = self.ge_view.pictograph
        self.data_updater = pictograph.managers.arrow_placement_manager.data_updater
        self.turns_tuple_generator = hotkey_adjuster.turns_tuple_generator
        self.beta_offset_calculator = BetaOffsetCalculator(self)

    def handle_prop_placement_override(self) -> None:
        # Use the pictograph directly from the view's scene
        self.ge_pictograph: "GE_Pictograph" = self.ge_view.pictograph
        self.special_placements = (
            AppContext.special_placement_loader().load_or_return_special_placements()
        )

        if self._is_mixed_ori():
            return

        beta_ori = self._get_beta_ori()

        # Use letter from centralized state if available
        self.letter = self.state.get_letter() or self.ge_pictograph.state.letter

        if self.ge_view.pictograph.managers.check.ends_with_beta():
            adjustment_key_str, ori_key, override_key = self._get_keys(beta_ori)
            letter_data = self._get_letter_data(ori_key, self.letter)
            turn_data = self._get_turn_data(letter_data, adjustment_key_str)

            if override_key in turn_data:
                del turn_data[override_key]
            else:
                turn_data[override_key] = True

            letter_data[adjustment_key_str] = turn_data
            self.special_placements[self.ge_view.pictograph.state.grid_mode][ori_key][
                self.letter
            ] = letter_data
            self._update_json_entry(self.letter, letter_data)

            # Update pictograph and state simultaneously
            self.ge_view.pictograph.managers.updater.update_pictograph()
            self.state.sync_from_pictograph(self.ge_view.pictograph)

            # Update all pictographs with the same letter
            for (
                pictograph
            ) in (
                self.ge_pictograph.main_widget.pictograph_collector.collect_all_pictographs()
            ):
                if pictograph.state.letter == self.letter:
                    pictograph.managers.updater.update_pictograph()

        AppContext.special_placement_loader().reload()

    def _get_keys(self, beta_ori):
        adjustment_key_str = self._generate_adjustment_key_str(self.letter)
        ori_key = self.data_updater.ori_key_generator.generate_ori_key_from_motion(
            self.ge_view.pictograph.elements.blue_motion
        )
        override_key = self._generate_override_key(beta_ori)
        return adjustment_key_str, ori_key, override_key

    def _is_mixed_ori(self) -> bool:
        return not (
            self.ge_view.pictograph.managers.check.ends_with_nonradial_ori()
            or self.ge_view.pictograph.managers.check.ends_with_radial_ori()
        )

    def _get_beta_ori(self):
        if self.ge_view.pictograph.managers.check.ends_with_nonradial_ori():
            beta_ori = "nonradial"
        elif self.ge_view.pictograph.managers.check.ends_with_radial_ori():
            beta_ori = "radial"
        return beta_ori

    def _generate_adjustment_key_str(self, letter) -> str:
        return self.turns_tuple_generator.generate_turns_tuple(self.ge_view.pictograph)

    def _generate_override_key(self, beta_state) -> str:
        return (
            f"swap_beta_{self.ge_view.pictograph.elements.blue_prop.loc}_{beta_state}_"
            f"blue_{self.ge_view.pictograph.elements.blue_motion.state.motion_type}_{self.ge_view.pictograph.elements.blue_arrow.state.loc}_"
            f"red_{self.ge_view.pictograph.elements.red_motion.state.motion_type}_{self.ge_view.pictograph.elements.red_arrow.state.loc}"
        )

    def _get_letter_data(self, ori_key, letter: Letter) -> dict:
        return (
            AppContext.special_placement_loader()
            .load_or_return_special_placements()[
                self.ge_view.pictograph.state.grid_mode
            ][ori_key]
            .get(letter.value, {})
        )

    def _get_turn_data(self, letter_data, adjustment_key_str) -> dict:
        return letter_data.get(adjustment_key_str, {})

    def _update_json_entry(self, letter, letter_data) -> None:
        ori_key = self.data_updater.ori_key_generator.generate_ori_key_from_motion(
            self.ge_view.pictograph.elements.blue_motion
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
