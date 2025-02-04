from Enums.letters import Letter
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .mirrored_entry_manager import MirroredEntryManager


class MirroredEntryDataPrep:
    def __init__(self, manager: "MirroredEntryManager"):
        self.manager = manager

    def is_new_entry_needed(self, arrow: Arrow) -> bool:
        """Determines if a new mirrored entry is needed for the given arrow."""
        ori_key = self._get_ori_key(arrow.motion)
        return (
            arrow.pictograph.letter
            not in self.manager.data_updater.positioner.placement_manager.pictograph.main_widget.special_placements.get(
                ori_key, {}
            )
        )

    def _get_ori_key(self, motion):
        """Fetches the orientation key based on the motion's properties."""
        return self.manager.data_updater._generate_ori_key(motion)

    def get_keys_for_mixed_start_ori(self, letter, ori_key) -> tuple[str, dict]:
        """Fetches keys and data for mixed start orientation cases."""
        if (
            self.manager.data_updater.positioner.pictograph.check.starts_from_mixed_orientation()
        ):
            other_ori_key = self.manager.data_updater.get_other_layer3_ori_key(ori_key)
            other_letter_data = self._get_letter_data(other_ori_key, letter)
            return other_ori_key, other_letter_data
        return ori_key, self._get_letter_data(ori_key, letter)

    def _get_letter_data(self, ori_key: str, letter: Letter) -> dict:
        """Fetches letter data for a given orientation key and letter."""
        return self.manager.data_updater.positioner.placement_manager.pictograph.main_widget.special_placements.get(
            ori_key, {}
        ).get(
            letter.value, {}
        )

    def _fetch_letter_data_and_original_turn_data(
        self, ori_key: str, letter: Letter, arrow: Arrow
    ) -> tuple[dict, dict]:
        """Fetches letter data and the original turns tuple for the given arrow."""
        letter_data = self._get_letter_data(ori_key, letter)
        original_turns_tuple = self.manager.turns_tuple_generator.generate_turns_tuple(
            arrow.pictograph
        )
        original_turn_data = letter_data.get(original_turns_tuple, {})
        return letter_data, original_turn_data
