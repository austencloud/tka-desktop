import os
from typing import TYPE_CHECKING
from enums.letter.letter import Letter

from data.constants import BLUE, RED
from main_window.main_widget.json_manager.special_placement_saver import (
    SpecialPlacementSaver,
)

from src.legacy_settings_manager.global_settings.app_context import AppContext
from objects.arrow.arrow import Arrow
from placement_managers.attr_key_generator import (
    AttrKeyGenerator,
)
if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.hotkey_graph_adjuster import (
        HotkeyGraphAdjuster,
    )
    from .special_placement_data_updater import SpecialPlacementDataUpdater




class SpecialPlacementEntryRemover:
    """Handles removal of special placement entries."""

    def __init__(
        self,
        hotkey_graph_adjuster: "HotkeyGraphAdjuster",
    ) -> None:
        self.turns_tuple_generator = hotkey_graph_adjuster.turns_tuple_generator
        self.special_placement_saver = SpecialPlacementSaver()
        self.special_placement_loader = AppContext.special_placement_loader()
        self.ge_view = hotkey_graph_adjuster.ge_view
        self.data_updater: "SpecialPlacementDataUpdater" = (
            self.ge_view.pictograph.managers.arrow_placement_manager.data_updater
        )

    def remove_special_placement_entry(self, letter: Letter, arrow: Arrow) -> None:
        ori_key = self.data_updater.ori_key_generator.generate_ori_key_from_motion(
            arrow.motion
        )
        file_path = self._generate_file_path(
            ori_key, letter, arrow.pictograph.state.grid_mode
        )

        if os.path.exists(file_path):
            data = self.load_data(file_path)
            self._process_removal(letter, arrow, ori_key, file_path, data)
            AppContext.special_placement_loader().reload()
        arrow.pictograph.managers.updater.placement_updater.update()
        for (
            pictograph
        ) in self.ge_view.main_widget.pictograph_collector.collect_all_pictographs():
            if pictograph.state.letter == letter:
                pictograph.managers.updater.update_pictograph()
                pictograph.managers.arrow_placement_manager.update_arrow_placements()

    def _process_removal(
        self, letter: Letter, arrow: Arrow, ori_key: str, file_path: str, data: dict
    ):
        self.turns_tuple = self.turns_tuple_generator.generate_turns_tuple(
            self.data_updater.placement_manager.pictograph
        )
        if letter.value in data:
            letter_data = data[letter.value]

            key = AttrKeyGenerator().get_key_from_arrow(arrow)
            self._remove_turn_data_entry(letter_data, self.turns_tuple, key)

            if arrow.pictograph.managers.check.starts_from_mixed_orientation():
                self._handle_mixed_start_ori_mirrored_entry_removal(
                    letter, arrow, ori_key, letter_data, key
                )
            elif arrow.pictograph.managers.check.starts_from_standard_orientation():
                self._handle_standard_start_ori_mirrored_entry_removal(
                    letter, arrow, letter_data, key
                )

            data[letter.value] = letter_data
            AppContext.special_placement_saver().save_json_data(data, file_path)

    def _handle_standard_start_ori_mirrored_entry_removal(
        self, letter, arrow: Arrow, letter_data: dict, key
    ):
        if (
            arrow.motion.state.turns
            == arrow.pictograph.managers.get.other_arrow(arrow).motion.state.turns
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
        self, letter: Letter, arrow: "Arrow", ori_key, letter_data, key
    ):

        other_ori_key = self.data_updater.get_other_layer3_ori_key(ori_key)

        other_file_path = self._generate_file_path(
            other_ori_key, letter, arrow.pictograph.state.grid_mode
        )
        other_data = self.special_placement_loader.load_json_data(other_file_path)
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
            self.special_placement_saver.save_json_data(other_data, other_file_path)
        new_turns_tuple = self.turns_tuple_generator.generate_mirrored_tuple(arrow)
        self._remove_turn_data_entry(other_letter_data, new_turns_tuple, new_key)

    def load_data(self, file_path):  # -> Any:
        return self.special_placement_loader.load_json_data(file_path)

    def _generate_file_path(self, ori_key: str, letter: Letter, grid_mode: str) -> str:
        file_path = os.path.join(
            "src",
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
