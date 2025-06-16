from typing import TYPE_CHECKING
from enums.letter.letter import Letter

from src.legacy_settings_manager.global_settings.app_context import AppContext
from objects.arrow.arrow import Arrow
from placement_managers.attr_key_generator import (
    AttrKeyGenerator,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.data_updater.special_placement_data_updater import (
        SpecialPlacementDataUpdater,
    )

    from .mirrored_entry_manager import MirroredEntryManager

    from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
        TurnsTupleGenerator,
    )


class MirroredEntryCreator:
    def __init__(self, mirrored_entry_manager: "MirroredEntryManager"):
        self.special_placement_data_updater: "SpecialPlacementDataUpdater" = (
            mirrored_entry_manager.data_updater
        )
        self.turns_tuple_generator: TurnsTupleGenerator = (
            mirrored_entry_manager.turns_tuple_generator
        )

    def create_entry(self, letter: Letter, arrow: Arrow):
        ori_key = self.special_placement_data_updater.ori_key_generator.generate_ori_key_from_motion(
            arrow.motion
        )
        letter_data, _ = self._fetch_letter_data_and_original_turn_data(
            ori_key, letter, arrow
        )
        turns_tuple = self.turns_tuple_generator.generate_turns_tuple(arrow.pictograph)
        if arrow.pictograph.managers.check.starts_from_mixed_orientation():
            other_ori_key, other_letter_data = self._get_keys_for_mixed_start_ori(
                letter, ori_key
            )

            mirrored_turns_tuple = self.turns_tuple_generator.generate_mirrored_tuple(
                arrow
            )

            attr_key = AttrKeyGenerator().get_key_from_arrow(arrow)

            if mirrored_turns_tuple not in other_letter_data:
                other_letter_data[mirrored_turns_tuple] = {}
            if attr_key not in letter_data:
                letter_data[attr_key] = {}

            other_letter_data[mirrored_turns_tuple][attr_key] = letter_data[
                turns_tuple
            ][attr_key]

            self._initialize_dicts(mirrored_turns_tuple, other_letter_data, attr_key)
            self.special_placement_data_updater.update_specific_entry_in_json(
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
        letter_data: dict = (
            AppContext.special_placement_loader()
            .load_special_placements_fresh()
            .get(self.special_placement_data_updater.getter.grid_mode(), {})
            .get(ori_key, {})
            .get(letter.value, {})
        )
        original_turns_tuple = self.turns_tuple_generator.generate_turns_tuple(
            arrow.pictograph
        )
        return letter_data, letter_data.get(original_turns_tuple, {})

    def _get_keys_for_mixed_start_ori(
        self, letter: Letter, ori_key
    ) -> tuple[str, dict]:
        AppContext.special_placement_loader().reload()
        other_ori_key = self.special_placement_data_updater.get_other_layer3_ori_key(
            ori_key
        )
        other_letter_data = (
            AppContext.special_placement_loader()
            .load_or_return_special_placements()
            .get(self.special_placement_data_updater.getter.grid_mode(), {})
            .get(other_ori_key, {})
            .get(letter.value, {})
        )
        return other_ori_key, other_letter_data
