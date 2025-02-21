from typing import TYPE_CHECKING, Union

from data.constants import DASH, NO_ROT, STATIC
from main_window.main_widget.sequence_properties_manager.sequence_properties_manager import (
    SequencePropertiesManager,
)


if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )
    from main_window.main_widget.json_manager.json_sequence_updater.json_sequence_updater import (
        JsonSequenceUpdater,
    )


class JsonTurnsUpdater:
    def __init__(self, json_updater: "JsonSequenceUpdater"):
        self.json_updater = json_updater
        self.json_manager = json_updater.json_manager

    def update_turns_in_json_at_index(
        self,
        index: int,
        color: str,
        turns: Union[int, float],
        beat_frame: "SequenceBeatFrame",
    ) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence()
        sequence[index][f"{color}_attributes"]["turns"] = turns
        end_ori = self.json_manager.ori_calculator.calculate_end_ori(
            sequence[index], color
        )
        sequence[index][f"{color}_attributes"]["end_ori"] = end_ori
        if sequence[index][f"{color}_attributes"]["turns"] != "fl":
            if sequence[index][f"{color}_attributes"]["turns"] > 0:
                pictograph = beat_frame.beat_views[index - 2].beat
                if pictograph:
                    motion = pictograph.managers.get.motion_by_color(color)
                    prop_rot_dir = motion.prop_rot_dir
                    sequence[index][f"{color}_attributes"][
                        "prop_rot_dir"
                    ] = prop_rot_dir

        elif sequence[index][f"{color}_attributes"]["turns"] == "fl":
            pictograph = beat_frame.beat_views[index - 2].beat
            if pictograph:
                motion = pictograph.managers.get.motion_by_color(color)

        if sequence[index][f"{color}_attributes"]["motion_type"] in [DASH, STATIC]:
            if sequence[index][f"{color}_attributes"]["turns"] == 0:
                prop_rot_dir = NO_ROT
                sequence[index][f"{color}_attributes"]["prop_rot_dir"] = prop_rot_dir

        self.json_manager.loader_saver.save_current_sequence(sequence)
        SequencePropertiesManager().update_sequence_properties()
