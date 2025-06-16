from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import pyqtSignal
from typing import TYPE_CHECKING
from enums.letter.letter import Letter

from data.constants import (
    BLUE_ATTRS,
    BOX,
    DIAMOND,
    END_ORI,
    RED_ATTRS,
    START_ORI,
    START_POS,
    END_POS,
)
from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
from main_window.main_widget.pictograph_key_generator import PictographKeyGenerator
from main_window.main_widget.sequence_workbench.legacy_beat_frame.start_pos_beat import (
    StartPositionBeat,
)
from .start_pos_picker_variations_button import StartPosVariationsButton
from .start_pos_pictograph_frame import StartPosPickerPictographFrame
from .choose_your_start_pos_label import ChooseYourStartPosLabel
from .base_start_pos_picker import BaseStartPosPicker

if TYPE_CHECKING:
    from legacy.src.main_window.main_widget.sequence_workbench.legacy_beat_frame.legacy_beat_frame import (
        LegacyBeatFrame,
    )

# Define start position keys at the top
DIAMOND_START_POS_KEYS = ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]
BOX_START_POS_KEYS = ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"]


class StartPosPicker(BaseStartPosPicker):
    SPACING = 10
    start_position_selected = pyqtSignal(LegacyPictograph)
    COLUMN_COUNT = 3

    def __init__(
        self,
        pictograph_dataset: dict,
        beat_frame: "LegacyBeatFrame",
        mw_size_provider,
        advanced_transition_handler,
    ):
        super().__init__(pictograph_dataset, mw_size_provider=mw_size_provider)
        self.beat_frame = beat_frame  # ✅ Store the beat_frame
        self.advanced_transition_handler = advanced_transition_handler
        self.pictograph_frame = StartPosPickerPictographFrame(self)
        self.choose_your_start_pos_label = ChooseYourStartPosLabel(self)
        self.button_layout = self._setup_variations_button_layout()
        self.setup_layout()
        self.setStyleSheet("background-color: white;")
        self.initialized = False
        self.pictograph_dataset = pictograph_dataset
        self.display_variations()

    def setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.start_label_layout = QHBoxLayout()
        self.pictograph_layout = QHBoxLayout()

        self.start_label_layout.addWidget(self.choose_your_start_pos_label)
        self.pictograph_layout.addWidget(self.pictograph_frame)

        self.layout.addStretch(1)
        self.layout.addLayout(self.start_label_layout, 1)
        self.layout.addStretch(1)
        self.layout.addLayout(self.pictograph_layout, 5)
        self.layout.addStretch(1)
        self.layout.addLayout(self.button_layout, 5)
        self.layout.addStretch(1)

    def _setup_variations_button_layout(self) -> QHBoxLayout:
        self.variations_button = StartPosVariationsButton(self)
        self.variations_button.clicked.connect(self.advanced_transition_handler)
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.variations_button)
        button_layout.addStretch(1)
        return button_layout

    def display_variations(self) -> None:
        """Load only the start positions relevant to the current grid mode."""
        self.pictograph_frame.clear_pictographs()
        grid_mode = DIAMOND
        start_pos_keys = (
            DIAMOND_START_POS_KEYS if grid_mode == DIAMOND else BOX_START_POS_KEYS
        )
        if grid_mode == BOX:
            self.get_box_pictographs()
            for position_key in start_pos_keys:
                self._add_start_position_option_to_start_pos_frame(position_key, BOX)
        elif grid_mode == DIAMOND:
            self.get_diamond_pictographs()
            for position_key in start_pos_keys:
                self._add_start_position_option_to_start_pos_frame(
                    position_key, DIAMOND
                )

    def _add_start_position_option_to_start_pos_frame(
        self, position_key: str, grid_mode: str
    ) -> None:
        """Adds an option for the specified start position based on the current grid mode."""
        self.start_position_adder = self.beat_frame.start_position_adder
        start_pos, end_pos = position_key.split("_")
        for letter, pictograph_datas in self.pictograph_dataset.items():
            for pictograph_data in pictograph_datas:
                if (
                    pictograph_data[START_POS] == start_pos
                    and pictograph_data[END_POS] == end_pos
                ):
                    pictograph = self.create_pictograph_from_dict(
                        pictograph_data, grid_mode
                    )
                    pictograph.state.letter = letter
                    pictograph.state.start_pos = start_pos
                    pictograph.state.end_pos = end_pos
                    self.pictograph_frame._add_start_pos_to_layout(pictograph)

                    pictograph.elements.start_to_end_pos_glyph.hide()
                    break

    def convert_current_sequence_json_entry_to_start_pos_pictograph(
        self, start_pos_entry
    ) -> StartPositionBeat:
        start_position_pictograph = self.get_start_pos_pictograph(
            start_pos_entry[1] if start_pos_entry else None
        )
        start_pos_beat = StartPositionBeat(
            self.beat_frame,
        )
        start_pos_beat.managers.updater.update_pictograph(
            start_position_pictograph.state.pictograph_data
        )

        return start_pos_beat

    def get_start_pos_pictograph(self, start_pos_data) -> "LegacyPictograph":
        if not start_pos_data:
            raise ValueError("start_pos_data cannot be None")
        start_pos_key = start_pos_data[END_POS]
        letter_str = self.start_pos_key_to_letter(start_pos_key)
        letter = Letter(letter_str)
        matching_letter_pictographs = self.pictograph_dataset.get(letter, [])
        for pictograph_data in matching_letter_pictographs:
            if pictograph_data[START_POS] == start_pos_key:

                pictograph_data[BLUE_ATTRS][START_ORI] = start_pos_data[BLUE_ATTRS][
                    END_ORI
                ]
                pictograph_data[RED_ATTRS][START_ORI] = start_pos_data[RED_ATTRS][
                    END_ORI
                ]
                pictograph_factory = self.beat_frame.beat_factory
                pictograph_key = PictographKeyGenerator().generate_pictograph_key(
                    pictograph_data
                )
                start_pos_pictograph = pictograph_factory.create_start_pos_beat(
                    pictograph_key, pictograph_data
                )
                return start_pos_pictograph

        print(f"No matching start position found for key: {start_pos_key}")
        return None

    def start_pos_key_to_letter(self, start_pos_key: str) -> str:
        mapping = {"alpha": "α", "beta": "β", "gamma": "Γ"}
        for key in mapping:
            if start_pos_key.startswith(key):
                return mapping[key]
        return None
