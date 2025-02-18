from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import QWidget, QStackedWidget
from PyQt6.QtCore import QParallelAnimationGroup, QPropertyAnimation, QEasingCurve

if TYPE_CHECKING:
    from main_window.main_widget.fade_manager.fade_manager import FadeManager


class WidgetAndStackFader:
    def __init__(self, manager: "FadeManager"):
        self.manager = manager

    def fade_widgets_and_stack(
        self,
        widgets: list[QWidget],
        stack: QStackedWidget,
        new_index: int,
        duration: int = 300,
        callback: Optional[callable] = None,
    ):
        current_widget = stack.currentWidget()
        next_widget = stack.widget(new_index)

        if not current_widget or not next_widget or stack.currentIndex() == new_index:
            return

        self.manager.graphics_effect_remover.clear_graphics_effects(
            [current_widget, next_widget] + widgets
        )

        fade_enabled = self.manager.fades_enabled()

        def switch_stack():
            stack.setCurrentIndex(new_index)

        def finalize():
            if callback:
                callback()

        if not fade_enabled:
            switch_stack()
            finalize()
            return

        animation_group = QParallelAnimationGroup(self.manager)

        for widget in widgets + [current_widget]:
            if widget:
                self._add_fade_animation(animation_group, widget, fade_in=False, duration=duration)

        def on_fade_out_finished():
            switch_stack()

            fade_in_group = QParallelAnimationGroup(self.manager)

            for widget in widgets + [next_widget]:
                if widget:
                    self._add_fade_animation(fade_in_group, widget, fade_in=True, duration=duration)

            fade_in_group.finished.connect(finalize)
            fade_in_group.start()

        animation_group.finished.connect(on_fade_out_finished)
        animation_group.start()

    def _add_fade_animation(
        self,
        group: QParallelAnimationGroup,
        widget: QWidget,
        fade_in: bool,
        duration: int,
    ):
        effect = self.manager.widget_fader._ensure_opacity_effect(widget)
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0 if fade_in else 1.0)
        animation.setEndValue(1.0 if fade_in else 0.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        group.addAnimation(animation)
