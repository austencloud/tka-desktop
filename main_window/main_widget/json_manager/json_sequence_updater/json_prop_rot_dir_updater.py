from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_sequence_updater.json_sequence_updater import (
        JsonSequenceUpdater,
    )


class JsonstrUpdater:
    def __init__(self, json_updater: "JsonSequenceUpdater") -> None:
        self.json_manager = json_updater.json_manager

    def update_prefloat_prop_rot_dir_in_json(
        self, index: int, color: str, prop_rot_dir: str
    ) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        sequence[index][f"{color}_attributes"]["prefloat_prop_rot_dir"] = prop_rot_dir
        self.json_manager.loader_saver.save_current_sequence(sequence)

    def update_prop_rot_dir_in_json_at_index(
        self, index: int, color: str, prop_rot_dir: str
    ) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        sequence[index][f"{color}_attributes"]["prop_rot_dir"] = prop_rot_dir
        if sequence[index][f"{color}_attributes"]["turns"] != "fl":
            if "prefloat_prop_rot_dir" in sequence[index][f"{color}_attributes"]:
                del sequence[index][f"{color}_attributes"]["prefloat_prop_rot_dir"]
        self.json_manager.loader_saver.save_current_sequence(sequence)
