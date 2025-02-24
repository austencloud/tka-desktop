from PyQt6.QtCore import QObject, pyqtSignal
from base_widgets.pictograph.base_pictograph import BasePictograph

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...advanced_start_pos_picker.advanced_start_pos_picker import (
        AdvancedStartPosPicker,
    )


class AdvancedStartPosManager(QObject):
    start_position_selected = pyqtSignal(BasePictograph)

    def __init__(self, advanced_start_pos_picker: "AdvancedStartPosPicker") -> None:
        super().__init__()
        self.sequence_builder = advanced_start_pos_picker.construct_tab
        self.advanced_start_pos_picker = advanced_start_pos_picker
        self.pictograph_frame = advanced_start_pos_picker.pictograph_frame
        self.start_pos_cache = advanced_start_pos_picker.start_pos_cache

    def set_all_orientations_to_in(self) -> None:
        for (
            start_position_pictograph_list
        ) in self.advanced_start_pos_picker.start_pos_cache.values():
            for start_position_pictograph in start_position_pictograph_list:
                start_position_pictograph.pictograph_dict["blue_attributes"][
                    "start_ori"
                ] = "in"
                start_position_pictograph.pictograph_dict["blue_attributes"][
                    "end_ori"
                ] = "in"
                start_position_pictograph.pictograph_dict["red_attributes"][
                    "start_ori"
                ] = "in"
                start_position_pictograph.pictograph_dict["red_attributes"][
                    "end_ori"
                ] = "in"
                start_position_pictograph.managers.updater.update_pictograph(
                    start_position_pictograph.pictograph_dict
                )

    def update_left_default_ori(self, left_ori: str):
        for (
            start_pos_pictographs_by_letter
        ) in self.advanced_start_pos_picker.start_pos_cache.values():
            for pictograph in start_pos_pictographs_by_letter:
                pictograph.pictograph_dict["blue_attributes"]["start_ori"] = left_ori
                pictograph.pictograph_dict["red_attributes"]["blue_ori"] = left_ori
                pictograph.managers.updater.update_pictograph(
                    pictograph.pictograph_dict
                )

    def update_right_default_ori(self, right_ori: str):
        for (
            start_pos_pictographs_by_letter
        ) in self.advanced_start_pos_picker.start_pos_cache.values():
            for pictograph in start_pos_pictographs_by_letter:
                pictograph.pictograph_dict["red_attributes"]["start_ori"] = right_ori
                pictograph.pictograph_dict["red_attributes"]["end_ori"] = right_ori
                pictograph.managers.updater.update_pictograph(
                    pictograph.pictograph_dict
                )
