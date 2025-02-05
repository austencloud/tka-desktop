from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_sequence_updater.json_sequence_updater import (
        JsonSequenceUpdater,
    )


class JsonMotionTypeUpdater:
    def __init__(self, json_updater: "JsonSequenceUpdater"):
        self.json_updater = json_updater
        self.json_manager = json_updater.json_manager
        self.main_widget = self.json_manager.main_widget

    def update_json_motion_type(self, index: int, color: str, motion_type: str) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        sequence[index][f"{color}_attributes"]["motion_type"] = motion_type
        if sequence[index][f"{color}_attributes"]["turns"] != "fl":
            if "prefloat_motion_type" in sequence[index][f"{color}_attributes"]:
                del sequence[index][f"{color}_attributes"]["prefloat_motion_type"]
        self.json_manager.loader_saver.save_current_sequence(sequence)

    def update_json_prefloat_motion_type(
        self, index: int, color: str, motion_type: str
    ) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        if motion_type == "float":
            raise ValueError("prefloat_motion_type cannot be 'float'")
        else:
            sequence[index][f"{color}_attributes"]["prefloat_motion_type"] = motion_type
            self.json_manager.loader_saver.save_current_sequence(sequence)
