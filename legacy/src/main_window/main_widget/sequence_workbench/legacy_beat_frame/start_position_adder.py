from typing import TYPE_CHECKING
from copy import deepcopy
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
from data.constants import BLUE_ATTRS, MOTION_TYPE, STATIC
from interfaces.json_manager_interface import IJsonManager

from .start_pos_beat import StartPositionBeat

if TYPE_CHECKING:
    from .legacy_beat_frame import LegacyBeatFrame


class StartPositionAdder:
    def __init__(
        self, beat_frame: "LegacyBeatFrame", json_manager: IJsonManager = None
    ):
        self.beat_frame = beat_frame
        self.sequence_workbench = beat_frame.sequence_workbench
        self.main_widget = beat_frame.main_widget
        self.json_manager = json_manager

    def add_start_pos_to_sequence(
        self, clicked_start_option: "LegacyPictograph"
    ) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        try:
            start_pos_beat = StartPositionBeat(self.beat_frame)

            start_pos_view = self.beat_frame.start_pos_view

            # Get construct tab through the new tab manager system
            try:
                construct_tab = self.main_widget.tab_manager.get_tab_widget("construct")
                if construct_tab:
                    construct_tab.last_beat = start_pos_beat
                    self.construct_tab = construct_tab
                else:
                    # Fallback: try direct access for backward compatibility
                    if hasattr(self.main_widget, "construct_tab"):
                        self.main_widget.construct_tab.last_beat = start_pos_beat
                        self.construct_tab = self.main_widget.construct_tab
                    else:
                        import logging

                        logger = logging.getLogger(__name__)
                        logger.warning(
                            "construct_tab not available in StartPositionAdder"
                        )
                        return
            except AttributeError:
                # Fallback: try direct access for backward compatibility
                if hasattr(self.main_widget, "construct_tab"):
                    self.main_widget.construct_tab.last_beat = start_pos_beat
                    self.construct_tab = self.main_widget.construct_tab
                else:
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.warning("construct_tab not available in StartPositionAdder")
                    return
            start_pos_dict = clicked_start_option.state.pictograph_data
            graph_editor = self.sequence_workbench.graph_editor

            if not graph_editor.is_toggled:
                graph_editor.animator.toggle()
            start_pos_dict[BLUE_ATTRS][MOTION_TYPE] == STATIC
            start_pos_beat.managers.updater.update_pictograph(deepcopy(start_pos_dict))
            clicked_start_option.managers.updater.update_dict_from_attributes()

            # Use the injected json_manager if available, otherwise get it from dependency injection
            json_manager = self.json_manager
            if not json_manager:
                try:
                    json_manager = self.main_widget.app_context.json_manager
                except AttributeError:
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.warning("json_manager not available in StartPositionAdder")
                    return

            json_manager.start_pos_handler.set_start_position_data(start_pos_beat)
            self.beat_frame.start_pos_view.set_start_pos(start_pos_beat)
            self.beat_frame.selection_overlay.select_beat_view(start_pos_view, False)
            self.construct_tab.transition_to_option_picker()
            self.construct_tab.option_picker.updater.update_options()
        finally:
            # Revert cursor back to default
            QApplication.restoreOverrideCursor()
