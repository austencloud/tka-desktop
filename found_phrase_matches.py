# GENERATED FILE: Matching classes for phrase: 'OpacityEffect'
# Search directory: C:/the-kinetic-constructor

# -------------------------------------------------------
# File: C:/the-kinetic-constructor\main_window\main_widget\base_indicator_label.py
# -------------------------------------------------------
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, pyqtSlot
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.base_lesson_widget import (
        BaseLessonWidget,
    )
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


# [Line 13]
class BaseIndicatorLabel(QLabel):
    def __init__(
        self, parent_widget: Union["BaseLessonWidget", "SequenceWorkbench"]
    ) -> None:
        super().__init__(parent_widget)
        self.parent_widget = parent_widget
        self.font_size = parent_widget.width() // 40
        font = self.font()
        font.setPointSize(self.font_size)
        font.setWeight(QFont.Weight.DemiBold)
        self.setFont(font)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.clear()
        self.setContentsMargins(0, 0, 0, 0)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.start_fade_out)

    def show_message(self, text) -> None:
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(1)
        self.setGraphicsEffect(None)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(2000)
        self.animation.finished.connect(self.clear)
        if self.timer.isActive():
            self.timer.stop()
        if self.animation.state() == QPropertyAnimation.State.Running:
            self.animation.stop()

        self.setText(text)
        self.timer.start(1000)

    @pyqtSlot()
    def start_fade_out(self) -> None:
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def clear(self) -> None:
        self.setText(" ")


# -------------------------------------------------------
# File: C:/the-kinetic-constructor\main_window\main_widget\construct_tab\option_picker\option_scroll\section_widget\option_picker_section_pictograph_frame.py
# -------------------------------------------------------
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QGridLayout, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .option_picker_section_widget import OptionPickerSectionWidget


# [Line 9]
class OptionPickerSectionPictographFrame(QFrame):
    opacity_effect: QGraphicsOpacityEffect

    def __init__(self, section: "OptionPickerSectionWidget") -> None:
        super().__init__()
        self.section = section
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(self.section.option_scroll.spacing)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


# -------------------------------------------------------
# File: C:/the-kinetic-constructor\main_window\main_widget\fade_manager\fadeable_opacity_effect.py
# -------------------------------------------------------
from PyQt6.QtWidgets import QGraphicsOpacityEffect


# [Line 4]
class FadableOpacityEffect(QGraphicsOpacityEffect):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.in_animation = False


# -------------------------------------------------------
# File: C:/the-kinetic-constructor\main_window\main_widget\fade_manager\widget_fader.py
# -------------------------------------------------------
import os
from typing import TYPE_CHECKING, Optional, Union
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect, QGraphicsItem
from PyQt6.QtCore import (
    QParallelAnimationGroup,
    QPropertyAnimation,
    QEasingCurve,
    QTimer,
)
from Enums.Enums import Glyph
from base_widgets.pictograph.grid.non_radial_points_group import (
    NonRadialPointsGroup,
)
from main_window.main_widget.fade_manager.fade_when_ready_helper import (
    FadeWhenReadyHelper,
)
from main_window.main_widget.fade_manager.fadeable_opacity_effect import (
    FadableOpacityEffect,
)

if TYPE_CHECKING:
    from main_window.main_widget.fade_manager.fade_manager import FadeManager


def safe_remove_effect(widget: QWidget, effect: QGraphicsOpacityEffect):
    if widget.graphicsEffect() is effect:
        widget.setGraphicsEffect(None)


