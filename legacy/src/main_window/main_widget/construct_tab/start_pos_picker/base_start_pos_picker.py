from typing import TYPE_CHECKING, Callable
from PyQt6.QtWidgets import QWidget
from copy import deepcopy
from base_widgets.pictograph.elements.views.start_pos_picker_pictograph_view import (
    StartPosPickerPictographView,
)
from data.positions_maps import box_positions, diamond_positions
from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
from data.constants import BOX, DIAMOND, END_POS, GRID_MODE, LETTER, START_POS
from PyQt6.QtCore import QSize


class BaseStartPosPicker(QWidget):
    def __init__(
        self, pictograph_dataset: dict, mw_size_provider: Callable[[], QSize]
    ) -> None:
        super().__init__()
        self.pictograph_dataset = pictograph_dataset
        self.mw_size_provider = mw_size_provider
        self.box_pictographs: list[LegacyPictograph] = []
        self.diamond_pictographs: list[LegacyPictograph] = []
        self.start_options: dict[str, LegacyPictograph] = {}

    def create_pictograph_from_dict(
        self, pictograph_data: dict, target_grid_mode: str
    ) -> LegacyPictograph:
        """
        Create a pictograph using the provided dictionary, setting a local grid_mode.
        No context managers, no flipping global states.
        """
        local_dict = deepcopy(pictograph_data)
        local_dict[GRID_MODE] = target_grid_mode

        pictograph_key = self.generate_pictograph_key(local_dict, target_grid_mode)
        if pictograph_key in self.start_options:
            return self.start_options[pictograph_key]

        pictograph = LegacyPictograph()
        pictograph.elements.view = StartPosPickerPictographView(
            self, pictograph, size_provider=self.mw_size_provider
        )
        pictograph.managers.updater.update_pictograph(local_dict)
        pictograph.elements.view.update_borders()
        self.start_options[pictograph_key] = pictograph

        if target_grid_mode == BOX:
            self.box_pictographs.append(pictograph)
        elif target_grid_mode == DIAMOND:
            self.diamond_pictographs.append(pictograph)
        return pictograph

    def generate_pictograph_key(self, pictograph_data: dict, grid_mode: str) -> str:
        letter = pictograph_data.get(LETTER, "unknown")
        start_pos = pictograph_data.get(START_POS, "no_start")
        end_pos = pictograph_data.get(END_POS, "no_end")
        return f"{letter}_{start_pos}_{end_pos}_{grid_mode}"

    def get_box_pictographs(self) -> list[LegacyPictograph]:
        if self.box_pictographs:
            return self.box_pictographs

        for letter, p_dicts in self.pictograph_dataset.items():
            for p_dict in p_dicts:
                if p_dict[START_POS] == p_dict[END_POS]:
                    if p_dict[START_POS] in box_positions:
                        self.create_pictograph_from_dict(p_dict, BOX)

        return self.box_pictographs

    def get_diamond_pictographs(self) -> list[LegacyPictograph]:
        if self.diamond_pictographs:
            return self.diamond_pictographs

        for letter, p_dicts in self.pictograph_dataset.items():
            for p_dict in p_dicts:
                if p_dict[START_POS] == p_dict[END_POS]:
                    if p_dict[START_POS] in diamond_positions:
                        self.create_pictograph_from_dict(p_dict, DIAMOND)

        return self.diamond_pictographs
