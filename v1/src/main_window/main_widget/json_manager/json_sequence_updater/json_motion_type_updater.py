from typing import TYPE_CHECKING

from data.constants import ANTI, FLOAT, PREFLOAT_MOTION_TYPE, MOTION_TYPE, PRO, TURNS


if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_sequence_updater.json_sequence_updater import (
        JsonSequenceUpdater,
    )


class JsonMotionTypeUpdater:
    def __init__(self, json_updater: "JsonSequenceUpdater"):
        self.json_updater = json_updater
        self.json_manager = json_updater.json_manager

    def update_motion_type_in_json(
        self, index: int, color: str, motion_type: str
    ) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence()
        sequence[index][f"{color}_attributes"][MOTION_TYPE] = motion_type
        if motion_type in [PRO, ANTI]:
            if PREFLOAT_MOTION_TYPE in sequence[index][f"{color}_attributes"]:
                del sequence[index][f"{color}_attributes"][PREFLOAT_MOTION_TYPE]
        self.json_manager.loader_saver.save_current_sequence(sequence)

    def update_prefloat_motion_type_in_json(
        self, index: int, color: str, motion_type: str
    ) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence()
        if motion_type == FLOAT:
            raise ValueError("prefloat_motion_type cannot be 'float'")
        else:
            sequence[index][f"{color}_attributes"][PREFLOAT_MOTION_TYPE] = motion_type
            self.json_manager.loader_saver.save_current_sequence(sequence)
