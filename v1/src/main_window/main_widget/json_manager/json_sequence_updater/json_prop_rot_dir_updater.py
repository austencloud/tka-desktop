from typing import TYPE_CHECKING

from data.constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    PREFLOAT_PROP_ROT_DIR,
    PROP_ROT_DIR,
    TURNS,
)

if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_sequence_updater.json_sequence_updater import (
        JsonSequenceUpdater,
    )


class JsonPropRotDirUpdater:
    def __init__(self, json_updater: "JsonSequenceUpdater") -> None:
        self.json_manager = json_updater.json_manager

    def update_prop_rot_dir_in_json(
        self, index: int, color: str, prop_rot_dir: str
    ) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence()
        sequence[index][f"{color}_attributes"][PROP_ROT_DIR] = prop_rot_dir
        if prop_rot_dir in [CLOCKWISE, COUNTER_CLOCKWISE]:
            if PREFLOAT_PROP_ROT_DIR in sequence[index][f"{color}_attributes"]:
                del sequence[index][f"{color}_attributes"][PREFLOAT_PROP_ROT_DIR]
        self.json_manager.loader_saver.save_current_sequence(sequence)

    def update_prefloat_prop_rot_dir_in_json(
        self, index: int, color: str, prop_rot_dir: str
    ) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence()
        sequence[index][f"{color}_attributes"][PREFLOAT_PROP_ROT_DIR] = prop_rot_dir
        self.json_manager.loader_saver.save_current_sequence(sequence)
