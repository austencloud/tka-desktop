from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...beat_deleter import BeatDeleter


class StartPositionDeleter:
    def __init__(self, deleter: "BeatDeleter"):
        self.deleter = deleter
        self.main_widget = deleter.main_widget
        self.beat_frame = deleter.beat_frame

    def delete_all_beats(self, show_indicator=True) -> None:
        beats = self.beat_frame.beat_views
        widgets = self.deleter.widget_collector.collect_shared_widgets()
        beats_filled = any(beat.is_filled for beat in beats)
        start_pos_filled = self.beat_frame.start_pos_view.is_filled

        fade_enabled = (
            self.main_widget.settings_manager.global_settings.get_enable_fades()
        )

        if not beats_filled and not start_pos_filled:
            adjustment_panel_items = (
                self.deleter.widget_collector.get_adjustment_panel_items()
            )
            for item in adjustment_panel_items:
                if item in widgets:
                    widgets.remove(item)

            if fade_enabled:
                self.deleter.fade_and_reset_widgets(widgets, show_indicator)
            else:
                self.deleter.reset_widgets(show_indicator)

        elif not beats_filled and start_pos_filled:
            adjustment_panel_items = (
                self.deleter.widget_collector.get_adjustment_panel_items()
            )
            for item in adjustment_panel_items:
                if item in widgets:
                    widgets.remove(item)

            if fade_enabled:
                self.main_widget.fade_manager.widget_and_stack_fader.fade_widgets_and_stack(
                    widgets,
                    self.main_widget.right_stack,
                    self.main_widget.right_start_pos_picker_index,
                    300,
                    lambda: self.deleter.reset_widgets(show_indicator),
                )
            else:
                self.main_widget.right_stack.setCurrentIndex(
                    self.main_widget.right_start_pos_picker_index
                )
                self.deleter.reset_widgets(show_indicator)

        elif (
            self.main_widget.right_stack.currentWidget()
            == self.main_widget.generate_tab
        ):
            if fade_enabled:
                self.deleter.fade_and_reset_widgets(widgets, show_indicator)
            else:
                self.deleter.reset_widgets(show_indicator)
        else:
            if fade_enabled:
                self.main_widget.fade_manager.widget_and_stack_fader.fade_widgets_and_stack(
                    widgets,
                    self.main_widget.right_stack,
                    self.main_widget.right_start_pos_picker_index,
                    300,
                    lambda: self.deleter.reset_widgets(show_indicator),
                )
            else:
                self.main_widget.right_stack.setCurrentIndex(
                    self.main_widget.right_start_pos_picker_index
                )
                self.deleter.reset_widgets(show_indicator)
