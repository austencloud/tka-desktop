from typing import TYPE_CHECKING

from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat import Beat

if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_manager import JsonManager
    from main_window.main_widget.sequence_workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )
    from base_widgets.pictograph.pictograph import Pictograph


class AddToSequenceManager:
    def __init__(
        self,
        json_manager: "JsonManager",
        beat_frame: "SequenceBeatFrame",
        last_beat: "Beat",
    ):
        self.json_manager = json_manager
        self.beat_frame = beat_frame
        self.last_beat = last_beat

    def create_new_beat(self, clicked_option: "Pictograph") -> "Beat":
        sequence = self.json_manager.loader_saver.load_current_sequence()

        last_beat_data = None
        if len(sequence) > 1:
            last_beat_data = sequence[-1]
            if last_beat_data.get("is_placeholder", False):
                last_beat_data = sequence[-2]

        new_beat = Beat(self.beat_frame)
        new_beat.setSceneRect(clicked_option.sceneRect())
        pictograph_data = clicked_option.managers.get.pictograph_data()

        pictograph_data["duration"] = 1
        pictograph_data = dict(
            list(pictograph_data.items())[:1]
            + [("duration", 1)]
            + list(pictograph_data.items())[1:]
        )

        new_beat.managers.updater.update_pictograph(pictograph_data)
        self.last_beat = new_beat

        return new_beat
