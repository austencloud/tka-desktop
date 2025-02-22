import os
from typing import TYPE_CHECKING
from Enums.letters import Letter
from data.constants import BLUE, RED
from main_window.main_widget.json_manager.json_special_placement_handler import (
    JsonSpecialPlacementHandler,
)
from main_window.main_widget.special_placement_loader import SpecialPlacementLoader
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)
from main_window.settings_manager.global_settings.app_context import AppContext
from objects.arrow.arrow import Arrow

if TYPE_CHECKING:
    from .special_placement_data_updater import SpecialPlacementDataUpdater


class SpecialPlacementEntryRemover:
    """Handles removal of special placement entries."""

    def __init__(
        self,
        data_updater: "SpecialPlacementDataUpdater",
    ) -> None:
        self.positioner = data_updater.positioner
        self.data_updater = data_updater
        self.turns_tuple_generator = data_updater.turns_tuple_generator
        self.special_placement_handler = JsonSpecialPlacementHandler()

    def remove_special_placement_entry(self, letter: Letter, arrow: Arrow) -> None:
        ori_key = self.data_updater._generate_ori_key(arrow.motion)
        file_path = self._generate_file_path(ori_key, letter)

        if os.path.exists(file_path):
            data = self.load_data(file_path)
            self._process_removal(letter, arrow, ori_key, file_path, data)
            SpecialPlacementLoader().load_special_placements()
        arrow.pictograph.managers.updater.placement_updater.update()

    def _process_removal(
        self, letter: Letter, arrow: Arrow, ori_key: str, file_path: str, data: dict
    ):
        self.turns_tuple = self.turns_tuple_generator.generate_turns_tuple(
            self.positioner.placement_manager.pictograph
        )
        if letter.value in data:
            letter_data = data[letter.value]

            key = self.data_updater.positioner.attr_key_generator.get_key(arrow)
            self._remove_turn_data_entry(letter_data, self.turns_tuple, key)

            if arrow.pictograph.managers.check.starts_from_mixed_orientation():
                self._handle_mixed_start_ori_mirrored_entry_removal(
                    letter, arrow, ori_key, letter_data, key
                )
            elif arrow.pictograph.managers.check.starts_from_standard_orientation():
                self._handle_standard_start_ori_mirrored_entry_removal(
                    letter, arrow, ori_key, letter_data, key
                )
            data[letter.value] = letter_data
            AppContext.special_placement_handler().write_json_data(data, file_path)

    def _handle_standard_start_ori_mirrored_entry_removal(
        self, letter, arrow: Arrow, ori_key, letter_data, key
    ):
        if (
            arrow.motion.state.turns
            == arrow.pictograph.managers.get.other_arrow(arrow).turns
            or arrow.motion.state.motion_type
            != arrow.pictograph.managers.get.other_arrow(arrow).motion.state.motion_type
            or letter in ["S", "T"]
        ):
            return

        mirrored_tuple = self.turns_tuple_generator.generate_mirrored_tuple(arrow)

        if key == BLUE:
            new_key = RED
        elif key == RED:
            new_key = BLUE
        else:
            new_key = key

        if letter_data.get(mirrored_tuple, {}).get(new_key, {}):
            del letter_data[mirrored_tuple][new_key]
            if not letter_data[mirrored_tuple]:
                del letter_data[mirrored_tuple]

    def _handle_mixed_start_ori_mirrored_entry_removal(
        self, letter: Letter, arrow, ori_key, letter_data, key
    ):

        other_ori_key = self.data_updater.get_other_layer3_ori_key(ori_key)
        other_file_path = self._generate_file_path(other_ori_key, letter)
        other_data = self.special_placement_handler.load_json_data(other_file_path)
        other_letter_data = other_data.get(letter, {})
        mirrored_tuple = self.turns_tuple_generator.generate_mirrored_tuple(arrow)
        if key == BLUE:
            new_key = RED
        elif key == RED:
            new_key = BLUE
        else:
            new_key = key
        if other_letter_data != letter_data:
            if mirrored_tuple not in other_letter_data:
                other_letter_data[mirrored_tuple] = {}
            if new_key not in other_letter_data[mirrored_tuple]:
                if self.turns_tuple in letter_data:
                    if key not in letter_data[self.turns_tuple]:
                        letter_data[self.turns_tuple][key] = {}
                    other_letter_data[mirrored_tuple][new_key] = letter_data[
                        self.turns_tuple
                    ][key]
            if other_data:
                if other_data[letter.value].get(mirrored_tuple, {}):
                    if other_data[letter.value].get(mirrored_tuple, {}).get(new_key):
                        del other_data[letter.value][mirrored_tuple][new_key]

            elif key not in letter_data[self.turns_tuple]:
                if other_data:
                    del other_data[letter][mirrored_tuple][new_key]
            self.special_placement_handler.write_json_data(other_data, other_file_path)
        new_turns_tuple = self.turns_tuple_generator.generate_mirrored_tuple(arrow)
        self._remove_turn_data_entry(other_letter_data, new_turns_tuple, new_key)

    def load_data(self, file_path):
        return self.special_placement_handler.load_json_data(file_path)

    def _generate_file_path(self, ori_key: str, letter: Letter) -> str:
        grid_mode = self.positioner.placement_manager.pictograph.state.grid_mode
        file_path = os.path.join(
            "data",
            "arrow_placement",
            grid_mode,
            "special",
            ori_key,
            f"{letter.value}_placements.json",
        )

        return file_path

    def _get_other_color(self, color: str) -> str:
        return RED if color == BLUE else BLUE

    def _remove_turn_data_entry(self, letter_data: dict, turns_tuple: str, key) -> None:
        turn_data = letter_data.get(turns_tuple, {})
        if key in turn_data:
            del turn_data[key]
            if not turn_data:
                del letter_data[turns_tuple]
