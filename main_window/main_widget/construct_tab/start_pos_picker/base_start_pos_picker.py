from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
from copy import deepcopy
from data.positions import box_positions, diamond_positions
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from data.constants import BOX, DIAMOND
from .start_pos_picker_pictograph_view import StartPosPickerPictographView

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.construct_tab import ConstructTab


class BaseStartPosPicker(QWidget):
    def __init__(self, construct_tab: "ConstructTab"):
        super().__init__(construct_tab)
        self.construct_tab = construct_tab
        self.main_widget = construct_tab.main_widget

        self.pictograph_cache: dict[str, BasePictograph] = {}
        self.box_pictographs: list[BasePictograph] = []
        self.diamond_pictographs: list[BasePictograph] = []

    def create_pictograph_from_dict(
        self, pictograph_dict: dict, target_grid_mode: str, advanced: bool = False
    ) -> BasePictograph:
        """
        Create a pictograph using the provided dictionary, setting a local grid_mode.
        No context managers, no flipping global states.
        """
        local_dict = deepcopy(pictograph_dict)
        local_dict["grid_mode"] = target_grid_mode

        pictograph_key = self.generate_pictograph_key(local_dict, target_grid_mode)
        if pictograph_key in self.pictograph_cache:
            return self.pictograph_cache[pictograph_key]

        pictograph = BasePictograph(self.main_widget)
        pictograph.view = StartPosPickerPictographView(self, pictograph)
        pictograph.updater.update_pictograph(local_dict)
        pictograph.view.update_borders()
        self.pictograph_cache[pictograph_key] = pictograph

        if target_grid_mode == BOX:
            self.box_pictographs.append(pictograph)
        elif target_grid_mode == DIAMOND:
            self.diamond_pictographs.append(pictograph)

        return pictograph

    def generate_pictograph_key(self, pictograph_dict: dict, grid_mode: str) -> str:
        letter = pictograph_dict.get("letter", "unknown")
        start_pos = pictograph_dict.get("start_pos", "no_start")
        end_pos = pictograph_dict.get("end_pos", "no_end")
        return f"{letter}_{start_pos}_{end_pos}_{grid_mode}"

    def get_box_pictographs(self, advanced: bool = False) -> list[BasePictograph]:
        if self.box_pictographs:
            return self.box_pictographs

        for letter, p_dicts in self.main_widget.pictograph_dicts.items():
            for p_dict in p_dicts:
                if p_dict["start_pos"] == p_dict["end_pos"]:
                    if p_dict["start_pos"] in box_positions:
                        self.create_pictograph_from_dict(p_dict, BOX)

        return self.box_pictographs

    def get_diamond_pictographs(self, advanced: bool = False) -> list[BasePictograph]:
        if self.diamond_pictographs:
            return self.diamond_pictographs

        for letter, p_dicts in self.main_widget.pictograph_dicts.items():
            for p_dict in p_dicts:
                if p_dict["start_pos"] == p_dict["end_pos"]:
                    if p_dict["start_pos"] in diamond_positions:
                        self.create_pictograph_from_dict(p_dict, DIAMOND)

        return self.diamond_pictographs
