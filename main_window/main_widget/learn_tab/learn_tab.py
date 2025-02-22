from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QStackedLayout

from main_window.main_widget.codex.codex import Codex
from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.lesson_results_widget import (
    LessonResultsWidget,
)
from .lesson_selector import LessonSelector
from .lesson_1.lesson_1_widget import Lesson1Widget
from .lesson_2.lesson_2_widget import Lesson2Widget
from .lesson_3.lesson_3_widget import Lesson3Widget

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class LearnTab(QWidget):
    """Widget for the learning module, managing lesson selection and individual lessons."""

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.main_widget.splash.updater.update_progress("LearnTab")

        self.stack = QStackedLayout()
        self._setup_components()
        self._setup_layout()


    def _setup_components(self):
        self.lesson_selector = LessonSelector(self)
        self.lesson_1_widget = Lesson1Widget(self)
        self.lesson_2_widget = Lesson2Widget(self)
        self.lesson_3_widget = Lesson3Widget(self)
        self.results_widget = LessonResultsWidget(self)

    def _setup_layout(self) -> None:
        self.stack.addWidget(self.lesson_selector)
        self.stack.addWidget(self.lesson_1_widget)
        self.stack.addWidget(self.lesson_2_widget)
        self.stack.addWidget(self.lesson_3_widget)
        self.stack.setCurrentWidget(self.lesson_selector)
        self.stack.addWidget(self.results_widget)
        self.setLayout(self.stack)
