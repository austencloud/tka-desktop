from typing import TYPE_CHECKING
from PyQt6.QtCore import QObject

from main_window.main_widget.fade_manager.widget_and_stack_fader import (
    WidgetAndStackFader,
)
from .graphics_effect_remover import GraphicsEffectRemover
from .widget_fader import WidgetFader
from .stack_fader import StackFader
from .parallel_stack_fader import ParallelStackFader

if TYPE_CHECKING:
    from ..main_widget import MainWidget


class FadeManager(QObject):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget
        self.widget_fader = WidgetFader(self)
        self.stack_fader = StackFader(self)
        self.parallel_stack_fader = ParallelStackFader(self)
        self.widget_and_stack_fader = WidgetAndStackFader(self)
        self.graphics_effect_remover = GraphicsEffectRemover(self)

    def fades_enabled(self) -> bool:
        return self.main_widget.settings_manager.global_settings.get_enable_fades()
