from Enums.letters import LetterConditions, Letter

from data.constants import *
from main_window.settings_manager.global_settings.app_context import AppContext
from .base_mirrored_entry_updater import BaseMirroredEntryUpdater


class StandardOrientationUpdater(BaseMirroredEntryUpdater):
    def update_entry(self, letter: Letter, original_turn_data: dict):
        mirrored_turns_tuple = (
            self.mirrored_entry_updater.turns_tuple_generator.generate_mirrored_tuple(
                self.arrow
            )
        )
        self._mirror_entry(mirrored_turns_tuple, letter)

    def _mirror_entry(self, mirrored_turns_tuple, letter: Letter):
        if letter.value in ["S", "T", "β"] or letter in Letter.get_letters_by_condition(
            LetterConditions.HYBRID
        ):
            return
        ori_key = self.mirrored_entry_updater.manager.data_updater.ori_key_generator.generate_ori_key_from_motion(
            self.arrow.motion
        )

        letter_data = (
            AppContext.special_placement_loader()
            .load_special_placements_fresh()
            .get(
                ori_key,
                {},
            )
            .get(letter.value, {})
        )
        turns_tuple = (
            self.mirrored_entry_updater.turns_tuple_generator.generate_turns_tuple(
                self.arrow.pictograph
            )
        )

        self.mirrored_entry_updater.manager.data_updater.update_specific_entry_in_json(
            letter, letter_data, ori_key
        )
        if (
            not self.arrow.motion.state.turns
            == self.arrow.pictograph.managers.get.other_arrow(self.arrow).turns
            and self.arrow.motion.state.motion_type
            == self.arrow.pictograph.managers.get.other_arrow(
                self.arrow
            ).motion.state.motion_type
        ):
            if mirrored_turns_tuple not in letter_data:
                letter_data[mirrored_turns_tuple] = {}
            letter_data[mirrored_turns_tuple][
                BLUE if self.arrow.state.color == RED else RED
            ] = letter_data[turns_tuple][self.arrow.state.color]
            self.mirrored_entry_updater.manager.data_updater.update_specific_entry_in_json(
                letter, letter_data, ori_key
            )
        elif (
            not self.arrow.motion.state.turns
            == self.arrow.pictograph.managers.get.other_arrow(self.arrow).turns
            and self.arrow.motion.state.motion_type
            != self.arrow.pictograph.managers.get.other_arrow(
                self.arrow
            ).motion.state.motion_type
            and not self.arrow.pictograph.managers.check.has_one_float()
        ):
            if mirrored_turns_tuple not in letter_data:
                letter_data[mirrored_turns_tuple] = {}
            letter_data[mirrored_turns_tuple][self.arrow.motion.state.motion_type] = (
                letter_data[turns_tuple][self.arrow.motion.state.motion_type]
            )
            self.mirrored_entry_updater.manager.data_updater.update_specific_entry_in_json(
                letter, letter_data, ori_key
            )
        elif (
            not self.arrow.motion.state.turns
            == self.arrow.pictograph.managers.get.other_arrow(self.arrow).turns
            and self.arrow.motion.state.motion_type
            != self.arrow.pictograph.managers.get.other_arrow(
                self.arrow
            ).motion.state.motion_type
            and self.arrow.pictograph.managers.check.has_one_float()
        ):
            if mirrored_turns_tuple not in letter_data:
                letter_data[mirrored_turns_tuple] = {}
            letter_data[mirrored_turns_tuple][self.arrow.motion.state.motion_type] = (
                letter_data[turns_tuple][self.arrow.motion.state.motion_type]
            )
            self.mirrored_entry_updater.manager.data_updater.update_specific_entry_in_json(
                letter, letter_data, ori_key
            )

    def _determine_motion_attribute(self) -> str:
        letter = self.arrow.pictograph.state.letter
        if letter in ["S", "T"]:
            return self.arrow.motion.state.lead_state
        elif self.arrow.pictograph.managers.check.has_hybrid_motions():
            return self.arrow.motion.state.motion_type
        else:
            return self.arrow.state.color
