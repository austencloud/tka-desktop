from typing import TYPE_CHECKING
from Enums.letters import Letter
from main_window.main_widget.special_placement_loader import SpecialPlacementLoader
from main_window.settings_manager.global_settings.app_context import AppContext
from objects.arrow.arrow import Arrow

if TYPE_CHECKING:
    from base_widgets.pictograph.hotkey_graph_adjuster.special_placement_data_updater.special_placement_data_updater import (
        SpecialPlacementDataUpdater,
    )

    from .mirrored_entry_manager import MirroredEntryManager

    from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
        TurnsTupleGenerator,
    )


class MirroredEntryCreator:
    def __init__(self, mirrored_entry_manager: "MirroredEntryManager"):
        self.data_updater: "SpecialPlacementDataUpdater" = (
            mirrored_entry_manager.data_updater
        )
        self.turns_tuple_generator: TurnsTupleGenerator = (
            mirrored_entry_manager.turns_tuple_generator
        )

    def create_entry(self, letter: Letter, arrow: Arrow):
        ori_key = self.data_updater._generate_ori_key(arrow.motion)
        letter_data, _ = self._fetch_letter_data_and_original_turn_data(
            ori_key, letter, arrow
        )

        if arrow.pictograph.managers.check.starts_from_mixed_orientation():
            other_ori_key, other_letter_data = self._get_keys_for_mixed_start_ori(
                letter, ori_key
            )
            mirrored_turns_tuple = self.turns_tuple_generator.generate_mirrored_tuple(
                arrow
            )

            attr = self.data_updater.positioner.attr_key_generator.get_key(arrow)
            if mirrored_turns_tuple not in other_letter_data:
                other_letter_data[mirrored_turns_tuple] = {}
            if attr not in letter_data:
                letter_data[attr] = {}
            other_letter_data[mirrored_turns_tuple][attr] = letter_data[attr]

            self._initialize_dicts(mirrored_turns_tuple, other_letter_data, attr)
            self.data_updater.update_specific_entry_in_json(
                letter, other_letter_data, other_ori_key
            )

    def _initialize_dicts(self, mirrored_turns_tuple, other_letter_data, attr):
        if mirrored_turns_tuple not in other_letter_data:
            other_letter_data[mirrored_turns_tuple] = {}
        if attr not in other_letter_data[mirrored_turns_tuple]:
            other_letter_data[mirrored_turns_tuple][attr] = {}

    def _fetch_letter_data_and_original_turn_data(
        self, ori_key, letter: Letter, arrow: Arrow
    ) -> tuple[dict, dict]:
        letter_data = (
            AppContext.special_placement_loader()
            .load_or_return_special_placements()
            .get(arrow.pictograph.state.grid_mode, {})
            .get(ori_key, {})
            .get(letter.value, {})
        )

        letter_data: dict = letter_data
        original_turns_tuple = self.turns_tuple_generator.generate_turns_tuple(
            arrow.pictograph
        )
        return letter_data, letter_data.get(original_turns_tuple, {})

    def _get_keys_for_mixed_start_ori(
        self, letter: Letter, ori_key
    ) -> tuple[str, dict]:
        AppContext.special_placement_loader().reload()
        other_ori_key = self.data_updater.get_other_layer3_ori_key(ori_key)
        other_letter_data = (
            AppContext.special_placement_loader()
            .load_or_return_special_placements()
            .get(other_ori_key, {})
            .get(letter.value, {})
        )
        return other_ori_key, other_letter_data
