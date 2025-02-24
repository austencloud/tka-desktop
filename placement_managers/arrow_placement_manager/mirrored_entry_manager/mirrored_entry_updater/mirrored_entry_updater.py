from Enums.letters import Letter
from .base_mirrored_entry_updater import BaseMirroredEntryUpdater
from .mixed_orientation_updater import MixedOrientationUpdater
from .standard_orientation_updater import StandardOrientationUpdater
from data.constants import *
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from ..mirrored_entry_manager import MirroredEntryManager


class MirroredEntryUpdater:
    def __init__(
        self,
        special_placement_mirrored_entry_manager: "MirroredEntryManager",
    ):
        self.manager = special_placement_mirrored_entry_manager
        self.data_updater = self.manager.data_updater
        self.turns_tuple_generator = self.manager.turns_tuple_generator

    def _get_mirrored_entry_updater(self, arrow: Arrow) -> BaseMirroredEntryUpdater:
        if arrow.pictograph.managers.check.starts_from_mixed_orientation():
            return MixedOrientationUpdater(self, arrow)
        else:
            return StandardOrientationUpdater(self, arrow)

    def update_entry(self, arrow: Arrow):
        ori_key = self.manager.data_updater._generate_ori_key(arrow.motion)
        letter = arrow.pictograph.state.letter
        letter_data, original_turn_data = (
            self.manager.data_prep._fetch_letter_data_and_original_turn_data(
                ori_key, letter, arrow
            )
        )

        mirrored_entry_updater = self._get_mirrored_entry_updater(arrow)
        mirrored_entry_updater.update_entry(letter, original_turn_data)
        QApplication.processEvents()
        self.manager.data_updater.update_specific_entry_in_json(
            letter, letter_data, ori_key
        )

    def _update_mirrored_entry_data(
        self, mirrored_turns_tuple, other_letter_data, key, original_turn_data, arrow
    ):
        if mirrored_turns_tuple not in other_letter_data:
            other_letter_data[mirrored_turns_tuple] = {}
        if key not in other_letter_data[mirrored_turns_tuple]:
            other_letter_data[mirrored_turns_tuple][key] = {}

        data_key = self._determine_data_key(arrow, key)
        other_letter_data[mirrored_turns_tuple][key] = original_turn_data.get(data_key)

    def _determine_data_key(self, arrow: Arrow, key: str) -> str:
        if arrow.pictograph.managers.check.starts_from_mixed_orientation():
            if arrow.pictograph.state.letter in ["S", "T"]:
                return f"{arrow.motion.state.lead_state}_from_layer{self._determine_layer(arrow)}"
            elif arrow.pictograph.managers.check.has_hybrid_motions():
                return f"{arrow.motion.state.motion_type}_from_layer{self._determine_layer(arrow)}"
            else:
                return f"{arrow.state.color}"
        else:
            return key

    def _determine_layer(self, arrow: Arrow) -> str:
        return "1" if arrow.motion.state.start_ori in [IN, OUT] else "2"

    def _generate_turns_tuple(self, arrow: Arrow) -> str:
        return self.turns_tuple_generator.generate_turns_tuple(arrow.pictograph)

    def _get_letter_data(self, ori_key: str, letter: Letter) -> dict:
        return self.data_updater.positioner.placement_manager.pictograph.main_widget.special_placements.get(
            ori_key, {}
        ).get(
            letter.value, {}
        )

    def _get_keys_for_mixed_start_ori(
        self, letter: Letter, ori_key
    ) -> tuple[str, dict]:
        other_ori_key = self.data_updater.get_other_layer3_ori_key(ori_key)
        other_letter_data = self._get_letter_data(other_ori_key, letter)
        return other_ori_key, other_letter_data