# [Line 28]
class WidgetFader:
    def __init__(self, manager: "FadeManager"):
        self.manager = manager
        self.profiler = manager.main_widget.main_window.profiler

    def fade_widgets(
        self,
        widgets: list[QWidget],
        fade_in: bool,
        duration: int,
        callback: Optional[callable] = None,
    ) -> None:
        if not widgets:
            if callback:
                callback()
            return

        ready_widgets: list[QWidget] = []
        for widget in widgets:
            if widget.isVisible() and widget.window().winId():
                ready_widgets.append(widget)
            else:
                from main_window.main_widget.fade_manager.fade_when_ready_helper import (
                    FadeWhenReadyHelper,
                )

                helper = FadeWhenReadyHelper(widget, fade_in, duration, callback, self)
                widget.installEventFilter(helper)

        if not ready_widgets:
            return

        animation_group = QParallelAnimationGroup(self.manager)
        for widget in ready_widgets:
            effect = self._ensure_opacity_effect(widget)
            # Mark the effect as in use.
            effect.in_animation = True

            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(duration)
            animation.setStartValue(0.0 if fade_in else 1.0)
            animation.setEndValue(1.0 if fade_in else 0.0)
            animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            animation_group.addAnimation(animation)

            # When the animation finishes, mark the effect as no longer in use and then remove it safely.
            animation.finished.connect(
                lambda w=widget, eff=effect: self._animation_finished(w, eff)
            )

        if callback:
            animation_group.finished.connect(callback)
        animation_group.start()

    def _animation_finished(self, widget: QWidget, effect: FadableOpacityEffect):
        effect.in_animation = False
        # Only remove if the widget’s current effect is still ours.
        if widget.graphicsEffect() is effect:
            widget.setGraphicsEffect(None)

    def _ensure_opacity_effect(self, widget: QWidget) -> FadableOpacityEffect:
        effect = widget.graphicsEffect()
        if not effect or not isinstance(effect, FadableOpacityEffect):
            effect = FadableOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
        return effect

    def fade_and_update(
        self,
        widget: list[QWidget],
        callback: Union[callable, tuple[callable, callable]] = None,
        duration: int = 250,
    ) -> None:

        # self.profiler.enable()

        def on_fade_out_finished():
            self.manager.graphics_effect_remover.clear_graphics_effects(widget)

            if callback:
                if isinstance(callback, tuple):
                    callback[0]()
                    self.fade_widgets(
                        widget,
                        True,
                        duration,
                        lambda: QTimer.singleShot(0, callback[1]),
                    )
                else:
                    callback()
                    self.fade_widgets(widget, True, duration)

        self.fade_widgets(widget, False, duration, on_fade_out_finished)

        # self.profiler.disable()
        # self.profiler.write_profiling_stats_to_file(
        #     "option_updater_profile.txt", os.getcwd()
        # )

    def fade_visibility_items_to_opacity(
        self,
        visibility_element: Union[Glyph, NonRadialPointsGroup],
        opacity: float,
        duration: int = 300,
        callback: Optional[callable] = None,
    ) -> None:
        if not visibility_element:
            if callback:
                callback()
            return
        items = self._get_corresponding_items(visibility_element)

        self.manager.graphics_effect_remover.clear_graphics_effects(
            [visibility_element]
        )
        animation_group = QParallelAnimationGroup(self.manager)
        for item in items:
            self.manager.graphics_effect_remover.clear_graphics_effects([item])
            if isinstance(item, QGraphicsItem):
                item.setOpacity(opacity)
            elif isinstance(item, QWidget):
                effect = self._ensure_opacity_effect(item)
                if effect:
                    start_opacity = effect.opacity() if effect else 1.0
                    animation = QPropertyAnimation(effect, b"opacity")
                    animation.setDuration(duration)
                    animation.setStartValue(start_opacity)
                    animation.setEndValue(opacity)
                    animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
                    animation_group.addAnimation(animation)
        if callback:
            animation_group.finished.connect(callback)
        animation_group.start()

    def _get_corresponding_items(
        self, element: Union[Glyph, NonRadialPointsGroup]
    ) -> list[Union[Glyph, NonRadialPointsGroup]]:
        if element.name == "TKA":
            items = element.get_all_items()
        elif element.name == "VTG":
            items = [element]
        elif element.name == "Elemental":
            items = [element]
        elif element.name == "Positions":
            items = element.get_all_items()
        elif element.name == "Reversals":
            items = list(element.reversal_items.values())
        elif element.name == "non_radial_points":
            items = element.child_points
        return items
