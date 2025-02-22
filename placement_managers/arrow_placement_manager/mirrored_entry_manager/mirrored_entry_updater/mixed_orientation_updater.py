from Enums.letters import Letter

from data.constants import *
from .base_mirrored_entry_updater import BaseMirroredEntryUpdater


class MixedOrientationUpdater(BaseMirroredEntryUpdater):
    def update_entry(self, letter: Letter, original_turn_data: dict):
        mirrored_turns_tuple = (
            self.mirrored_entry_updater.turns_tuple_generator.generate_mirrored_tuple(
                self.arrow
            )
        )
        other_ori_key, other_letter_data = (
            self.mirrored_entry_updater._get_keys_for_mixed_start_ori(
                letter,
                self.mirrored_entry_updater.manager.data_updater._generate_ori_key(
                    self.arrow.motion
                ),
            )
        )
        layer = "1" if self.arrow.motion.state.start_ori in [IN, OUT] else "2"

        if letter.value in ["S", "T"]:
            attr = self.arrow.motion.state.lead_state
            key = f"{attr}_from_layer{layer}"
        elif self.arrow.pictograph.managers.check.has_hybrid_motions():
            attr = self.arrow.motion.state.motion_type
            key = f"{attr}_from_layer{layer}"
        else:
            key = f"{BLUE if self.arrow.color == RED else RED}"

        self.mirrored_entry_updater._update_mirrored_entry_data(
            mirrored_turns_tuple, other_letter_data, key, original_turn_data, self.arrow
        )
        self.mirrored_entry_updater.manager.data_updater.update_specific_entry_in_json(
            letter, other_letter_data, other_ori_key
        )
