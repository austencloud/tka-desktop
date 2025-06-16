from typing import TYPE_CHECKING

from base_widgets.pictograph.elements.views.beat_view import (
    LegacyBeatView,
)


if TYPE_CHECKING:
    from .beat_deleter import BeatDeleter


class FirstBeatDeleter:
    def __init__(self, deleter: "BeatDeleter"):
        self.deleter = deleter
        self.main_widget = self.deleter.main_widget

    def delete_first_beat(self, selected_beat: LegacyBeatView):
        # Get construct tab using the new dependency injection pattern
        construct_tab = self._get_construct_tab()
        if not construct_tab or not hasattr(construct_tab, "option_picker"):
            # If construct tab or option picker is not available, skip the fade operation
            self._delete_beat_and_following(selected_beat)
            return

        self.option_picker = construct_tab.option_picker
        widgets = self.deleter.widget_collector.collect_shared_widgets()
        views = [option.elements.view for option in self.option_picker.option_pool]
        widgets.extend(views)
        widgets.remove(self.deleter.beat_frame.start_pos_view)

        panel = self.deleter.sequence_workbench.graph_editor.adjustment_panel
        turns_boxes = [panel.red_turns_box, panel.blue_turns_box]

        for box in turns_boxes:
            widgets.extend(
                [
                    box.turns_widget.display_frame.increment_button,
                    box.turns_widget.display_frame.decrement_button,
                    box.turns_widget.turns_text,
                ]
            )

        self.deleter.main_widget.fade_manager.widget_fader.fade_and_update(
            widgets,
            callback=lambda: self._delete_beat_and_following(selected_beat),
            duration=300,
        )

    def _delete_beat_and_following(self, start_beat: LegacyBeatView):
        # Get construct tab using the new dependency injection pattern
        construct_tab = self._get_construct_tab()
        if construct_tab:
            construct_tab.last_beat = self.deleter.beat_frame.start_pos_view.beat

        self.deleter.beat_frame.selection_overlay.deselect_beat()
        beats = self.deleter.beat_frame.beat_views
        start_index = beats.index(start_beat)
        for beat in beats[start_index:]:
            self.deleter._delete_beat(beat)
        self.deleter._post_deletion_updates()

        # Update option picker if available
        if construct_tab and hasattr(construct_tab, "option_picker"):
            self.option_picker = construct_tab.option_picker
            self.option_picker.updater.update_options()

        self.deleter.beat_frame.selection_overlay.select_beat_view(
            self.deleter.beat_frame.start_pos_view, toggle_animation=False
        )

    def _get_construct_tab(self):
        """Get the construct tab using the new dependency injection pattern with graceful fallbacks."""
        try:
            # Try to get construct tab through the new coordinator pattern
            return self.deleter.main_widget.get_tab_widget("construct")
        except AttributeError:
            # Fallback: try through tab_manager for backward compatibility
            try:
                return self.deleter.main_widget.tab_manager.get_tab_widget("construct")
            except AttributeError:
                # Final fallback: try direct access for legacy compatibility
                try:
                    if hasattr(self.deleter.main_widget, "construct_tab"):
                        return self.deleter.main_widget.construct_tab
                except AttributeError:
                    pass
        return None
