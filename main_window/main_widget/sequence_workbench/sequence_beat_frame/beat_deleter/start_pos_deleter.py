from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .beat_deleter import BeatDeleter


class StartPositionDeleter:
    def __init__(self, deleter: "BeatDeleter"):
        self.deleter = deleter
        self.main_widget = deleter.main_widget
        self.beat_frame = deleter.beat_frame

    def delete_all_beats(self, show_indicator=True) -> None:

        from PyQt6.QtWidgets import QGraphicsView

        # Ensure all painting is stopped before clearing
        for beat_view in self.beat_frame.beat_views:
            if isinstance(beat_view, QGraphicsView):
                beat_view.viewport().update()  # Force re-render to clear any pending paints
            if beat_view.graphicsEffect():
                beat_view.setGraphicsEffect(None)
            beat_view.setScene(None)
            beat_view.is_filled = False
            beat_view.update()  # Force repaint to prevent lingering QPainter

        # Clean up any orphaned effects
        beats = self.beat_frame.beat_views  # List of Beat Views
        widgets = self.deleter.widget_collector.collect_shared_widgets()
        beats_filled = any(beat.is_filled for beat in beats)
        start_pos_filled = self.beat_frame.start_pos_view.is_filled
        fade_enabled = (
            self.main_widget.settings_manager.global_settings.get_enable_fades()
        )

        # ✅ Step 1: Properly clear all beats but don't delete them
        for beat_view in beats:
            if beat_view.graphicsEffect():
                beat_view.setGraphicsEffect(None)  # Remove lingering opacity effects
            if beat_view.scene():
                beat_view.setScene(None)  # Ensure no invalid scene remains
            beat_view.is_filled = False
            beat_view.update()  # Force a repaint to prevent QPainter errors

        # ✅ Step 2: Clean up orphaned effects
        self.main_widget.fade_manager.graphics_effect_remover.clear_graphics_effects(
            beats
        )

        # ✅ Step 3: Handle fade or direct reset logic
        if not beats_filled and not start_pos_filled:
            if fade_enabled:
                self.deleter.fade_and_reset_widgets(widgets, show_indicator)
            else:
                self.deleter.reset_widgets(show_indicator)

        elif not beats_filled and start_pos_filled:
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
        self.beat_frame.update()  # Forces a repaint at the beat frame level
        self.main_widget.update()  # Ensures any higher-level widgets repaint correctly
