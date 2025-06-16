from typing import TYPE_CHECKING

from base_widgets.pictograph.elements.views.beat_view import (
    LegacyBeatView,
)
from main_window.main_widget.sequence_workbench.legacy_beat_frame.start_pos_beat_view import (
    StartPositionBeatView,
)
from src.legacy_settings_manager.global_settings.app_context import AppContext
from .first_beat_deleter import FirstBeatDeleter
from .non_first_beat_deleter import NonFirstBeatDeleter
from .all_beats_deleter import AllBeatsDeleter
from .widget_collector import WidgetCollector


if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


class BeatDeleter:
    message = "You can't delete a beat if you haven't selected one."

    def __init__(self, sequence_workbench: "SequenceWorkbench"):
        self.sequence_workbench = sequence_workbench
        self.beat_frame = sequence_workbench.beat_frame
        self.json_manager = AppContext.json_manager()
        self.main_widget = sequence_workbench.main_widget
        self.selection_overlay = self.beat_frame.selection_overlay

        # Instantiate helpers
        self.widget_collector = WidgetCollector(self)
        self.start_position_deleter = AllBeatsDeleter(self)
        self.first_beat_deleter = FirstBeatDeleter(self)
        self.other_beat_deleter = NonFirstBeatDeleter(self)

    def delete_selected_beat(self) -> None:
        selected_beat = self.selection_overlay.get_selected_beat()
        if not selected_beat:
            self._show_no_beat_selected_message()
            return

        if isinstance(selected_beat, StartPositionBeatView):
            self.start_position_deleter.delete_all_beats(show_indicator=True)
        else:
            if selected_beat == self.beat_frame.beat_views[0]:
                self.first_beat_deleter.delete_first_beat(selected_beat)
            else:
                self.other_beat_deleter.delete_non_first_beat(selected_beat)

    def _show_no_beat_selected_message(self) -> None:
        self.sequence_workbench.indicator_label.show_message(self.message)

    def _post_deletion_updates(self) -> None:
        self.json_manager.updater.clear_and_repopulate_json_from_beat_view(
            self.beat_frame
        )
        self.beat_frame.layout_manager.configure_beat_frame_for_filled_beats()
        self.beat_frame.sequence_workbench.current_word_label.update_current_word_label()
        self.beat_frame.sequence_workbench.difficulty_label.update_difficulty_label()
        # Update the circular indicator
        self.sequence_workbench.circular_indicator.update_indicator()
        self.beat_frame.emit_update_image_export_preview()
        self.sequence_workbench.difficulty_label.update_difficulty_label()

        # Auto-switch construct tab view after individual beat deletion
        construct_tab = self.sequence_workbench.main_widget.get_tab_widget("construct")
        if construct_tab and self._is_construct_tab_active():
            self._auto_switch_construct_tab_view_after_deletion(construct_tab)

    def _delete_beat_and_following(self, beat: LegacyBeatView) -> None:
        beats = self.beat_frame.beat_views
        start_index = beats.index(beat)
        beats = [beat for beat in beats[start_index:]]
        for beat in beats:
            self._delete_beat(beat)

    def _delete_beat(self, beat_view: LegacyBeatView) -> None:
        if beat_view.graphicsEffect():
            beat_view.setGraphicsEffect(None)  # Remove lingering effects
        beat_view.setScene(beat_view.blank_beat)  # Assign a valid scene
        beat_view.is_filled = False
        beat_view.update()  # Ensure it repaints correctly

    def reset_widgets(self, show_indicator=False):
        self.json_manager.loader_saver.clear_current_sequence_file()
        self.beat_frame.updater.reset_beat_frame()
        if show_indicator:
            self.sequence_workbench.indicator_label.show_message("Sequence cleared")
        self.beat_frame.layout_manager.configure_beat_frame_for_filled_beats()
        self.sequence_workbench.graph_editor.pictograph_container.GE_view.set_to_blank_grid()
        construct_tab = self.sequence_workbench.main_widget.get_tab_widget("construct")
        if construct_tab:
            construct_tab.last_beat = self.sequence_workbench.beat_frame.start_pos
            # Only auto-switch picker if we're currently in the construct tab
            if self._is_construct_tab_active():
                self._auto_switch_construct_tab_view_after_deletion(construct_tab)
        self.sequence_workbench.graph_editor.update_graph_editor()
        self.sequence_workbench.difficulty_label.update_difficulty_label()

    def _auto_switch_construct_tab_view_after_deletion(self, construct_tab):
        """
        Automatically switch the construct tab view after beat deletion based on remaining sequence state.

        Logic:
        - Show Start Position Picker when: Sequence is completely empty (no start position set AND no beats)
        - Show Option Picker when: A start position has been selected (regardless of beat count), OR
                                  there are any beats in the sequence (even if start position is somehow unset)
        """
        try:
            picker_type = self._determine_appropriate_picker()

            import logging

            logger = logging.getLogger(__name__)

            if picker_type == "start_pos_picker":
                if hasattr(construct_tab, "transition_to_start_pos_picker"):
                    construct_tab.transition_to_start_pos_picker()
                    logger.info(
                        "Switched to start position picker (sequence completely empty)"
                    )
            elif picker_type == "option_picker":
                if hasattr(construct_tab, "transition_to_option_picker"):
                    construct_tab.transition_to_option_picker()
                    logger.info(
                        "Switched to option picker (start position set or beats exist)"
                    )

        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                f"Failed to auto-switch construct tab view after deletion: {e}"
            )

    def _determine_appropriate_picker(self) -> str:
        """
        Centralized logic to determine which picker should be shown based on current sequence state.

        Returns:
            "start_pos_picker" if sequence is completely empty (no start position AND no beats)
            "option_picker" if start position is set OR beats exist
        """
        try:
            # Get current sequence state
            beat_count = self.beat_frame.get.beat_count()
            start_pos_is_filled = self.beat_frame.start_pos_view.is_filled

            import logging

            logger = logging.getLogger(__name__)
            logger.debug(
                f"Determining picker: beat_count={beat_count}, start_pos_filled={start_pos_is_filled}"
            )

            # Show Start Position Picker only when sequence is completely empty
            if beat_count == 0 and not start_pos_is_filled:
                return "start_pos_picker"

            # Show Option Picker when start position is set OR beats exist
            return "option_picker"

        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(f"Error determining appropriate picker: {e}")
            # Default to option picker on error
            return "option_picker"

    def _is_construct_tab_active(self) -> bool:
        """
        Check if the construct tab is currently the active tab.

        Returns:
            True if construct tab is active, False otherwise
        """
        try:
            # Check if we have a tab manager and get the current tab
            if hasattr(self.main_widget, "tab_manager"):
                current_tab = self.main_widget.tab_manager.get_current_tab()
                return current_tab == "construct"

            # Fallback: check if construct tab is visible in the right stack
            if hasattr(self.main_widget, "right_stack"):
                current_widget = self.main_widget.right_stack.currentWidget()
                if current_widget:
                    # Check if the current widget is related to construct tab
                    widget_name = current_widget.__class__.__name__
                    return widget_name in [
                        "StartPosPicker",
                        "OptionPicker",
                        "AdvancedStartPosPicker",
                    ]

            return False

        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(f"Error checking if construct tab is active: {e}")
            # Default to False to avoid unwanted picker switching
            return False

    def fade_and_reset_widgets(self, widgets, show_indicator):
        self.main_widget.fade_manager.widget_fader.fade_and_update(
            widgets,
            callback=lambda: self.reset_widgets(show_indicator),
            duration=300,
        )
