from copy import deepcopy
from functools import partial
from PyQt6.QtCore import QObject, pyqtSignal
from Enums.letters import Letter
from data.constants import BOX, DIAMOND, END_POS, START_POS
from base_widgets.base_pictograph.pictograph import Pictograph
from data.position_maps import box_positions, diamond_positions

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

from main_window.main_widget.sequence_workbench.beat_frame.start_pos_beat import (
    StartPositionBeat,
)

if TYPE_CHECKING:
    from .start_pos_picker import StartPosPicker


class StartPosManager(QObject):
    """
    Manages creation and display of start-position pictographs for
    both box and diamond modes, without relying on a global grid mode
    or a temporary context manager.
    """

    start_position_selected = pyqtSignal(Pictograph)

    def __init__(self, start_pos_picker: "StartPosPicker") -> None:
        super().__init__()
        self.start_pos_picker = start_pos_picker
        self.construct_tab = start_pos_picker.construct_tab
        self.main_widget = self.construct_tab.main_widget
        self.start_pos_frame = start_pos_picker.pictograph_frame

        self.top_builder_widget = None

        # Track pictographs we create for box/diamond
        self.box_pictographs: list[Pictograph] = []
        self.diamond_pictographs: list[Pictograph] = []

        # Map letter -> pictograph (or however you prefer to store them)
        self.start_options: dict[str, Pictograph] = {}

        # When user picks a start position, proceed
        self.start_position_selected.connect(
            self.construct_tab.transition_to_option_picker
        )

        # Load whichever mode we want to show initially
        # e.g., if the user can pick, or we have a default approach:
        self.load_relevant_start_positions()

    def get_all_start_positions(self) -> list[Pictograph]:
        """
        Returns both box + diamond pictographs (or whichever ones
        are relevant if you only loaded one mode).
        """
        return self.box_pictographs + self.diamond_pictographs

    def clear_start_positions(self) -> None:
        """Hide all start-position pictographs and clear them from the frame."""
        for start_position_pictograph in self.start_options.values():
            start_position_pictograph.view.hide()

    def load_relevant_start_positions(self, grid_mode: str = None) -> None:
        """
        Load only the start positions relevant to a chosen grid mode,
        or keep both if you want both available.
        Replaces the old logic that used a global grid_mode call.
        """
        # If you still want to read from global settings as a fallback:
        if not grid_mode:
            # fallback: read from global or pick a default
            grid_mode = DIAMOND

        # Example approach: we only load either BOX or DIAMOND at once.
        if grid_mode == BOX:
            self.box_pictographs = self.get_box_variations()
            for position_key in ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"]:
                self._add_start_position_option_to_start_pos_frame(position_key, BOX)
        elif grid_mode == DIAMOND:
            self.diamond_pictographs = self.get_diamond_variations()
            for position_key in ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]:
                self._add_start_position_option_to_start_pos_frame(
                    position_key, DIAMOND
                )

    def get_box_variations(self) -> list[Pictograph]:
        """Retrieve box mode variations (without using a global or context manager)."""
        box_variations = []
        for letter, pictograph_datas in self.main_widget.pictograph_dataset.items():
            for pictograph_data in pictograph_datas:
                # Only create if it’s in box_positions
                if pictograph_data["start_pos"] in box_positions:
                    # We supply 'BOX' as the local grid mode
                    pictograph = self.create_pictograph_from_dict(pictograph_data, BOX)
                    box_variations.append(pictograph)

        return box_variations

    def get_diamond_variations(self) -> list[Pictograph]:
        """Retrieve diamond mode variations."""
        diamond_variations = []
        for letter, pictograph_datas in self.main_widget.pictograph_dataset.items():
            for pictograph_data in pictograph_datas:
                if pictograph_data["start_pos"] in diamond_positions:
                    pictograph = self.create_pictograph_from_dict(
                        pictograph_data, DIAMOND
                    )
                    diamond_variations.append(pictograph)

        return diamond_variations

    def _add_start_position_option_to_start_pos_frame(
        self, position_key: str, grid_mode: str
    ) -> None:
        """
        Adds an option for the specified start position under the chosen grid mode.
        e.g., position_key = "alpha1_alpha1".
        """
        start_pos, end_pos = position_key.split("_")

        for letter, pictograph_datas in self.main_widget.pictograph_dataset.items():
            for pictograph_data in pictograph_datas:
                if (
                    pictograph_data[START_POS] == start_pos
                    and pictograph_data[END_POS] == end_pos
                ):
                    pictograph = self.create_pictograph_from_dict(
                        pictograph_data, grid_mode
                    )
                    self.start_options[letter] = pictograph

                    pictograph.letter = letter
                    pictograph.start_pos = start_pos
                    pictograph.end_pos = end_pos
                    # Add to layout
                    self.start_pos_frame._add_start_pos_to_layout(pictograph)

                    # On mousePressEvent, user picks this start position
                    pictograph.view.mousePressEvent = partial(
                        self.add_start_pos_to_sequence, pictograph
                    )

                    pictograph.start_to_end_pos_glyph.hide()

    def add_start_pos_to_sequence(
        self, clicked_start_option: Pictograph, event: QWidget = None
    ) -> None:
        """Handle user clicking a start position pictograph."""
        seq_widget = self.main_widget.sequence_workbench
        start_position_beat = StartPositionBeat(seq_widget.beat_frame)

        clicked_start_option.updater.update_dict_from_attributes()

        # Copy and set the data to the start_position_beat
        start_position_beat.updater.update_pictograph(
            deepcopy(clicked_start_option.pictograph_data)
        )

        seq_widget.beat_frame.start_pos_view.set_start_pos(start_position_beat)
        self.construct_tab.last_beat = start_position_beat

        # For selection
        beat_frame = seq_widget.beat_frame
        start_pos_view = beat_frame.start_pos_view
        beat_frame.selection_overlay.select_beat(start_pos_view)

        # If you store data in a JSON manager:
        self.main_widget.json_manager.start_pos_handler.set_start_position_data(
            start_position_beat
        )
        self.start_position_selected.emit(start_position_beat)

    def hide_start_positions(self) -> None:
        """Hides the start position pictographs."""
        for start_position_pictograph in self.start_options.values():
            start_position_pictograph.view.hide()

    def convert_current_sequence_json_entry_to_start_pos_pictograph(
        self, start_pos_entry
    ) -> StartPositionBeat:
        """
        Convert a JSON entry describing a start pos into a StartPositionBeat object.
        """
        start_position_pictograph = self.get_start_pos_pictograph(
            start_pos_entry[1] if start_pos_entry else None
        )
        start_pos_beat = StartPositionBeat(
            self.main_widget.sequence_workbench.beat_frame
        )

        start_pos_beat.updater.update_pictograph(
            start_position_pictograph.pictograph_data
        )
        return start_pos_beat

    def get_start_pos_pictograph(self, start_pos_data) -> "Pictograph":
        if not start_pos_data:
            return None

        start_pos_key = start_pos_data["end_pos"]
        letter_str = self.start_pos_key_to_letter(start_pos_key)
        letter = Letter(letter_str)
        matching_letter_pictographs = self.main_widget.pictograph_dataset.get(
            letter, []
        )

        for pictograph_data in matching_letter_pictographs:
            if pictograph_data["start_pos"] == start_pos_key:
                # Transfer orientation data
                pictograph_data["blue_attributes"]["start_ori"] = start_pos_data[
                    "blue_attributes"
                ]["end_ori"]
                pictograph_data["red_attributes"]["start_ori"] = start_pos_data[
                    "red_attributes"
                ]["end_ori"]

                # Use the existing beat_factory or however you build your start pos beats
                pictograph_factory = (
                    self.main_widget.sequence_workbench.beat_frame.beat_factory
                )
                pictograph_key = (
                    self.main_widget.pictograph_key_generator.generate_pictograph_key(
                        pictograph_data
                    )
                )
                start_pos_pictograph = pictograph_factory.create_start_pos_beat(
                    pictograph_key, pictograph_data
                )
                return start_pos_pictograph

        print(f"No matching start position found for key: {start_pos_key}")
        return None

    def start_pos_key_to_letter(self, start_pos_key: str) -> str:
        """Example mapping from 'alpha1' -> 'α', etc."""
        mapping = {"alpha": "α", "beta": "β", "gamma": "Γ"}
        for key in mapping:
            if start_pos_key.startswith(key):
                return mapping[key]
        return None

    def create_pictograph_from_dict(
        self, pictograph_data: dict, target_grid_mode: str
    ) -> Pictograph:
        """
        Create a pictograph with a local 'grid_mode' in its dictionary,
        no context manager or global flips.
        """
        local_dict = deepcopy(pictograph_data)
        local_dict["grid_mode"] = target_grid_mode

        pictograph = Pictograph(self.main_widget)
        pictograph.updater.update_pictograph(local_dict)

        # Append to the relevant list
        if target_grid_mode == BOX:
            self.box_pictographs.append(pictograph)
        else:
            self.diamond_pictographs.append(pictograph)

        return pictograph

    def reinitialize_pictographs(self, new_grid_mode: str = None):
        """
        Reload pictographs under the newly selected mode, if desired.
        """
        self.clear_start_positions()
        self.start_options.clear()
        self.box_pictographs.clear()
        self.diamond_pictographs.clear()

        # Re-load if you want to switch to new mode
        if new_grid_mode:
            self.load_relevant_start_positions(new_grid_mode)
        else:
            self.load_relevant_start_positions()  # fallback
