from copy import deepcopy
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QWidget
from typing import Callable, Dict, List, TYPE_CHECKING

from base_widgets.pictograph.pictograph_scene import PictographScene
from data.constants import BOX, DIAMOND
from main_window.main_widget.construct_tab.advanced_start_pos_picker.advanced_start_pos_picker_pictograph_view import (
    AdvancedStartPosPickerPictographView,
)
from main_window.main_widget.construct_tab.start_pos_picker.base_start_pos_picker import (
    BaseStartPosPicker,
)
from main_window.main_widget.construct_tab.start_pos_picker.choose_your_start_pos_label import (
    ChooseYourStartPosLabel,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )


class AdvancedStartPosPicker(BaseStartPosPicker):
    """
    AdvancedStartPosPicker is responsible for generating and displaying pictograph
    variations for start positions in advanced mode. It manages caching and layout of
    pictograph scenes for different grid modes (BOX and DIAMOND) and provides a unified
    interface for the beat frame to add selected start positions to the sequence.
    """

    COLUMN_COUNT: int = 4

    def __init__(
        self,
        pictograph_dataset: Dict,
        beat_frame: "SequenceBeatFrame",
        size_provider: Callable[[], int],
    ) -> None:
        """
        :param pictograph_dataset: Dictionary with pictograph definitions.
        :param beat_frame: The SequenceBeatFrame that will use selected start positions.
        :param size_provider: A callable that returns a size (int) for scaling.
        """
        super().__init__(pictograph_dataset, mw_size_provider=size_provider)
        self.beat_frame = beat_frame
        self.choose_start_pos_label = ChooseYourStartPosLabel(self)
        self.start_pos_cache: Dict[str, List[PictographScene]] = {}
        # Inject the start position adder dependency from the beat frame
        self.start_position_adder = beat_frame.start_position_adder
        self._init_layout()
        self.generate_pictographs()

    def _init_layout(self) -> None:
        """Initializes the widget's layout."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addStretch(1)

        # Setup the label area
        label_layout = QHBoxLayout()
        label_layout.addWidget(self.choose_start_pos_label)
        self.main_layout.addLayout(label_layout, 1)
        self.main_layout.addStretch(1)

        # Setup the grid layout for pictograph variations
        self.grid_layout = QGridLayout()
        self.grid_layout.setHorizontalSpacing(20)
        self.grid_layout.setVerticalSpacing(20)
        self.main_layout.addLayout(self.grid_layout, 15)
        self.main_layout.addStretch(1)

        self.setLayout(self.main_layout)

    def create_pictograph_from_dict(
        self, pictograph_data: Dict, target_grid_mode: str
    ) -> PictographScene:
        """
        Creates (or retrieves from cache) a PictographScene based on the given data,
        with the specified grid mode.
        """
        key = self._generate_pictograph_key(pictograph_data, target_grid_mode)
        if key in self.pictograph_cache:
            return self.pictograph_cache[key]

        local_data = deepcopy(pictograph_data)
        local_data["grid_mode"] = target_grid_mode

        pictograph = PictographScene()
        # Use a specialized view for advanced start position selection
        pictograph.elements.view = AdvancedStartPosPickerPictographView(
            self, pictograph, size_provider=self.mw_size_provider
        )
        pictograph.managers.updater.update_pictograph(local_data)
        pictograph.elements.view.update_borders()

        self.pictograph_cache[key] = pictograph
        if target_grid_mode == BOX:
            self.box_pictographs.append(pictograph)
        elif target_grid_mode == DIAMOND:
            self.diamond_pictographs.append(pictograph)
        return pictograph

    def _generate_pictograph_key(self, data: Dict, grid_mode: str) -> str:
        """Generates a unique cache key based on letter, start, end, and grid mode."""
        letter = data.get("letter", "unknown")
        start_pos = data.get("start_pos", "no_start")
        end_pos = data.get("end_pos", "no_end")
        return f"{letter}_{start_pos}_{end_pos}_{grid_mode}"

    def display_variations(self) -> None:
        """Clears and repopulates the grid layout with pictograph variation views."""
        while self.grid_layout.count():
            widget = self.grid_layout.takeAt(0).widget()
            if widget:
                widget.setParent(None)
        for group in self.all_variations.values():
            for index, pictograph in enumerate(group):
                row, col = divmod(index, self.COLUMN_COUNT)
                self.grid_layout.addWidget(pictograph.elements.view, row, col)

    def generate_pictographs(self) -> None:
        """
        Generates pictograph variations for both grid modes, sorts them, and stores them in self.all_variations.
        Also attaches click handlers to allow selection.
        """
        self.all_variations = {BOX: [], DIAMOND: []}
        for grid_mode in [BOX, DIAMOND]:
            pictographs = (
                self.get_box_pictographs(advanced=True)
                if grid_mode == BOX
                else self.get_diamond_pictographs(advanced=True)
            )
            # Sort variations (for example, by start position)
            pictographs.sort(
                key=lambda p: (p.state.start_pos[:-1], int(p.state.start_pos[-1]))
            )
            for pictograph in pictographs:
                self.all_variations[grid_mode].append(pictograph)
                # Attach a click handler via lambda capturing the current pictograph
                view = pictograph.elements.view
                view.mousePressEvent = (
                    lambda event, v=pictograph: self.on_variation_selected(v)
                )
                view.update_borders()

    def on_variation_selected(self, variation: PictographScene) -> None:
        """Handles selection of a pictograph variation."""
        self.start_position_adder.add_start_pos_to_sequence(variation)
