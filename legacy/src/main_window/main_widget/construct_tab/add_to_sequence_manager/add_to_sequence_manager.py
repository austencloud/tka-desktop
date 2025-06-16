from typing import TYPE_CHECKING

from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat import Beat
from interfaces.settings_manager_interface import ISettingsManager
from interfaces.json_manager_interface import IJsonManager

if TYPE_CHECKING:
    from legacy.src.main_window.main_widget.sequence_workbench.legacy_beat_frame.legacy_beat_frame import (
        LegacyBeatFrame,
    )
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class AddToSequenceManager:
    def __init__(
        self,
        json_manager: IJsonManager,
        beat_frame: "LegacyBeatFrame",
        last_beat: "Beat",
        settings_manager: ISettingsManager = None,
    ):
        self.json_manager = json_manager
        self.beat_frame = beat_frame
        self.last_beat = last_beat
        self.settings_manager = settings_manager

    def create_new_beat(self, clicked_option: "LegacyPictograph") -> "Beat":
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
