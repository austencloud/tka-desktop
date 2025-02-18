from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import QStackedWidget

if TYPE_CHECKING:
    from main_window.main_widget.fade_manager.fade_manager import FadeManager


class StackFader:
    def __init__(self, manager: "FadeManager"):
        self.manager = manager

    def fade_stack(
        self,
        stack: QStackedWidget,
        new_index: int,
        duration: int = 300,
        callback: Optional[callable] = None,
    ):
        current_widget = stack.currentWidget()
        next_widget = stack.widget(new_index)
        self.manager.graphics_effect_remover.clear_graphics_effects(
            [current_widget, next_widget]
        )

        if not current_widget or not next_widget or stack.currentIndex() == new_index:
            return

        def on_fade_out_finished():
            self.manager.graphics_effect_remover.clear_graphics_effects(
                [current_widget, next_widget]
            )
            stack.setCurrentIndex(new_index)

            if self.manager.fades_enabled():
                self.manager.widget_fader.fade_widgets(
                    [next_widget], fade_in=True, duration=duration, callback=callback
                )
            else:
                effect = self.manager.widget_fader._ensure_opacity_effect(next_widget)
                effect.setOpacity(1.0)
                next_widget.setGraphicsEffect(effect)
                if callback:
                    callback()

        if self.manager.fades_enabled():
            self.manager.widget_fader.fade_widgets(
                [current_widget], fade_in=False, duration=duration, callback=on_fade_out_finished
            )
        else:
            effect = self.manager.widget_fader._ensure_opacity_effect(current_widget)
            effect.setOpacity(0.0)
            current_widget.setGraphicsEffect(effect)
            on_fade_out_finished()
