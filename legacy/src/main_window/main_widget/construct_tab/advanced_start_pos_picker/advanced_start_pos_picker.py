from copy import deepcopy
from functools import partial
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from typing import Callable, List, TYPE_CHECKING
from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
from data.constants import BOX, DIAMOND, END_POS, GRID_MODE, LETTER, START_POS
from .advanced_start_pos_picker_pictograph_view import (
    AdvancedStartPosPickerPictographView,
)
from ..start_pos_picker.base_start_pos_picker import (
    BaseStartPosPicker,
)
from ..start_pos_picker.choose_your_start_pos_label import (
    ChooseYourStartPosLabel,
)

if TYPE_CHECKING:
    from ...sequence_workbench.legacy_beat_frame.legacy_beat_frame import (
        LegacyBeatFrame,
    )


class AdvancedStartPosPicker(BaseStartPosPicker):
    COLUMN_COUNT: int = 4

    def __init__(
        self,
        pictograph_dataset: dict,
        beat_frame: "LegacyBeatFrame",
        size_provider: Callable[[], int],
    ) -> None:
        super().__init__(pictograph_dataset, mw_size_provider=size_provider)
        self.beat_frame = beat_frame
        self.choose_start_pos_label = ChooseYourStartPosLabel(self)
        self.start_position_adder = beat_frame.start_position_adder
        self._init_layout()
        self.generate_pictographs()

    def _init_layout(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addStretch(1)

        label_layout = QHBoxLayout()
        label_layout.addWidget(self.choose_start_pos_label)
        self.main_layout.addLayout(label_layout, 1)
        self.main_layout.addStretch(1)

        self.grid_layout = QGridLayout()
        self.grid_layout.setHorizontalSpacing(20)
        self.grid_layout.setVerticalSpacing(20)
        self.main_layout.addLayout(self.grid_layout, 15)
        self.main_layout.addStretch(1)

        self.setLayout(self.main_layout)

    def create_pictograph_from_dict(
        self, pictograph_data: dict, target_grid_mode: str
    ) -> LegacyPictograph:
        key = self._generate_pictograph_key(pictograph_data, target_grid_mode)
        if key in self.start_options:
            return self.start_options[key]

        local_data = deepcopy(pictograph_data)
        local_data[GRID_MODE] = target_grid_mode

        pictograph = LegacyPictograph()
        pictograph.elements.view = AdvancedStartPosPickerPictographView(
            self, pictograph, size_provider=self.mw_size_provider
        )
        pictograph.managers.updater.update_pictograph(local_data)
        pictograph.elements.view.update_borders()

        self.start_options[key] = pictograph
        if target_grid_mode == BOX:
            self.box_pictographs.append(pictograph)
        elif target_grid_mode == DIAMOND:
            self.diamond_pictographs.append(pictograph)
        return pictograph

    def _generate_pictograph_key(self, data: dict, grid_mode: str) -> str:
        letter = data.get(LETTER, "unknown")
        start_pos = data.get(START_POS, "no_start")
        end_pos = data.get(END_POS, "no_end")
        return f"{letter}_{start_pos}_{end_pos}_{grid_mode}"

    def display_variations(self) -> None:
        while self.grid_layout.count():
            widget = self.grid_layout.takeAt(0).widget()
            if widget:
                widget.setParent(None)
        for group in self.all_variations.values():
            for index, pictograph in enumerate(group):
                row, col = divmod(index, self.COLUMN_COUNT)
                self.grid_layout.addWidget(pictograph.elements.view, row, col)

    def generate_pictographs(self) -> None:
        self.all_variations: dict[str, List[LegacyPictograph]] = {BOX: [], DIAMOND: []}
        for grid_mode in [BOX, DIAMOND]:
            pictographs = (
                self.get_box_pictographs()
                if grid_mode == BOX
                else self.get_diamond_pictographs()
            )
            pictographs.sort(
                key=lambda p: (p.state.start_pos[:-1], int(p.state.start_pos[-1]))
            )
            for pictograph in pictographs:
                self.all_variations[grid_mode].append(pictograph)
                view = pictograph.elements.view
                view.mousePressEvent = partial(self.on_variation_selected, pictograph)
                view.update_borders()

    def on_variation_selected(self, variation: LegacyPictograph, event=None) -> None:
        self.start_position_adder.add_start_pos_to_sequence(variation)
