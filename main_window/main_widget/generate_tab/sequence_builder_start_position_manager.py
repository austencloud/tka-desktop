# base_classes/start_position_manager.py

from copy import deepcopy
import random
from typing import TYPE_CHECKING, Dict, Any

from data.constants import (
    BLUE_ATTRIBUTES,
    DIAMOND,
    END_POS,
    IN,
    RED_ATTRIBUTES,
    START_ORI,
    END_ORI,
    START_POS,
)
from main_window.main_widget.sequence_workbench.sequence_beat_frame.start_pos_beat import (
    StartPositionBeat,
)

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SequenceBuilderStartPosManager:
    """
    Manages the logic for adding a starting position pictograph to the sequence.
    """

    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget
        # This could be parameterized; for now, we assume DIAMOND mode.
        self.grid_mode = DIAMOND

    def add_start_position(self) -> None:
        """
        Chooses a random valid start position and adds it to the sequence.
        """
        start_keys = (
            ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]
            if self.grid_mode == DIAMOND
            else ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"]
        )
        chosen_key = random.choice(start_keys)
        self._add_start_position(chosen_key)

    def _add_start_position(self, position_key: str) -> None:
        """
        Finds the pictograph matching the given key and adds it as the start position.
        Raises LookupError if no match is found.
        """
        try:
            start_pos, end_pos = position_key.split("_")
        except ValueError:
            raise ValueError(f"Invalid position key format: {position_key}")

        dataset = deepcopy(self.main_widget.pictograph_dataset)
        for pictograph_list in dataset.values():
            for pictograph_data in pictograph_list:
                if (
                    pictograph_data.get(START_POS) == start_pos
                    and pictograph_data.get(END_POS) == end_pos
                ):
                    self._set_orientation_in(pictograph_data)
                    start_pos_beat = StartPositionBeat(
                        self.main_widget.sequence_workbench.sequence_beat_frame
                    )
                    start_pos_beat.managers.updater.update_pictograph(
                        deepcopy(pictograph_data)
                    )
                    self.main_widget.json_manager.start_pos_handler.set_start_position_data(
                        start_pos_beat
                    )
                    self.main_widget.sequence_workbench.sequence_beat_frame.start_pos_view.set_start_pos(
                        start_pos_beat
                    )
                    return
        raise LookupError(f"No matching start position found for key: {position_key}")

    def _set_orientation_in(self, pictograph_data: Dict[str, Any]) -> None:
        """
        Sets all relevant orientation attributes to 'in'.
        """
        pictograph_data[BLUE_ATTRIBUTES][START_ORI] = IN
        pictograph_data[RED_ATTRIBUTES][START_ORI] = IN
        pictograph_data[BLUE_ATTRIBUTES][END_ORI] = IN
        pictograph_data[RED_ATTRIBUTES][END_ORI] = IN
