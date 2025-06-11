from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )
    from .main_widget import MainWidget


class MainWidgetState:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget

    def load_state(self, beat_frame: "SequenceBeatFrame"):
        try:
            json_manager = self.main_widget.app_context.json_manager
            current_sequence = json_manager.loader_saver.load_current_sequence()
            if len(current_sequence) > 1:
                beat_frame.populator.populate_beat_frame_from_json(
                    current_sequence, initial_state_load=True
                )
        except AttributeError:
            # Fallback for cases where app_context is not available
            import logging

            logger = logging.getLogger(__name__)
            logger.warning("json_manager not available during state loading")
