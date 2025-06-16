from typing import TYPE_CHECKING, Union

from data.constants import (
    CLOCKWISE,
    DASH,
    END_ORI,
    NO_ROT,
    STATIC,
    TURNS,
    MOTION_TYPE,
    PROP_ROT_DIR,
)
from main_window.main_widget.sequence_properties_manager.sequence_properties_manager import (
    SequencePropertiesManager,
)
from src.legacy_settings_manager.global_settings.app_context import AppContext


if TYPE_CHECKING:
    from legacy.src.main_window.main_widget.sequence_workbench.legacy_beat_frame.legacy_beat_frame import (
        LegacyBeatFrame,
    )
    from main_window.main_widget.json_manager.json_sequence_updater.json_sequence_updater import (
        JsonSequenceUpdater,
    )


class JsonTurnsUpdater:
    def __init__(self, json_updater: "JsonSequenceUpdater"):
        self.json_updater = json_updater
        self.json_manager = json_updater.json_manager

    def update_turns_in_json(
        self,
        index: int,
        color: str,
        turns: Union[int, float],
    ) -> None:
        beat_frame = self._get_sequence_beat_frame()
        sequence = self.json_manager.loader_saver.load_current_sequence()
        pictograph_data = sequence[index]
        motion_data = pictograph_data[f"{color}_attributes"]
        if turns in [0.0, 1.0, 2.0, 3.0]:
            turns = int(turns)
        motion_data[TURNS] = turns

        if motion_data[PROP_ROT_DIR] == NO_ROT and motion_data[MOTION_TYPE] in [
            DASH,
            STATIC,
        ]:
            motion_data[PROP_ROT_DIR] = CLOCKWISE

        end_ori = self.json_manager.ori_calculator.calculate_end_ori(
            pictograph_data, color
        )
        motion_data[END_ORI] = end_ori
        if beat_frame:  # Only proceed if beat_frame is available
            if motion_data[TURNS] != "fl":
                if motion_data[TURNS] > 0:
                    pictograph = beat_frame.beat_views[index - 2].beat
                    if pictograph:
                        motion = pictograph.managers.get.motion_by_color(color)
                        prop_rot_dir = motion.state.prop_rot_dir
                        motion_data[PROP_ROT_DIR] = prop_rot_dir

            elif motion_data[TURNS] == "fl":
                pictograph = beat_frame.beat_views[index - 2].beat
                if pictograph:
                    motion = pictograph.managers.get.motion_by_color(color)

        if motion_data[MOTION_TYPE] in [DASH, STATIC]:
            if motion_data[TURNS] == 0:
                prop_rot_dir = NO_ROT
                motion_data[PROP_ROT_DIR] = prop_rot_dir

        self.json_manager.loader_saver.save_current_sequence(sequence)
        SequencePropertiesManager().update_sequence_properties()

    def _get_sequence_beat_frame(self):
        """Get the sequence beat frame using graceful fallbacks for the MainWidgetCoordinator refactoring."""
        try:
            # Try to get sequence beat frame through AppContext
            from src.legacy_settings_manager.global_settings.app_context import AppContext

            return AppContext.sequence_beat_frame()
        except RuntimeError:
            # AppContext.sequence_beat_frame() not initialized yet
            # This can happen during MainWidgetCoordinator initialization
            import logging

            logger = logging.getLogger(__name__)
            logger.debug(
                "AppContext.sequence_beat_frame() not available yet - this is normal during initialization"
            )
            return None
        except Exception as e:
            # Other unexpected errors
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(f"Unexpected error accessing sequence beat frame: {e}")
            return None
