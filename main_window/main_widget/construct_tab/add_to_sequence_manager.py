from typing import TYPE_CHECKING
from main_window.main_widget.sequence_widget.beat_frame.beat_view import (
    Beat,
)

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph

    from main_window.main_widget.construct_tab.construct_tab import (
        ConstructTab,
    )
    from main_window.main_widget.sequence_widget.beat_frame.beat_view import (
        Beat,
    )


class AddToSequenceManager:
    def __init__(self, construct_tab: "ConstructTab") -> None:
        self.construct_tab = construct_tab

    def create_new_beat(self, clicked_option: "BasePictograph") -> "Beat":
        sequence = (
            self.construct_tab.main_widget.json_manager.loader_saver.load_current_sequence_json()
        )

        last_beat_dict = None
        if len(sequence) > 1:
            last_beat_dict = sequence[-1]
            if last_beat_dict.get("is_placeholder", False):
                last_beat_dict = sequence[-2]

        new_beat = Beat(clicked_option.main_widget.sequence_widget.beat_frame)
        new_beat.setSceneRect(clicked_option.sceneRect())
        pictograph_dict = clicked_option.get.pictograph_dict()

        pictograph_dict["duration"] = 1
        pictograph_dict = dict(
            list(pictograph_dict.items())[:1]
            + [("duration", 1)]
            + list(pictograph_dict.items())[1:]
        )

        new_beat.updater.update_pictograph(pictograph_dict)
        self.construct_tab.last_beat = new_beat
        SW_beat_frame = self.construct_tab.main_widget.sequence_widget.beat_frame
        if not SW_beat_frame.sequence_changed:
            SW_beat_frame.sequence_changed = True
        return new_beat
