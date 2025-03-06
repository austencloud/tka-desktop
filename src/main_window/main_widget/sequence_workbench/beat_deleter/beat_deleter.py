from typing import TYPE_CHECKING

from base_widgets.pictograph.elements.views.beat_view import (
    BeatView,
)
from main_window.main_widget.sequence_workbench.sequence_beat_frame.start_pos_beat_view import (
    StartPositionBeatView,
)
from settings_manager.global_settings.app_context import AppContext
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
        self.beat_frame.sequence_workbench.current_word_label.update_current_word_label_from_beats()
        self.beat_frame.sequence_workbench.difficulty_label.update_difficulty_label()
        self.beat_frame.emit_update_image_export_preview()
        self.sequence_workbench.difficulty_label.update_difficulty_label()

    def _delete_beat_and_following(self, beat: BeatView) -> None:
        beats = self.beat_frame.beat_views
        start_index = beats.index(beat)
        beats = [beat for beat in beats[start_index:]]
        for beat in beats:
            self._delete_beat(beat)

    def _delete_beat(self, beat_view: BeatView) -> None:
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
        self.sequence_workbench.main_widget.construct_tab.last_beat = (
            self.sequence_workbench.beat_frame.start_pos
        )
        self.sequence_workbench.graph_editor.update_graph_editor()
        self.sequence_workbench.difficulty_label.update_difficulty_label()

    def fade_and_reset_widgets(self, widgets, show_indicator):
        self.main_widget.fade_manager.widget_fader.fade_and_update(
            widgets,
            callback=lambda: self.reset_widgets(show_indicator),
            duration=300,
        )
